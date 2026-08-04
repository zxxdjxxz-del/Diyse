#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


def fail(message: str) -> None:
    raise SystemExit(f"BATTLE POLISH ERROR: {message}")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        fail(f"expected exactly one {label} match, found {count}")
    return text.replace(old, new, 1)


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: apply_battle_polish.py <project_dir>")

    root = Path(sys.argv[1]).resolve()
    simulator_path = root / "src/core/battle_simulator.gd"
    scene_path = root / "src/scenes/battle_scene.gd"

    simulator = simulator_path.read_text(encoding="utf-8")
    simulator = replace_once(
        simulator,
        '''func _execute_intent(intent: Dictionary) -> Array[Dictionary]:
    var actor_id := str(intent.get("actor_id", ""))
    var action_id := str(intent.get("action_id", "ATTACK"))
    var target_id := str(intent.get("target_id", ""))
    var events: Array[Dictionary] = []
    match action_id:
''',
        '''func _execute_intent(intent: Dictionary) -> Array[Dictionary]:
    var actor_id := str(intent.get("actor_id", ""))
    var action_id := str(intent.get("action_id", "ATTACK"))
    var target_id := str(intent.get("target_id", ""))
    var events: Array[Dictionary] = []
    if _uses_hostile_single_target(action_id) and not _is_alive(target_id):
        var original_target_id := target_id
        var replacement_target_id := _next_living_target(actor_id, target_id)
        if not replacement_target_id.is_empty():
            target_id = replacement_target_id
            events.append(_event(
                "retarget",
                "%s's %s shifts from %s to %s." % [_name(actor_id), _pretty(action_id), _name(original_target_id), _name(target_id)],
                actor_id,
                target_id,
                0,
            ))
    match action_id:
''',
        "intent retarget hook",
    )

    helpers = '''func _uses_hostile_single_target(action_id: String) -> bool:
    return action_id in [
        "ATTACK",
        "ENEMY_ATTACK",
        "CREST_STRIKE",
        "DRIVING_STRIKE",
        "OATH_STRIKE",
        "IRON_TESTAMENT",
        "QUARRY_APPRAISAL",
        "DIYSEAN_APPRAISAL",
        "PINNING_STRIKE",
        "SUNDER_THE_GATE",
        "CINDER_JUDGMENT",
    ]

func _next_living_target(actor_id: String, original_target_id: String) -> String:
    if _is_alive(original_target_id):
        return original_target_id
    var target_team := ""
    if actors.has(original_target_id):
        target_team = str(actors[original_target_id].get("team", ""))
    if target_team.is_empty() and actors.has(actor_id):
        target_team = ENEMY_RED if str(actors[actor_id].get("team", PARTY_BLUE)) == PARTY_BLUE else PARTY_BLUE
    var order: Array[String] = party_ids if target_team == PARTY_BLUE else enemy_ids
    if order.is_empty():
        return ""
    var start_index := order.find(original_target_id)
    for offset in range(1, order.size() + 1):
        var candidate_index := (start_index + offset) % order.size()
        var candidate_id := order[candidate_index]
        if _is_alive(candidate_id):
            return candidate_id
    return ""

'''
    simulator = replace_once(
        simulator,
        "func _damage(actor_id: String, target_id: String, multiplier: float, magical: bool, label: String) -> Dictionary:\n",
        helpers + "func _damage(actor_id: String, target_id: String, multiplier: float, magical: bool, label: String) -> Dictionary:\n",
        "retarget helper insertion point",
    )

    if "_next_living_target" not in simulator or "shifts from" not in simulator:
        fail("retargeting repair was not applied")
    simulator_path.write_text(simulator, encoding="utf-8", newline="\n")

    scene = scene_path.read_text(encoding="utf-8")
    scene = replace_once(
        scene,
        "var detail_box: VBoxContainer\n",
        "var detail_scroll: ScrollContainer\nvar detail_box: GridContainer\n",
        "detail container declaration",
    )
    scene = replace_once(
        scene,
        '''    var detail_scroll := ScrollContainer.new()
    detail_scroll.custom_minimum_size = Vector2(420, 0)
    detail_scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
    detail_scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
    command_row.add_child(detail_scroll)

    detail_box = VBoxContainer.new()
    detail_box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    detail_box.add_theme_constant_override("separation", 7)
    detail_scroll.add_child(detail_box)
''',
        '''    detail_scroll = ScrollContainer.new()
    detail_scroll.custom_minimum_size = Vector2(440, 0)
    detail_scroll.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    detail_scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
    detail_scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
    detail_scroll.vertical_scroll_mode = ScrollContainer.SCROLL_MODE_AUTO
    detail_scroll.follow_focus = true
    detail_scroll.scroll_deadzone = 8
    detail_scroll.mouse_filter = Control.MOUSE_FILTER_STOP
    command_row.add_child(detail_scroll)

    detail_box = GridContainer.new()
    detail_box.columns = 2
    detail_box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    detail_box.add_theme_constant_override("h_separation", 8)
    detail_box.add_theme_constant_override("v_separation", 8)
    detail_scroll.add_child(detail_box)
''',
        "touch-scroll grid construction",
    )
    scene = replace_once(
        scene,
        '''func _detail_button(text: String) -> Button:
    var button := Button.new()
    button.text = text
    button.custom_minimum_size = Vector2(0, 54)
    button.add_theme_font_size_override("font_size", 17)
    return button
''',
        '''func _detail_button(text: String) -> Button:
    var button := Button.new()
    button.text = text
    button.custom_minimum_size = Vector2(0, 52)
    button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    button.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
    button.mouse_filter = Control.MOUSE_FILTER_PASS
    button.add_theme_font_size_override("font_size", 17)
    return button
''',
        "touch-friendly detail button",
    )
    scene = replace_once(
        scene,
        '''func _clear(parent: Node) -> void:
    for child in parent.get_children():
        parent.remove_child(child)
        child.queue_free()
''',
        '''func _clear(parent: Node) -> void:
    if parent == detail_box and is_instance_valid(detail_scroll):
        detail_scroll.set_deferred("scroll_vertical", 0)
    for child in parent.get_children():
        parent.remove_child(child)
        child.queue_free()
''',
        "detail scroll reset",
    )

    required = [
        "var detail_scroll: ScrollContainer",
        "var detail_box: GridContainer",
        "detail_box.columns = 2",
        "detail_scroll.scroll_deadzone = 8",
        "button.mouse_filter = Control.MOUSE_FILTER_PASS",
    ]
    for token in required:
        if token not in scene:
            fail(f"missing scrolling repair token: {token}")
    scene_path.write_text(scene, encoding="utf-8", newline="\n")

    print("PASS: deterministic retargeting and touch-scroll battle polish applied.")


if __name__ == "__main__":
    main()
