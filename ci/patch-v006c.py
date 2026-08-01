from pathlib import Path
import base64
import hashlib
import io
import zipfile

root = Path("source")
parts = sorted((Path("ci") / "v006c").glob("part-*.txt"))
if len(parts) != 4:
    raise SystemExit(f"Expected 4 Diyse v0.06C payload parts, found {len(parts)}")

payload_text = "".join(part.read_text().strip() for part in parts)
try:
    payload = base64.b64decode(payload_text, validate=True)
except Exception as exception:
    raise SystemExit(f"v0.06C payload Base64 validation failed: {exception}")

expected_sha256 = "574024eff56110b7fc2b343118598103550eba7b06c6f52604744d5c5c7ef572"
actual_sha256 = hashlib.sha256(payload).hexdigest()
if actual_sha256 != expected_sha256:
    raise SystemExit(f"v0.06C payload checksum mismatch: {actual_sha256}")

try:
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        bad_member = archive.testzip()
        if bad_member is not None:
            raise SystemExit(f"v0.06C payload ZIP integrity failed at {bad_member}")
        archive.extractall(root)
except zipfile.BadZipFile as exception:
    raise SystemExit(f"v0.06C payload is not a valid ZIP: {exception}")

required = [
    "core/src/main/java/com/dj/diyse/DiyseGame.java",
    "core/src/main/java/com/dj/diyse/combat/BattlePresentation.java",
    "core/src/main/java/com/dj/diyse/screens/BattleScreen.java",
    "core/src/main/java/com/dj/diyse/screens/MenuScreen.java",
    "core/src/main/java/com/dj/diyse/ui/BattleArenaArt.java",
    "core/src/main/java/com/dj/diyse/ui/BattleModelArt.java",
    "core/src/test/java/com/dj/diyse/combat/BattlePresentationTest.java",
    "android/build.gradle",
    "android/prototype-signing/diyse-prototype.keystore",
    "docs/CHANGELOG_v0.06C.md",
]
for relative in required:
    if not (root / relative).is_file():
        raise SystemExit(f"v0.06C patch did not create {relative}")

version = (root / "core/src/main/java/com/dj/diyse/DiyseGame.java").read_text()
if 'VERSION = "0.06C"' not in version:
    raise SystemExit("v0.06C game version verification failed")

game_state = (root / "core/src/main/java/com/dj/diyse/model/GameState.java").read_text()
for marker in ('SAVE_SCHEMA_VERSION = 3', 'putString("save_build", "0.06C")'):
    if marker not in game_state:
        raise SystemExit(f"v0.06C save compatibility verification failed for {marker}")

battle = (root / "core/src/main/java/com/dj/diyse/screens/BattleScreen.java").read_text()
for marker in (
    "BattleArenaArt.background",
    "BattleModelArt.cyanis",
    "startNextPresentedAction",
    "presentation.consumeImpact",
    "drawActionEffect",
    "victoryPoseTime",
    "screenTransitioned",
    "Items → Defend → Speed.",
    "EnemyBehavior.lockActions",
    "ENCOUNTER_XP = 40",
    "Prototype Card Test",
    "temporary prototype Card",
    "attack + power - defense / 2",
    "magic + power - resistance / 2",
):
    if marker not in battle:
        raise SystemExit(f"v0.06C battle-presentation verification failed for {marker}")
if " RES" in battle:
    raise SystemExit("v0.06C BattleScreen still exposes retired RES terminology")

menu = (root / "core/src/main/java/com/dj/diyse/screens/MenuScreen.java").read_text()
if " RES" in menu or " MP " not in menu:
    raise SystemExit("v0.06C menu MP terminology verification failed")

presentation = (root / "core/src/main/java/com/dj/diyse/combat/BattlePresentation.java").read_text()
for marker in ("enum Kind", "enum Phase", "consumeImpact", "actorOffsetX", "impactFlashAlpha", "kindFor"):
    if marker not in presentation:
        raise SystemExit(f"v0.06C presentation-timing verification failed for {marker}")

models = (root / "core/src/main/java/com/dj/diyse/ui/BattleModelArt.java").read_text()
for marker in ("enum Pose", "STRIKE", "CAST", "GUARD", "HURT", "DOWN", "VICTORY", "test silhouettes"):
    if marker not in models:
        raise SystemExit(f"v0.06C battle-model verification failed for {marker}")

arena = (root / "core/src/main/java/com/dj/diyse/ui/BattleArenaArt.java").read_text()
for marker in ("pre-rendered-style battle arena", "deliberately not the Crest", "targetRing", "impactGlow", "magicOrb"):
    if marker not in arena:
        raise SystemExit(f"v0.06C arena verification failed for {marker}")

changelog = (root / "docs/CHANGELOG_v0.06C.md").read_text()
for marker in (
    "current **v0.80 active master canon**",
    "exact Crest of Yahtrea is not approximated",
    "No balance values or enemy decision rules were changed",
    "Save schema remains 3",
):
    if marker not in changelog:
        raise SystemExit(f"v0.06C canon/status verification failed for {marker}")

android_gradle = (root / "android/build.gradle").read_text()
for marker in ("versionCode 8", "versionName '0.06C'", "diyse-prototype.keystore", "signingConfig signingConfigs.prototype"):
    if marker not in android_gradle:
        raise SystemExit(f"v0.06C Android signing/version verification failed for {marker}")

keystore = root / "android/prototype-signing/diyse-prototype.keystore"
if keystore.stat().st_size < 1000:
    raise SystemExit("v0.06C permanent prototype keystore is missing or truncated")

print("Applied Diyse Prototype v0.06C battle graphics vertical slice.")
