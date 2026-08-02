#!/usr/bin/env python3
"""Validate Diyse map/traversal design authority and PR traceability."""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_REFERENCE_FILES = (
    ROOT / "docs" / "REFERENCE_INDEX.md",
    ROOT / "docs" / "Diyse_Final_Fantasy_VII_X_Map_and_Traversal_Design_Standard.md",
    ROOT / "docs" / "templates" / "Diyse_Map_Design_Sheet.md",
    ROOT / ".github" / "ISSUE_TEMPLATE" / "map-and-traversal.yml",
    ROOT / ".github" / "pull_request_template.md",
)

REQUIRED_STANDARD_MARKERS = (
    "Final Fantasy VII–X Study Consolidation Edition",
    "## 54. Binding Diyse Requirements",
    "## 56. Per-Map Audit Template",
    "Cyanis as the sole normally visible controllable field character",
    "no permanent follower train",
)

REQUIRED_TEMPLATE_MARKERS = (
    "## C. Three Visible Time Layers",
    "## D. Final Fantasy VII–X Source Trace",
    "## U. Android Device Acceptance",
    "## V. Standard Traceability",
)

MAP_PATH_PATTERNS = (
    re.compile(r"^docs/maps/.*\.md$", re.IGNORECASE),
    re.compile(r"^docs/templates/Diyse_Map_Design_Sheet\.md$", re.IGNORECASE),
    re.compile(r"^docs/Diyse_.*Map_and_Traversal.*\.md$", re.IGNORECASE),
    re.compile(r"^ci/v009", re.IGNORECASE),
    re.compile(r"^ci/patch-v009", re.IGNORECASE),
    re.compile(r"(^|/)(field|fields|walkmesh|traversal|gatehouse|worldmap|world-map|regional|settlement|dungeon)(/|\.|_|-)", re.IGNORECASE),
    re.compile(r"Gatehouse|Traversal|FieldMap|Walkmesh|WorldMap|RegionalMap|Settlement|Dungeon", re.IGNORECASE),
)

REQUIRED_PR_SECTIONS = (
    "Canon status",
    "Map design sheet",
    "Standard sections",
    "Tested requirements",
    "Deferred",
)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def run_git(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        fail(f"git {' '.join(args)} failed: {completed.stderr.strip()}")
    return completed.stdout


def verify_reference_files() -> None:
    for path in REQUIRED_REFERENCE_FILES:
        if not path.is_file():
            fail(f"required authority file is missing: {path.relative_to(ROOT)}")

    standard = REQUIRED_REFERENCE_FILES[1].read_text(encoding="utf-8")
    for marker in REQUIRED_STANDARD_MARKERS:
        if marker not in standard:
            fail(f"map standard is missing required marker: {marker}")

    template = REQUIRED_REFERENCE_FILES[2].read_text(encoding="utf-8")
    for marker in REQUIRED_TEMPLATE_MARKERS:
        if marker not in template:
            fail(f"map design template is missing required marker: {marker}")


def load_event() -> dict:
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        return {}
    path = Path(event_path)
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def changed_files(event_name: str, event: dict) -> list[str]:
    if event_name == "pull_request":
        base_sha = event.get("pull_request", {}).get("base", {}).get("sha")
        head_sha = event.get("pull_request", {}).get("head", {}).get("sha", "HEAD")
        if not base_sha:
            fail("pull_request event did not provide a base SHA")
        output = run_git("diff", "--name-only", f"{base_sha}...{head_sha}")
    elif event_name == "push":
        before = event.get("before")
        after = event.get("after", "HEAD")
        if before and before != "0" * 40:
            output = run_git("diff", "--name-only", before, after)
        else:
            output = run_git("show", "--pretty=format:", "--name-only", after)
    else:
        output = run_git("show", "--pretty=format:", "--name-only", "HEAD")

    return sorted({line.strip() for line in output.splitlines() if line.strip()})


def is_map_related(paths: Iterable[str]) -> bool:
    return any(pattern.search(path) for path in paths for pattern in MAP_PATH_PATTERNS)


def section_body(body: str, heading: str) -> str:
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*$\n(?P<body>.*?)(?=^##\s+|\Z)",
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(body)
    return match.group("body").strip() if match else ""


def verify_map_sheet(path_text: str) -> None:
    sheet_path = ROOT / path_text
    if not sheet_path.is_file():
        fail(f"PR references a map design sheet that does not exist: {path_text}")

    sheet = sheet_path.read_text(encoding="utf-8")
    required_sheet_markers = (
        "Authority:",
        "VII–X Source Trace",
        "Android Device Acceptance",
        "Standard Traceability",
    )
    for marker in required_sheet_markers:
        if marker not in sheet:
            fail(f"map design sheet {path_text} is missing required marker: {marker}")


def verify_pull_request_traceability(event: dict, paths: list[str]) -> None:
    pull_request = event.get("pull_request", {})
    body = pull_request.get("body") or ""

    missing_headings = [heading for heading in REQUIRED_PR_SECTIONS if not section_body(body, heading)]
    if missing_headings:
        fail("map-related PR is missing completed sections: " + ", ".join(missing_headings))

    map_section = section_body(body, "Map design sheet")
    match = re.search(r"docs/maps/[A-Za-z0-9_./-]+\.md", map_section)
    if not match:
        fail("map-related PR must name a repository design sheet under docs/maps/")
    verify_map_sheet(match.group(0))

    standards = section_body(body, "Standard sections")
    if standards.lower() == "not applicable" or not re.search(r"\b(section|sections|§|requirement|requirements)\b", standards, re.IGNORECASE):
        fail("map-related PR must identify exact VII–X standard sections or binding requirements")

    tested = section_body(body, "Tested requirements")
    if tested.lower() == "not applicable" or len(tested) < 30:
        fail("map-related PR must describe automated and device acceptance coverage")

    canon = section_body(body, "Canon status")
    if canon.lower() == "not applicable" or len(canon) < 15:
        fail("map-related PR must state canon or placeholder status")

    deferred = section_body(body, "Deferred")
    if len(deferred) < 4:
        fail("map-related PR must state deferred work or explicitly write None")

    print(f"Map traceability sheet: {match.group(0)}")
    print(f"Map-related changed files: {len(paths)}")


def main() -> None:
    verify_reference_files()

    event_name = os.environ.get("GITHUB_EVENT_NAME", "local")
    event = load_event()
    paths = changed_files(event_name, event)

    print("Changed files:")
    for path in paths:
        print(f"  {path}")

    map_related = is_map_related(paths)
    print(f"Map/traversal change detected: {str(map_related).lower()}")

    if map_related and event_name == "pull_request":
        verify_pull_request_traceability(event, paths)
    elif map_related:
        print("Push/local validation: required reference files and markers verified.")
    else:
        print("No map/traversal traceability fields required for this change.")

    print("Diyse map and traversal traceability validation passed.")


if __name__ == "__main__":
    main()
