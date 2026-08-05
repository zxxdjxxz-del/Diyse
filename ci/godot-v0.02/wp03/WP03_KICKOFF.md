# WP-03 — Core Traversal Vertical Slice

## Status

- Work package: **WP-03 — Core traversal vertical slice**
- Priority: **P0**
- Active authority: **Diyse Active Master Canon v1.12 / Audit 25**
- Approved dependencies:
  - **WP-01R v0.2 / Godot v0.03.1-WP01R**
  - **WP-02R v0.04.1-WP02R**, device-approved August 4, 2026
- Base commit: `20034f740bea1c8b868fe484ad82381966c2e4ad`
- Branch: `agent/godot-wp03`
- Merge policy: stacked draft only; do not merge automatically

## Acceptance authority

WP-03 is accepted only when a representative playable area meets the controlling **Section 32L / Section 74** traversal and presentation criteria.

## Required traversal slice

1. Cyanis is the normally sole visible controllable field character.
2. Camera-relative analog movement has very short acceleration/deceleration, fast turning, responsive blending, and minimized foot sliding.
3. Fixed and semi-fixed authored camera changes preserve held-direction continuity; movement must not suddenly reverse.
4. Walkable collision is forgiving and supports smooth wall sliding without catching on decorative details.
5. Stairs use smooth navigation slopes with visual step adaptation rather than literal collision on each step.
6. Narrow ledges, bridges, platforms, and mechanisms use generous invisible safe lanes and edge protection.
7. Cyanis remains readable across depth and camera distance.
8. Foreground occlusion triggers selective transparency, silhouette support, or another authored visibility aid before control is impaired.
9. At least one interaction/mechanism, one treasure interaction, and one location transition are operational.
10. Save and Continue restore the traversal state through the approved WP-02R foundation.
11. Android touch controls and safe-area behavior remain functional.
12. Reduced-motion and 30-fps fallback behavior must not reverse input, remove critical tells, or introduce unacceptable latency.

## Initial implementation order

1. Freeze the approved WP-02R baseline and add WP-03-specific regressions.
2. Build the representative traversal map with authored walkable lanes and collision proxies.
3. Implement camera-relative movement and authored-camera basis blending.
4. Add stairs, ledge safety, wall sliding, foreground occlusion assistance, interaction, treasure, and transition fixtures.
5. Integrate traversal-state save/continue with WP-02R.
6. Build and sign a new Android candidate.
7. Require explicit on-device acceptance before WP-03 is approved or WP-07/WP-08 traversal dependencies are unblocked.

## Non-goals

- No full-world content production.
- No final art requirement beyond readable representative assets.
- No canon, stat, identity, encounter, Card, equipment, or narrative mutation.
- No merge into `main` or earlier work-package branches without an explicit instruction.
