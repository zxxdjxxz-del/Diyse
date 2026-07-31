from pathlib import Path
import base64
import hashlib
import io
import zipfile

root = Path("source")
parts = sorted((Path("ci") / "v006a").glob("part-*.txt"))
if len(parts) != 7:
    raise SystemExit(f"Expected 7 Diyse v0.06A payload parts, found {len(parts)}")

payload_text = "".join(part.read_text().strip() for part in parts)
try:
    payload = base64.b64decode(payload_text, validate=True)
except Exception as exception:
    raise SystemExit(f"v0.06A payload Base64 validation failed: {exception}")

expected_sha256 = "38793f8f44ce77a5982d972764d49bbd0590c250c8bbf563ef6342978d22ba6b"
actual_sha256 = hashlib.sha256(payload).hexdigest()
if actual_sha256 != expected_sha256:
    raise SystemExit(f"v0.06A payload checksum mismatch: {actual_sha256}")

try:
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        bad_member = archive.testzip()
        if bad_member is not None:
            raise SystemExit(f"v0.06A payload ZIP integrity failed at {bad_member}")
        archive.extractall(root)
except zipfile.BadZipFile as exception:
    raise SystemExit(f"v0.06A payload is not a valid ZIP: {exception}")

required = [
    "core/src/main/java/com/dj/diyse/DiyseGame.java",
    "core/src/main/java/com/dj/diyse/screens/CourtyardScreen.java",
    "core/src/main/java/com/dj/diyse/exploration/CourtyardWalkmesh.java",
    "core/src/main/java/com/dj/diyse/ui/FieldCharacterArt.java",
    "core/src/main/java/com/dj/diyse/ui/FixedCameraCourtyardArt.java",
    "core/src/test/java/com/dj/diyse/exploration/CourtyardWalkmeshTest.java",
    "android/build.gradle",
    "android/prototype-signing/diyse-prototype.keystore",
    "docs/CHANGELOG_v0.06A.md",
]
for relative in required:
    if not (root / relative).is_file():
        raise SystemExit(f"v0.06A patch did not create {relative}")

version = (root / "core/src/main/java/com/dj/diyse/DiyseGame.java").read_text()
if 'VERSION = "0.06A"' not in version:
    raise SystemExit("v0.06A game version verification failed")

game_state = (root / "core/src/main/java/com/dj/diyse/model/GameState.java").read_text()
for marker in ('SAVE_SCHEMA_VERSION = 3', 'putString("save_build", "0.06A")'):
    if marker not in game_state:
        raise SystemExit(f"v0.06A save compatibility verification failed for {marker}")

courtyard = (root / "core/src/main/java/com/dj/diyse/screens/CourtyardScreen.java").read_text()
for marker in (
    "FixedCameraCourtyardArt.background",
    "FieldCharacterArt",
    "CourtyardWalkmesh",
    "Walkmesh: Off",
    "drawWalkmeshOverlay",
    "Perspective scaling and foreground masking are active",
    "new BattleScreen(game)",
    "new MenuScreen(game)",
):
    if marker not in courtyard:
        raise SystemExit(f"v0.06A courtyard verification failed for {marker}")

walkmesh = (root / "core/src/main/java/com/dj/diyse/exploration/CourtyardWalkmesh.java").read_text()
for marker in ("Axis-separated collision", "scaleAt", "sanitize", "raised central dais"):
    if marker not in walkmesh:
        raise SystemExit(f"v0.06A walkmesh verification failed for {marker}")

field_art = (root / "core/src/main/java/com/dj/diyse/ui/FieldCharacterArt.java").read_text()
for marker in ("enum Facing", "late-1990s JRPG", "Texture[][] frames", "walkFrame"):
    if marker not in field_art:
        raise SystemExit(f"v0.06A field-model verification failed for {marker}")

scene_art = (root / "core/src/main/java/com/dj/diyse/ui/FixedCameraCourtyardArt.java").read_text()
for marker in ("pre-rendered-style", "foreground", "exact-crest rule", "near-camera column"):
    if marker not in scene_art:
        raise SystemExit(f"v0.06A scene-art verification failed for {marker}")

changelog = (root / "docs/CHANGELOG_v0.06A.md").read_text()
for marker in ("current v0.79 authority", "exact Crest is intentionally not approximated", "save schema 3"):
    if marker not in changelog:
        raise SystemExit(f"v0.06A canon/status verification failed for {marker}")

android_gradle = (root / "android/build.gradle").read_text()
for marker in ("versionCode 6", "versionName '0.06A'", "diyse-prototype.keystore", "signingConfig signingConfigs.prototype"):
    if marker not in android_gradle:
        raise SystemExit(f"v0.06A Android signing/version verification failed for {marker}")

for screen in (root / "core/src/main/java/com/dj/diyse/screens").glob("*.java"):
    text = screen.read_text()
    for forbidden in ("environments/", "characters/", "enemies/"):
        if forbidden in text:
            raise SystemExit(f"Missing runtime asset reference remains in {screen}: {forbidden}")

keystore = root / "android/prototype-signing/diyse-prototype.keystore"
if keystore.stat().st_size < 1000:
    raise SystemExit("v0.06A permanent prototype keystore is missing or truncated")

print("Applied Diyse Prototype v0.06A fixed-camera graphics vertical slice.")
