from pathlib import Path
import base64
import hashlib
import io
import zipfile

root = Path("source")
parts = sorted((Path("ci") / "v004").glob("part-*.txt"))
if len(parts) != 2:
    raise SystemExit(f"Expected 2 Diyse v0.04 payload parts, found {len(parts)}")

payload_text = "".join(part.read_text().strip() for part in parts)
try:
    payload = base64.b64decode(payload_text, validate=True)
except Exception as exception:
    raise SystemExit(f"v0.04 payload Base64 validation failed: {exception}")

expected_sha256 = "1cd71767e8a44f40d554662553cd3645f885705a3b0bceaad7177bb99075ab81"
actual_sha256 = hashlib.sha256(payload).hexdigest()
if actual_sha256 != expected_sha256:
    raise SystemExit(f"v0.04 payload checksum mismatch: {actual_sha256}")

try:
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        bad_member = archive.testzip()
        if bad_member is not None:
            raise SystemExit(f"v0.04 payload ZIP integrity failed at {bad_member}")
        archive.extractall(root)
except zipfile.BadZipFile as exception:
    raise SystemExit(f"v0.04 payload is not a valid ZIP: {exception}")

required = [
    "core/src/main/java/com/dj/diyse/DiyseGame.java",
    "core/src/main/java/com/dj/diyse/model/GameState.java",
    "core/src/main/java/com/dj/diyse/screens/CourtyardScreen.java",
    "core/src/main/java/com/dj/diyse/screens/MenuScreen.java",
    "core/src/test/java/com/dj/diyse/model/GameStateContractTest.java",
    "android/build.gradle",
    "android/prototype-signing/diyse-prototype.keystore",
    "docs/CHANGELOG_v0.04.md",
]
for relative in required:
    if not (root / relative).is_file():
        raise SystemExit(f"v0.04 patch did not create {relative}")

version = (root / "core/src/main/java/com/dj/diyse/DiyseGame.java").read_text()
if 'VERSION = "0.04"' not in version:
    raise SystemExit("v0.04 game version verification failed")

game_state = (root / "core/src/main/java/com/dj/diyse/model/GameState.java").read_text()
for marker in ("SAVE_SCHEMA_VERSION = 3", "INVENTORY_STACK_LIMIT = 999", "objectiveStep", "useHealingDraught"):
    if marker not in game_state:
        raise SystemExit(f"v0.04 state verification failed for {marker}")

menu = (root / "core/src/main/java/com/dj/diyse/screens/MenuScreen.java").read_text()
for marker in ("Party", "Abilities", "Cards", "Items", "Equipment", "Objectives", "Save", "Options"):
    if f'"{marker}"' not in menu:
        raise SystemExit(f"v0.04 menu verification failed for {marker}")

courtyard = (root / "core/src/main/java/com/dj/diyse/screens/CourtyardScreen.java").read_text()
for marker in ("COMMAND MARKER", "SUPPLY CACHE", "TRAINING INCURSION", "OBJECTIVE 4/4"):
    if marker not in courtyard:
        raise SystemExit(f"v0.04 courtyard sequence verification failed for {marker}")

android_gradle = (root / "android/build.gradle").read_text()
for marker in ("versionCode 4", "versionName '0.04'", "diyse-prototype.keystore", "signingConfig signingConfigs.prototype"):
    if marker not in android_gradle:
        raise SystemExit(f"v0.04 Android signing/version verification failed for {marker}")

for screen in (root / "core/src/main/java/com/dj/diyse/screens").glob("*.java"):
    text = screen.read_text()
    for forbidden in ("environments/", "characters/", "enemies/"):
        if forbidden in text:
            raise SystemExit(f"Missing runtime asset reference remains in {screen}: {forbidden}")

keystore = root / "android/prototype-signing/diyse-prototype.keystore"
if keystore.stat().st_size < 1000:
    raise SystemExit("v0.04 permanent prototype keystore is missing or truncated")

print("Applied Diyse Prototype v0.04 core-menu and courtyard-exploration pass.")
