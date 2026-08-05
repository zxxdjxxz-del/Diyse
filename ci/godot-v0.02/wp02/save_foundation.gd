extends Node

signal save_committed(slot_id: String, revision: int)
signal save_recovered(slot_id: String, source: String)
signal save_failed(slot_id: String, code: String)

const SAVE_FORMAT := "diyse.save.envelope"
const CURRENT_SCHEMA_VERSION := 2
const BUILD_VERSION := "0.04.0-WP02"
const DEFAULT_STORAGE_ROOT := "user://diyse_saves"
const FINAL_RETURN_SLOT := "final_return"
const COMPLETION_RECORD := "completion_record"

var storage_root := DEFAULT_STORAGE_ROOT

func _ready() -> void:
    _ensure_storage_root()

func set_storage_root(root_path: String) -> Dictionary:
    if root_path.is_empty():
        return _error("SAVE_ROOT_EMPTY", "Storage root cannot be empty.")
    storage_root = root_path.trim_suffix("/")
    if not _ensure_storage_root():
        return _error("SAVE_ROOT_CREATE_FAILED", "Could not create the save storage root.")
    return {"ok": true, "root": storage_root}

func save_game(slot_id: String, payload: Dictionary, kind: String = "playable") -> Dictionary:
    var slot_check := _validate_slot_id(slot_id)
    if not bool(slot_check.get("ok", false)):
        return slot_check
    var payload_check := _validate_playable_payload(payload, kind)
    if not bool(payload_check.get("ok", false)):
        save_failed.emit(slot_id, String(payload_check.get("code", "SAVE_PAYLOAD_INVALID")))
        return payload_check

    var existing := _load_verified_envelope(slot_id, ["playable", "final_return"], false)
    var revision := 1
    if bool(existing.get("ok", false)):
        revision = int(existing.get("revision", 0)) + 1

    var envelope := _make_envelope(payload, kind, revision, CURRENT_SCHEMA_VERSION)
    var result := _commit_envelope(slot_id, envelope)
    if bool(result.get("ok", false)):
        save_committed.emit(slot_id, revision)
    else:
        save_failed.emit(slot_id, String(result.get("code", "SAVE_COMMIT_FAILED")))
    return result

func load_game(slot_id: String, alias_map: Dictionary = {}) -> Dictionary:
    var slot_check := _validate_slot_id(slot_id)
    if not bool(slot_check.get("ok", false)):
        return slot_check
    var loaded := _load_verified_envelope(slot_id, ["playable", "final_return"], true)
    if not bool(loaded.get("ok", false)):
        return loaded
    var migration := migrate_payload(Dictionary(loaded.get("payload", {})), alias_map)
    loaded["payload"] = migration.get("payload", {})
    loaded["migration"] = migration.get("report", {})
    return loaded

func transact(slot_id: String, mutation: Callable, alias_map: Dictionary = {}) -> Dictionary:
    if not mutation.is_valid():
        return _error("TRANSACTION_CALLABLE_INVALID", "Transaction mutation is not callable.")
    var loaded := load_game(slot_id, alias_map)
    if not bool(loaded.get("ok", false)):
        return loaded

    var before: Dictionary = Dictionary(loaded.get("payload", {})).duplicate(true)
    var working: Dictionary = before.duplicate(true)
    var mutation_result = mutation.call(working)
    if mutation_result is bool and not bool(mutation_result):
        return _error("TRANSACTION_REJECTED", "Transaction mutation rejected the operation.")
    if mutation_result is Dictionary and not bool(mutation_result.get("ok", false)):
        return mutation_result

    var migrated := migrate_payload(working, alias_map)
    var commit := save_game(slot_id, Dictionary(migrated.get("payload", {})), String(loaded.get("kind", "playable")))
    if not bool(commit.get("ok", false)):
        commit["rolled_back"] = true
        commit["prior_payload"] = before
        return commit
    commit["migration"] = migrated.get("report", {})
    return commit

func migrate_slot(slot_id: String, alias_map: Dictionary = {}) -> Dictionary:
    var loaded := _load_verified_envelope(slot_id, ["playable", "final_return"], true)
    if not bool(loaded.get("ok", false)):
        return loaded
    var migrated := migrate_payload(Dictionary(loaded.get("payload", {})), alias_map)
    var commit := save_game(slot_id, Dictionary(migrated.get("payload", {})), String(loaded.get("kind", "playable")))
    if bool(commit.get("ok", false)):
        commit["migration"] = migrated.get("report", {})
        commit["from_schema"] = int(loaded.get("schema_version", CURRENT_SCHEMA_VERSION))
        commit["to_schema"] = CURRENT_SCHEMA_VERSION
    return commit

func migrate_payload(payload: Dictionary, alias_map: Dictionary = {}) -> Dictionary:
    var report := {
        "aliases_resolved": 0,
        "collisions_merged": 0,
        "array_duplicates_removed": 0,
    }
    var migrated = _migrate_value(payload.duplicate(true), alias_map, report)
    return {"ok": true, "payload": migrated, "report": report}

func write_final_return_save(payload: Dictionary) -> Dictionary:
    var final_payload := payload.duplicate(true)
    final_payload["pre_act_vi"] = true
    final_payload["post_victory_world"] = false
    return save_game(FINAL_RETURN_SLOT, final_payload, "final_return")

func write_completion_metadata(metadata: Dictionary) -> Dictionary:
    var metadata_check := _validate_completion_metadata(metadata)
    if not bool(metadata_check.get("ok", false)):
        return metadata_check
    var existing := _load_verified_envelope(COMPLETION_RECORD, ["completion"], false)
    var revision := 1
    if bool(existing.get("ok", false)):
        revision = int(existing.get("revision", 0)) + 1
    var envelope := _make_envelope(metadata, "completion", revision, CURRENT_SCHEMA_VERSION)
    return _commit_envelope(COMPLETION_RECORD, envelope)

func load_completion_metadata() -> Dictionary:
    return _load_verified_envelope(COMPLETION_RECORD, ["completion"], true)

func load_continue_state(default_slot: String = "autosave", alias_map: Dictionary = {}) -> Dictionary:
    var completion := load_completion_metadata()
    if bool(completion.get("ok", false)):
        var final_return := load_game(FINAL_RETURN_SLOT, alias_map)
        if not bool(final_return.get("ok", false)):
            return _error("FINAL_RETURN_REQUIRED", "Completion exists but the pre-Act-VI Final Return Save is unavailable.")
        if String(final_return.get("kind", "")) != "final_return":
            return _error("FINAL_RETURN_KIND_INVALID", "Continue after completion must load a Final Return Save.")
        var payload: Dictionary = final_return.get("payload", {})
        if not bool(payload.get("pre_act_vi", false)) or bool(payload.get("post_victory_world", true)):
            return _error("FINAL_RETURN_STATE_INVALID", "Final Return Save is not a valid pre-Act-VI state.")
        final_return["continue_source"] = "final_return"
        return final_return

    var ordinary := load_game(default_slot, alias_map)
    if bool(ordinary.get("ok", false)):
        ordinary["continue_source"] = default_slot
    return ordinary

func inspect_slot(slot_id: String) -> Dictionary:
    var paths := _slot_paths(slot_id)
    var result := {"slot_id": slot_id}
    for key in paths.keys():
        var path := String(paths[key])
        result[key] = {
            "exists": FileAccess.file_exists(path),
            "path": path,
            "sha256": _sha256_file(path) if FileAccess.file_exists(path) else "",
        }
    return result

func create_legacy_fixture_for_test(slot_id: String, payload: Dictionary, schema_version: int = 1) -> Dictionary:
    var envelope := _make_envelope(payload, "playable", 1, schema_version)
    return _commit_envelope(slot_id, envelope)

func simulate_interrupted_write_for_test(slot_id: String, payload: Dictionary) -> Dictionary:
    var paths := _slot_paths(slot_id)
    var envelope := _make_envelope(payload, "playable", 999, CURRENT_SCHEMA_VERSION)
    var write_result := _write_envelope(String(paths["pending"]), envelope)
    if not bool(write_result.get("ok", false)):
        return write_result
    var journal := {
        "format": "diyse.save.journal",
        "slot_id": slot_id,
        "stage": "prepared",
        "pending_sha256": _sha256_file(String(paths["pending"])),
    }
    return _write_json(String(paths["journal"]), journal)

func clear_test_storage() -> void:
    var absolute_root := ProjectSettings.globalize_path(storage_root)
    if DirAccess.dir_exists_absolute(absolute_root):
        _remove_directory_contents(absolute_root)
    _ensure_storage_root()

func _commit_envelope(slot_id: String, envelope: Dictionary) -> Dictionary:
    if not _ensure_storage_root():
        return _error("SAVE_ROOT_CREATE_FAILED", "Could not create the save storage root.")
    var paths := _slot_paths(slot_id)
    _remove_if_exists(String(paths["pending"]))
    _remove_if_exists(String(paths["backup_pending"]))

    var pending_write := _write_envelope(String(paths["pending"]), envelope)
    if not bool(pending_write.get("ok", false)):
        return pending_write

    var pending_check := _read_and_validate_envelope(String(paths["pending"]), [String(envelope.get("kind", ""))])
    if not bool(pending_check.get("ok", false)):
        _remove_if_exists(String(paths["pending"]))
        return _error("SAVE_PENDING_INVALID", "Pending save failed validation.")

    var journal := {
        "format": "diyse.save.journal",
        "slot_id": slot_id,
        "stage": "prepared",
        "pending_sha256": _sha256_file(String(paths["pending"])),
        "target_revision": int(envelope.get("revision", 0)),
    }
    var journal_write := _write_json(String(paths["journal"]), journal)
    if not bool(journal_write.get("ok", false)):
        _remove_if_exists(String(paths["pending"]))
        return journal_write

    if FileAccess.file_exists(String(paths["primary"])):
        var primary_check := _read_and_validate_envelope(String(paths["primary"]), ["playable", "final_return", "completion"])
        if bool(primary_check.get("ok", false)):
            var backup_copy := _copy_text_file(String(paths["primary"]), String(paths["backup_pending"]))
            if not bool(backup_copy.get("ok", false)):
                return backup_copy
            var backup_check := _read_and_validate_envelope(String(paths["backup_pending"]), [String(primary_check.get("kind", ""))])
            if not bool(backup_check.get("ok", false)):
                return _error("SAVE_BACKUP_PENDING_INVALID", "Backup candidate failed validation.")
            _remove_if_exists(String(paths["backup"]))
            var backup_rename := DirAccess.rename_absolute(
                ProjectSettings.globalize_path(String(paths["backup_pending"])),
                ProjectSettings.globalize_path(String(paths["backup"]))
            )
            if backup_rename != OK:
                return _error("SAVE_BACKUP_RENAME_FAILED", "Could not install the verified backup.")

        _remove_if_exists(String(paths["previous"]))
        var move_primary := DirAccess.rename_absolute(
            ProjectSettings.globalize_path(String(paths["primary"])),
            ProjectSettings.globalize_path(String(paths["previous"]))
        )
        if move_primary != OK:
            return _error("SAVE_PRIMARY_STAGE_FAILED", "Could not stage the current primary save.")

    journal["stage"] = "primary_staged"
    _write_json(String(paths["journal"]), journal)

    var install_pending := DirAccess.rename_absolute(
        ProjectSettings.globalize_path(String(paths["pending"])),
        ProjectSettings.globalize_path(String(paths["primary"]))
    )
    if install_pending != OK:
        _restore_previous(paths)
        return _error("SAVE_PRIMARY_INSTALL_FAILED", "Could not install the pending save.")

    var installed := _read_and_validate_envelope(String(paths["primary"]), [String(envelope.get("kind", ""))])
    if not bool(installed.get("ok", false)):
        _remove_if_exists(String(paths["primary"]))
        _restore_previous(paths)
        return _error("SAVE_PRIMARY_VERIFY_FAILED", "Installed primary save failed validation and was rolled back.")

    _remove_if_exists(String(paths["previous"]))
    _remove_if_exists(String(paths["journal"]))
    _remove_if_exists(String(paths["backup_pending"]))
    return {
        "ok": true,
        "slot_id": slot_id,
        "kind": String(envelope.get("kind", "")),
        "revision": int(envelope.get("revision", 0)),
        "sha256": _sha256_file(String(paths["primary"])),
    }

func _load_verified_envelope(slot_id: String, allowed_kinds: Array, recover: bool) -> Dictionary:
    var paths := _slot_paths(slot_id)
    var primary := _read_and_validate_envelope(String(paths["primary"]), allowed_kinds)
    if bool(primary.get("ok", false)):
        if recover:
            _remove_if_exists(String(paths["pending"]))
            _remove_if_exists(String(paths["previous"]))
            _remove_if_exists(String(paths["journal"]))
        primary["source"] = "primary"
        return primary

    var previous := _read_and_validate_envelope(String(paths["previous"]), allowed_kinds)
    if bool(previous.get("ok", false)):
        if recover:
            _remove_if_exists(String(paths["primary"]))
            var restore_previous := DirAccess.rename_absolute(
                ProjectSettings.globalize_path(String(paths["previous"])),
                ProjectSettings.globalize_path(String(paths["primary"]))
            )
            if restore_previous != OK:
                return _error("SAVE_PREVIOUS_RECOVERY_FAILED", "Verified previous save could not be restored.")
            _remove_if_exists(String(paths["pending"]))
            _remove_if_exists(String(paths["journal"]))
            save_recovered.emit(slot_id, "previous")
        previous["source"] = "previous"
        previous["recovered"] = recover
        return previous

    var backup := _read_and_validate_envelope(String(paths["backup"]), allowed_kinds)
    if bool(backup.get("ok", false)):
        if recover:
            var recovery_copy := _copy_text_file(String(paths["backup"]), String(paths["pending"]))
            if not bool(recovery_copy.get("ok", false)):
                return recovery_copy
            _remove_if_exists(String(paths["primary"]))
            var install_recovery := DirAccess.rename_absolute(
                ProjectSettings.globalize_path(String(paths["pending"])),
                ProjectSettings.globalize_path(String(paths["primary"]))
            )
            if install_recovery != OK:
                return _error("SAVE_BACKUP_RECOVERY_FAILED", "Verified backup could not be restored.")
            _remove_if_exists(String(paths["previous"]))
            _remove_if_exists(String(paths["journal"]))
            save_recovered.emit(slot_id, "backup")
        backup["source"] = "backup"
        backup["recovered"] = recover
        return backup

    return _error("SAVE_NO_VERIFIED_STATE", "No verified primary, previous, or backup save exists.")

func _make_envelope(payload: Dictionary, kind: String, revision: int, schema_version: int) -> Dictionary:
    var envelope := {
        "format": SAVE_FORMAT,
        "schema_version": schema_version,
        "build_version": BUILD_VERSION,
        "kind": kind,
        "revision": revision,
        "written_unix": int(Time.get_unix_time_from_system()),
        "payload": payload.duplicate(true),
        "payload_sha256": _sha256_variant(payload),
    }
    envelope["envelope_sha256"] = _hash_envelope(envelope)
    return envelope

func _write_envelope(path: String, envelope: Dictionary) -> Dictionary:
    return _write_json(path, envelope)

func _read_and_validate_envelope(path: String, allowed_kinds: Array) -> Dictionary:
    if not FileAccess.file_exists(path):
        return _error("SAVE_FILE_MISSING", "Save file does not exist.")
    var text := FileAccess.get_file_as_string(path)
    if text.is_empty():
        return _error("SAVE_FILE_EMPTY", "Save file is empty.")
    var parsed = JSON.parse_string(text)
    if not (parsed is Dictionary):
        return _error("SAVE_JSON_INVALID", "Save file is not valid JSON.")
    var envelope: Dictionary = parsed
    if String(envelope.get("format", "")) != SAVE_FORMAT:
        return _error("SAVE_FORMAT_INVALID", "Save format is invalid.")
    var schema_version := int(envelope.get("schema_version", 0))
    if schema_version < 1 or schema_version > CURRENT_SCHEMA_VERSION:
        return _error("SAVE_SCHEMA_UNSUPPORTED", "Save schema is unsupported.")
    var kind := String(envelope.get("kind", ""))
    if not allowed_kinds.has(kind):
        return _error("SAVE_KIND_INVALID", "Save kind is not allowed in this context.")
    if int(envelope.get("revision", 0)) < 1:
        return _error("SAVE_REVISION_INVALID", "Save revision is invalid.")
    var payload = envelope.get("payload", null)
    if not (payload is Dictionary):
        return _error("SAVE_PAYLOAD_INVALID", "Save payload is invalid.")
    if String(envelope.get("payload_sha256", "")) != _sha256_variant(payload):
        return _error("SAVE_PAYLOAD_HASH_MISMATCH", "Save payload checksum mismatch.")
    if String(envelope.get("envelope_sha256", "")) != _hash_envelope(envelope):
        return _error("SAVE_ENVELOPE_HASH_MISMATCH", "Save envelope checksum mismatch.")
    if kind == "completion":
        var completion_check := _validate_completion_metadata(payload)
        if not bool(completion_check.get("ok", false)):
            return completion_check
    else:
        var payload_check := _validate_playable_payload(payload, kind)
        if not bool(payload_check.get("ok", false)):
            return payload_check
    return {
        "ok": true,
        "kind": kind,
        "revision": int(envelope.get("revision", 0)),
        "schema_version": schema_version,
        "build_version": String(envelope.get("build_version", "")),
        "payload": Dictionary(payload).duplicate(true),
        "sha256": _sha256_file(path),
    }

func _validate_playable_payload(payload: Dictionary, kind: String) -> Dictionary:
    if kind != "playable" and kind != "final_return":
        return _error("SAVE_PLAYABLE_KIND_INVALID", "Playable save kind is invalid.")
    if bool(payload.get("post_victory_world", false)):
        return _error("SAVE_POST_VICTORY_PROHIBITED", "A post-victory world state cannot be saved or loaded.")
    if bool(payload.get("cleared_world", false)):
        return _error("SAVE_CLEARED_WORLD_PROHIBITED", "A cleared-world save cannot be created.")
    if String(payload.get("world_state", "")) == "post_victory":
        return _error("SAVE_POST_VICTORY_PROHIBITED", "A post-victory world state cannot be saved or loaded.")
    if bool(payload.get("completion_record", false)):
        return _error("SAVE_COMPLETION_NOT_PLAYABLE", "Completion metadata cannot be loaded as a playable state.")
    if kind == "final_return":
        if not bool(payload.get("pre_act_vi", false)):
            return _error("SAVE_FINAL_RETURN_NOT_PRE_ACT_VI", "Final Return Save must be a pre-Act-VI state.")
        if int(payload.get("act", 0)) >= 6:
            return _error("SAVE_FINAL_RETURN_ACT_INVALID", "Final Return Save cannot begin in Act VI.")
    return {"ok": true}

func _validate_completion_metadata(metadata: Dictionary) -> Dictionary:
    var prohibited := ["world_state", "location_id", "position", "party_state", "battle_state", "inventory"]
    for key in prohibited:
        if metadata.has(key):
            return _error("COMPLETION_METADATA_CONTAINS_WORLD", "Completion metadata cannot contain playable world state.")
    return {"ok": true}

func _migrate_value(value, alias_map: Dictionary, report: Dictionary):
    if value is Dictionary:
        var output := {}
        for raw_key in value.keys():
            var migrated_key = raw_key
            if raw_key is String:
                migrated_key = _resolve_alias(String(raw_key), alias_map, report)
            var migrated_value = _migrate_value(value[raw_key], alias_map, report)
            if output.has(migrated_key):
                output[migrated_key] = _merge_collision(output[migrated_key], migrated_value, report)
            else:
                output[migrated_key] = migrated_value
        return output
    if value is Array:
        var output_array := []
        var seen := {}
        for item in value:
            var migrated_item = _migrate_value(item, alias_map, report)
            var identity := JSON.stringify(migrated_item, "", true)
            if seen.has(identity):
                report["array_duplicates_removed"] = int(report.get("array_duplicates_removed", 0)) + 1
                continue
            seen[identity] = true
            output_array.append(migrated_item)
        return output_array
    if value is String:
        return _resolve_alias(String(value), alias_map, report)
    return value

func _resolve_alias(candidate: String, alias_map: Dictionary, report: Dictionary) -> String:
    var current := candidate
    var visited := {}
    for _step in range(64):
        if visited.has(current):
            return current
        visited[current] = true
        var next := current
        if alias_map.has(current):
            next = String(alias_map[current])
        else:
            var authority = get_node_or_null("/root/AuthorityManager")
            if authority != null and authority.has_method("resolve_id"):
                next = String(authority.resolve_id(current))
        if next == current:
            return current
        report["aliases_resolved"] = int(report.get("aliases_resolved", 0)) + 1
        current = next
    return current

func _merge_collision(left, right, report: Dictionary):
    report["collisions_merged"] = int(report.get("collisions_merged", 0)) + 1
    if left is Dictionary and right is Dictionary:
        var merged: Dictionary = left.duplicate(true)
        for key in right.keys():
            if merged.has(key):
                merged[key] = _merge_collision(merged[key], right[key], report)
            else:
                merged[key] = right[key]
        return merged
    if left is Array and right is Array:
        var combined: Array = left.duplicate(true)
        var seen := {}
        for item in combined:
            seen[JSON.stringify(item, "", true)] = true
        for item in right:
            var identity := JSON.stringify(item, "", true)
            if not seen.has(identity):
                seen[identity] = true
                combined.append(item)
            else:
                report["array_duplicates_removed"] = int(report.get("array_duplicates_removed", 0)) + 1
        return combined
    if (left is int or left is float) and (right is int or right is float):
        return max(left, right)
    if left is bool and right is bool:
        return bool(left) or bool(right)
    if left == right:
        return left
    return left

func _hash_envelope(envelope: Dictionary) -> String:
    var body := envelope.duplicate(true)
    body.erase("envelope_sha256")
    return _sha256_variant(body)

func _sha256_variant(value) -> String:
    return _sha256_text(JSON.stringify(value, "", true))

func _sha256_text(text: String) -> String:
    var context := HashingContext.new()
    if context.start(HashingContext.HASH_SHA256) != OK:
        return ""
    context.update(text.to_utf8_buffer())
    return context.finish().hex_encode()

func _sha256_file(path: String) -> String:
    if not FileAccess.file_exists(path):
        return ""
    var file := FileAccess.open(path, FileAccess.READ)
    if file == null:
        return ""
    var context := HashingContext.new()
    if context.start(HashingContext.HASH_SHA256) != OK:
        file.close()
        return ""
    while file.get_position() < file.get_length():
        var remaining := file.get_length() - file.get_position()
        context.update(file.get_buffer(int(min(remaining, 65536))))
    file.close()
    return context.finish().hex_encode()

func _write_json(path: String, value) -> Dictionary:
    var file := FileAccess.open(path, FileAccess.WRITE)
    if file == null:
        return _error("SAVE_WRITE_OPEN_FAILED", "Could not open save file for writing.")
    file.store_string(JSON.stringify(value, "", true))
    file.flush()
    file.close()
    if not FileAccess.file_exists(path):
        return _error("SAVE_WRITE_MISSING", "Written save file is missing.")
    return {"ok": true, "path": path, "sha256": _sha256_file(path)}

func _copy_text_file(source: String, destination: String) -> Dictionary:
    if not FileAccess.file_exists(source):
        return _error("SAVE_COPY_SOURCE_MISSING", "Save copy source is missing.")
    var text := FileAccess.get_file_as_string(source)
    var file := FileAccess.open(destination, FileAccess.WRITE)
    if file == null:
        return _error("SAVE_COPY_OPEN_FAILED", "Could not open save copy destination.")
    file.store_string(text)
    file.flush()
    file.close()
    if _sha256_file(source) != _sha256_file(destination):
        _remove_if_exists(destination)
        return _error("SAVE_COPY_HASH_MISMATCH", "Save copy checksum mismatch.")
    return {"ok": true, "path": destination}

func _restore_previous(paths: Dictionary) -> void:
    if FileAccess.file_exists(String(paths["previous"])):
        _remove_if_exists(String(paths["primary"]))
        DirAccess.rename_absolute(
            ProjectSettings.globalize_path(String(paths["previous"])),
            ProjectSettings.globalize_path(String(paths["primary"]))
        )
    _remove_if_exists(String(paths["pending"]))
    _remove_if_exists(String(paths["journal"]))

func _slot_paths(slot_id: String) -> Dictionary:
    var base := storage_root.path_join(slot_id)
    return {
        "primary": base + ".json",
        "backup": base + ".backup.json",
        "pending": base + ".pending.json",
        "backup_pending": base + ".backup.pending.json",
        "previous": base + ".previous.json",
        "journal": base + ".journal.json",
    }

func _validate_slot_id(slot_id: String) -> Dictionary:
    if slot_id.is_empty() or slot_id.contains("/") or slot_id.contains("\\") or slot_id.contains(".."):
        return _error("SAVE_SLOT_INVALID", "Save slot ID is invalid.")
    return {"ok": true}

func _ensure_storage_root() -> bool:
    var absolute_root := ProjectSettings.globalize_path(storage_root)
    if DirAccess.dir_exists_absolute(absolute_root):
        return true
    return DirAccess.make_dir_recursive_absolute(absolute_root) == OK

func _remove_if_exists(path: String) -> void:
    if FileAccess.file_exists(path):
        DirAccess.remove_absolute(ProjectSettings.globalize_path(path))

func _remove_directory_contents(absolute_root: String) -> void:
    var directory := DirAccess.open(absolute_root)
    if directory == null:
        return
    directory.list_dir_begin()
    var entry := directory.get_next()
    while not entry.is_empty():
        if entry != "." and entry != "..":
            var child := absolute_root.path_join(entry)
            if directory.current_is_dir():
                _remove_directory_contents(child)
                DirAccess.remove_absolute(child)
            else:
                DirAccess.remove_absolute(child)
        entry = directory.get_next()
    directory.list_dir_end()

func _error(code: String, message: String) -> Dictionary:
    return {"ok": false, "code": code, "message": message}
