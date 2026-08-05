#!/usr/bin/env bash
set -euo pipefail

: "${GODOT_VERSION:=4.7.1}"
: "${PROJECT_DIR:=The_Role_of_the_Diyse_Godot_Prototype_v0.02}"
: "${APK_NAME:=The_Role_of_the_Diyse_v0.04.1_WP02R_QA.apk}"
: "${SIMULATOR_SHA256:=ca6cdb5aa2fa65031dd4d41bc53ce2f3a55c7bb1c50b8ca08da3ea23d893c59a}"
: "${BATTLE_SCENE_SHA256:=f9a391784df0bd24afa2e9d0ad1ee5739827e4c6d25a131fc80ebd519c977ea8}"
: "${AUTHORITY_ZIP_SHA256:=89bb3e75aa2658471bf1a092901fb69adcc1dd44059db8d1a96685e8f305fc19}"

WP01R_DIR="ci/godot-v0.02/wp01r"
WP02_DIR="ci/godot-v0.02/wp02"

printf '\n=== Install Android export packages ===\n'
yes | sdkmanager --licenses >/dev/null || true
sdkmanager \
  "platform-tools" \
  "build-tools;35.0.1" \
  "platforms;android-35" \
  "cmake;3.10.2.4988404" \
  "ndk;28.1.13356709"

printf '\n=== Reconstruct and verify v0.02.5 project sources ===\n'
cat ci/godot-v0.02/project.part.*.b64 | base64 --decode > /tmp/godot-v0.02.zip
unzip -qq -o /tmp/godot-v0.02.zip || true
test -f "${PROJECT_DIR}/project.godot"
echo "${SIMULATOR_SHA256}  ci/godot-v0.02/repairs/battle_simulator.gd" | sha256sum --check --strict
mkdir -p "${PROJECT_DIR}/src/core"
cp ci/godot-v0.02/repairs/battle_simulator.gd "${PROJECT_DIR}/src/core/battle_simulator.gd"
(
  cd "${PROJECT_DIR}"
  grep -v 'src/core/battle_simulator.gd$' SOURCE_MANIFEST.sha256 | sha256sum --strict -c -
)
echo "${SIMULATOR_SHA256}  ${PROJECT_DIR}/src/core/battle_simulator.gd" | sha256sum --check --strict
python "${PROJECT_DIR}/tools/validate_project.py"
python "${PROJECT_DIR}/tests/reference_battle_test.py"

printf '\n=== Apply v0.02.5 compatibility and battle repairs ===\n'
JOYSTICK="${PROJECT_DIR}/src/ui/virtual_joystick.gd"
RUIN="${PROJECT_DIR}/src/scenes/ruin_scene.gd"
BATTLE="${PROJECT_DIR}/src/scenes/battle_scene.gd"
PROJECT_SETTINGS="${PROJECT_DIR}/project.godot"
sed -i 's/^class_name VirtualJoystick$/class_name DiyseVirtualJoystick/' "${JOYSTICK}"
sed -i 's/VirtualJoystick/DiyseVirtualJoystick/g' "${RUIN}"
! grep -RInw --include='*.gd' 'VirtualJoystick' "${PROJECT_DIR}/src"
if grep -q '^textures/vram_compression/import_etc2_astc=' "${PROJECT_SETTINGS}"; then
  sed -i 's|^textures/vram_compression/import_etc2_astc=.*$|textures/vram_compression/import_etc2_astc=true|' "${PROJECT_SETTINGS}"
else
  sed -i '/^\[rendering\]$/a textures/vram_compression/import_etc2_astc=true' "${PROJECT_SETTINGS}"
fi
python ci/godot-v0.02/repairs/apply_qa_fixes.py "${PROJECT_DIR}"
cat ci/godot-v0.02/repairs/battle_scene.part.* > "${BATTLE}"
echo "${BATTLE_SCENE_SHA256}  ${BATTLE}" | sha256sum --check --strict
python ci/godot-v0.02/repairs/apply_battle_polish.py "${PROJECT_DIR}"

printf '\n=== Apply v0.02.5 compact ornate battle UI ===\n'
mkdir -p "${PROJECT_DIR}/assets/ui" "${PROJECT_DIR}/tests"
cp ci/godot-v0.02/assets/diyse_battle_outer_frame.svg "${PROJECT_DIR}/assets/ui/diyse_battle_outer_frame.svg"
cp ci/godot-v0.02/repairs/battle_polish_test.gd "${PROJECT_DIR}/tests/battle_polish_test.gd"
cp ci/godot-v0.02/repairs/battle_polish_test.tscn "${PROJECT_DIR}/tests/battle_polish_test.tscn"
cp ci/godot-v0.02/repairs/battle_ui_v0025_test.gd "${PROJECT_DIR}/tests/battle_ui_v0025_test.gd"
cp ci/godot-v0.02/repairs/battle_ui_v0025_test.tscn "${PROJECT_DIR}/tests/battle_ui_v0025_test.tscn"
python ci/godot-v0.02/repairs/apply_battle_ui_v0025.py "${PROJECT_DIR}"
grep -Fq 'confirm_button.text = "RESOLVE ROUND"' "${PROJECT_DIR}/src/scenes/battle_scene.gd"
grep -Fq 'edit_plan_button.text = "EDIT PLAN"' "${PROJECT_DIR}/src/scenes/battle_scene.gd"
grep -Fq 'frame.draw_center = false' "${PROJECT_DIR}/src/scenes/battle_scene.gd"
grep -Fq 'plan_label.max_lines_visible = 2' "${PROJECT_DIR}/src/scenes/battle_scene.gd"

printf '\n=== Reconstruct and validate v1.12 authority bundle ===\n'
cat "${WP01R_DIR}"/authority.part.*.b64 | base64 --decode > /tmp/diyse-authority-v1.12.zip
echo "${AUTHORITY_ZIP_SHA256}  /tmp/diyse-authority-v1.12.zip" | sha256sum --check --strict
rm -rf /tmp/diyse-authority-v1.12
mkdir -p /tmp/diyse-authority-v1.12
unzip -q /tmp/diyse-authority-v1.12.zip -d /tmp/diyse-authority-v1.12
python "${WP01R_DIR}/validate_wp01r_authority.py" /tmp/diyse-authority-v1.12 | tee wp01r-authority-python.log
grep -Fq "WP-01R VALIDATION: PASS" wp01r-authority-python.log

printf '\n=== Apply WP-01R Godot authority integration ===\n'
mkdir -p \
  "${PROJECT_DIR}/assets/authority/v1_12" \
  "${PROJECT_DIR}/src/autoload" \
  "${PROJECT_DIR}/tests"
cp -a /tmp/diyse-authority-v1.12/. "${PROJECT_DIR}/assets/authority/v1_12/"
cp "${WP01R_DIR}/authority_manager.gd" "${PROJECT_DIR}/src/autoload/authority_manager.gd"
cp "${WP01R_DIR}/authority_smoke_test.gd" "${PROJECT_DIR}/tests/authority_smoke_test.gd"
cp "${WP01R_DIR}/authority_smoke_test.tscn" "${PROJECT_DIR}/tests/authority_smoke_test.tscn"
python "${WP01R_DIR}/apply_wp01r.py" "${PROJECT_DIR}"
python "${WP01R_DIR}/validate_wp01r_authority.py" "${PROJECT_DIR}/assets/authority/v1_12" | tee wp01r-installed-authority.log
grep -Fqx 'const BUILD_VERSION := "0.03.1-WP01R"' "${PROJECT_DIR}/src/autoload/build_identity.gd"
grep -Fqx 'version/name="0.03.1-WP01R"' "${PROJECT_DIR}/export_presets.cfg"
grep -Fq 'AuthorityManager="*res://src/autoload/authority_manager.gd"' "${PROJECT_DIR}/project.godot"
test -f "${PROJECT_DIR}/assets/authority/v1_12/bundle_manifest.json"
test -f "${PROJECT_DIR}/assets/authority/v1_12/indexes/master_identity_index.json"

printf '\n=== Apply WP-02R save/UI integration and battle-frame removal ===\n'
cp "${WP02_DIR}/save_foundation.gd" "${PROJECT_DIR}/src/autoload/save_foundation.gd"
cp "${WP02_DIR}/wp02_save_regression_test.gd" "${PROJECT_DIR}/tests/wp02_save_regression_test.gd"
cp "${WP02_DIR}/wp02_save_regression_test.tscn" "${PROJECT_DIR}/tests/wp02_save_regression_test.tscn"
python "${WP02_DIR}/validate_wp02_contract.py" "${WP02_DIR}" | tee wp02-contract-validation.log
python "${WP02_DIR}/apply_wp02.py" "${PROJECT_DIR}"
grep -Fqx 'const BUILD_VERSION := "0.04.1-WP02R"' "${PROJECT_DIR}/src/autoload/build_identity.gd"
grep -Fqx 'version/name="0.04.1-WP02R"' "${PROJECT_DIR}/export_presets.cfg"
grep -Fq 'SaveFoundation="*res://src/autoload/save_foundation.gd"' "${PROJECT_DIR}/project.godot"
grep -Fq 'AuthorityManager="*res://src/autoload/authority_manager.gd"' "${PROJECT_DIR}/project.godot"
grep -Fq "WP-02 CONTRACT VALIDATION: PASS" wp02-contract-validation.log
grep -Fq 'const SLOT_ID := "autosave"' "${PROJECT_DIR}/src/autoload/save_manager.gd"
grep -Fq 'SaveFoundation.save_game(SLOT_ID, payload, "playable")' "${PROJECT_DIR}/src/autoload/save_manager.gd"
grep -Fq 'PASS: WP-02 device-path SaveManager' "${PROJECT_DIR}/tests/wp02_ui_save_integration_test.gd"
! grep -Fq 'OrnateBattleFrame' "${PROJECT_DIR}/src/scenes/battle_scene.gd"
! grep -Fq 'diyse_battle_outer_frame.svg' "${PROJECT_DIR}/src/scenes/battle_scene.gd"
test ! -f "${PROJECT_DIR}/assets/ui/diyse_battle_outer_frame.svg"

printf '\n=== Install Godot 4.7.1 and export templates ===\n'
GODOT_ROOT="${RUNNER_TEMP}/godot"
TEMPLATE_ROOT="${HOME}/.local/share/godot/export_templates/${GODOT_VERSION}.stable"
mkdir -p "${GODOT_ROOT}" "${TEMPLATE_ROOT}"
curl --fail --location --retry 4 --retry-delay 3 \
  --output /tmp/godot.zip \
  "https://github.com/godotengine/godot/releases/download/${GODOT_VERSION}-stable/Godot_v${GODOT_VERSION}-stable_linux.x86_64.zip"
unzip -q /tmp/godot.zip -d "${GODOT_ROOT}"
mv "${GODOT_ROOT}/Godot_v${GODOT_VERSION}-stable_linux.x86_64" "${GODOT_ROOT}/godot"
chmod +x "${GODOT_ROOT}/godot"
curl --fail --location --retry 4 --retry-delay 3 \
  --output /tmp/templates.tpz \
  "https://github.com/godotengine/godot/releases/download/${GODOT_VERSION}-stable/Godot_v${GODOT_VERSION}-stable_export_templates.tpz"
unzip -q /tmp/templates.tpz -d /tmp/godot-templates
cp -a /tmp/godot-templates/templates/. "${TEMPLATE_ROOT}/"
GODOT_BIN="${GODOT_ROOT}/godot"
"${GODOT_BIN}" --version
test -f "${TEMPLATE_ROOT}/android_debug.apk"

printf '\n=== Configure QA signing and Android paths ===\n'
KEYSTORE="${RUNNER_TEMP}/diyse-v0.04.1-wp02r-qa.keystore"
keytool -genkeypair \
  -keystore "${KEYSTORE}" \
  -storepass diyse-v0041-wp02r-qa \
  -alias diyse-v0041-wp02r-qa \
  -keypass diyse-v0041-wp02r-qa \
  -keyalg RSA \
  -keysize 2048 \
  -validity 3650 \
  -dname "CN=The Role of the Diyse WP-02R QA,O=Diyse Prototype,C=US"
export GODOT_ANDROID_KEYSTORE_DEBUG_PATH="${KEYSTORE}"
export GODOT_ANDROID_KEYSTORE_DEBUG_USER="diyse-v0041-wp02r-qa"
export GODOT_ANDROID_KEYSTORE_DEBUG_PASSWORD="diyse-v0041-wp02r-qa"
mkdir -p "${HOME}/.config/godot"
"${GODOT_BIN}" --headless --editor --path "${PROJECT_DIR}" --quit-after 2 || true
SETTINGS_FILE="$(find "${HOME}/.config/godot" -maxdepth 1 -type f -name 'editor_settings-4*.tres' | head -n 1)"
if [[ -z "${SETTINGS_FILE}" ]]; then
  SETTINGS_FILE="${HOME}/.config/godot/editor_settings-4.tres"
  printf '[gd_resource type="EditorSettings" format=3]\n\n[resource]\n' > "${SETTINGS_FILE}"
fi
printf '\nexport/android/android_sdk_path = "%s"\n' "${ANDROID_HOME}" >> "${SETTINGS_FILE}"
printf 'export/android/java_sdk_path = "%s"\n' "${JAVA_HOME}" >> "${SETTINGS_FILE}"
printf 'export/android/shutdown_adb_on_exit = false\n' >> "${SETTINGS_FILE}"

printf '\n=== Import and compile project ===\n'
set +e
"${GODOT_BIN}" --headless --editor --path "${PROJECT_DIR}" --import --quit-after 60 --verbose 2>&1 | tee godot-import.log
IMPORT_STATUS=${PIPESTATUS[0]}
set -e
test "${IMPORT_STATUS}" -eq 0
! grep -E "SCRIPT ERROR|Parse Error|Compile Error|ERROR: Failed to load script" godot-import.log

printf '\n=== Run WP-01R authority runtime smoke test ===\n'
set +e
"${GODOT_BIN}" --headless --path "${PROJECT_DIR}" --quit-after 240 --verbose res://tests/authority_smoke_test.tscn 2>&1 | tee authority-runtime.log
AUTHORITY_STATUS=${PIPESTATUS[0]}
set -e
test "${AUTHORITY_STATUS}" -eq 0
grep -Fq "PASS: WP-01R authority bundle loaded, verified, and enforced in Godot." authority-runtime.log
! grep -E "SCRIPT ERROR|Parse Error|Compile Error|WP-01R AUTHORITY TEST FAILED|DIYSE AUTHORITY FAILURE|ERROR:" authority-runtime.log

printf '\n=== Run WP-02 save and migration runtime regression ===\n'
set +e
"${GODOT_BIN}" --headless --path "${PROJECT_DIR}" --quit-after 240 --verbose res://tests/wp02_save_regression_test.tscn 2>&1 | tee wp02-save-runtime.log
WP02_STATUS=${PIPESTATUS[0]}
set -e
test "${WP02_STATUS}" -eq 0
grep -Fq "PASS: WP-02 atomic save, migration, rollback, recovery, completion metadata, and Final Return Save gates passed." wp02-save-runtime.log
! grep -E "SCRIPT ERROR|Parse Error|Compile Error|WP-02 SAVE TEST FAILED|Invalid call|Invalid assignment|Invalid access|ERROR:" wp02-save-runtime.log

printf '\n=== Run WP-02 device-path save and Continue integration regression ===\n'
set +e
"${GODOT_BIN}" --headless --path "${PROJECT_DIR}" --quit-after 240 --verbose res://tests/wp02_ui_save_integration_test.tscn 2>&1 | tee wp02-ui-save-runtime.log
WP02_UI_STATUS=${PIPESTATUS[0]}
set -e
test "${WP02_UI_STATUS}" -eq 0
grep -Fq "PASS: WP-02 device-path SaveManager, Continue, backup recovery, and title integration are operational." wp02-ui-save-runtime.log
! grep -E "SCRIPT ERROR|Parse Error|Compile Error|WP-02 UI SAVE INTEGRATION FAILED|Invalid call|Invalid assignment|Invalid access|ERROR:" wp02-ui-save-runtime.log

printf '\n=== Run inherited battle regressions ===\n'
set +e
"${GODOT_BIN}" --headless --path "${PROJECT_DIR}" --quit-after 180 --verbose res://src/scenes/battle_scene.tscn 2>&1 | tee battle-runtime.log
BATTLE_STATUS=${PIPESTATUS[0]}
set -e
test "${BATTLE_STATUS}" -eq 0
grep -Fq "DIYSE AUTHORITY READY: registries=75 records=7800 canonical_ids=2098" battle-runtime.log
! grep -E "SCRIPT ERROR|Parse Error|Compile Error|Invalid call|Invalid assignment|Invalid access|DIYSE AUTHORITY FAILURE|ERROR:" battle-runtime.log

set +e
"${GODOT_BIN}" --headless --path "${PROJECT_DIR}" --quit-after 180 --verbose res://tests/battle_polish_test.tscn 2>&1 | tee battle-polish-test.log
POLISH_STATUS=${PIPESTATUS[0]}
set -e
test "${POLISH_STATUS}" -eq 0
grep -Fq "PASS: dead-target retargeting and touch ability scrolling are operational." battle-polish-test.log
! grep -E "SCRIPT ERROR|Parse Error|Compile Error|Invalid call|Invalid assignment|Invalid access|DIYSE AUTHORITY FAILURE|ERROR:" battle-polish-test.log

set +e
"${GODOT_BIN}" --headless --path "${PROJECT_DIR}" --quit-after 180 --verbose res://tests/battle_ui_v0025_test.tscn 2>&1 | tee battle-ui-test.log
UI_STATUS=${PIPESTATUS[0]}
set -e
test "${UI_STATUS}" -eq 0
grep -Fq "PASS: compact fixed round controls instantiate without the custom outer battle frame." battle-ui-test.log
! grep -E "SCRIPT ERROR|Parse Error|Compile Error|Invalid call|Invalid assignment|Invalid access|DIYSE AUTHORITY FAILURE|ERROR:" battle-ui-test.log

printf '\n=== Export and verify signed WP-02 QA APK ===\n'
mkdir -p "${PROJECT_DIR}/build/android" android-artifact
set +e
"${GODOT_BIN}" \
  --headless \
  --path "${PROJECT_DIR}" \
  --export-debug "Android QA" \
  "${GITHUB_WORKSPACE}/${PROJECT_DIR}/build/android/${APK_NAME}" \
  --verbose 2>&1 | tee godot-export.log
EXPORT_STATUS=${PIPESTATUS[0]}
set -e
test "${EXPORT_STATUS}" -eq 0
APK="${PROJECT_DIR}/build/android/${APK_NAME}"
test -s "${APK}"
unzip -t "${APK}"
unzip -l "${APK}" | grep -Fq "assets/authority/v1_12/bundle_manifest.json"
unzip -l "${APK}" | grep -Fq "assets/src/autoload/save_foundation.gdc"
unzip -l "${APK}" | grep -Fq "assets/src/autoload/save_manager.gdc"
! unzip -l "${APK}" | grep -Fq "diyse_battle_outer_frame"
"${ANDROID_HOME}/build-tools/35.0.1/apksigner" verify --verbose --print-certs "${APK}" | tee apk-signature.txt
sha256sum "${APK}" | tee "${APK}.sha256"
cp \
  "${APK}" \
  "${APK}.sha256" \
  wp01r-authority-python.log \
  wp01r-installed-authority.log \
  wp02-contract-validation.log \
  authority-runtime.log \
  wp02-save-runtime.log \
  wp02-ui-save-runtime.log \
  godot-import.log \
  battle-runtime.log \
  battle-polish-test.log \
  battle-ui-test.log \
  godot-export.log \
  apk-signature.txt \
  android-artifact/

printf '\nWP-02R DEVICE-INTEGRATED CI BUILD: PASS\n'
