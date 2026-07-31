from pathlib import Path
import base64
import io
import zipfile

root = Path("source")
parts = sorted((Path("ci") / "v002").glob("part-*.txt"))
if len(parts) != 7:
    raise SystemExit(f"Expected 7 v0.02 payload parts, found {len(parts)}")

payload_text = "".join(part.read_text().strip() for part in parts)
try:
    payload = base64.b64decode(payload_text, validate=True)
except Exception as exception:
    raise SystemExit(f"v0.02 payload Base64 validation failed: {exception}")

try:
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        bad_member = archive.testzip()
        if bad_member is not None:
            raise SystemExit(f"v0.02 payload ZIP integrity failed at {bad_member}")
        archive.extractall(root)
except zipfile.BadZipFile as exception:
    raise SystemExit(f"v0.02 payload is not a valid ZIP: {exception}")

required = [
    "core/src/main/java/com/dj/diyse/model/GameState.java",
    "core/src/test/java/com/dj/diyse/model/PrototypeDataTest.java",
    "android/build.gradle",
]
for relative in required:
    if not (root / relative).is_file():
        raise SystemExit(f"v0.02 patch did not create {relative}")

game_state = (root / "core/src/main/java/com/dj/diyse/model/GameState.java").read_text()
if "SAVE_SCHEMA_VERSION = 2" not in game_state or "stableMemberPrefix" not in game_state:
    raise SystemExit("v0.02 save schema verification failed")

prototype = (root / "core/src/main/java/com/dj/diyse/model/PrototypeData.java").read_text()
for name in ("Cyanis", "Ilyra", "Torren"):
    if name not in prototype:
        raise SystemExit(f"v0.02 identity verification failed for {name}")

battle = (root / "core/src/main/java/com/dj/diyse/screens/BattleScreen.java").read_text()
for marker in ("YAHTREAN PARTY", "BLACK HOST", "Confirm Round"):
    if marker not in battle:
        raise SystemExit(f"v0.02 battle HUD verification failed for {marker}")

android_gradle = (root / "android/build.gradle").read_text()
if "versionCode 2" not in android_gradle or "versionName '0.02'" not in android_gradle:
    raise SystemExit("v0.02 Android version verification failed")

print("Applied Diyse Prototype v0.02 identity, HUD, and save-schema pass.")
