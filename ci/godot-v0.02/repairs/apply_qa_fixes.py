#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


def fail(message: str) -> None:
    raise SystemExit(f"QA FIX ERROR: {message}")


def read(path: Path) -> str:
    if not path.is_file():
        fail(f"missing required file: {path}")
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def replace_once(text: str, pattern: str, replacement: str, label: str, flags: int = 0) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1, flags=flags)
    if count != 1:
        fail(f"expected exactly one {label} match, found {count}")
    return updated


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: apply_qa_fixes.py <project_dir>")

    root = Path(sys.argv[1]).resolve()
    ruin_path = root / "src/scenes/ruin_scene.gd"
    identity_path = root / "src/autoload/build_identity.gd"
    preset_path = root / "export_presets.cfg"

    ruin = read(ruin_path)

    # Godot screen input uses negative Y for up. The previous camera-relative
    # conversion multiplied that value by camera-forward, reversing vertical
    # movement. Subtracting the Y component restores intuitive up/down motion
    # for touch, keyboard, and controller input.
    ruin = replace_once(
        ruin,
        r"(?m)^(\s*)var direction := \(right \* input_vector\.x \+ forward \* input_vector\.y\)\s*$",
        r"\1var direction := (right * input_vector.x - forward * input_vector.y)",
        "camera-relative movement line",
    )

    # Keep the distance encounter system, but also guarantee the authored first
    # formation when Cyanis crosses the post-bridge atrium gate.
    encounter_line = re.search(r"(?m)^    var can_encounter := .+$", ruin)
    if encounter_line is None:
        fail("could not locate can_encounter definition")
    guaranteed_gate = (
        encounter_line.group(0)
        + "\n"
        + "    if can_encounter and player.global_position.z <= -3.0:\n"
        + "        GameState.world[\"encounter_distance\"] = 0.0\n"
        + "        _start_battle(\"ORDINARY\", \"FORM_VS_A\")\n"
        + "        return"
    )
    ruin = ruin[: encounter_line.start()] + guaranteed_gate + ruin[encounter_line.end() :]

    if "right * input_vector.x - forward * input_vector.y" not in ruin:
        fail("vertical movement correction was not applied")
    if 'player.global_position.z <= -3.0' not in ruin:
        fail("guaranteed first-battle gate was not applied")
    if '_start_battle("ORDINARY", "FORM_VS_A")' not in ruin:
        fail("guaranteed formation call is missing")
    write(ruin_path, ruin)

    identity = read(identity_path)
    identity = replace_once(
        identity,
        r'(?m)^const BUILD_VERSION := "[^"]+"$',
        'const BUILD_VERSION := "0.02.2"',
        "build version",
    )
    identity = replace_once(
        identity,
        r'(?m)^const CONTENT_VERSION := "[^"]+"$',
        'const CONTENT_VERSION := "vs-0.02.2"',
        "content version",
    )
    write(identity_path, identity)

    presets = read(preset_path)
    presets = replace_once(
        presets,
        r"(?m)^version/code=\d+$",
        "version/code=4",
        "Android version code",
    )
    presets = replace_once(
        presets,
        r'(?m)^version/name="[^"]+"$',
        'version/name="0.02.2"',
        "Android version name",
    )
    write(preset_path, presets)

    print("PASS: v0.02.2 QA fixes applied (vertical movement, guaranteed first battle, build identity).")


if __name__ == "__main__":
    main()
