# Diyse Project Reference Index

**Status:** Authoritative repository index  
**Updated:** 2026-08-02

This index identifies which repository documents control future design and implementation work.

## 1. Primary Game Canon

The newest approved **Diyse: 3D JRPG Active Master Canon** remains the authority for world, story, characters, classes, combat, Cards, equipment, progression, relationships, quests, and other game canon.

A prototype implementation does not silently replace or amend the master canon. Placeholder prototype content remains provisional unless separately approved and consolidated into the newest full master.

## 2. Map and Traversal Authority

**Authoritative file:**

`docs/Diyse_Final_Fantasy_VII_X_Map_and_Traversal_Design_Standard.md`

This controls future work involving:

- local field movement;
- fixed and semi-fixed cameras;
- pre-rendered or pre-composed fields;
- walkmeshes and collision;
- perspective scaling;
- foreground occlusion;
- interactions and contextual traversal;
- timing hazards;
- dynamic map connectivity;
- towns and settlements;
- dungeons and facilities;
- regional and world travel;
- vehicles and transport;
- optional areas;
- revisits and destruction states;
- multi-party routes;
- final-dungeon structure.

It consolidates approved lessons from Final Fantasy VII, VIII, IX, and X while keeping each game’s contribution distinct and traceable.

The older file `docs/Diyse_FFVII_Map_and_Traversal_Design_Standard.md` is superseded and exists only as a redirect.

## 3. Required Map-Design Template

**Template:**

`docs/templates/Diyse_Map_Design_Sheet.md`

Every substantial new field, settlement, dungeon, regional route, vehicle space, optional area, or revisit state should begin from this template.

A completed map sheet must include:

- map identity and narrative role;
- culture, biome, function, history, emotion, landmark, and traversal identity;
- original function, transformation, and current adaptation;
- selected traversal grammar;
- critical path, optional routes, loops, shortcuts, and state changes;
- screen or zone composition plan;
- movement, camera, scale, and occlusion rules;
- mechanism and hazard vocabulary;
- encounter and recovery placement;
- revisit and late-access behavior;
- Android acceptance tests;
- a Standard Traceability table naming the exact sections of the VII–X standard being implemented.

## 4. Implementation Traceability Rule

Every future map-related issue, implementation branch, and pull request must state:

1. which completed map-design sheet it implements;
2. which sections of the VII–X standard apply;
3. which binding requirements are directly tested;
4. which elements are intentionally deferred;
5. whether any proposed behavior conflicts with the active master canon;
6. whether the build is a technical placeholder, provisional design, or approved canon implementation.

A map feature is not considered fully accepted solely because automated tests pass. Device testing must confirm touch feel, camera continuity, route readability, occlusion, performance, and complete route accessibility.

## 5. Automated Enforcement

The repository enforces this rule through:

- `.github/ISSUE_TEMPLATE/map-and-traversal.yml` for new map and traversal work;
- `.github/pull_request_template.md` for canon status, design-sheet path, standard sections, tested requirements, deferred work, and device acceptance;
- `ci/validate-map-traceability.py` for diff-aware pull-request validation;
- the **Validate map and traversal traceability** step in the Android build workflow.

When a pull request changes field, walkmesh, traversal, gatehouse, world-map, regional, settlement, dungeon, v0.09 traversal overlay, map-standard, or location-sheet files, CI requires:

- a real completed design sheet under `docs/maps/`;
- a PR body naming that sheet;
- exact VII–X standard sections or binding requirements;
- canon or placeholder status;
- automated and Android device-acceptance coverage;
- deferred-work disclosure.

Non-map work is not required to provide a map sheet merely because it shares the same Android build workflow.

## 6. Prototype Baseline Rule

The newest device-tested stable prototype is the implementation baseline for subsequent work. A newer draft build does not replace that baseline until:

- the required automated and regression tests pass;
- the Android APK compiles and retains the permanent prototype certificate;
- the full target route works on the user’s phone;
- the relevant pull request is approved and merged.

## 7. Authority Order

When documents appear to conflict, use this order:

1. newest explicit user-approved decision;
2. newest approved full Active Master Canon;
3. this reference index for document routing;
4. the VII–X Map and Traversal Design Standard for map/traversal principles;
5. an approved completed map-design sheet for the specific location;
6. device-tested stable prototype behavior;
7. draft implementation notes and experimental builds;
8. superseded or recovery-only material.

Any unresolved conflict must be documented rather than silently reconciled.
