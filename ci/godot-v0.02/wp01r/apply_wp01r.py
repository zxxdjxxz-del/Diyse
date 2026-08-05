#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

VERSION = "0.03.1-WP01R"


def replace_once(text: str, pattern: str, replacement: str, label: str) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.MULTILINE)
    if count != 1:
        raise RuntimeError(f"Could not update {label}; expected exactly one match, got {count}.")
    return updated


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: apply_wp01r.py <godot-project-dir>", file=sys.stderr)
        return 2

    project = Path(sys.argv[1]).resolve()
    project_file = project / "project.godot"
    build_identity = project / "src/autoload/build_identity.gd"
    export_presets = project / "export_presets.cfg"
    content_manifest = project / "data/content_manifest.json"

    for required in (project_file, build_identity, export_presets):
        if not required.is_file():
            raise FileNotFoundError(required)

    project_text = project_file.read_text(encoding="utf-8")
    autoload_line = 'AuthorityManager="*res://src/autoload/authority_manager.gd"'
    if autoload_line not in project_text:
        if "[autoload]" in project_text:
            project_text = project_text.replace("[autoload]\n", f"[autoload]\n{autoload_line}\n", 1)
        else:
            project_text += f"\n[autoload]\n{autoload_line}\n"
    project_file.write_text(project_text, encoding="utf-8")

    identity_text = build_identity.read_text(encoding="utf-8")
    identity_text = replace_once(
        identity_text,
        r'^const BUILD_VERSION := ".*"$',
        f'const BUILD_VERSION := "{VERSION}"',
        "build identity",
    )
    build_identity.write_text(identity_text, encoding="utf-8")

    preset_text = export_presets.read_text(encoding="utf-8")
    preset_text = replace_once(
        preset_text,
        r'^version/name=".*"$',
        f'version/name="{VERSION}"',
        "Android version name",
    )
    if 'include_filter="assets/authority/v1_12/**"' not in preset_text:
        if re.search(r'^include_filter=".*"$', preset_text, flags=re.MULTILINE):
            preset_text = re.sub(
                r'^include_filter="(.*)"$',
                lambda match: 'include_filter="' + (
                    match.group(1) + "," if match.group(1) else ""
                ) + 'assets/authority/v1_12/**"',
                preset_text,
                count=1,
                flags=re.MULTILINE,
            )
        else:
            preset_text += '\ninclude_filter="assets/authority/v1_12/**"\n'
    export_presets.write_text(preset_text, encoding="utf-8")

    if content_manifest.is_file():
        data = json.loads(content_manifest.read_text(encoding="utf-8"))
        data["build_version"] = VERSION
        data["authority_bundle"] = "v1.12 / Audit 25 / WP-01R-v0.2"
        data["authority_root"] = "res://assets/authority/v1_12"
        content_manifest.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    print(f"Applied WP-01R authority integration to {project}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
