# Diyse Map Design Sheet

**Template version:** 1.0  
**Authority:** Complete this sheet under `docs/Diyse_Final_Fantasy_VII_X_Map_and_Traversal_Design_Standard.md` and the newest approved Diyse Active Master Canon.

---

## A. Document Control

- **Location name:**
- **Map type:** Local field / settlement / dungeon / regional route / world-map area / vehicle / optional area / revisit / final region
- **Design status:** Concept / Provisional / Approved / Implementation-ready / Device-tested
- **Authoritative canon version:**
- **Prototype baseline:**
- **Related issue:**
- **Related branch or PR:**
- **Last updated:**

### Scope Statement

Describe exactly what this sheet controls and what remains outside its scope.

### Canon Status

Identify which names, events, characters, architecture, mechanics, rewards, and visual details are canon, provisional, placeholder, or pending approval.

---

## B. Location Identity

### Culture

Who built, inhabits, controls, remembers, or contests this place?

### Biome

What climate, terrain, natural system, or environmental condition shapes it?

### Practical Function

Why does the place exist? What do people, goods, soldiers, water, power, information, worshippers, or machinery do here?

### History

What happened here, and which older layers remain visible?

### Narrative Emotion

What should the player feel while entering, traversing, understanding, and leaving the location?

### Signature Landmark

What composition, object, structure, horizon, or environmental event makes the location memorable?

### Traversal Identity

What spatial grammar or mechanism distinguishes this location from every other map?

---

## C. Three Visible Time Layers

### 1. Original Function

What was this place originally built to do?

### 2. Transformation

How did war, Ruin, occupation, disaster, political change, religious change, abandonment, or technological failure alter it?

### 3. Current Adaptation

How do present users repair, inhabit, misunderstand, worship, exploit, fortify, or avoid it?

### Required Visual Evidence

List the materials, blocked routes, repairs, reused rooms, fortifications, ritual marks, machinery, furniture, trade, housing, defenses, or environmental changes that make all three layers visible without relying only on lore text.

---

## D. Final Fantasy VII–X Source Trace

Record which studied principles inform this map. Do not copy exact layouts or proprietary visual identity.

### FFVII Contribution

Examples: varied topology, fixed-camera fields, vertical routes, world-map landmarks, dynamic connectivity, vehicle permissions, timing hazards, changed-state revisits, final-dungeon commitment.

### FFVIII Contribution

Examples: functional architecture, institutional hub, diegetic transport, evaluated traversal, advance/evacuation reversal, synchronized operations, facility vocabulary, moving map, cross-era causality.

### FFIX Contribution

Examples: compact dense composition, layered town, rooftop or underground route, character-circumstance access, geographically grounded side events, district transit, destruction-driven topology, place-based optional activity.

### FFX Contribution

Examples: pilgrimage spine, continuous regional route, side pockets, changing spatial scale, contextual traversal verbs, rule-based temple system, late return network, three visible historical layers.

---

## E. Spatial Grammar

Select the primary and supporting structures.

- [ ] Linear infiltration
- [ ] Pilgrimage spine
- [ ] Hub-and-spoke
- [ ] Radial institutional hub
- [ ] Branch-and-rejoin
- [ ] Loop with shortcut
- [ ] Vertical climb or descent
- [ ] Gated network
- [ ] Forward advance / reverse evacuation
- [ ] Synchronized multi-route operation
- [ ] Moving-operation map
- [ ] Character-circumstance route
- [ ] Open landmark field
- [ ] Rare justified maze
- [ ] Multi-state revisit
- [ ] Cross-era causality map

### Why This Grammar Fits

Explain why the selected grammar expresses the location’s function and story.

### Route Graph

Document:

- start point;
- critical path;
- optional branches;
- branch rejoin points;
- one-way drops;
- locked or inactive links;
- mechanism-created links;
- shortcut;
- recovery point;
- boss or climax approach;
- exit;
- return or revisit routes.

Use a diagram, ASCII graph, or linked image where useful.

---

## F. Zone and Composition Plan

For every field composition or regional zone, record:

| Zone | Purpose | Camera | Elevation | Main landmark | Critical route | Optional content | Foreground/occlusion | Entry/exit |
|---|---|---|---|---|---|---|---|---|
| 1 |  |  |  |  |  |  |  |  |

### Destination Foreshadowing

Which later destination or landmark is visible before it becomes reachable?

### Scale Rhythm

Explain how narrow, broad, enclosed, vertical, social, quiet, dangerous, and spectacular spaces alternate.

---

## G. Movement and Walkmesh

### Movement Model

- camera-relative analog movement;
- acceleration target;
- deceleration target;
- maximum field speed;
- turn-blend behavior;
- any temporary context-specific speed changes.

### Walkable Surfaces

List each major surface, its elevation range, connections, and enabled states.

### Collision

Document:

- broad clean boundaries;
- wall-sliding behavior;
- decorative geometry excluded from collision;
- narrow-looking safe-lane widths;
- edge protection;
- auto-centering where appropriate;
- intentional fall points, if any.

### Stairs and Ramps

Identify all visible stairs and the smooth navigation slopes beneath them.

### Complete-Route Accessibility

Define the full end-to-end route test from spawn to objective. Component tests alone are not sufficient.

---

## H. Camera, Projection, and Transitions

For each camera:

- camera ID;
- fixed or semi-fixed type;
- position and target;
- field of view or orthographic definition;
- supported pan range;
- actor scale range;
- transition boundary;
- old and new input bases;
- blend duration;
- safe destination spawn.

### Transition Rules

Confirm:

- [ ] held input does not reverse;
- [ ] geographic direction remains understandable;
- [ ] elevation continuity is preserved;
- [ ] spawn cannot immediately retrigger the prior camera;
- [ ] local transition is as short as performance allows;
- [ ] longer fade has a dramatic or technical reason.

---

## I. Perspective, Silhouette, and Occlusion

### Actor Scaling

Describe the authored depth curve and minimum readable Cyanis scale.

### Silhouette

How do pose, hair, mantle, weapon, shoulder shape, color separation, and grounding shadow keep Cyanis readable?

### Foreground Masks

List each foreground layer and the route states in which it appears before or after Cyanis.

### Occlusion Response

Define:

- brief occlusion allowed without fade;
- partial fade threshold;
- full-obscuration silhouette threshold;
- restoration speed;
- protection against a mask remaining faded or opaque incorrectly.

---

## J. Contextual Traversal and Interaction

For every contextual action, record:

| Action | Trigger zone | Alignment anchor | Input | Animation | Walkmesh/state change | Failure behavior |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

Approved examples include ladders, mantles, marked jumps, ropes, squeezes, lifts, doors, mechanisms, designed drops, swimming transitions, boarding, and special crossings.

### Interaction Requirements

- broad proximity zone;
- clear prompt;
- automatic final alignment;
- short movement lock;
- safe orientation when control returns.

---

## K. Facility Vocabulary, Mechanisms, and Puzzles

### Local Mechanical Vocabulary

List the limited set of objects and rules the location teaches.

### Rule Introduction

Where is each rule introduced safely and clearly?

### Rule Development

How are known rules combined or transformed later?

### Spatial Consequence

For every mechanism, explain what visibly changes:

- route connectivity;
- elevation access;
- hazard state;
- lighting or power;
- water level;
- architecture;
- transport;
- shortcut;
- later historical state.

A mechanism that does not affect the map or the player’s understanding requires justification.

---

## L. Timing Hazards

For each hazard:

- visible cycle;
- warning phase;
- active phase;
- recovery phase;
- collision synchronization;
- safe pockets;
- checkpoint sequence;
- knockback or penalty;
- reset position;
- encounter-overlap rules;
- accessibility adjustment.

Confirm the challenge tests timing or route reading rather than precision steering.

---

## M. Encounters, Recovery, and Pacing

### Encounter Placement

Document visible ordinary encounters, elites, avoidance space, preparation space, and routes that must remain combat-free.

### Recovery

Identify camps, sanctuaries, secure rooms, restoration points, allied positions, or safe overlooks.

### Pacing Rhythm

Describe the sequence of danger, shelter, story, spectacle, discovery, puzzle, combat, and quiet traversal.

### Boss Approach

Explain how the final approach reduces irrelevant interruption and preserves momentum.

---

## N. Settlement and Social Use

Complete when applicable.

### Districts

Residential, market, inn, workshop, military, government, guild, research, sanctuary, industrial, agricultural, transit, hidden, rooftop, underground, or character-specific districts.

### Social Circulation

Where do merchants, guards, workers, officials, residents, travelers, refugees, and Black Host forces naturally move?

### Place-Based Optional Systems

Identify Yahtzee challengers, hunts, crafting, training, festivals, character scenes, treasure systems, or local minigames and explain why each belongs here.

### Geographically Grounded Side Events

Record optional scenes that occur elsewhere in the same location and how the player understands their spatial relationship.

---

## O. Transport and Regional Integration

### Regional Connection

How does this location connect to roads, rivers, rails, sea, air, ancient routes, or adjacent fields?

### Diegetic Transport

What transport exists visibly in the world before it becomes a transition or fast-travel option?

### Vehicle Permissions

Which vehicles or later abilities change access?

### Late Return Network

How does late-game travel make this location easier to revisit without erasing geographic understanding?

---

## P. Character-Circumstance and Multi-Party Routes

### Character-Specific Knowledge or Authority

Identify optional or authored access related to Cyanis, Ilyra, Vaelira, Seyrik, Nimera, Torren, Maevra, or Kessara.

### Party Visibility Rule

Cyanis remains the normally sole visible controllable field character. Other members appear through authored scenes, interactions, or specially designed sequences. No permanent follower train.

### Multi-Route Operation

When groups split:

- define each route’s purpose;
- define cause and effect between routes;
- identify control-switch points;
- identify the shared landmark or objective;
- define reunion and failure behavior.

---

## Q. Revisit, Destruction, and Historical Consequence

### Revisit States

For each future state, document changes to:

- route topology;
- population;
- political control;
- danger;
- services;
- mechanism state;
- environment;
- optional content;
- emotional meaning.

### Destruction

List which streets, doors, stairs, lifts, bridges, services, and safe zones physically change. A visual-only damaged reskin is insufficient.

### Cross-Era Causality

Identify earlier actions that alter later routes, rewards, machinery, records, hazards, or structural survival.

### Backtracking Reduction

Explain how solved traversal becomes shorter through shortcuts, transit, repaired links, secured roads, or disabled hazards.

---

## R. Accessibility and Navigation Support

- optional route indicators;
- interactable indicators;
- hazard warning strength;
- silhouette assistance;
- camera-motion reduction;
- timing-window adjustment;
- minimap or map support;
- high-contrast route support;
- control remapping considerations;
- protection against accidental falls or repeated failure loops.

Navigation aids support readable design rather than replacing it.

---

## S. Performance and Asset Plan

For every composition, identify:

- background resolution;
- foreground plate count;
- dynamic layers;
- animation format;
- texture-memory estimate;
- lower-resolution fallback;
- loading boundary;
- Android performance target;
- disposal and restoration behavior;
- debug overlay requirements.

---

## T. Automated Tests

Required categories:

- projection and scale;
- complete route accessibility;
- surface connectivity;
- elevation continuity;
- wall sliding;
- edge protection;
- camera-basis blend;
- held-input transition;
- interaction alignment;
- mechanism state;
- hazard timing and checkpoint reset;
- occlusion activation and restoration;
- shortcut behavior;
- save and migration where applicable;
- version, signing, and regression protection.

List exact proposed test names.

---

## U. Android Device Acceptance

The build is not accepted until the user verifies applicable items on the target phone:

- [ ] complete route can be traversed;
- [ ] movement feels responsive;
- [ ] no important connection is too narrow;
- [ ] stairs and slopes are smooth;
- [ ] wall sliding is reliable;
- [ ] camera changes do not reverse input;
- [ ] upper and lower routes remain understandable;
- [ ] Cyanis remains readable at depth;
- [ ] foreground fading behaves correctly;
- [ ] mechanisms visibly update navigation;
- [ ] hazards are readable and fair;
- [ ] shortcuts work in intended directions;
- [ ] exits and interactions are forgiving;
- [ ] performance remains stable;
- [ ] battle, menu, save, and return behavior remain intact;
- [ ] APK installs over the current stable baseline with the permanent certificate.

Record device-test findings and required corrections here.

---

## V. Standard Traceability

Every implemented principle must name the controlling standard section and its verification.

| Standard section | Requirement used | Map implementation | Automated test | Device acceptance |
|---|---|---|---|---|
|  |  |  |  |  |

### Deferred Requirements

List relevant requirements intentionally postponed and explain why.

### Conflicts or Exceptions

Document any proposed conflict with the Active Master Canon or VII–X standard. Do not silently override authority.

---

## W. Approval Record

- **Design approved:**
- **Implementation approved:**
- **Device tested:**
- **Merged baseline:**
- **Supersedes:**
- **Superseded by:**

### Final Acceptance Statement

State exactly what the approved map proves and which future maps may rely on it as a baseline.
