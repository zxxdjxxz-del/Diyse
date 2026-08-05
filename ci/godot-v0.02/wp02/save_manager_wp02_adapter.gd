extends Node

const SLOT_ID := "autosave"
const LEGACY_SAVE_PATH := "user://diyse_save_01.json"
const LEGACY_TEMP_PATH := "user://diyse_save_01.tmp"
const LEGACY_BACKUP_PATH := "user://diyse_save_01.backup.json"

func _ready() -> void:
    _migrate_legacy_save_if_needed()

func has_save() -> bool:
    _migrate_legacy_save_if_needed()
    return SaveFoundation.has_verified_save(SLOT_ID)

func has_backup() -> bool:
    _migrate_legacy_save_if_needed()
    return SaveFoundation.has_verified_backup(SLOT_ID)

func save_game(reason: String = "manual", preserve_backup: bool = false) -> bool:
    var payload := GameState.to_save_data()
    payload["saved_at"] = Time.get_datetime_string_from_system()
    payload["reason"] = reason
    payload["post_victory_world"] = false
    payload["cleared_world"] = false
    var result: Dictionary = SaveFoundation.save_game(SLOT_ID, payload, "playable")
    if bool(result.get("ok", false)):
        Diagnostics.record("save", "WP-02 save committed", {
            "reason": reason,
            "revision": int(result.get("revision", 0)),
            "preserve_backup_requested": preserve_backup,
        })
        _remove_legacy_files()
        return true
    Diagnostics.record("save", "WP-02 save failed", {
        "reason": reason,
        "code": String(result.get("code", "SAVE_UNKNOWN")),
        "message": String(result.get("message", "")),
    })
    return false

func load_game(use_backup: bool = false) -> bool:
    _migrate_legacy_save_if_needed()
    var result: Dictionary
    if use_backup:
        result = SaveFoundation.load_backup_game(SLOT_ID)
    else:
        result = SaveFoundation.load_game(SLOT_ID)
    if not bool(result.get("ok", false)):
        Diagnostics.record("save", "WP-02 load failed", {
            "backup_requested": use_backup,
            "code": String(result.get("code", "SAVE_UNKNOWN")),
            "message": String(result.get("message", "")),
        })
        return false
    var payload: Dictionary = result.get("payload", {})
    if not GameState.load_save_data(payload):
        Diagnostics.record("save", "WP-02 payload rejected by GameState", {
            "backup_requested": use_backup,
            "source": String(result.get("source", "")),
        })
        return false
    Diagnostics.record("save", "WP-02 save loaded", {
        "backup_requested": use_backup,
        "source": String(result.get("source", "primary")),
        "revision": int(result.get("revision", 0)),
    })
    return true

func delete_save() -> void:
    SaveFoundation.delete_slot(SLOT_ID)
    _remove_legacy_files()

func _migrate_legacy_save_if_needed() -> void:
    if SaveFoundation.has_verified_save(SLOT_ID):
        return
    var candidates := [LEGACY_SAVE_PATH, LEGACY_BACKUP_PATH]
    for path in candidates:
        if not FileAccess.file_exists(path):
            continue
        var parsed = JSON.parse_string(FileAccess.get_file_as_string(path))
        if not (parsed is Dictionary):
            continue
        var payload = Dictionary(parsed).get("payload", null)
        if not (payload is Dictionary):
            continue
        var migrated_payload: Dictionary = Dictionary(payload).duplicate(true)
        migrated_payload["post_victory_world"] = false
        migrated_payload["cleared_world"] = false
        migrated_payload["legacy_imported"] = true
        var result: Dictionary = SaveFoundation.save_game(SLOT_ID, migrated_payload, "playable")
        if bool(result.get("ok", false)):
            Diagnostics.record("save", "legacy prototype save imported into WP-02", {"source": path})
            _remove_legacy_files()
            return
        Diagnostics.record("save", "legacy prototype save import failed", {
            "source": path,
            "code": String(result.get("code", "SAVE_UNKNOWN")),
        })

func _remove_legacy_files() -> void:
    for path in [LEGACY_SAVE_PATH, LEGACY_TEMP_PATH, LEGACY_BACKUP_PATH]:
        if FileAccess.file_exists(path):
            DirAccess.remove_absolute(ProjectSettings.globalize_path(path))
