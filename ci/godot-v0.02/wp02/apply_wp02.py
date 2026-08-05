#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

VERSION = "0.04.1-WP02R"


def replace_once(text: str, pattern: str, replacement: str, label: str) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.MULTILINE)
    if count != 1:
        raise RuntimeError(f"Could not update {label}; expected exactly one match, got {count}.")
    return updated


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: apply_wp02.py <godot-project-dir>", file=sys.stderr)
        return 2

    project = Path(sys.argv[1]).resolve()
    project_file = project / "project.godot"
    build_identity = project / "src/autoload/build_identity.gd"
    export_presets = project / "export_presets.cfg"
    content_manifest = project / "data/content_manifest.json"
    source_dir = Path(__file__).resolve().parent
    save_manager = project / "src/autoload/save_manager.gd"
    save_foundation = project / "src/autoload/save_foundation.gd"
    battle_scene = project / "src/scenes/battle_scene.gd"
    tests_dir = project / "tests"

    for required in (project_file, build_identity, export_presets, save_manager, save_foundation, battle_scene):
        if not required.is_file():
            raise FileNotFoundError(required)

    adapter = source_dir / "save_manager_wp02_adapter.gd"
    ui_save_test = source_dir / "wp02_ui_save_integration_test.gd"
    ui_save_scene = source_dir / "wp02_ui_save_integration_test.tscn"
    no_frame_test = source_dir / "battle_ui_no_frame_test.gd"
    for required in (adapter, ui_save_test, ui_save_scene, no_frame_test):
        if not required.is_file():
            raise FileNotFoundError(required)

    foundation_text = save_foundation.read_text(encoding="utf-8")
    foundation_text = foundation_text.replace('const BUILD_VERSION := "0.04.0-WP02"', f'const BUILD_VERSION := "{VERSION}"')
    public_anchor = "func create_legacy_fixture_for_test(slot_id: String, payload: Dictionary, schema_version: int = 1) -> Dictionary:\n"
    public_methods = """func has_verified_save(slot_id: String) -> bool:
    var slot_check := _validate_slot_id(slot_id)
    if not bool(slot_check.get("ok", false)):
        return false
    return bool(_load_verified_envelope(slot_id, ["playable", "final_return"], false).get("ok", false))

func has_verified_backup(slot_id: String) -> bool:
    var slot_check := _validate_slot_id(slot_id)
    if not bool(slot_check.get("ok", false)):
        return false
    var paths := _slot_paths(slot_id)
    var backup := _read_and_validate_envelope(String(paths["backup"]), ["playable", "final_return"])
    if bool(backup.get("ok", false)):
        return true
    var previous := _read_and_validate_envelope(String(paths["previous"]), ["playable", "final_return"])
    return bool(previous.get("ok", false))

func load_backup_game(slot_id: String, alias_map: Dictionary = {}) -> Dictionary:
    var slot_check := _validate_slot_id(slot_id)
    if not bool(slot_check.get("ok", false)):
        return slot_check
    var paths := _slot_paths(slot_id)
    for source in ["backup", "previous"]:
        var loaded := _read_and_validate_envelope(String(paths[source]), ["playable", "final_return"])
        if not bool(loaded.get("ok", false)):
            continue
        var migration := migrate_payload(Dictionary(loaded.get("payload", {})), alias_map)
        loaded["payload"] = migration.get("payload", {})
        loaded["migration"] = migration.get("report", {})
        loaded["source"] = source
        return loaded
    return _error("SAVE_NO_VERIFIED_BACKUP", "No verified backup or previous save exists.")

func delete_slot(slot_id: String) -> Dictionary:
    var slot_check := _validate_slot_id(slot_id)
    if not bool(slot_check.get("ok", false)):
        return slot_check
    var paths := _slot_paths(slot_id)
    for path in paths.values():
        _remove_if_exists(String(path))
    return {"ok": true, "slot_id": slot_id}

"""
    if "func has_verified_save(slot_id: String) -> bool:" not in foundation_text:
        if public_anchor not in foundation_text:
            raise RuntimeError("Could not find SaveFoundation device-method insertion point.")
        foundation_text = foundation_text.replace(public_anchor, public_methods + public_anchor, 1)
    save_foundation.write_text(foundation_text, encoding="utf-8")

    save_manager.write_text(adapter.read_text(encoding="utf-8"), encoding="utf-8")
    tests_dir.mkdir(parents=True, exist_ok=True)
    (tests_dir / "wp02_ui_save_integration_test.gd").write_text(ui_save_test.read_text(encoding="utf-8"), encoding="utf-8")
    (tests_dir / "wp02_ui_save_integration_test.tscn").write_text(ui_save_scene.read_text(encoding="utf-8"), encoding="utf-8")
    (tests_dir / "battle_ui_v0025_test.gd").write_text(no_frame_test.read_text(encoding="utf-8"), encoding="utf-8")

    battle_text = battle_scene.read_text(encoding="utf-8")
    battle_text = battle_text.replace('const FRAME_TEXTURE := preload("res://assets/ui/diyse_battle_outer_frame.svg")\n\n', '', 1)
    battle_text = battle_text.replace('    _add_ornate_outer_frame()\n', '', 1)
    battle_text, removed = re.subn(
        r'func _add_ornate_outer_frame\(\) -> void:\n.*?(?=func _panel_style\()',
        '',
        battle_text,
        count=1,
        flags=re.DOTALL,
    )
    if removed != 1:
        raise RuntimeError(f"Could not remove custom battle frame helper; expected one match, got {removed}.")
    prohibited = ("FRAME_TEXTURE", "OrnateBattleFrame", "_add_ornate_outer_frame", "diyse_battle_outer_frame.svg")
    for token in prohibited:
        if token in battle_text:
            raise RuntimeError(f"Custom battle frame token remains after removal: {token}")
    battle_scene.write_text(battle_text, encoding="utf-8")
    frame_asset = project / "assets/ui/diyse_battle_outer_frame.svg"
    if frame_asset.exists():
        frame_asset.unlink()

    project_text = project_file.read_text(encoding="utf-8")
    autoload_line = 'SaveFoundation="*res://src/autoload/save_foundation.gd"'
    if autoload_line not in project_text:
        if "[autoload]" in project_text:
            project_text = project_text.replace("[autoload]\n", f"[autoload]\n{autoload_line}\n", 1)
        else:
            project_text += f"\n[autoload]\n{autoload_line}\n"
    project_file.write_text(project_text, encoding="utf-8")

    identity_text = build_identity.read_text(encoding="utf-8")
    identity_text = replace_once(
        identity_text,
        r'^const BUILD_VERSION := ".*"$',
        f'const BUILD_VERSION := "{VERSION}"',
        "build identity",
    )
    build_identity.write_text(identity_text, encoding="utf-8")

    preset_text = export_presets.read_text(encoding="utf-8")
    preset_text = replace_once(
        preset_text,
        r'^version/name=".*"$',
        f'version/name="{VERSION}"',
        "Android version name",
    )
    export_presets.write_text(preset_text, encoding="utf-8")

    if content_manifest.is_file():
        data = json.loads(content_manifest.read_text(encoding="utf-8"))
        data["build_version"] = VERSION
        data["implementation_work_package"] = "WP-02"
        data["save_foundation"] = "atomic-primary-backup-migration-rollback-final-return"
        data["save_ui_integration"] = "SaveManager adapter over SaveFoundation"
        data["battle_outer_frame"] = "removed"
        content_manifest.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    print(f"Applied WP-02R save/UI integration and removed the custom battle frame in {project}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
