from pathlib import Path
import base64
import hashlib
import io
import zipfile
import zlib

root = Path("source")
parts = sorted((Path("ci") / "v009a").glob("part-*.txt"))
if len(parts) != 9:
    raise SystemExit(f"Expected 9 Diyse v0.09A payload parts, found {len(parts)}")

payload_text = "".join(part.read_text().strip() for part in parts)
try:
    payload = base64.b64decode(payload_text, validate=True)
except Exception as exception:
    raise SystemExit(f"v0.09A payload Base64 validation failed: {exception}")

expected_sha256 = "0c51f3e3a8ef683b9e8934ae7d265198d45ac5a571168ac7aca24bc9b20b5ab6"
actual_sha256 = hashlib.sha256(payload).hexdigest()
if actual_sha256 != expected_sha256:
    raise SystemExit(f"v0.09A payload checksum mismatch: {actual_sha256}")

try:
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        bad_member = archive.testzip()
        if bad_member is not None:
            raise SystemExit(f"v0.09A payload ZIP integrity failed at {bad_member}")
        archive.extractall(root)
except zipfile.BadZipFile as exception:
    raise SystemExit(f"v0.09A payload is not a valid ZIP: {exception}")

required = [
    "core/src/main/java/com/dj/diyse/screens/TraversalCalibrationScreen.java",
    "core/src/main/java/com/dj/diyse/field/FieldMapDefinition.java",
    "core/src/main/java/com/dj/diyse/field/TraversalCalibrationMap.java",
    "core/src/main/java/com/dj/diyse/ui/TraversalCalibrationArt.java",
    "core/src/test/java/com/dj/diyse/field/TraversalCalibrationMapTest.java",
    "docs/CHANGELOG_v0.09A.md",
]
for relative in required:
    if not (root / relative).is_file():
        raise SystemExit(f"v0.09A patch did not create {relative}")

version = (root / "core/src/main/java/com/dj/diyse/DiyseGame.java").read_text()
for marker in ('VERSION = "0.09A"', "TraversalCalibrationScreen"):
    if marker not in version:
        raise SystemExit(f"v0.09A game verification failed for {marker}")

game_state = (root / "core/src/main/java/com/dj/diyse/model/GameState.java").read_text()
for marker in ("SAVE_SCHEMA_VERSION = 4", 'putString("save_build", "0.09A")'):
    if marker not in game_state:
        raise SystemExit(f"v0.09A GameState verification failed for {marker}")

screen = (root / "core/src/main/java/com/dj/diyse/screens/TraversalCalibrationScreen.java").read_text()
for marker in ("Touchpad", "beginCameraBasisBlend", "archAlpha", "new CourtyardScreen"):
    if marker not in screen:
        raise SystemExit(f"v0.09A traversal screen verification failed for {marker}")

field_map = (root / "core/src/main/java/com/dj/diyse/field/TraversalCalibrationMap.java").read_text()
for marker in ("UPPER_BRIDGE", "UNDERPASS", ".connect(UPPER_RETURN, UPPER_BRIDGE)"):
    if marker not in field_map:
        raise SystemExit(f"v0.09A calibration map verification failed for {marker}")
if ".connect(UNDERPASS, UPPER_BRIDGE)" in field_map or ".connect(UPPER_BRIDGE, UNDERPASS)" in field_map:
    raise SystemExit("v0.09A incorrectly connected the overlapping tunnel and bridge")

android_gradle = (root / "android/build.gradle").read_text()
for marker in ("versionCode 13", "versionName '0.09A'", "diyse-prototype.keystore"):
    if marker not in android_gradle:
        raise SystemExit(f"v0.09A Android verification failed for {marker}")

hotfix_parts = sorted((Path("ci") / "v009a1").glob("part-*.txt"))
if len(hotfix_parts) != 8:
    raise SystemExit(f"Expected 8 Diyse v0.09A1 hotfix parts, found {len(hotfix_parts)}")
hotfix_text = "".join(part.read_text().strip() for part in hotfix_parts)
if hashlib.sha256(hotfix_text.encode()).hexdigest() != "0d7f60a1d841226ec803f4ee3bde7cb3c737e99159006e12dcc68bfb43faec7d":
    raise SystemExit("v0.09A1 hotfix Base64 text checksum mismatch")
try:
    hotfix_compressed = base64.b64decode(hotfix_text, validate=True)
except Exception as exception:
    raise SystemExit(f"v0.09A1 hotfix Base64 validation failed: {exception}")
if hashlib.sha256(hotfix_compressed).hexdigest() != "eeb34e8a101d0e9a2c43119084a90b33385256e4610744346757301d377bb4c2":
    raise SystemExit("v0.09A1 hotfix compressed checksum mismatch")
try:
    hotfix_bytes = zlib.decompress(hotfix_compressed)
except Exception as exception:
    raise SystemExit(f"v0.09A1 hotfix decompression failed: {exception}")
if hashlib.sha256(hotfix_bytes).hexdigest() != "a80e27e080d8bd5c2be671c282a26d03498243c534a6bd69e4015f65d4a35dd4":
    raise SystemExit("v0.09A1 hotfix script checksum mismatch")
hotfix_code = hotfix_bytes.decode("utf-8")
exec(compile(hotfix_code, "ci/patch-v009a1.py", "exec"))

version = (root / "core/src/main/java/com/dj/diyse/DiyseGame.java").read_text()
if 'VERSION = "0.09A1"' not in version:
    raise SystemExit("v0.09A1 version verification failed")

field_engine = (root / "core/src/main/java/com/dj/diyse/field/FieldMapDefinition.java").read_text()
for marker in ("bestElevationDelta", "candidate.elevationAt", "bestDepthDelta"):
    if marker not in field_engine:
        raise SystemExit(f"v0.09A1 elevation-continuity verification failed for {marker}")

route_test = (root / "core/src/test/java/com/dj/diyse/field/TraversalCalibrationMapTest.java").read_text()
for marker in ("completeCalibrationRouteIsReachableFromSpawn", "underpassToStairPortalIsBroadEnoughForTouchMovement"):
    if marker not in route_test:
        raise SystemExit(f"v0.09A1 route test verification failed for {marker}")

android_gradle = (root / "android/build.gradle").read_text()
for marker in ("versionCode 14", "versionName '0.09A1'", "diyse-prototype.keystore"):
    if marker not in android_gradle:
        raise SystemExit(f"v0.09A1 Android verification failed for {marker}")

print("Applied Diyse Prototype v0.09A1 upper-platform accessibility fix.")
