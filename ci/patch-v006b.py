from pathlib import Path
import base64
import hashlib
import io
import zipfile

root = Path("source")
parts = sorted((Path("ci") / "v006b").glob("part-*.txt"))
if len(parts) != 4:
    raise SystemExit(f"Expected 4 Diyse v0.06B payload parts, found {len(parts)}")

payload_text = "".join(part.read_text().strip() for part in parts)
try:
    payload = base64.b64decode(payload_text, validate=True)
except Exception as exception:
    raise SystemExit(f"v0.06B payload Base64 validation failed: {exception}")

expected_sha256 = "dca69fbedf5d040b5424ae6a4c919baeabee44d59d7c5acbc3df621d402730bb"
actual_sha256 = hashlib.sha256(payload).hexdigest()
if actual_sha256 != expected_sha256:
    raise SystemExit(f"v0.06B payload checksum mismatch: {actual_sha256}")

try:
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        bad_member = archive.testzip()
        if bad_member is not None:
            raise SystemExit(f"v0.06B payload ZIP integrity failed at {bad_member}")
        archive.extractall(root)
except zipfile.BadZipFile as exception:
    raise SystemExit(f"v0.06B payload is not a valid ZIP: {exception}")

required = [
    "core/src/main/java/com/dj/diyse/DiyseGame.java",
    "core/src/main/java/com/dj/diyse/exploration/CourtyardInteraction.java",
    "core/src/main/java/com/dj/diyse/exploration/CourtyardWalkmesh.java",
    "core/src/main/java/com/dj/diyse/screens/CourtyardScreen.java",
    "core/src/main/java/com/dj/diyse/ui/FieldCharacterArt.java",
    "core/src/main/java/com/dj/diyse/ui/FixedCameraCourtyardArt.java",
    "core/src/test/java/com/dj/diyse/exploration/CourtyardInteractionTest.java",
    "core/src/test/java/com/dj/diyse/exploration/CourtyardWalkmeshTest.java",
    "android/build.gradle",
    "android/prototype-signing/diyse-prototype.keystore",
    "docs/CHANGELOG_v0.06B.md",
]
for relative in required:
    if not (root / relative).is_file():
        raise SystemExit(f"v0.06B patch did not create {relative}")

version = (root / "core/src/main/java/com/dj/diyse/DiyseGame.java").read_text()
if 'VERSION = "0.06B"' not in version:
    raise SystemExit("v0.06B game version verification failed")

game_state = (root / "core/src/main/java/com/dj/diyse/model/GameState.java").read_text()
for marker in ('SAVE_SCHEMA_VERSION = 3', 'putString("save_build", "0.06B")'):
    if marker not in game_state:
        raise SystemExit(f"v0.06B save compatibility verification failed for {marker}")

interaction = (root / "core/src/main/java/com/dj/diyse/exploration/CourtyardInteraction.java").read_text()
for marker in (
    "NORMAL_FIELD_LEAD_COUNT = 1",
    "NORMAL_EXPLORATION_USES_FOLLOWERS = false",
    '"Inspect Orders"',
    '"Collect Supply"',
    '"Enter Incursion"',
    '"File Report"',
):
    if marker not in interaction:
        raise SystemExit(f"v0.06B field-direction verification failed for {marker}")

courtyard = (root / "core/src/main/java/com/dj/diyse/screens/CourtyardScreen.java").read_text()
for marker in (
    "FixedCameraCourtyardArt.atmosphere",
    "acceleration = length > 0f",
    "drawCharacterShadow",
    "drawAmbientDust",
    "transitionToBattle",
    "SINGLE FIELD LEAD",
):
    if marker not in courtyard:
        raise SystemExit(f"v0.06B courtyard verification failed for {marker}")
for forbidden in ("PartyFollower", "followerPositions", "new FieldCharacterArt(\"Ilyra\"", "new FieldCharacterArt(\"Torren\""):
    if forbidden in courtyard:
        raise SystemExit(f"v0.06B introduced forbidden follower implementation: {forbidden}")

walkmesh = (root / "core/src/main/java/com/dj/diyse/exploration/CourtyardWalkmesh.java").read_text()
for marker in ("movementScaleAt", "lerp(1f, 0.72f", "Axis-separated collision"):
    if marker not in walkmesh:
        raise SystemExit(f"v0.06B movement verification failed for {marker}")

field_art = (root / "core/src/main/java/com/dj/diyse/ui/FieldCharacterArt.java").read_text()
for marker in ("FRAME_COUNT = 4", "Frame zero is idle", "coat tails", "Original procedural"):
    if marker not in field_art:
        raise SystemExit(f"v0.06B field-model verification failed for {marker}")

scene_art = (root / "core/src/main/java/com/dj/diyse/ui/FixedCameraCourtyardArt.java").read_text()
for marker in ("public static Texture atmosphere", "green-glass windows", "exact approved Crest", "pre-rendered-style"):
    if marker not in scene_art:
        raise SystemExit(f"v0.06B scene-art verification failed for {marker}")

changelog = (root / "docs/CHANGELOG_v0.06B.md").read_text()
for marker in ("current v0.80 active master authority", "does not use automatic party followers", "Save schema 3", "exact Crest of Yahtrea"):
    if marker not in changelog:
        raise SystemExit(f"v0.06B canon/status verification failed for {marker}")

android_gradle = (root / "android/build.gradle").read_text()
for marker in ("versionCode 7", "versionName '0.06B'", "diyse-prototype.keystore", "signingConfig signingConfigs.prototype"):
    if marker not in android_gradle:
        raise SystemExit(f"v0.06B Android signing/version verification failed for {marker}")

for screen in (root / "core/src/main/java/com/dj/diyse/screens").glob("*.java"):
    text = screen.read_text()
    for forbidden in ("environments/", "characters/", "enemies/"):
        if forbidden in text:
            raise SystemExit(f"Missing runtime asset reference remains in {screen}: {forbidden}")

keystore = root / "android/prototype-signing/diyse-prototype.keystore"
if keystore.stat().st_size < 1000:
    raise SystemExit("v0.06B permanent prototype keystore is missing or truncated")

print("Applied Diyse Prototype v0.06B field-presentation refinement.")
