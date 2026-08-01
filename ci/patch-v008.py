from pathlib import Path
import base64
import hashlib
import io
import zipfile

root = Path("source")
parts = sorted((Path("ci") / "v008").glob("part-*.txt"))
if len(parts) != 10:
    raise SystemExit(f"Expected 10 Diyse v0.08 payload parts, found {len(parts)}")

payload_text = "".join(part.read_text().strip() for part in parts)
try:
    payload = base64.b64decode(payload_text, validate=True)
except Exception as exception:
    raise SystemExit(f"v0.08 payload Base64 validation failed: {exception}")

expected_sha256 = "29dd00a6c2f03acc8aafe29ec0af0f78745fadf4c909238db8e0475dba7b520c"
actual_sha256 = hashlib.sha256(payload).hexdigest()
if actual_sha256 != expected_sha256:
    raise SystemExit(f"v0.08 payload checksum mismatch: {actual_sha256}")

try:
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        bad_member = archive.testzip()
        if bad_member is not None:
            raise SystemExit(f"v0.08 payload ZIP integrity failed at {bad_member}")
        archive.extractall(root)
except zipfile.BadZipFile as exception:
    raise SystemExit(f"v0.08 payload is not a valid ZIP: {exception}")

required = [
    "core/src/main/java/com/dj/diyse/DiyseGame.java",
    "core/src/main/java/com/dj/diyse/model/GameState.java",
    "core/src/main/java/com/dj/diyse/screens/MenuScreen.java",
    "core/src/main/java/com/dj/diyse/screens/BattleScreen.java",
    "core/src/test/java/com/dj/diyse/model/CardLoadoutInteractionTest.java",
    "docs/CHANGELOG_v0.08.md",
    "android/build.gradle",
    "android/prototype-signing/diyse-prototype.keystore",
]
for relative in required:
    if not (root / relative).is_file():
        raise SystemExit(f"v0.08 patch did not create {relative}")

version = (root / "core/src/main/java/com/dj/diyse/DiyseGame.java").read_text()
if 'VERSION = "0.08"' not in version:
    raise SystemExit("v0.08 game version verification failed")

game_state = (root / "core/src/main/java/com/dj/diyse/model/GameState.java").read_text()
for marker in (
    "SAVE_SCHEMA_VERSION = 4",
    'putString("save_build", "0.08")',
    "boolean setStandardCard",
    "boolean setPrimeCard",
    "CardDefinition.SlotType.STANDARD",
    "CardDefinition.SlotType.PRIME",
):
    if marker not in game_state:
        raise SystemExit(f"v0.08 GameState verification failed for {marker}")

menu = (root / "core/src/main/java/com/dj/diyse/screens/MenuScreen.java").read_text()
for marker in (
    "Tap either Standard slot to equip or remove",
    "game.state().setStandardCard",
    "Loadout saved.",
    "Personal Prime: Empty",
    "Duplicate diagnostics equips are allowed only for this test",
):
    if marker not in menu:
        raise SystemExit(f"v0.08 Cards menu verification failed for {marker}")

battle = (root / "core/src/main/java/com/dj/diyse/screens/BattleScreen.java").read_text()
for marker in (
    "cardSlotButtons",
    "selectingCardSlot",
    "chooseCardSlot",
    "Choose a Standard Card slot",
    "actionName(actor, action.command, action.cardSlot)",
    "cardBattleState.remaining(pendingActor, slot)",
    "Items → Defend → Speed.",
):
    if marker not in battle:
        raise SystemExit(f"v0.08 battle slot-selection verification failed for {marker}")
if "cardUsed" in battle:
    raise SystemExit("v0.08 restored the retired universal Card-use flag")

prototype = (root / "core/src/main/java/com/dj/diyse/model/PrototypeData.java").read_text()
if prototype.count("new CardDefinition(") != 1:
    raise SystemExit("v0.08 unexpectedly changed the prototype Card catalog")
if "PROTOTYPE_STANDARD_CARD_ID" not in prototype or "SlotType.STANDARD" not in prototype:
    raise SystemExit("v0.08 diagnostics Card verification failed")

changelog = (root / "docs/CHANGELOG_v0.08.md").read_text()
for marker in (
    "explicit Standard slot selection",
    "not one of the approved 35 Standard Cards",
    "Save schema remains 4",
    "current v0.80 active master canon authority",
):
    if marker not in changelog:
        raise SystemExit(f"v0.08 canon/status verification failed for {marker}")

android_gradle = (root / "android/build.gradle").read_text()
for marker in ("versionCode 12", "versionName '0.08'", "diyse-prototype.keystore", "signingConfig signingConfigs.prototype"):
    if marker not in android_gradle:
        raise SystemExit(f"v0.08 Android signing/version verification failed for {marker}")

keystore = root / "android/prototype-signing/diyse-prototype.keystore"
if keystore.stat().st_size < 1000:
    raise SystemExit("v0.08 permanent prototype keystore is missing or truncated")

print("Applied Diyse Prototype v0.08 Card loadout interaction pass.")
