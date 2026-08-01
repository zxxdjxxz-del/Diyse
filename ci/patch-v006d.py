from pathlib import Path
import base64
import hashlib
import io
import zipfile

root = Path("source")
parts = [Path("ci/v006d_safe") / f"part-{index:02d}.txt" for index in range(6)]
for part in parts:
    if not part.is_file():
        raise SystemExit(f"Missing Diyse v0.06D safe payload segment: {part}")

payload_text = "".join(part.read_text().strip() for part in parts)
try:
    payload = base64.b64decode(payload_text, validate=True)
except Exception as exception:
    raise SystemExit(f"v0.06D payload Base64 validation failed: {exception}")

expected_sha256 = "016da928a730590da1441898e917ce0787d73d71ee758f527c1cff41ba8dafd9"
actual_sha256 = hashlib.sha256(payload).hexdigest()
if actual_sha256 != expected_sha256:
    raise SystemExit(f"v0.06D payload checksum mismatch: {actual_sha256}")

try:
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        bad_member = archive.testzip()
        if bad_member is not None:
            raise SystemExit(f"v0.06D payload ZIP integrity failed at {bad_member}")
        archive.extractall(root)
except zipfile.BadZipFile as exception:
    raise SystemExit(f"v0.06D payload is not a valid ZIP: {exception}")

required = [
    "core/src/main/java/com/dj/diyse/DiyseGame.java",
    "core/src/main/java/com/dj/diyse/combat/BattleModelOrientation.java",
    "core/src/main/java/com/dj/diyse/screens/BattleScreen.java",
    "core/src/test/java/com/dj/diyse/combat/BattleModelOrientationTest.java",
    "android/build.gradle",
    "android/prototype-signing/diyse-prototype.keystore",
    "docs/CHANGELOG_v0.06D.md",
]
for relative in required:
    if not (root / relative).is_file():
        raise SystemExit(f"v0.06D patch did not create {relative}")

version = (root / "core/src/main/java/com/dj/diyse/DiyseGame.java").read_text()
if 'VERSION = "0.06D"' not in version:
    raise SystemExit("v0.06D game version verification failed")

game_state = (root / "core/src/main/java/com/dj/diyse/model/GameState.java").read_text()
for marker in ('SAVE_SCHEMA_VERSION = 3', 'putString("save_build", "0.06D")'):
    if marker not in game_state:
        raise SystemExit(f"v0.06D save compatibility verification failed for {marker}")

orientation = (root / "core/src/main/java/com/dj/diyse/combat/BattleModelOrientation.java").read_text()
for marker in (
    "negative draw height performs the required single vertical correction",
    "mirrorHorizontally ? x + width : x",
    "y + height",
    "mirrorHorizontally ? -width : width",
    "-height",
):
    if marker not in orientation:
        raise SystemExit(f"v0.06D orientation transform verification failed for {marker}")

battle = (root / "core/src/main/java/com/dj/diyse/screens/BattleScreen.java").read_text()
for marker in (
    "BattleModelOrientation.upright(x, y, p[2], p[3], false)",
    "BattleModelOrientation.upright(x, y, p[2], p[3], true)",
    "Items → Defend → Speed.",
    "EnemyBehavior.lockActions",
    "ENCOUNTER_XP = 40",
    "attack + power - defense / 2",
    "magic + power - resistance / 2",
    "presentation.consumeImpact",
):
    if marker not in battle:
        raise SystemExit(f"v0.06D battle preservation verification failed for {marker}")
for forbidden in (
    "game.batch().draw(texture, x + p[2], y, -p[2], p[3]);",
    "game.batch().draw(partyModel(i).texture(partyPose(i)), x, y, p[2], p[3]);",
):
    if forbidden in battle:
        raise SystemExit(f"v0.06D still contains upside-down draw path: {forbidden}")

changelog = (root / "docs/CHANGELOG_v0.06D.md").read_text()
for marker in (
    "Current v0.80 active master canon authority",
    "exactly one vertical texture-coordinate correction",
    "Enemy models retain their intended horizontal mirroring",
    "Save schema 3",
    "exact Crest of Yahtrea is not approximated",
):
    if marker not in changelog:
        raise SystemExit(f"v0.06D changelog verification failed for {marker}")

android_gradle = (root / "android/build.gradle").read_text()
for marker in ("versionCode 9", "versionName '0.06D'", "diyse-prototype.keystore", "signingConfig signingConfigs.prototype"):
    if marker not in android_gradle:
        raise SystemExit(f"v0.06D Android signing/version verification failed for {marker}")

keystore = root / "android/prototype-signing/diyse-prototype.keystore"
if keystore.stat().st_size < 1000:
    raise SystemExit("v0.06D permanent prototype keystore is missing or truncated")

print("Applied Diyse Prototype v0.06D battle orientation correction.")
