extends SceneTree

func _initialize() -> void:
    call_deferred("_run")

func _fail(message: String) -> void:
    push_error("BATTLE POLISH TEST FAILED: " + message)
    quit(1)

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

    var packed := load("res://src/scenes/battle_scene.tscn") as PackedScene
    if packed == null:
        _fail("battle scene could not be loaded")
        return
    var scene := packed.instantiate()
    root.add_child(scene)
    await process_frame
    await process_frame

    var detail_scroll := scene.get("detail_scroll") as ScrollContainer
    var detail_box := scene.get("detail_box") as GridContainer
    if detail_scroll == null:
        _fail("detail scroll container is missing")
        return
    if detail_scroll.vertical_scroll_mode == ScrollContainer.SCROLL_MODE_DISABLED:
        _fail("vertical ability scrolling is disabled")
        return
    if not bool(detail_scroll.follow_focus):
        _fail("ability scroll does not follow focused controls")
        return
    if detail_box == null or int(detail_box.columns) != 2:
        _fail("ability choices are not arranged in the two-column touch grid")
        return

    scene.call("_show_abilities")
    await process_frame
    if detail_box.get_child_count() < 4:
        _fail("the ability list did not populate")
        return
    for child in detail_box.get_children():
        if child is Button and child.mouse_filter != Control.MOUSE_FILTER_PASS:
            _fail("an ability button blocks touch-drag scrolling")
            return

    scene.queue_free()
    print("PASS: dead-target retargeting and touch ability scrolling are operational.")
    quit(0)
