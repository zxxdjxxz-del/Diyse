extends Node

func _ready() -> void:
    await get_tree().process_frame
    var manager = get_node_or_null("/root/AuthorityManager")
    if manager == null:
        _fail("AuthorityManager autoload is missing.")
        return
    if not manager.is_loaded:
        _fail("AuthorityManager did not load the authority bundle.")
        return

    var summary: Dictionary = manager.get_summary()
    if int(summary.get("registry_count", 0)) != 75:
        _fail("Expected 75 authority registries.")
        return
    if int(summary.get("record_total", 0)) != 7800:
        _fail("Expected 7,800 authority records.")
        return
    if int(summary.get("canonical_id_count", 0)) != 2098:
        _fail("Expected 2,098 canonical IDs.")
        return
    if manager.resolve_id("CARD_PRIME_CATACLYSM_LAST_WEAPON") != "CARD_PRIME_CATACLYSM_FIRST_RECKONING":
        _fail("Last Weapon alias migration failed.")
        return
    if manager.resolve_id("CARD_PRIME_CATACLYSM_STAR_OF_THE_CROWN") != "CARD_PRIME_CATACLYSM_FIRST_RECKONING":
        _fail("Star of the Crown alias migration failed.")
        return
    if manager.has_canonical_id("CARD_PRIME_CATACLYSM_LAST_WEAPON"):
        _fail("Last Weapon alias incorrectly exists as a canonical ID.")
        return
    if bool(summary.get("post_game_playable", true)):
        _fail("Playable post-game was incorrectly enabled.")
        return

    print("PASS: WP-01R authority bundle loaded, verified, and enforced in Godot.")
    get_tree().quit(0)

func _fail(message: String) -> void:
    push_error("WP-01R AUTHORITY TEST FAILED: %s" % message)
    get_tree().quit(1)
