from pathlib import Path
import base64
import hashlib
import io
import zipfile

root = Path("source")
parts = sorted((Path("ci") / "v009b").glob("part-*.txt"))
if len(parts) != 7:
    raise SystemExit(f"Expected 7 Diyse v0.09B payload parts, found {len(parts)}")

payload_text = "".join(part.read_text().strip() for part in parts)
if hashlib.sha256(payload_text.encode()).hexdigest() != "b2497bea3b847cba99b277fd9867cf8d11a78d8b20411bfb3f5afe1a88deec5a":
    raise SystemExit("v0.09B payload Base64 text checksum mismatch")
try:
    payload = base64.b64decode(payload_text, validate=True)
except Exception as exception:
    raise SystemExit(f"v0.09B payload Base64 validation failed: {exception}")

actual_sha256 = hashlib.sha256(payload).hexdigest()
expected_sha256 = "dcc2698149a0b1aab8f3f9892c5fba9063503e1eb25bc8c063e0045f7aa5f63c"
if actual_sha256 != expected_sha256:
    raise SystemExit(f"v0.09B payload checksum mismatch: {actual_sha256}")

try:
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        bad_member = archive.testzip()
        if bad_member is not None:
            raise SystemExit(f"v0.09B payload ZIP integrity failed at {bad_member}")
        archive.extractall(root)
except zipfile.BadZipFile as exception:
    raise SystemExit(f"v0.09B payload is not a valid ZIP: {exception}")

required = [
    "core/src/main/java/com/dj/diyse/screens/GatehouseScreen.java",
    "core/src/main/java/com/dj/diyse/field/GatehouseMap.java",
    "core/src/main/java/com/dj/diyse/ui/GatehouseArt.java",
    "core/src/test/java/com/dj/diyse/field/GatehouseMapTest.java",
    "docs/CHANGELOG_v0.09B.md",
]
for relative in required:
    if not (root / relative).is_file():
        raise SystemExit(f"v0.09B patch did not create {relative}")

version = (root / "core/src/main/java/com/dj/diyse/DiyseGame.java").read_text()
for marker in ('VERSION = "0.09B"', "GatehouseScreen"):
    if marker not in version:
        raise SystemExit(f"v0.09B game verification failed for {marker}")

state = (root / "core/src/main/java/com/dj/diyse/model/GameState.java").read_text()
for marker in ("SAVE_SCHEMA_VERSION = 4", 'putString("save_build", "0.09B")'):
    if marker not in state:
        raise SystemExit(f"v0.09B GameState verification failed for {marker}")

field_engine = (root / "core/src/main/java/com/dj/diyse/field/FieldMapDefinition.java").read_text()
for marker in ("isConnected", "disconnect", "bestElevationDelta"):
    if marker not in field_engine:
        raise SystemExit(f"v0.09B field-engine verification failed for {marker}")

gatehouse_map = (root / "core/src/main/java/com/dj/diyse/field/GatehouseMap.java").read_text()
for marker in (
    "CAMERA_APPROACH", "CAMERA_STAIRS", "CAMERA_ARCH", "CAMERA_MECHANISM",
    "CAMERA_BRIDGE", "CAMERA_PULSE", "CAMERA_SUMMIT", "activateBridge",
    "PULSE_CORRIDOR", "POCKET_ONE", "SUMMIT", "unlockShortcut"
):
    if marker not in gatehouse_map:
        raise SystemExit(f"v0.09B gatehouse-map verification failed for {marker}")
if ".connect(MECHANISM_CHAMBER, BRIDGE)" in gatehouse_map.split("public void activateBridge", 1)[0]:
    raise SystemExit("v0.09B bridge must remain disconnected until mechanism activation")

screen = (root / "core/src/main/java/com/dj/diyse/screens/GatehouseScreen.java").read_text()
for marker in (
    "PULSE_CYCLE_SECONDS", "beginAction", "map.activateBridge()", "teleportTo",
    "map.unlockShortcut()", "new CourtyardScreen", "Touchpad", "beginCameraBasisBlend"
):
    if marker not in screen:
        raise SystemExit(f"v0.09B gatehouse-screen verification failed for {marker}")

route_test = (root / "core/src/test/java/com/dj/diyse/field/GatehouseMapTest.java").read_text()
for marker in (
    "completeGatehouseRouteReachesSummitAfterActivation",
    "routeStopsAtMechanismUntilBridgeIsActivated",
    "safePocketsAreConnectedButRemainOutsideThePulseLane",
    "summitUnlocksBothDirectionsOfTheShortcutInteraction"
):
    if marker not in route_test:
        raise SystemExit(f"v0.09B route-test verification failed for {marker}")

android_gradle = (root / "android/build.gradle").read_text()
for marker in ("versionCode 15", "versionName '0.09B'", "diyse-prototype.keystore"):
    if marker not in android_gradle:
        raise SystemExit(f"v0.09B Android verification failed for {marker}")

print("Applied Diyse Prototype v0.09B full gatehouse traversal route.")
