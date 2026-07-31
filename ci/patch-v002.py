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

# The repository's compact source archive does not reliably retain the original
# binary launcher icon. Supply a deterministic provisional vector icon so AAPT
# can always link the v0.02 Android package. This is not final Diyse branding.
icon_path = root / "android/src/main/res/drawable/diyse_icon_v002.xml"
icon_path.parent.mkdir(parents=True, exist_ok=True)
icon_path.write_text('''<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path android:fillColor="#073A26" android:pathData="M0,0h108v108h-108z" />
    <path android:fillColor="#D6B45B" android:pathData="M14,10h80v88h-80z" />
    <path android:fillColor="#0B4A32" android:pathData="M21,17h66v74h-66z" />
    <path android:fillColor="#F4EBD8" android:pathData="M34,29h23c19,0 30,10 30,25s-11,25 -30,25h-23zM47,41v26h10c11,0 17,-5 17,-13s-6,-13 -17,-13z" />
</vector>
''')

manifest_path = root / "android/src/main/AndroidManifest.xml"
manifest = manifest_path.read_text()
if 'android:icon="@drawable/icon"' not in manifest:
    raise SystemExit("Expected provisional Android icon reference was not found in the manifest")
manifest_path.write_text(manifest.replace(
    'android:icon="@drawable/icon"',
    'android:icon="@drawable/diyse_icon_v002"',
    1,
))

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

if not icon_path.is_file() or "diyse_icon_v002" not in manifest_path.read_text():
    raise SystemExit("v0.02 Android icon verification failed")

print("Applied Diyse Prototype v0.02 identity, HUD, save-schema, and provisional launcher-icon pass.")
