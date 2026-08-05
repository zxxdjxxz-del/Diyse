#!/usr/bin/env bash
set -euo pipefail

: "${GODOT_VERSION:=4.7.1}"
: "${PROJECT_DIR:=The_Role_of_the_Diyse_Godot_Prototype_v0.02}"
: "${WP03_APK_NAME:=The_Role_of_the_Diyse_v0.05.1_WP03R_QA.apk}"

WP03_TRANSPORT_DIR="ci/godot-v0.02/wp03/source"
WP03_SOURCE_SHA256="0a20d960b9ed5887ce5ecc3be58e1495355e5744c70b518adae747af16621a99"
WP03_DIR="/tmp/wp03_source_package"
BASELINE_APK_NAME="The_Role_of_the_Diyse_v0.04.1_WP02R_QA.apk"

printf '\n=== Reconstruct and verify WP-03 source package ===\n'
cat "${WP03_TRANSPORT_DIR}"/source.part.* | base64 --decode > /tmp/wp03-source.tar.xz
echo "${WP03_SOURCE_SHA256}  /tmp/wp03-source.tar.xz" | sha256sum --check --strict
rm -rf "${WP03_DIR}"
tar -xJf /tmp/wp03-source.tar.xz -C /tmp
python ci/godot-v0.02/wp03/apply_wp03r_input_fix.py "${WP03_DIR}"
python "${WP03_DIR}/validate_wp03_contract.py" "${WP03_DIR}" | tee wp03-contract-validation.log
grep -Fq "WP-03 CONTRACT VALIDATION: PASS" wp03-contract-validation.log
grep -Fq 'func _desktop_input() -> Vector2:' "${WP03_DIR}/ruin_scene_wp03.gd"
grep -Fq 'func _desktop_input() -> Vector2:' "${WP03_DIR}/traversal_annex_scene.gd"
grep -Fq 'menu_button.text = "Menu"' "${WP03_DIR}/traversal_annex_scene.gd"
grep -Fq 'Annex touch Menu button is missing.' "${WP03_DIR}/wp03_traversal_regression_test.gd"

printf '\n=== Reconstruct and verify approved WP-02R baseline ===\n'
APK_NAME="${BASELINE_APK_NAME}" source ci/godot-v0.02/wp02/run_wp02_ci.sh

test -n "${GODOT_BIN:-}"
test -d "${PROJECT_DIR}"
test -f "${PROJECT_DIR}/src/autoload/save_foundation.gd"
test -f "${PROJECT_DIR}/src/autoload/save_manager.gd"

printf '\n=== Apply WP-03 representative traversal vertical slice ===\n'
mkdir -p "${PROJECT_DIR}/src/core" "${PROJECT_DIR}/src/scenes" "${PROJECT_DIR}/tests"
cp "${WP03_DIR}/traversal_foundation.gd" "${PROJECT_DIR}/src/core/traversal_foundation.gd"
cp "${WP03_DIR}/ruin_scene_wp03.gd" "${PROJECT_DIR}/src/scenes/ruin_scene.gd"
cp "${WP03_DIR}/traversal_annex_scene.gd" "${PROJECT_DIR}/src/scenes/traversal_annex_scene.gd"
cp "${WP03_DIR}/traversal_annex_scene.tscn" "${PROJECT_DIR}/src/scenes/traversal_annex_scene.tscn"
cp "${WP03_DIR}/title_wp03.gd" "${PROJECT_DIR}/src/scenes/title.gd"
cp "${WP03_DIR}/wp03_traversal_regression_test.gd" "${PROJECT_DIR}/tests/wp03_traversal_regression_test.gd"
cp "${WP03_DIR}/wp03_traversal_regression_test.tscn" "${PROJECT_DIR}/tests/wp03_traversal_regression_test.tscn"
python "${WP03_DIR}/apply_wp03.py" "${PROJECT_DIR}"

grep -Fqx 'const BUILD_VERSION := "0.05.1-WP03R"' "${PROJECT_DIR}/src/autoload/build_identity.gd"
grep -Fqx 'version/name="0.05.1-WP03R"' "${PROJECT_DIR}/export_presets.cfg"
grep -Fq 'DiyseTraversalFoundation.camera_relative_direction' "${PROJECT_DIR}/src/scenes/ruin_scene.gd"
grep -Fq 'DiyseTraversalFoundation.wall_slide' "${PROJECT_DIR}/src/scenes/ruin_scene.gd"
grep -Fq 'GameState.world["camera_zone"]' "${PROJECT_DIR}/src/scenes/ruin_scene.gd"
grep -Fq 'MAP_VS_ANNEX' "${PROJECT_DIR}/src/scenes/title.gd"
test -f "${PROJECT_DIR}/src/scenes/traversal_annex_scene.tscn"

printf '\n=== Re-import and compile WP-03 project ===\n'
set +e
"${GODOT_BIN}" --headless --editor --path "${PROJECT_DIR}" --import --quit-after 90 --verbose 2>&1 | tee godot-wp03-import.log
WP03_IMPORT_STATUS=${PIPESTATUS[0]}
set -e
test "${WP03_IMPORT_STATUS}" -eq 0
if grep -E "SCRIPT ERROR|Parse Error|Compile Error|ERROR: Failed to load script" godot-wp03-import.log; then
  echo "WP-03R import produced a script load failure." >&2
  exit 1
fi

printf '\n=== Run WP-03 traversal runtime regression ===\n'
set +e
"${GODOT_BIN}" --headless --path "${PROJECT_DIR}" --quit-after 300 --verbose res://tests/wp03_traversal_regression_test.tscn 2>&1 | tee wp03-traversal-runtime.log
WP03_STATUS=${PIPESTATUS[0]}
set -e
test "${WP03_STATUS}" -eq 0
grep -Fq "PASS: WP-03 traversal movement, camera continuity, collision safety, occlusion, transition, and save restoration gates passed." wp03-traversal-runtime.log
if grep -E "SCRIPT ERROR|Parse Error|Compile Error|WP-03 TRAVERSAL TEST FAILED|Invalid call|Invalid assignment|Invalid access|The InputMap action|ERROR:" wp03-traversal-runtime.log; then
  echo "WP-03R traversal runtime produced an unexpected error." >&2
  exit 1
fi

printf '\n=== Re-run approved WP-02R device-path save regression ===\n'
set +e
"${GODOT_BIN}" --headless --path "${PROJECT_DIR}" --quit-after 240 --verbose res://tests/wp02_ui_save_integration_test.tscn 2>&1 | tee wp03-wp02r-save-regression.log
WP02R_SAVE_STATUS=${PIPESTATUS[0]}
set -e
test "${WP02R_SAVE_STATUS}" -eq 0
grep -Fq "PASS: WP-02 device-path SaveManager, Continue, backup recovery, and title integration are operational." wp03-wp02r-save-regression.log
if grep -E "SCRIPT ERROR|Parse Error|Compile Error|WP-02 UI SAVE INTEGRATION FAILED|Invalid call|Invalid assignment|Invalid access" wp03-wp02r-save-regression.log; then
  echo "WP-03R inherited save regression produced an unexpected script error." >&2
  exit 1
fi

printf '\n=== Re-run no-frame battle regression ===\n'
set +e
"${GODOT_BIN}" --headless --path "${PROJECT_DIR}" --quit-after 180 --verbose res://tests/battle_ui_v0025_test.tscn 2>&1 | tee wp03-battle-ui-regression.log
WP03_BATTLE_UI_STATUS=${PIPESTATUS[0]}
set -e
test "${WP03_BATTLE_UI_STATUS}" -eq 0
grep -Fq "PASS: compact fixed round controls instantiate without the custom outer battle frame." wp03-battle-ui-regression.log
if grep -E "SCRIPT ERROR|Parse Error|Compile Error|BATTLE UI TEST FAILED|Invalid call|Invalid assignment|Invalid access|ERROR:" wp03-battle-ui-regression.log; then
  echo "WP-03R battle UI regression produced an unexpected error." >&2
  exit 1
fi

printf '\n=== Configure WP-03 QA signing ===\n'
WP03_KEYSTORE="${RUNNER_TEMP}/diyse-v0.05.1-wp03r-qa.keystore"
keytool -genkeypair \
  -keystore "${WP03_KEYSTORE}" \
  -storepass diyse-v0051-wp03r-qa \
  -alias diyse-v0051-wp03r-qa \
  -keypass diyse-v0051-wp03r-qa \
  -keyalg RSA \
  -keysize 2048 \
  -validity 3650 \
  -dname "CN=The Role of the Diyse WP-03R QA,O=Diyse Prototype,C=US"
export GODOT_ANDROID_KEYSTORE_DEBUG_PATH="${WP03_KEYSTORE}"
export GODOT_ANDROID_KEYSTORE_DEBUG_USER="diyse-v0051-wp03r-qa"
export GODOT_ANDROID_KEYSTORE_DEBUG_PASSWORD="diyse-v0051-wp03r-qa"

printf '\n=== Export and verify WP-03 Android APK ===\n'
rm -rf android-artifact
mkdir -p android-artifact "${PROJECT_DIR}/build/android"
set +e
"${GODOT_BIN}" \
  --headless \
  --path "${PROJECT_DIR}" \
  --export-debug "Android QA" \
  "${GITHUB_WORKSPACE}/${PROJECT_DIR}/build/android/${WP03_APK_NAME}" \
  --verbose 2>&1 | tee godot-wp03-export.log
WP03_EXPORT_STATUS=${PIPESTATUS[0]}
set -e
test "${WP03_EXPORT_STATUS}" -eq 0
WP03_APK="${PROJECT_DIR}/build/android/${WP03_APK_NAME}"
test -s "${WP03_APK}"
unzip -t "${WP03_APK}"
unzip -l "${WP03_APK}" | grep -Fq "assets/authority/v1_12/bundle_manifest.json"
unzip -l "${WP03_APK}" | grep -Fq "assets/src/autoload/save_foundation.gdc"
unzip -l "${WP03_APK}" | grep -Fq "assets/src/autoload/save_manager.gdc"
unzip -l "${WP03_APK}" | grep -Fq "assets/src/core/traversal_foundation.gdc"
unzip -l "${WP03_APK}" | grep -Fq "assets/src/scenes/traversal_annex_scene.gdc"
unzip -l "${WP03_APK}" | grep -Fq "assets/src/scenes/ruin_scene.gdc"
if unzip -l "${WP03_APK}" | grep -Fq "diyse_battle_outer_frame"; then
  echo "Removed custom battle-frame asset is present in the WP-03R APK." >&2
  exit 1
fi
"${ANDROID_HOME}/build-tools/35.0.1/apksigner" verify --verbose --print-certs "${WP03_APK}" | tee wp03-apk-signature.txt
sha256sum "${WP03_APK}" | tee "${WP03_APK}.sha256"

cp \
  "${WP03_APK}" \
  "${WP03_APK}.sha256" \
  wp03-contract-validation.log \
  wp03-traversal-runtime.log \
  wp03-wp02r-save-regression.log \
  wp03-battle-ui-regression.log \
  godot-wp03-import.log \
  godot-wp03-export.log \
  wp03-apk-signature.txt \
  wp02-contract-validation.log \
  wp02-save-runtime.log \
  wp02-ui-save-runtime.log \
  authority-runtime.log \
  battle-polish-test.log \
  battle-ui-test.log \
  android-artifact/

printf '\nWP-03R TRAVERSAL CI BUILD: PASS\n'
