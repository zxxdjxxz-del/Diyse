#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).parent.resolve()


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if new in text:
        return
    if old not in text:
        raise SystemExit(f"Expected text not found in {path.name}: {old[:120]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def patch_scene(path: Path, add_menu: bool) -> None:
    replace_once(
        path,
        '    var desktop_input := Input.get_vector("move_left", "move_right", "move_up", "move_down")\n',
        '    var desktop_input := _desktop_input()\n',
    )

    old_unhandled = (
        'func _unhandled_input(event: InputEvent) -> void:\n'
        '    if event.is_action_pressed("interact"):\n'
        '        _perform_interaction()\n'
        '    elif event.is_action_pressed("pause"):\n'
        '        pause_panel.visible = not pause_panel.visible\n'
    )
    new_unhandled = (
        'func _unhandled_input(event: InputEvent) -> void:\n'
        '    var interact_pressed := event.is_action_pressed("ui_accept")\n'
        '    if InputMap.has_action("interact"):\n'
        '        interact_pressed = interact_pressed or event.is_action_pressed("interact")\n'
        '    var pause_pressed := event.is_action_pressed("ui_cancel")\n'
        '    if InputMap.has_action("pause"):\n'
        '        pause_pressed = pause_pressed or event.is_action_pressed("pause")\n'
        '    if interact_pressed:\n'
        '        _perform_interaction()\n'
        '    elif pause_pressed:\n'
        '        pause_panel.visible = not pause_panel.visible\n'
    )
    replace_once(path, old_unhandled, new_unhandled)

    text = path.read_text(encoding="utf-8")
    helper = (
        'func _desktop_input() -> Vector2:\n'
        '    var custom_actions := ["move_left", "move_right", "move_up", "move_down"]\n'
        '    var custom_ready := true\n'
        '    for action in custom_actions:\n'
        '        if not InputMap.has_action(action):\n'
        '            custom_ready = false\n'
        '            break\n'
        '    if custom_ready:\n'
        '        return Input.get_vector("move_left", "move_right", "move_up", "move_down")\n'
        '    return Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")\n\n'
    )
    marker = 'func _unhandled_input(event: InputEvent) -> void:\n'
    if helper not in text:
        if marker not in text:
            raise SystemExit(f"Unhandled-input marker missing in {path.name}")
        text = text.replace(marker, helper + marker, 1)
        path.write_text(text, encoding="utf-8")

    if add_menu:
        menu_block = (
            '    var menu_button := Button.new()\n'
            '    menu_button.text = "Menu"\n'
            '    menu_button.position = Vector2(1085, 10)\n'
            '    menu_button.size = Vector2(130, 56)\n'
            '    menu_button.pressed.connect(func(): pause_panel.visible = not pause_panel.visible)\n'
            '    root.add_child(menu_button)\n'
        )
        text = path.read_text(encoding="utf-8")
        if menu_block not in text:
            anchor = (
                '    action_button.pressed.connect(_perform_interaction)\n'
                '    root.add_child(action_button)\n'
            )
            if anchor not in text:
                raise SystemExit("Annex action-button anchor missing.")
            text = text.replace(anchor, anchor + menu_block, 1)
            path.write_text(text, encoding="utf-8")


patch_scene(root / "ruin_scene_wp03.gd", add_menu=False)
patch_scene(root / "traversal_annex_scene.gd", add_menu=True)

test_path = root / "wp03_traversal_regression_test.gd"
test_text = test_path.read_text(encoding="utf-8")
old = (
    '        _expect(annex.find_child("AnnexReturn", true, false) != null, "Annex return transition is missing.")\n'
    '        annex.queue_free()\n'
)
new = (
    '        _expect(annex.find_child("AnnexReturn", true, false) != null, "Annex return transition is missing.")\n'
    '        _expect(_find_button(annex, "Menu") != null, "Annex touch Menu button is missing.")\n'
    '        _expect(_find_button(annex, "Action") != null, "Annex touch Action button is missing.")\n'
    '        annex.queue_free()\n'
)
if new not in test_text:
    if old not in test_text:
        raise SystemExit("Annex regression anchor missing.")
    test_text = test_text.replace(old, new, 1)

helper = (
    'func _find_button(root: Node, label: String) -> Button:\n'
    '    for node in root.find_children("*", "Button", true, false):\n'
    '        var button := node as Button\n'
    '        if button != null and button.text == label:\n'
    '            return button\n'
    '    return null\n\n'
)
if helper not in test_text:
    marker = 'func _expect(condition: bool, message: String) -> void:\n'
    if marker not in test_text:
        raise SystemExit("Test helper marker missing.")
    test_text = test_text.replace(marker, helper + marker, 1)

test_path.write_text(test_text, encoding="utf-8")

apply_path = root / "apply_wp03.py"
apply_text = apply_path.read_text(encoding="utf-8")
apply_text = apply_text.replace("0.05.0-WP03", "0.05.1-WP03R")
apply_path.write_text(apply_text, encoding="utf-8")

print("WP-03R input fallback, touch-menu, controller-action fallback, regression, and build-version repairs applied.")
