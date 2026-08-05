extends Node

var manager
var _failures: Array[String] = []

func _ready() -> void:
    await get_tree().process_frame
    manager = get_node_or_null("/root/SaveFoundation")
    if manager == null:
        _fail("SaveFoundation autoload is missing.")
        return

    var root_result: Dictionary = manager.set_storage_root("user://wp02_regression")
    if not bool(root_result.get("ok", false)):
        _fail("Could not configure isolated regression storage.")
        return
    manager.clear_test_storage()

    _test_initial_save_and_load()
    _test_backup_and_corruption_recovery()
    _test_interrupted_write_is_ignored()
    _test_alias_migration_without_duplication()
    _test_alias_chain_and_array_deduplication()
    _test_transaction_rollback()
    _test_successful_transaction()
    _test_legacy_schema_migration()
    _test_completion_metadata_separation()
    _test_final_return_continue_behavior()
    _test_post_victory_rejection()
    _test_checksum_tamper_detection()
    _test_valid_primary_ignores_bad_backup()
    _test_both_invalid_fail_closed()

    if not _failures.is_empty():
        for failure in _failures:
            push_error("WP-02 SAVE TEST FAILED: %s" % failure)
        get_tree().quit(1)
        return

    print("PASS: WP-02 atomic save, migration, rollback, recovery, completion metadata, and Final Return Save gates passed.")
    get_tree().quit(0)

func _test_initial_save_and_load() -> void:
    var payload := {"chapter": 3, "inventory": {"ITEM_POTION": 4}, "flags": {"intro": true}}
    var save: Dictionary = manager.save_game("slot_a", payload)
    _expect(bool(save.get("ok", false)), "Initial save failed.")
    _expect(int(save.get("revision", 0)) == 1, "Initial revision was not 1.")
    var loaded: Dictionary = manager.load_game("slot_a")
    _expect(bool(loaded.get("ok", false)), "Initial load failed.")
    _expect(String(loaded.get("source", "")) == "primary", "Initial load did not use primary.")
    _expect(int(Dictionary(loaded.get("payload", {})).get("chapter", 0)) == 3, "Initial payload changed.")

func _test_backup_and_corruption_recovery() -> void:
    var second := {"chapter": 4, "inventory": {"ITEM_POTION": 6}, "flags": {"intro": true}}
    var save: Dictionary = manager.save_game("slot_a", second)
    _expect(bool(save.get("ok", false)), "Second save failed.")
    _expect(int(save.get("revision", 0)) == 2, "Second revision was not 2.")
    var paths: Dictionary = manager.inspect_slot("slot_a")
    _expect(bool(Dictionary(paths.get("backup", {})).get("exists", false)), "Verified backup was not created.")
    _overwrite(String(Dictionary(paths.get("primary", {})).get("path", "")), "{corrupt")
    var recovered: Dictionary = manager.load_game("slot_a")
    _expect(bool(recovered.get("ok", false)), "Backup recovery failed.")
    _expect(String(recovered.get("source", "")) == "backup", "Corruption did not recover from backup.")
    _expect(int(Dictionary(recovered.get("payload", {})).get("chapter", 0)) == 3, "Backup recovery did not restore prior verified state.")

func _test_interrupted_write_is_ignored() -> void:
    var before: Dictionary = manager.load_game("slot_a")
    var interruption: Dictionary = manager.simulate_interrupted_write_for_test("slot_a", {"chapter": 99})
    _expect(bool(interruption.get("ok", false)), "Could not create interrupted-write fixture.")
    var loaded := manager.load_game("slot_a")
    _expect(bool(loaded.get("ok", false)), "Load failed after interrupted write.")
    _expect(Dictionary(loaded.get("payload", {})) == Dictionary(before.get("payload", {})), "Interrupted pending data replaced verified primary.")
    var paths: Dictionary = manager.inspect_slot("slot_a")
    _expect(not bool(Dictionary(paths.get("pending", {})).get("exists", true)), "Stale pending file was not cleaned.")

func _test_alias_migration_without_duplication() -> void:
    var alias_map := {
        "OLD_CARD": "CARD_CANON",
        "OLD_ITEM": "ITEM_CANON",
    }
    var payload := {
        "cards": {"OLD_CARD": 1, "CARD_CANON": 1},
        "inventory": {"OLD_ITEM": 2, "ITEM_CANON": 5},
        "equipped": "OLD_CARD",
    }
    var result: Dictionary = manager.migrate_payload(payload, alias_map)
    var migrated: Dictionary = result.get("payload", {})
    _expect(not Dictionary(migrated.get("cards", {})).has("OLD_CARD"), "Old Card alias survived migration.")
    _expect(int(Dictionary(migrated.get("cards", {})).get("CARD_CANON", 0)) == 1, "Card alias migration duplicated progress.")
    _expect(int(Dictionary(migrated.get("inventory", {})).get("ITEM_CANON", 0)) == 5, "Item alias migration duplicated quantity.")
    _expect(String(migrated.get("equipped", "")) == "CARD_CANON", "String alias did not migrate.")

func _test_alias_chain_and_array_deduplication() -> void:
    var aliases := {"A": "B", "B": "C"}
    var result: Dictionary = manager.migrate_payload({"ids": ["A", "B", "C"]}, aliases)
    var ids: Array = Dictionary(result.get("payload", {})).get("ids", [])
    _expect(ids == ["C"], "Alias chain did not collapse and deduplicate.")
    _expect(int(Dictionary(result.get("report", {})).get("array_duplicates_removed", 0)) == 2, "Array deduplication was not reported.")

func _test_transaction_rollback() -> void:
    manager.save_game("tx", {"inventory": {"ITEM_A": 2}, "post_victory_world": false})
    var before_paths: Dictionary = manager.inspect_slot("tx")
    var before_hash := String(Dictionary(before_paths.get("primary", {})).get("sha256", ""))
    var result: Dictionary = manager.transact("tx", Callable(self, "_mutate_invalid_post_victory"))
    _expect(not bool(result.get("ok", true)), "Invalid transaction unexpectedly committed.")
    _expect(bool(result.get("rolled_back", false)), "Invalid transaction did not report rollback.")
    var after_paths: Dictionary = manager.inspect_slot("tx")
    var after_hash := String(Dictionary(after_paths.get("primary", {})).get("sha256", ""))
    _expect(before_hash == after_hash, "Failed transaction changed the verified primary.")

func _test_successful_transaction() -> void:
    var result: Dictionary = manager.transact("tx", Callable(self, "_mutate_add_item"))
    _expect(bool(result.get("ok", false)), "Valid transaction failed.")
    var loaded: Dictionary = manager.load_game("tx")
    _expect(int(Dictionary(Dictionary(loaded.get("payload", {})).get("inventory", {})).get("ITEM_A", 0)) == 3, "Valid transaction did not persist.")

func _test_legacy_schema_migration() -> void:
    var fixture: Dictionary = manager.create_legacy_fixture_for_test("legacy", {"inventory": {"OLD": 1}}, 1)
    _expect(bool(fixture.get("ok", false)), "Legacy fixture creation failed.")
    var migration: Dictionary = manager.migrate_slot("legacy", {"OLD": "NEW"})
    _expect(bool(migration.get("ok", false)), "Legacy schema migration failed.")
    _expect(int(migration.get("from_schema", 0)) == 1, "Legacy migration did not report source schema.")
    var loaded: Dictionary = manager.load_game("legacy")
    _expect(int(loaded.get("schema_version", 0)) == 2, "Legacy save was not rewritten to current schema.")
    _expect(Dictionary(Dictionary(loaded.get("payload", {})).get("inventory", {})).has("NEW"), "Legacy alias did not migrate.")

func _test_completion_metadata_separation() -> void:
    var completion := {
        "ending_complete": true,
        "final_policy": "shared_control",
        "difficulty": "normal",
        "playtime_seconds": 12345,
    }
    var write: Dictionary = manager.write_completion_metadata(completion)
    _expect(bool(write.get("ok", false)), "Completion metadata write failed.")
    var loaded: Dictionary = manager.load_completion_metadata()
    _expect(bool(loaded.get("ok", false)), "Completion metadata load failed.")
    _expect(String(loaded.get("kind", "")) == "completion", "Completion metadata has a playable save kind.")
    var invalid := completion.duplicate(true)
    invalid["location_id"] = "LOC_POST_GAME"
    _expect(not bool(manager.write_completion_metadata(invalid).get("ok", true)), "Completion metadata accepted playable world state.")

func _test_final_return_continue_behavior() -> void:
    var final_state := {
        "act": 5,
        "chapter": 21,
        "location_id": "LOC_CENTRAL_PRIME_SANCTUARY",
        "optional_content_open": true,
    }
    var write: Dictionary = manager.write_final_return_save(final_state)
    _expect(bool(write.get("ok", false)), "Final Return Save write failed.")
    var continued: Dictionary = manager.load_continue_state("slot_a")
    _expect(bool(continued.get("ok", false)), "Continue after completion failed.")
    _expect(String(continued.get("continue_source", "")) == "final_return", "Continue after completion did not load Final Return Save.")
    var payload: Dictionary = continued.get("payload", {})
    _expect(bool(payload.get("pre_act_vi", false)), "Final Return Save lost pre-Act-VI marker.")
    _expect(not bool(payload.get("post_victory_world", true)), "Continue loaded a post-victory state.")

func _test_post_victory_rejection() -> void:
    var rejected: Dictionary = manager.save_game("bad_world", {"post_victory_world": true})
    _expect(not bool(rejected.get("ok", true)), "Post-victory world save was accepted.")
    var cleared: Dictionary = manager.save_game("bad_clear", {"cleared_world": true})
    _expect(not bool(cleared.get("ok", true)), "Cleared-world save was accepted.")

func _test_checksum_tamper_detection() -> void:
    manager.save_game("tamper", {"chapter": 5})
    var paths: Dictionary = manager.inspect_slot("tamper")
    var primary := String(Dictionary(paths.get("primary", {})).get("path", ""))
    var text := FileAccess.get_file_as_string(primary)
    _overwrite(primary, text.replace('"chapter":5', '"chapter":6'))
    var loaded: Dictionary = manager.load_game("tamper")
    _expect(not bool(loaded.get("ok", true)), "Checksum-tampered save did not fail closed.")

func _test_valid_primary_ignores_bad_backup() -> void:
    manager.save_game("backup_noise", {"chapter": 1})
    manager.save_game("backup_noise", {"chapter": 2})
    var paths: Dictionary = manager.inspect_slot("backup_noise")
    _overwrite(String(Dictionary(paths.get("backup", {})).get("path", "")), "bad backup")
    var loaded: Dictionary = manager.load_game("backup_noise")
    _expect(bool(loaded.get("ok", false)), "Valid primary failed because backup was corrupt.")
    _expect(int(Dictionary(loaded.get("payload", {})).get("chapter", 0)) == 2, "Valid primary was not preferred.")

func _test_both_invalid_fail_closed() -> void:
    manager.save_game("both_bad", {"chapter": 1})
    manager.save_game("both_bad", {"chapter": 2})
    var paths: Dictionary = manager.inspect_slot("both_bad")
    _overwrite(String(Dictionary(paths.get("primary", {})).get("path", "")), "bad primary")
    _overwrite(String(Dictionary(paths.get("backup", {})).get("path", "")), "bad backup")
    var loaded: Dictionary = manager.load_game("both_bad")
    _expect(not bool(loaded.get("ok", true)), "Invalid primary and backup did not fail closed.")
    _expect(String(loaded.get("code", "")) == "SAVE_NO_VERIFIED_STATE", "Both-invalid failure returned the wrong deterministic code.")

func _mutate_invalid_post_victory(state: Dictionary) -> bool:
    state["post_victory_world"] = true
    return true

func _mutate_add_item(state: Dictionary) -> bool:
    var inventory: Dictionary = state.get("inventory", {})
    inventory["ITEM_A"] = int(inventory.get("ITEM_A", 0)) + 1
    state["inventory"] = inventory
    return true

func _overwrite(path: String, text: String) -> void:
    var file := FileAccess.open(path, FileAccess.WRITE)
    if file == null:
        _failures.append("Could not overwrite fixture path: %s" % path)
        return
    file.store_string(text)
    file.flush()
    file.close()

func _expect(condition: bool, message: String) -> void:
    if not condition:
        _failures.append(message)

func _fail(message: String) -> void:
    push_error("WP-02 SAVE TEST FAILED: %s" % message)
    get_tree().quit(1)
