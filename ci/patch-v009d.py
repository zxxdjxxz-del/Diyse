from pathlib import Path
import base64
import hashlib
import subprocess
import zlib

root = Path("source")
parts = sorted((Path("ci") / "v009d").glob("part-*.txt"))
if len(parts) != 9:
    raise SystemExit(f"Expected 9 v0.09D payload parts, found {len(parts)}")

texts = []
for index, part in enumerate(parts):
    text = part.read_text(encoding="utf-8").strip()
    expected_length = 24 if index == 8 else 2000
    if len(text) != expected_length:
        raise SystemExit(f"v0.09D part {index + 1:02d} length mismatch: {len(text)} != {expected_length}")
    texts.append(text)

payload_text = "".join(texts)
if len(payload_text) != 16024:
    raise SystemExit(f"v0.09D Base64 length mismatch: {len(payload_text)}")
if hashlib.sha256(payload_text.encode("utf-8")).hexdigest() != "e488375e7677feee52e656d65021d59e443ef08e7e1da338137a807a654470f4":
    raise SystemExit("v0.09D Base64 stream checksum mismatch")

try:
    compressed = base64.b64decode(payload_text, validate=True)
except Exception as exception:
    raise SystemExit(f"v0.09D Base64 validation failed: {exception}")
if hashlib.sha256(compressed).hexdigest() != "2e5f49865e3464b637fcbc95f20fc9ee46dc19100f570f9c6c3ae8def6b6fe5e":
    raise SystemExit("v0.09D compressed payload checksum mismatch")

try:
    patch_bytes = zlib.decompress(compressed)
except zlib.error as exception:
    raise SystemExit(f"v0.09D zlib decompression failed: {exception}")
if hashlib.sha256(patch_bytes).hexdigest() != "48c7e11a77d9dde182cdfa53c2fce3fb4c24e4a73056a24b751b3a45543e1e69":
    raise SystemExit("v0.09D patch checksum mismatch")

patch_file = Path("v009d.patch")
patch_file.write_bytes(patch_bytes)
result = subprocess.run(
    ["patch", "--batch", "--forward", "-p2", "-d", str(root), "-i", str(patch_file.resolve())],
    text=True,
    capture_output=True,
)
if result.returncode != 0:
    raise SystemExit(f"v0.09D patch application failed:\n{result.stdout}\n{result.stderr}")

required = (
    "core/src/main/java/com/dj/diyse/model/FieldResumeState.java",
    "core/src/main/java/com/dj/diyse/field/GatehouseResumeCatalog.java",
    "core/src/test/java/com/dj/diyse/model/FieldPersistenceTest.java",
    "core/src/test/java/com/dj/diyse/model/FieldPersistenceSourceContractTest.java",
    "core/src/test/java/com/dj/diyse/field/GatehouseResumeCatalogTest.java",
    "docs/CHANGELOG_v0.09D.md",
    "docs/FIELD_PERSISTENCE_v0.09D.md",
)
for relative in required:
    if not (root / relative).is_file():
        raise SystemExit(f"v0.09D missing {relative}")

checks = {
    "core/src/main/java/com/dj/diyse/DiyseGame.java": (
        'VERSION = "0.09D"', "showSavedField", "returnToSavedField",
        "FieldResumeState.FIELD_COURTYARD"),
    "core/src/main/java/com/dj/diyse/model/GameState.java": (
        "SAVE_SCHEMA_VERSION = 5", 'putString("save_build", "0.09D")',
        'putString("current_field_id"', 'putString("field_spawn_id"',
        'putBoolean("gatehouse_bridge_active"', 'putBoolean("gatehouse_shortcut_unlocked"',
        "loadFrom(Preferences", "saveTo(Preferences", "Float.isFinite"),
    "core/src/main/java/com/dj/diyse/model/FieldResumeState.java": (
        'FIELD_GATEHOUSE = "gatehouse"', 'FIELD_COURTYARD = "courtyard"',
        'GATEHOUSE_POCKET_THREE', "sanitizeSpawnId"),
    "core/src/main/java/com/dj/diyse/field/GatehouseResumeCatalog.java": (
        "resolve(String requestedId, boolean bridgeActive)", "requiresBridge",
        "anchorForCheckpoint", "GatehouseMap.PULSE_CORRIDOR"),
    "core/src/main/java/com/dj/diyse/screens/GatehouseScreen.java": (
        "PERSISTENT GATEHOUSE FIELD", "GatehouseResumeCatalog.resolve",
        "persistGatehouseState", "public void pause()", "Save & Title",
        "setGatehouseProgress(true, true, true)"),
    "core/src/main/java/com/dj/diyse/screens/CourtyardScreen.java": (
        "FieldResumeState.FIELD_COURTYARD", "COURTYARD_SAVED"),
    "core/src/main/java/com/dj/diyse/screens/MenuScreen.java": (
        '"Return to Field"', "returnToSavedField"),
    "core/src/main/java/com/dj/diyse/screens/VictoryResultsScreen.java": (
        '"Return to Field"', "returnToSavedField"),
    "android/build.gradle": ("versionCode 17", "versionName '0.09D'", "diyse-prototype.keystore"),
    "core/src/test/java/com/dj/diyse/VersionContractTest.java": (
        'assertEquals("0.09D"', "assertEquals(5, GameState.saveSchemaVersion())"),
}
for relative, markers in checks.items():
    text = (root / relative).read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            raise SystemExit(f"v0.09D contract failed: {relative} missing {marker}")

state_text = (root / "core/src/main/java/com/dj/diyse/model/GameState.java").read_text(encoding="utf-8")
if 'PREFS = "diyse-prototype-v001"' not in state_text:
    raise SystemExit("v0.09D changed the permanent save namespace")

geometry = root / "core/src/main/java/com/dj/diyse/field/GatehouseMap.java"
if hashlib.sha256(geometry.read_bytes()).hexdigest() != "3ebfb60142bed4c09d6aacf054b1a642b21ba3f2e611fce4d60e3ffb141ae256":
    raise SystemExit("v0.09D changed accepted gatehouse geometry")

print("Applied Diyse Prototype v0.09D field persistence and release hardening.")
