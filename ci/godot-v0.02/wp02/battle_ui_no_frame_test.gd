extends Node

func _ready() -> void:
    call_deferred("_run")

func _fail(message: String) -> void:
    push_error("BATTLE UI WP-02R TEST FAILED: " + message)
    get_tree().quit(1)

func _run() -> void:
    var source := FileAccess.get_file_as_string("res://src/scenes/battle_scene.gd")
    if source.is_empty():
        _fail("battle scene source could not be read")
        return

    var required: Array[String] = [
        "var resolution_bar: HBoxContainer",
        "confirm_button.text = \"RESOLVE ROUND\"",
        "edit_plan_button.text = \"EDIT PLAN\"",
        "func _edit_plan() -> void:",
        "plan_label.max_lines_visible = 2",
        "command_panel.custom_minimum_size = Vector2(0, 136)",
    ]
    for token in required:
        if source.find(token) < 0:
            _fail("missing compact battle UI token: " + token)
            return

    var prohibited: Array[String] = [
        "FRAME_TEXTURE",
        "OrnateBattleFrame",
        "_add_ornate_outer_frame",
        "diyse_battle_outer_frame.svg",
    ]
    for token in prohibited:
        if source.find(token) >= 0:
            _fail("custom battle frame token remains: " + token)
            return

    var packed := load("res://src/scenes/battle_scene.tscn") as PackedScene
    if packed == null:
        _fail("battle scene could not be loaded")
        return
    var scene := packed.instantiate()
    add_child(scene)
    await get_tree().process_frame
    await get_tree().process_frame

    if scene.find_child("OrnateBattleFrame", true, false) != null:
        _fail("custom outer battle frame still instantiated")
        return
    var resolve_button := _find_button(scene, "RESOLVE ROUND")
    var edit_button := _find_button(scene, "EDIT PLAN")
    if resolve_button == null or edit_button == null:
        _fail("fixed plan controls did not instantiate")
        return

    print("PASS: compact fixed round controls instantiate without the custom outer battle frame.")
    get_tree().quit(0)

func _find_button(root: Node, label: String) -> Button:
    for node in root.find_children("*", "Button", true, false):
        var button := node as Button
        if button != null and button.text == label:
            return button
    return null
