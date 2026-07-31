from pathlib import Path
import base64
import hashlib
import io
import zipfile

root = Path("source")
parts = sorted((Path("ci") / "v003").glob("part-*.txt"))
if not parts:
    raise SystemExit("No Diyse v0.03 payload parts were found")

payload_text = "".join(part.read_text().strip() for part in parts)
try:
    payload = base64.b64decode(payload_text, validate=True)
except Exception as exception:
    raise SystemExit(f"v0.03 payload Base64 validation failed: {exception}")

expected_sha256 = "8f79123bfce556df3ced5cb71ac2952aea81fe7561e9db499d0f69e78920c377"
actual_sha256 = hashlib.sha256(payload).hexdigest()
if actual_sha256 != expected_sha256:
    raise SystemExit(f"v0.03 payload checksum mismatch: {actual_sha256}")

try:
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        bad_member = archive.testzip()
        if bad_member is not None:
            raise SystemExit(f"v0.03 payload ZIP integrity failed at {bad_member}")
        archive.extractall(root)
except zipfile.BadZipFile as exception:
    raise SystemExit(f"v0.03 payload is not a valid ZIP: {exception}")

required = [
    "core/src/main/java/com/dj/diyse/DiyseGame.java",
    "core/src/main/java/com/dj/diyse/screens/CourtyardScreen.java",
    "core/src/test/java/com/dj/diyse/VersionContractTest.java",
    "android/build.gradle",
    "android/prototype-signing/diyse-prototype.keystore",
    "docs/CHANGELOG_v0.03.md",
]
for relative in required:
    if not (root / relative).is_file():
        raise SystemExit(f"v0.03 patch did not create {relative}")

version = (root / "core/src/main/java/com/dj/diyse/DiyseGame.java").read_text()
if 'VERSION = "0.03"' not in version:
    raise SystemExit("v0.03 game version verification failed")

courtyard = (root / "core/src/main/java/com/dj/diyse/screens/CourtyardScreen.java").read_text()
for marker in ("Party / Objective", "PARTY & OBJECTIVE", "Training incursion cleared"):
    if marker not in courtyard:
        raise SystemExit(f"v0.03 courtyard verification failed for {marker}")

android_gradle = (root / "android/build.gradle").read_text()
for marker in ("versionCode 3", "versionName '0.03'", "diyse-prototype.keystore", "signingConfig signingConfigs.prototype"):
    if marker not in android_gradle:
        raise SystemExit(f"v0.03 Android signing/version verification failed for {marker}")

for screen in (root / "core/src/main/java/com/dj/diyse/screens").glob("*.java"):
    text = screen.read_text()
    for forbidden in ("environments/", "characters/", "enemies/"):
        if forbidden in text:
            raise SystemExit(f"Missing runtime asset reference remains in {screen}: {forbidden}")

keystore = root / "android/prototype-signing/diyse-prototype.keystore"
if keystore.stat().st_size < 1000:
    raise SystemExit("v0.03 prototype keystore is missing or truncated")

print("Applied Diyse Prototype v0.03 party/objective and permanent prototype-signing pass.")
