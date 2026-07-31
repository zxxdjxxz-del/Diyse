from pathlib import Path
import base64
import hashlib
import io
import zipfile

root = Path("source")
parts = sorted((Path("ci") / "v005").glob("part-*.txt"))
if len(parts) != 6:
    raise SystemExit(f"Expected 6 Diyse v0.05 payload parts, found {len(parts)}")

payload_text = "".join(part.read_text().strip() for part in parts)
try:
    payload = base64.b64decode(payload_text, validate=True)
except Exception as exception:
    raise SystemExit(f"v0.05 payload Base64 validation failed: {exception}")

expected_sha256 = "ea178e8c5dabffcfabbca2e3823e39608f2806f89958e9d431fd42c0d77e4ab1"
actual_sha256 = hashlib.sha256(payload).hexdigest()
if actual_sha256 != expected_sha256:
    raise SystemExit(f"v0.05 payload checksum mismatch: {actual_sha256}")

try:
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        bad_member = archive.testzip()
        if bad_member is not None:
            raise SystemExit(f"v0.05 payload ZIP integrity failed at {bad_member}")
        archive.extractall(root)
except zipfile.BadZipFile as exception:
    raise SystemExit(f"v0.05 payload is not a valid ZIP: {exception}")

required = [
    "core/src/main/java/com/dj/diyse/DiyseGame.java",
    "core/src/main/java/com/dj/diyse/combat/BattleAction.java",
    "core/src/main/java/com/dj/diyse/combat/EnemyBehavior.java",
    "core/src/main/java/com/dj/diyse/screens/BattleScreen.java",
    "core/src/main/java/com/dj/diyse/screens/VictoryResultsScreen.java",
    "core/src/test/java/com/dj/diyse/combat/EnemyBehaviorTest.java",
    "core/src/test/java/com/dj/diyse/model/CombatIdentityTest.java",
    "android/build.gradle",
    "android/prototype-signing/diyse-prototype.keystore",
    "docs/CHANGELOG_v0.05.md",
]
for relative in required:
    if not (root / relative).is_file():
        raise SystemExit(f"v0.05 patch did not create {relative}")

version = (root / "core/src/main/java/com/dj/diyse/DiyseGame.java").read_text()
if 'VERSION = "0.05"' not in version:
    raise SystemExit("v0.05 game version verification failed")

game_state = (root / "core/src/main/java/com/dj/diyse/model/GameState.java").read_text()
if "SAVE_SCHEMA_VERSION = 3" not in game_state:
    raise SystemExit("v0.05 must preserve save schema 3")

battle = (root / "core/src/main/java/com/dj/diyse/screens/BattleScreen.java").read_text()
for marker in (
    "TargetMode",
    "chooseEnemyTarget",
    "choosePartyTarget",
    "All commands and targets confirmed",
    "VictoryResultsScreen",
    "Cancel Target",
):
    if marker not in battle:
        raise SystemExit(f"v0.05 target-selection verification failed for {marker}")

enemy_behavior = (root / "core/src/main/java/com/dj/diyse/combat/EnemyBehavior.java").read_text()
for marker in ("Hooking Thrust", "Ruin Bolt", "Ember Ward", "lockActions"):
    if marker not in enemy_behavior:
        raise SystemExit(f"v0.05 enemy behavior verification failed for {marker}")

prototype = (root / "core/src/main/java/com/dj/diyse/model/PrototypeData.java").read_text()
for marker in (
    'new Ability("Crest Breaker", "physical", 17, 3)',
    'new Ability("Restoring Seal", "heal", 30, 4)',
    'new Ability("Shield Ram", "physical", 13, 2)',
):
    if marker not in prototype:
        raise SystemExit(f"v0.05 ability-cost verification failed for {marker}")

android_gradle = (root / "android/build.gradle").read_text()
for marker in ("versionCode 5", "versionName '0.05'", "diyse-prototype.keystore", "signingConfig signingConfigs.prototype"):
    if marker not in android_gradle:
        raise SystemExit(f"v0.05 Android signing/version verification failed for {marker}")

for screen in (root / "core/src/main/java/com/dj/diyse/screens").glob("*.java"):
    text = screen.read_text()
    for forbidden in ("environments/", "characters/", "enemies/"):
        if forbidden in text:
            raise SystemExit(f"Missing runtime asset reference remains in {screen}: {forbidden}")

keystore = root / "android/prototype-signing/diyse-prototype.keystore"
if keystore.stat().st_size < 1000:
    raise SystemExit("v0.05 permanent prototype keystore is missing or truncated")

print("Applied Diyse Prototype v0.05 combat-depth pass.")
