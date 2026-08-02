from pathlib import Path
import base64, hashlib, io, json, struct, subprocess, sys, zipfile

root = Path("source")
parts = sorted((Path("ci") / "v009c").glob("part-*.txt"))
if len(parts) != 27:
    raise SystemExit(f"Expected 27 v0.09C payload parts, found {len(parts)}")
for index, part in enumerate(parts):
    text = part.read_text(encoding="utf-8").strip()
    expected_length = 248 if index == 26 else 2000
    if len(text) != expected_length:
        raise SystemExit(f"v0.09C part {index:02d} length mismatch: {len(text)}")

payload_text = "".join(part.read_text(encoding="utf-8").strip() for part in parts)
try:
    payload = base64.b64decode(payload_text, validate=True)
except Exception as exception:
    raise SystemExit(f"v0.09C Base64 validation failed: {exception}")
if hashlib.sha256(payload).hexdigest() != "1b6a117882ec41e92e8f906e88a1826ecc871dabf2cabf1d9469774bc6cacfa0":
    raise SystemExit("v0.09C overlay checksum mismatch")

try:
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        bad = archive.testzip()
        if bad:
            raise SystemExit(f"v0.09C ZIP integrity failed at {bad}")
        archive.extractall(root)
except zipfile.BadZipFile as exception:
    raise SystemExit(f"v0.09C overlay is not a valid ZIP: {exception}")

renderer = root / "tools/render_v009c_assets.py"
subprocess.run([sys.executable, str(renderer)], check=True)
asset_root = root / "assets/field/v009c"
manifest = json.loads((asset_root / "visual_manifest.json").read_text(encoding="utf-8"))
if manifest.get("version") != "0.09C" or manifest.get("preservesV009BGeometry") is not True:
    raise SystemExit("v0.09C manifest contract failed")
if manifest.get("exactCrestIncluded") is not False or "deterministic original Diyse" not in manifest.get("renderer", ""):
    raise SystemExit("v0.09C provenance contract failed")

plates = (
    "stair_court_background.png", "stair_court_atmosphere.png", "stair_court_foreground.png",
    "lower_arch_background.png", "lower_arch_atmosphere.png", "lower_arch_foreground.png",
    "upper_bridge_background.png", "upper_bridge_atmosphere.png", "upper_bridge_foreground.png",
    "upper_bridge_active.png",
)

def png_contract(path, width, height):
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise SystemExit(f"Invalid PNG: {path}")
    if (*struct.unpack(">II", data[16:24]), data[25]) != (width, height, 6):
        raise SystemExit(f"PNG dimension/RGBA mismatch: {path}")
    if hashlib.sha256(data).hexdigest() != manifest["files"].get(path.name):
        raise SystemExit(f"Deterministic hash mismatch: {path}")

for name in plates:
    png_contract(asset_root / name, 1280, 720)
png_contract(asset_root / "cyanis_field_sheet.png", 640, 896)

required = (
    "core/src/main/java/com/dj/diyse/ui/GatehouseArt.java",
    "core/src/main/java/com/dj/diyse/ui/FieldCharacterArt.java",
    "core/src/test/java/com/dj/diyse/ui/AuthoredGatehouseAssetContractTest.java",
    "docs/CHANGELOG_v0.09C.md", "docs/VISUAL_PIPELINE_v0.09C.md",
)
for relative in required:
    if not (root / relative).is_file():
        raise SystemExit(f"v0.09C missing {relative}")

checks = {
    "core/src/main/java/com/dj/diyse/DiyseGame.java": ('VERSION = "0.09C"',),
    "core/src/main/java/com/dj/diyse/model/GameState.java": ('SAVE_SCHEMA_VERSION = 4', 'putString("save_build", "0.09C")'),
    "android/build.gradle": ("versionCode 16", "versionName '0.09C'", "diyse-prototype.keystore"),
    "core/src/main/java/com/dj/diyse/ui/GatehouseArt.java": ('AUTHORED_ROOT = "field/v009c/"', "loadAuthoredPlate", "upper_bridge_active.png"),
    "core/src/main/java/com/dj/diyse/ui/FieldCharacterArt.java": ("TextureRegion.split", "cyanis_field_sheet.png", "FRAME_WIDTH = 160", "FRAME_HEIGHT = 224"),
    "core/src/main/java/com/dj/diyse/screens/GatehouseScreen.java": ("AUTHORED GATEHOUSE VISUAL SLICE", "activePlate().atmosphere", "map.bridgeActive()"),
    "core/src/main/java/com/dj/diyse/field/GatehouseMap.java": ('.connect(STAIRS, UPPER_LANDING)', 'field.connect(MECHANISM_CHAMBER, BRIDGE)'),
}
for relative, markers in checks.items():
    text = (root / relative).read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            raise SystemExit(f"v0.09C contract failed: {relative} missing {marker}")
if "new Pixmap" in (root / "core/src/main/java/com/dj/diyse/ui/FieldCharacterArt.java").read_text(encoding="utf-8"):
    raise SystemExit("v0.09C restored per-pose runtime Pixmap generation")

print("Applied Diyse Prototype v0.09C authored gatehouse visual production slice.")
