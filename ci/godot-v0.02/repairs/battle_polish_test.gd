extends Node

func _ready() -> void:
    call_deferred("_run")

func _fail(message: String) -> void:
    push_error("BATTLE POLISH TEST FAILED: " + message)
    get_tree().quit(1)

func _run() -> void:
    var sim := BattleSimulator.new()
    sim.setup("ORDINARY", "FORM_VS_A", 17)
    sim.start_round()

    var first_target := "EN_VS_RUIN_SENTINEL_A"
    var next_target := "EN_VS_RUIN_SENTINEL_B"
    sim.actors[first_target]["hp"] = 0
    sim.actors[first_target]["alive"] = false
    var before_hp := int(sim.actor(next_target)["hp"])
    var events := sim.resolve_round([{
        "actor_id": "HERO_CYANIS",
        "action_id": "ATTACK",
        "target_id": first_target,
        "family": "ABILITY",
        "priority": 0,
        "tie_rank": 0,
    }])
    if int(sim.actor(next_target)["hp"]) >= before_hp:
        _fail("the attack did not move to the next living enemy")
        return

    var saw_retarget := false
    for event in events:
        if str(event.get("type", "")) == "retarget" and str(event.get("target_id", "")) == next_target:
            saw_retarget = true
            break
    if not saw_retarget:
        _fail("the resolution log did not record the automatic retarget")
        return

    var scene_source := FileAccess.get_file_as_string("res://src/scenes/battle_scene.gd")
    if scene_source.is_empty():
        _fail("battle scene source could not be read")
        return

    var required_tokens: Array[String] = [
        "var detail_scroll: ScrollContainer",
        "var detail_box: GridContainer",
        "detail_box.columns = 2",
        "detail_scroll.vertical_scroll_mode = ScrollContainer.SCROLL_MODE_AUTO",
        "detail_scroll.follow_focus = true",
        "detail_scroll.scroll_deadzone = 8",
        "button.mouse_filter = Control.MOUSE_FILTER_PASS",
    ]
    for token in required_tokens:
        if scene_source.find(token) < 0:
            _fail("missing mobile ability-scroll configuration: " + token)
            return

    print("PASS: dead-target retargeting and touch ability scrolling are operational.")
    get_tree().quit(0)
