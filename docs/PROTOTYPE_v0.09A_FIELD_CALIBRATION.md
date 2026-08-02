# Diyse Prototype v0.09A — Pre-rendered Field Calibration

This branch develops the first hybrid pre-rendered traversal slice on top of the stable v0.08 runtime.

## Calibration slice

- two connected fixed-camera compositions
- Cyanis as the sole normally visible field character
- responsive camera-relative analog movement
- short acceleration and deceleration
- clean walkable lanes with forgiving wall sliding
- a diagonal stair slope
- a lower path beneath an upper bridge
- distinct upper/lower route connectivity despite screen overlap
- depth-based actor scaling
- one foreground arch with selective occlusion handling
- held-input continuity across a camera transition
- contextual doorway alignment
- edge protection with no accidental falls
- developer walkmesh and camera diagnostics

## Implementation rule

The field uses pre-rendered background and foreground plates with a lightweight authored 2.5D walkmesh. Dynamic objects and Cyanis remain real-time. Ordinary traversal does not use precision platforming.

Tracks #17.
