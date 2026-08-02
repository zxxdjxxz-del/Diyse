from pathlib import Path
import base64
import hashlib
import io
import json
import struct
import subprocess
import sys
import zipfile

root = Path("source")
parts = sorted((Path("ci") / "v009a-safe").glob("safe-*.txt"))
if len(parts) != 16:
    raise SystemExit(f"Expected 16 Diyse v0.09A safe payload parts, found {len(parts)}")

payload_text = "".join(part.read_text().strip() for part in parts)
try:
    payload = base64.b64decode(payload_text, validate=True)
except Exception as exception:
    raise SystemExit(f"v0.09A payload Base64 validation failed: {exception}")

expected_sha256 = "e1ef258dea2d35b6da86d84454065d0812aba681bc166053d26a253ed106dd75"
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

renderer = root / "tools/render_v009a_assets.py"
if not renderer.is_file():
    raise SystemExit("v0.09A renderer script is missing")
subprocess.run([sys.executable, str(renderer)], check=True)

required = [
    "assets/field/v009a/courtyard_background.png",
    "assets/field/v009a/courtyard_atmosphere.png",
    "assets/field/v009a/courtyard_foreground.png",
    "assets/field/v009a/cyanis_field_sheet.png",
    "assets/field/v009a/courtyard_scene.json",
    "core/src/main/java/com/dj/diyse/ui/FixedCameraCourtyardArt.java",
    "core/src/main/java/com/dj/diyse/ui/FieldCharacterArt.java",
    "core/src/test/java/com/dj/diyse/ui/AuthoredFieldAssetTest.java",
    "tools/render_v009a_assets.py",
    "docs/CHANGELOG_v0.09A.md",
    "docs/VISUAL_PIPELINE_v0.09A.md",
    "android/prototype-signing/diyse-prototype.keystore",
]
for relative in required:
    if not (root / relative).is_file():
        raise SystemExit(f"v0.09A patch did not create {relative}")


def png_size(path):
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise SystemExit(f"v0.09A asset is not a valid PNG header: {path}")
    return struct.unpack(">II", data[16:24])

assets = {
    "assets/field/v009a/courtyard_background.png": (1280, 720, 100000),
    "assets/field/v009a/courtyard_atmosphere.png": (1280, 720, 20000),
    "assets/field/v009a/courtyard_foreground.png": (1280, 720, 50000),
    "assets/field/v009a/cyanis_field_sheet.png": (640, 896, 80000),
}
for relative, (width, height, minimum_bytes) in assets.items():
    path = root / relative
    if path.stat().st_size < minimum_bytes:
        raise SystemExit(f"v0.09A visual asset appears truncated: {relative}")
    if png_size(path) != (width, height):
        raise SystemExit(f"v0.09A visual asset dimensions are incorrect: {relative}")

manifest = json.loads((root / "assets/field/v009a/courtyard_scene.json").read_text())
if manifest.get("version") != "0.09A" or manifest.get("exactCrestIncluded") is not False:
    raise SystemExit("v0.09A visual manifest verification failed")
if "offline low-poly software renderer" not in manifest.get("renderer", ""):
    raise SystemExit("v0.09A renderer provenance verification failed")

version = (root / "core/src/main/java/com/dj/diyse/DiyseGame.java").read_text()
if 'VERSION = "0.09A"' not in version:
    raise SystemExit("v0.09A game version verification failed")

game_state = (root / "core/src/main/java/com/dj/diyse/model/GameState.java").read_text()
for marker in ('SAVE_SCHEMA_VERSION = 4', 'putString("save_build", "0.09A")'):
    if marker not in game_state:
        raise SystemExit(f"v0.09A save compatibility verification failed for {marker}")

courtyard_art = (root / "core/src/main/java/com/dj/diyse/ui/FixedCameraCourtyardArt.java").read_text()
field_art = (root / "core/src/main/java/com/dj/diyse/ui/FieldCharacterArt.java").read_text()
for text, marker in (
    (courtyard_art, "field/v009a/courtyard_background.png"),
    (courtyard_art, "Gdx.files.internal"),
    (field_art, "field/v009a/cyanis_field_sheet.png"),
    (field_art, "TextureRegion"),
):
    if marker not in text:
        raise SystemExit(f"v0.09A authored-asset verification failed for {marker}")
if "new Pixmap" in courtyard_art or "new Pixmap" in field_art:
    raise SystemExit("v0.09A restored runtime-drawn field placeholders")

screen = (root / "core/src/main/java/com/dj/diyse/screens/CourtyardScreen.java").read_text()
for marker in (
    "AUTHORED VISUAL TARGET",
    "TextureRegion characterFrame",
    "FixedCameraCourtyardArt.background",
    "game.batch().draw(foreground",
    "new BattleScreen(game)",
):
    if marker not in screen:
        raise SystemExit(f"v0.09A field-screen verification failed for {marker}")

interaction = (root / "core/src/main/java/com/dj/diyse/exploration/CourtyardInteraction.java").read_text()
for marker in ('477f, 403f', '628f, 390f', '788f, 355f', 'NORMAL_EXPLORATION_USES_FOLLOWERS = false'):
    if marker not in interaction:
        raise SystemExit(f"v0.09A interaction alignment verification failed for {marker}")

changelog = (root / "docs/CHANGELOG_v0.09A.md").read_text()
for marker in (
    "current v0.87 active master canon authority",
    "exact approved Crest of Yahtrea",
    "Save schema remains 4",
    "original Diyse work",
):
    if marker not in changelog:
        raise SystemExit(f"v0.09A canon/status verification failed for {marker}")

android_gradle = (root / "android/build.gradle").read_text()
for marker in ("versionCode 13", "versionName '0.09A'", "diyse-prototype.keystore", "signingConfig signingConfigs.prototype"):
    if marker not in android_gradle:
        raise SystemExit(f"v0.09A Android signing/version verification failed for {marker}")

keystore = root / "android/prototype-signing/diyse-prototype.keystore"
if keystore.stat().st_size < 1000:
    raise SystemExit("v0.09A permanent prototype keystore is missing or truncated")

print("Applied Diyse Prototype v0.09A authored visual target slice.")
