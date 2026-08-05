# WP-03 — Core Traversal Vertical Slice

This package implements the first representative Section 32L/74 traversal slice on top of the device-approved WP-02R baseline.

## Candidate

- Build: `0.05.0-WP03`
- Branch: `agent/godot-wp03`
- Base: approved WP-02R commit `20034f740bea1c8b868fe484ad82381966c2e4ad`
- Pull request: #30, stacked draft, unmerged
- Source package SHA-256: `0a20d960b9ed5887ce5ecc3be58e1495355e5744c70b518adae747af16621a99`

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
- WP-02R traversal-state Save and Continue routing
- Android safe-area controls, reduced-motion handoff, and 30-fps stability regression

## Acceptance boundary

WP-03 remains a candidate until the CI pipeline passes, a signed APK is independently verified, and the user explicitly approves the traversal behavior on-device. No branch is merged automatically.
