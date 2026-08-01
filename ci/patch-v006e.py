from pathlib import Path
import base64
import hashlib
import io
import zipfile

root = Path("source")
parts = [Path("ci/v006e") / f"part-{index:02d}.txt" for index in range(8)]
for part in parts:
    if not part.is_file():
        raise SystemExit(f"Missing Diyse v0.06E payload segment: {part}")

payload_text = "".join(part.read_text().strip() for part in parts)
try:
    payload = base64.b64decode(payload_text, validate=True)
except Exception as exception:
    raise SystemExit(f"v0.06E payload Base64 validation failed: {exception}")

expected_sha256 = "29905bbdd0522c55b79a0edca6c8a320822ec8b4f3f7c3e603e494259d70414e"
actual_sha256 = hashlib.sha256(payload).hexdigest()
if actual_sha256 != expected_sha256:
    raise SystemExit(f"v0.06E payload checksum mismatch: {actual_sha256}")

try:
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        bad_member = archive.testzip()
        if bad_member is not None:
            raise SystemExit(f"v0.06E payload ZIP integrity failed at {bad_member}")
        archive.extractall(root)
except zipfile.BadZipFile as exception:
    raise SystemExit(f"v0.06E payload is not a valid ZIP: {exception}")

required = [
    "core/src/main/java/com/dj/diyse/DiyseGame.java",
    "core/src/main/java/com/dj/diyse/combat/BattleArenaOrientation.java",
    "core/src/main/java/com/dj/diyse/combat/BattleModelOrientation.java",
    "core/src/main/java/com/dj/diyse/screens/BattleScreen.java",
    "core/src/test/java/com/dj/diyse/combat/BattleArenaOrientationTest.java",
    "core/src/test/java/com/dj/diyse/combat/BattleModelOrientationTest.java",
    "android/build.gradle",
    "android/prototype-signing/diyse-prototype.keystore",
    "docs/CHANGELOG_v0.06E.md",
]
for relative in required:
    if not (root / relative).is_file():
        raise SystemExit(f"v0.06E patch did not create or preserve {relative}")

version = (root / "core/src/main/java/com/dj/diyse/DiyseGame.java").read_text()
if 'VERSION = "0.06E"' not in version:
    raise SystemExit("v0.06E game version verification failed")

game_state = (root / "core/src/main/java/com/dj/diyse/model/GameState.java").read_text()
for marker in ('SAVE_SCHEMA_VERSION = 3', 'putString("save_build", "0.06E")'):
    if marker not in game_state:
        raise SystemExit(f"v0.06E save compatibility verification failed for {marker}")

arena_orientation = (root / "core/src/main/java/com/dj/diyse/combat/BattleArenaOrientation.java").read_text()
for marker in (
    "regression tests can fail independently",
    "return new float[] { x, y + height, width, -height }",
):
    if marker not in arena_orientation:
        raise SystemExit(f"v0.06E arena orientation verification failed for {marker}")

model_orientation = (root / "core/src/main/java/com/dj/diyse/combat/BattleModelOrientation.java").read_text()
for marker in (
    "mirrorHorizontally ? x + width : x",
    "mirrorHorizontally ? -width : width",
    "-height",
):
    if marker not in model_orientation:
        raise SystemExit(f"v0.06E model orientation preservation failed for {marker}")

battle = (root / "core/src/main/java/com/dj/diyse/screens/BattleScreen.java").read_text()
for marker in (
    "BattleArenaOrientation.upright",
    "backgroundDraw",
    "atmosphereDraw",
    "foregroundDraw",
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
        raise SystemExit(f"v0.06E battle verification failed for {marker}")
if battle.count("BattleArenaOrientation.upright") != 3:
    raise SystemExit("v0.06E must orient exactly three arena layers")
if battle.count("BattleModelOrientation.upright") != 2:
    raise SystemExit("v0.06E changed the two model-orientation call sites")
for forbidden in (
    "game.batch().draw(arenaBackground, shake, 0, DiyseGame.WORLD_WIDTH, DiyseGame.WORLD_HEIGHT);",
    "game.batch().draw(arenaForeground, shake * 0.35f, 0, DiyseGame.WORLD_WIDTH, DiyseGame.WORLD_HEIGHT);",
):
    if forbidden in battle:
        raise SystemExit(f"v0.06E still contains upside-down arena draw path: {forbidden}")

changelog = (root / "docs/CHANGELOG_v0.06E.md").read_text()
for marker in (
    "current v0.80 active master canon authority",
    "background, atmosphere, and foreground layers",
    "v0.06D upright party and mirrored-upright Black Host model transforms unchanged",
    "Save schema 3",
    "exact Crest of Yahtrea is not approximated",
):
    if marker not in changelog:
        raise SystemExit(f"v0.06E changelog verification failed for {marker}")

android_gradle = (root / "android/build.gradle").read_text()
for marker in ("versionCode 10", "versionName '0.06E'", "diyse-prototype.keystore", "signingConfig signingConfigs.prototype"):
    if marker not in android_gradle:
        raise SystemExit(f"v0.06E Android signing/version verification failed for {marker}")

keystore = root / "android/prototype-signing/diyse-prototype.keystore"
if keystore.stat().st_size < 1000:
    raise SystemExit("v0.06E permanent prototype keystore is missing or truncated")

print("Applied Diyse Prototype v0.06E battle background orientation correction.")
