#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


def fail(message: str) -> None:
    raise SystemExit(f"BATTLE UI 0.02.5 ERROR: {message}")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        fail(f"expected exactly one {label} match, found {count}")
    return text.replace(old, new, 1)


def regex_once(text: str, pattern: str, replacement: str, label: str, flags: int = 0) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1, flags=flags)
    if count != 1:
        fail(f"expected exactly one {label} match, found {count}")
    return updated


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: apply_battle_ui_v0025.py <project_dir>")

    root = Path(sys.argv[1]).resolve()
    scene_path = root / "src/scenes/battle_scene.gd"
    identity_path = root / "src/autoload/build_identity.gd"
    preset_path = root / "export_presets.cfg"

    scene = scene_path.read_text(encoding="utf-8")

    scene = replace_once(
        scene,
        "var confirm_button: Button\nvar battle_message_label: Label\n",
        "var command_row: HBoxContainer\nvar resolution_bar: HBoxContainer\nvar edit_plan_button: Button\nvar confirm_button: Button\nvar battle_message_label: Label\n",
        "battle control declarations",
    )

    scene = replace_once(
        scene,
        "const COLOR_BG := Color(0.025, 0.035, 0.055, 1.0)\nconst COLOR_PANEL := Color(0.075, 0.095, 0.13, 0.98)\nconst COLOR_PANEL_ALT := Color(0.045, 0.06, 0.085, 0.98)\nconst COLOR_LINE := Color(0.31, 0.42, 0.56, 1.0)\nconst COLOR_GOLD := Color(0.95, 0.77, 0.31, 1.0)\n",
        "const FRAME_TEXTURE := preload(\"res://assets/ui/diyse_battle_outer_frame.svg\")\n\nconst COLOR_BG := Color(0.018, 0.055, 0.042, 1.0)\nconst COLOR_PANEL := Color(0.028, 0.105, 0.073, 0.98)\nconst COLOR_PANEL_ALT := Color(0.025, 0.075, 0.057, 0.98)\nconst COLOR_LINE := Color(0.72, 0.49, 0.12, 1.0)\nconst COLOR_GOLD := Color(0.98, 0.77, 0.25, 1.0)\n",
        "frame texture and green-gold palette",
    )

    scene = replace_once(
        scene,
        "    command_panel.custom_minimum_size = Vector2(0, 235)\n",
        "    command_panel.custom_minimum_size = Vector2(0, 136)\n",
        "compact command panel height",
    )

    scene = replace_once(
        scene,
        "    plan_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART\n    plan_label.add_theme_font_size_override(\"font_size\", 20)\n",
        "    plan_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART\n    plan_label.max_lines_visible = 2\n    plan_label.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS\n    plan_label.custom_minimum_size = Vector2(0, 48)\n    plan_label.add_theme_font_size_override(\"font_size\", 18)\n",
        "compact plan label",
    )

    scene = replace_once(
        scene,
        "    var command_row := HBoxContainer.new()\n",
        "    command_row = HBoxContainer.new()\n",
        "persistent command row",
    )

    old_confirm = '''    confirm_button = Button.new()
    confirm_button.text = "CONFIRM ROUND"
    confirm_button.custom_minimum_size = Vector2(0, 62)
    confirm_button.add_theme_font_size_override("font_size", 21)
    confirm_button.visible = false
    confirm_button.pressed.connect(_confirm_round)
    command_root.add_child(confirm_button)
'''
    new_confirm = '''    resolution_bar = HBoxContainer.new()
    resolution_bar.visible = false
    resolution_bar.add_theme_constant_override("separation", 12)
    command_root.add_child(resolution_bar)

    edit_plan_button = Button.new()
    edit_plan_button.text = "EDIT PLAN"
    edit_plan_button.custom_minimum_size = Vector2(230, 58)
    edit_plan_button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    edit_plan_button.add_theme_font_size_override("font_size", 20)
    edit_plan_button.add_theme_stylebox_override("normal", _action_button_style(false))
    edit_plan_button.add_theme_color_override("font_color", Color(0.07, 0.12, 0.08, 1.0))
    edit_plan_button.pressed.connect(_edit_plan)
    resolution_bar.add_child(edit_plan_button)

    confirm_button = Button.new()
    confirm_button.text = "RESOLVE ROUND"
    confirm_button.custom_minimum_size = Vector2(360, 58)
    confirm_button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    confirm_button.add_theme_font_size_override("font_size", 21)
    confirm_button.add_theme_stylebox_override("normal", _action_button_style(true))
    confirm_button.add_theme_color_override("font_color", Color(1.0, 0.94, 0.72, 1.0))
    confirm_button.pressed.connect(_confirm_round)
    resolution_bar.add_child(confirm_button)

    _add_ornate_outer_frame()
'''
    scene = replace_once(scene, old_confirm, new_confirm, "resolution bar construction")

    old_ready_plan = '''    else:
        battle_message_label.text = "ROUND PLAN READY"
        var lines: Array[String] = ["Review the plan, then confirm:"]
        for plan in plans:
            lines.append("• %s → %s" % [sim.actor(plan["actor_id"])["name"], str(plan["action_id"]).replace("_", " ").capitalize()])
        plan_label.text = "   ".join(lines)
'''
    new_ready_plan = '''    else:
        battle_message_label.text = "ROUND PLAN READY"
        var entries: Array[String] = []
        for plan in plans:
            entries.append("%s: %s" % [sim.actor(plan["actor_id"])["name"], str(plan["action_id"]).replace("_", " ").capitalize()])
        plan_label.text = "Plan  •  " + "   •   ".join(entries)
'''
    scene = replace_once(scene, old_ready_plan, new_ready_plan, "compact plan summary")

    old_show = '''func _show_commands() -> void:
    _clear(command_box)
    _clear(detail_box)
    confirm_button.visible = false
    if current_party_index >= planning_ids.size():
        confirm_button.visible = true
        _refresh_plan_label()
        return
'''
    new_show = '''func _show_commands() -> void:
    _clear(command_box)
    _clear(detail_box)
    resolution_bar.visible = false
    command_row.visible = true
    if current_party_index >= planning_ids.size():
        command_row.visible = false
        resolution_bar.visible = true
        _refresh_plan_label()
        return
'''
    scene = replace_once(scene, old_show, new_show, "plan-ready command state")

    scene = replace_once(
        scene,
        "func _confirm_round() -> void:\n",
        '''func _edit_plan() -> void:
    plans.clear()
    current_party_index = 0
    planning_ids = sim.living_party()
    pending_action.clear()
    phase = "PLANNING"
    log_label.append_text("[i]Round plan reopened for editing.[/i]\\n")
    _refresh_all()
    _show_commands()

func _confirm_round() -> void:
''',
        "edit-plan function",
    )

    scene = replace_once(
        scene,
        "    confirm_button.visible = false\n    _clear(command_box)\n",
        "    resolution_bar.visible = false\n    command_row.visible = false\n    _clear(command_box)\n",
        "resolution start state",
    )

    scene = replace_once(
        scene,
        "func _show_defeat() -> void:\n    phase = \"DEFEAT\"\n",
        "func _show_defeat() -> void:\n    phase = \"DEFEAT\"\n    resolution_bar.visible = false\n    command_row.visible = true\n",
        "defeat command visibility",
    )

    helper_anchor = "func _panel_style(fill: Color, border: Color, radius: int, border_width: int) -> StyleBoxFlat:\n"
    helpers = '''func _action_button_style(primary: bool) -> StyleBoxFlat:
    var style := StyleBoxFlat.new()
    style.bg_color = Color(0.015, 0.19, 0.105, 1.0) if primary else Color(0.91, 0.87, 0.72, 1.0)
    style.border_color = COLOR_GOLD
    style.set_border_width_all(2)
    style.set_corner_radius_all(10)
    style.content_margin_left = 16
    style.content_margin_right = 16
    style.content_margin_top = 10
    style.content_margin_bottom = 10
    return style

func _add_ornate_outer_frame() -> void:
    var frame := NinePatchRect.new()
    frame.name = "OrnateBattleFrame"
    frame.texture = FRAME_TEXTURE
    frame.draw_center = false
    frame.patch_margin_left = 44
    frame.patch_margin_top = 44
    frame.patch_margin_right = 44
    frame.patch_margin_bottom = 44
    frame.mouse_filter = Control.MOUSE_FILTER_IGNORE
    frame.z_index = 100
    frame.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
    add_child(frame)

'''
    scene = replace_once(scene, helper_anchor, helpers + helper_anchor, "ornate frame helpers")

    required = [
        'FRAME_TEXTURE := preload("res://assets/ui/diyse_battle_outer_frame.svg")',
        'var resolution_bar: HBoxContainer',
        'confirm_button.text = "RESOLVE ROUND"',
        'edit_plan_button.text = "EDIT PLAN"',
        'func _edit_plan() -> void:',
        'frame.draw_center = false',
        'plan_label.max_lines_visible = 2',
        'command_panel.custom_minimum_size = Vector2(0, 136)',
    ]
    for token in required:
        if token not in scene:
            fail(f"missing battle UI token: {token}")

    scene_path.write_text(scene, encoding="utf-8", newline="\n")

    identity = identity_path.read_text(encoding="utf-8")
    identity = regex_once(identity, r'(?m)^const BUILD_VERSION := "[^"]+"$', 'const BUILD_VERSION := "0.02.5"', "build version")
    identity = regex_once(identity, r'(?m)^const CONTENT_VERSION := "[^"]+"$', 'const CONTENT_VERSION := "vs-0.02.5"', "content version")
    identity_path.write_text(identity, encoding="utf-8", newline="\n")

    presets = preset_path.read_text(encoding="utf-8")
    presets = regex_once(presets, r'(?m)^version/code=\d+$', 'version/code=7', "Android version code")
    presets = regex_once(presets, r'(?m)^version/name="[^"]+"$', 'version/name="0.02.5"', "Android version name")
    preset_path.write_text(presets, encoding="utf-8", newline="\n")

    print("PASS: compact Resolve Round bar and restrained ornate battle trim applied for v0.02.5.")


if __name__ == "__main__":
    main()
