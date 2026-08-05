# WP-03 — Core Traversal Vertical Slice

This package implements the first representative Section 32L/74 traversal slice on top of the device-approved WP-02R baseline.

## Current candidate

- Build: `0.05.1-WP03R`
- Branch: `agent/godot-wp03`
- Base: approved WP-02R commit `20034f740bea1c8b868fe484ad82381966c2e4ad`
- Pull request: #30, stacked draft, unmerged
- Source package SHA-256: `0a20d960b9ed5887ce5ecc3be58e1495355e5744c70b518adae747af16621a99`
- Deterministic repair: safe desktop-input fallback, guarded optional actions, annex touch Menu, strengthened regression coverage, and strict CI error detection

The earlier `0.05.0-WP03` artifact is rejected because independent log inspection found undefined `move_left/right/up/down` InputMap actions that the original CI negated-grep check failed to enforce.

## Implemented proof points

- Cyanis-only ordinary field control
- camera-relative responsive movement
- smooth fixed/semi-fixed camera-basis blending
- held-direction reversal protection
- forgiving wall sliding
- authored stair slope and visual step adaptation
- invisible bridge and ledge safety guards
- foreground-occlusion transparency and silhouette aid
- representative mechanism, treasure, boss threshold, and location transition
- second traversal location with return transition
- touch joystick, Action, and Menu controls in both traversal locations
- WP-02R traversal-state Save and Continue routing
- Android safe-area controls, reduced-motion handoff, and 30-fps stability regression
- CI failure on missing InputMap actions or other traversal runtime errors

## Acceptance boundary

WP-03 remains a candidate until the repaired CI pipeline passes, a signed APK is independently verified, and the user explicitly approves the traversal behavior on-device. No branch is merged automatically.
