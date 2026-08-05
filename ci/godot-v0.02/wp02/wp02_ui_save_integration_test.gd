extends Node

var failures: Array[String] = []

func _ready() -> void:
    await get_tree().process_frame
    var root_result: Dictionary = SaveFoundation.set_storage_root("user://wp02_ui_save_integration")
    _expect(bool(root_result.get("ok", false)), "Could not set isolated WP-02 UI save root.")
    SaveFoundation.clear_test_storage()
    SaveManager.delete_save()

    GameState.new_game("STANDARD")
    GameState.set_flag(GameState.FLAG_VS_BRIDGE_ACTIVATED, true)
    GameState.set_world_position(Vector3(2.5, 0.9, -4.25), Vector3.FORWARD)
    _expect(SaveManager.save_game("manual"), "Menu-compatible SaveManager save failed.")
    _expect(SaveManager.has_save(), "Title-compatible SaveManager did not report a verified save.")

    GameState.new_game("STANDARD")
    GameState.set_world_position(Vector3(0.0, 0.9, 8.0), Vector3.FORWARD)
    _expect(SaveManager.load_game(false), "Title-compatible Continue load failed.")
    _expect(GameState.has_flag(GameState.FLAG_VS_BRIDGE_ACTIVATED), "Loaded state lost the bridge flag.")
    _expect(GameState.get_world_position().distance_to(Vector3(2.5, 0.9, -4.25)) < 0.01, "Loaded state lost the saved world position.")

    GameState.set_world_position(Vector3(4.0, 0.9, -8.0), Vector3.FORWARD)
    _expect(SaveManager.save_game("second_manual"), "Second menu-compatible save failed.")
    _expect(SaveManager.has_backup(), "Verified backup was not exposed to the title screen.")
    _expect(SaveManager.load_game(true), "Recover Backup path failed.")
    _expect(GameState.get_world_position().distance_to(Vector3(2.5, 0.9, -4.25)) < 0.01, "Recover Backup did not load the previous verified state.")

    var title_scene := load("res://src/scenes/title.tscn") as PackedScene
    _expect(title_scene != null, "Title scene could not be loaded.")
    if title_scene != null:
        var title := title_scene.instantiate()
        add_child(title)
        await get_tree().process_frame
        await get_tree().process_frame
        _expect(_find_button(title, "Continue") != null, "Title screen did not expose Continue after a verified save.")
        title.queue_free()

    SaveManager.delete_save()
    _expect(not SaveManager.has_save(), "Delete Save did not remove the WP-02 slot.")

    if failures.is_empty():
        print("PASS: WP-02 device-path SaveManager, Continue, backup recovery, and title integration are operational.")
        get_tree().quit(0)
        return
    for failure in failures:
        push_error("WP-02 UI SAVE INTEGRATION FAILED: " + failure)
    get_tree().quit(1)

func _find_button(root: Node, label: String) -> Button:
    for node in root.find_children("*", "Button", true, false):
        var button := node as Button
        if button != null and button.text == label:
            return button
    return null

func _expect(condition: bool, message: String) -> void:
    if not condition:
        failures.append(message)
