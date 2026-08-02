# Diyse Map and Traversal Design Standard
## Final Fantasy VII Study Consolidation Edition

**Document version:** 1.0  
**Date:** 2026-08-02  
**Status:** Authoritative project reference  
**Project:** Diyse 3D JRPG

---

## 1. Authority and Purpose

This document consolidates the complete Final Fantasy VII map-design and traversal study conducted for Diyse, including:

- the full playable-space audit from Midgar through the Northern Cave;
- the world-map and regional-access audit;
- direct study of uploaded original Final Fantasy VII gameplay footage;
- real-time movement analysis from the Junon/Fort Condor clip;
- vertical-traversal analysis from the Temple of the Ancients clip;
- design conclusions already tested in Diyse prototype versions v0.06A, v0.06B, v0.09A1, and v0.09B.

This file supersedes scattered conversational notes about Final Fantasy VII map design and traversal. Future Diyse map work should reference this file as the single consolidated standard.

This does **not** require Diyse to imitate Final Fantasy VII’s exact locations, layouts, visual identity, or technical limitations. It preserves the underlying spatial principles and adapts them into an original modern 3D JRPG.

The central lesson is:

> **Diyse should simplify physical control so its environments can appear more dangerous, layered, cinematic, and complex than the movement challenge actually is.**

Diyse is not a precision platformer and should not become an unrestricted open-world traversal game. Its exploration identity is **authored cinematic traversal with modern responsive controls**.

---

## 2. Evidence Labels

- **Observed:** directly visible in Final Fantasy VII maps or uploaded footage.
- **Inferred:** a design conclusion supported by repeated observed patterns.
- **Diyse Standard:** the binding implementation rule adopted for Diyse.
- **Prototype-Proven:** already demonstrated successfully in a Diyse prototype build.

When controller input was not recorded, conclusions about acceleration, input timing, or direction changes remain informed visual inference rather than instrumented input data.

---

## 3. Core Spatial Philosophy

### 3.1 Every Major Location Must Express Seven Things

Every major Diyse location must communicate:

1. **Culture** — who built, inhabits, controls, or remembers it.
2. **Biome** — climate, terrain, natural systems, and environmental conditions.
3. **Function** — why it exists and what people use it for.
4. **History** — what happened there and what older layers remain visible.
5. **Narrative emotion** — what the player should feel while crossing it.
6. **Signature visual idea** — the composition or landmark that makes it memorable.
7. **Traversal identity** — the route grammar or mechanism unique to the location.

No major area should exist only because the game needs another forest, cave, city, or ruin.

### 3.2 Complexity Belongs in Arrangement, Not Difficult Controls

Final Fantasy VII repeatedly creates complex-looking space from simple movement:

- layered upper and lower routes;
- fixed-camera compositions;
- narrow-looking bridges with forgiving walkable width;
- stairs implemented as smooth traversal surfaces;
- state-changing pathways;
- timing obstacles with clear safe spaces;
- contextual ladders, climbs, drops, and jumps;
- foreground objects that partially hide the character;
- route networks made readable through landmarks.

**Diyse Standard:** The challenge should usually be reading the space, choosing a route, understanding a mechanism, timing a safe movement window, or recognizing a changed map state—not fighting unstable movement physics.

---

## 4. Traversal Grammar Library

A complete game must not repeat one route structure everywhere. Final Fantasy VII’s strongest map-design lesson is the deliberate variation of spatial grammar.

### 4.1 Linear Infiltration

A directed sequence with strong forward pressure, limited detours, escalating danger, and authored story beats.

Use for military assaults, escapes, rescues, collapsing facilities, pursuit, and urgent operations.

Requirements:

- strong forward landmark;
- limited but meaningful optional rooms;
- rising tension;
- clear stage transitions;
- no unnecessary return through unchanged corridors.

### 4.2 Hub-and-Spoke

A central safe or semi-safe space connects several branches.

Use for towns, headquarters, large ruins, laboratories, prison blocks, and multi-objective dungeons.

Requirements:

- central landmark;
- branches differentiated by function, architecture, lighting, or elevation;
- completed branches visibly change state;
- later movement through the hub becomes faster.

### 4.3 Branch-and-Rejoin / Braided Route

The player chooses between route variants that reconnect later.

Use for optional rewards, alternate encounters, risk-versus-reward decisions, and party-character flavor.

Requirements:

- choices read as intentional;
- branches differ mechanically or narratively;
- the rejoin point is understandable;
- neither route feels like an accidental wrong turn.

### 4.4 Loop with Shortcut

The player travels a longer path, completes an action, then opens a shorter return connection.

Use doors opened from the far side, lifts, ladders, gates, bridges, and mechanisms.

Requirements:

- shortcut materially reduces repetition;
- opening it visibly confirms progress;
- solved traversal is not repeated at full length.

### 4.5 Vertical Climb

The route is organized around ascent or descent through layered compositions.

Use towers, cliffs, gatehouses, industrial structures, temples, mountains, and siege works.

Requirements:

- upper and lower routes remain compositionally readable;
- stairs are smooth navigation slopes;
- narrow-looking paths receive generous invisible width and edge protection;
- perspective scale and silhouette remain readable;
- camera changes never reverse held input.

### 4.6 Gated Network

Several routes are visible before a mechanism, story state, item, vehicle, or environmental change unlocks them.

Use Crest devices, ancient mechanisms, power networks, fortress gates, water controls, and late-game return access.

Requirements:

- locked route is introduced visually before activation;
- activation visibly changes the map;
- the new connection is spatially understandable;
- gating creates anticipation, not arbitrary obstruction.

### 4.7 Rare Maze

A deliberately disorienting network used only when the narrative justifies it.

Requirements:

- recognizable landmarks;
- consistent internal rules;
- no repeated identical corridors;
- no random guessing;
- no maze used merely to extend playtime.

### 4.8 Open Landmark Field

A broader area navigated by distant anchors rather than corridor walls.

Use valleys, plains, large courtyards, ruined districts, forests, and regional staging spaces.

Requirements:

- dominant landmark identifies forward progress;
- secondary landmarks indicate optional routes;
- traversable area remains authored;
- decorative openness does not imply that every visible surface is reachable.

### 4.9 Multi-Party or Dual-Route Network

Different groups traverse distinct but related routes.

Use major operations, siege sequences, rescue missions, and final-dungeon splits.

Requirements:

- each route has a distinct identity;
- actions on one route affect another;
- cause and effect are readable;
- party splits are authored events, not permanent follower simulation.

### 4.10 Multi-State Revisit

A known location returns with changed routes, population, danger, purpose, or emotional meaning.

Use occupation, liberation, war damage, natural disaster, ancient awakening, and Black Host escalation.

Requirements:

- changed state is visually immediate;
- old knowledge helps but does not solve everything;
- repeated travel is shortened or transformed;
- new routes, dialogue, hazards, objectives, or story justify the revisit.

---

## 5. Critical-Path Readability

### 5.1 Forward Route

The player should usually identify the likely forward route within a few seconds of entering a composition.

Use:

- architectural framing;
- contrast and lighting;
- bridges, stairs, doors, and roads aimed toward the next area;
- dominant landmarks;
- characters or objects near important thresholds;
- repeated motifs that connect related spaces.

### 5.2 Optional Routes

Optional branches should look intentionally secondary through smaller openings, lower contrast, visible rewards, lateral departure from the main flow, or a mechanism-dependent path.

Optional content rewards attention, not pixel hunting.

### 5.3 Exits

Use broad exit trigger zones, clear framing, safe spawn points, and automatic final alignment when necessary.

Avoid:

- tiny exit zones;
- invisible door triggers;
- background art that looks walkable but is blocked without explanation;
- important routes hidden only by low contrast.

### 5.4 Traversal Indicators

The Temple of the Ancients demonstrates that ambiguous pre-rendered routes sometimes need explicit indicators.

Use restrained indicators for:

- climbable surfaces;
- foreground-hidden paths;
- contextual drops;
- screen exits;
- interaction points;
- changed mechanism routes.

Indicators support authored art rather than replacing it.

---

## 6. Local Field Presentation Standard

### 6.1 Approved Hybrid Field Model

Local cinematic maps use:

- pre-rendered or pre-composed environmental plate;
- real-time Cyanis actor;
- authored invisible walkmesh;
- depth and perspective data;
- foreground masks or selective dynamic layers;
- authored interactions and exits;
- selective real-time effects;
- fixed or semi-fixed camera composition.

The world map remains real-time 3D.

### 6.2 Every Field Composition Requires

1. background plate;
2. walkable polygons;
3. camera orientation and projection;
4. depth and perspective behavior;
5. foreground masks;
6. exits and spawn points;
7. interactions;
8. route indicators where needed;
9. dynamic layers or effects;
10. collision safety margins;
11. contextual traversal points;
12. environmental audio identity.

### 6.3 Composition Before Simulation

The environment may depict deep drops, dense machinery, ancient mechanisms, crowds, fragile ledges, or impossible-looking architecture while the actual route remains clean and reliable.

Decorative geometry must not directly dictate collision.

---

## 7. Movement Feel

### 7.1 Responsive Camera-Relative Movement

Binding requirements:

- 360-degree analog input where appropriate;
- camera-relative movement basis;
- very short acceleration and deceleration;
- immediate directional response;
- no heavy inertia;
- no tank controls;
- no precision-platforming movement model.

Final Fantasy VII’s original movement appears nearly immediate and momentum-free. Diyse modernizes it with slight blending rather than adding substantial weight.

### 7.2 Fast Turning

Preserve rapid directional response while improving animation blending.

- short turn blends;
- minimal foot sliding;
- no waiting for a turn animation before movement;
- player intent outranks animation purity.

### 7.3 Camera-Basis Blending

When the camera changes, held input must not reverse or rotate unpredictably.

Required behavior:

- blend old and new movement basis;
- preserve intended screen direction;
- typical target around 0.2–0.3 seconds;
- prevent rapid boundary oscillation;
- use safe transition spawn points.

### 7.4 Wall Sliding

Collision redirects movement along boundaries rather than stopping the character completely.

- forgiving wall sliding;
- stable movement around corners;
- no snagging on decorative protrusions;
- no collision matching every stone, root, railing, or ornament.

### 7.5 Stairs

- navigation uses smooth slopes;
- visual step adaptation handles posture and feet;
- no physical bump for every step;
- speed remains continuous;
- camera composition sells the staircase.

### 7.6 Narrow-Looking Routes

Bridges, ledges, rails, clock hands, and ancient mechanisms may look narrow but should not require balance-beam precision.

Required behavior:

- generous invisible safe lane;
- edge protection;
- soft auto-centering where appropriate;
- authored entry alignment;
- contextual animation when useful;
- falling only when deliberately designed as a mechanic.

### 7.7 Contextual Traversal

Use authored verbs instead of universal climb-anything traversal.

Approved examples include marked jumps, ladders, mantles, squeezes, ropes, designed drops, slides, and special mechanism crossings.

These verbs should be location-specific and cinematic.

---

## 8. Perspective, Silhouette, and Occlusion

### 8.1 Perspective Scaling

- scale Cyanis by authored depth;
- transitions remain smooth;
- collision footprint and interaction range remain stable;
- distant Cyanis must not become unreadably small;
- use depth zones or continuous authored curves.

### 8.2 Strong Silhouette

Original FFVII field models remain readable at tiny sizes because of exaggerated shape and contrast.

Diyse requires a clear Cyanis silhouette through hair, mantle, weapon, shoulder shape, pose, color separation, grounding shadow, and readable run/idle states.

### 8.3 Foreground Occlusion

Use foreground masks, selective transparency, temporary fading, Cyanis silhouette support, authored camera changes, or route repositioning.

Do not flatten the environment merely to keep Cyanis visible.

### 8.4 Party Visibility

Cyanis remains the normally sole visible controllable field character.

Other permanent party members remain present in battle, menus, progression, dialogue, story scenes, authored interactions, and specially designed sequences. They do not form a permanent follower train.

---

## 9. Interaction Standard

### 9.1 Forgiving Proximity

Use broad interaction radii or cones, clear prompts, and automatic final alignment. Do not require exact facing or sub-pixel positioning.

### 9.2 Authored Alignment Sequence

1. detect Cyanis in a forgiving zone;
2. smoothly align him;
3. briefly lock movement;
4. play the action;
5. return control in a safe orientation.

### 9.3 Mechanisms Must Change Space

A meaningful mechanism should alter walkmesh connectivity, route availability, elevation access, hazard state, lighting, power, visible architecture, environmental motion, or return-route efficiency.

A mechanism should not exist only as an isolated button press.

---

## 10. Timing Hazards

The Temple rolling-boulder sequence demonstrates that the challenge can be timing movement between generous safe areas rather than difficult steering.

Diyse requirements:

- simple movement input;
- visible hazard cycle;
- generous safe pockets;
- readable checkpoint progression;
- fast reset to the last safe position;
- limited punishment;
- clear audiovisual warning;
- safe pockets outside the active hazard lane.

The v0.09B Ruin-pulse corridor is the current prototype application of this principle.

---

## 11. Dynamic Connectivity

The Temple clock mechanism demonstrates that an environmental object can become a traversable route and alter the map graph.

Diyse maps may activate, remove, rotate, flood, power, raise, lower, repair, or destroy connections.

Requirements:

- navigation graph matches the visual state;
- the player understands what changed;
- changed connectivity produces a new route, shortcut, or decision;
- complexity comes from map state, not difficult controls.

---

## 12. World Map and Regional Travel

### 12.1 Distinct Movement Mode

Local fields use authored cameras, detailed collision, contextual traversal, and dense interactions.

Regional travel uses real-time 3D, broader terrain movement, a stable camera anchor, slight look-ahead, stylized scale, broad terrain restrictions, major landmarks, and regional orientation support.

### 12.2 Screen Lock and Camera Follow

Measured from the uploaded world-map clip, Cloud remained almost fixed near the center of the screen while the terrain scrolled. During a sustained run, the measured sprite center varied only slightly.

Diyse should:

- keep the regional leader near a stable screen anchor;
- use smooth follow;
- add slight directional look-ahead;
- prioritize terrain readability over dramatic camera lag.

### 12.3 Stylized Regional Scale

The regional avatar may be intentionally oversized. Literal geographic scale is less important than readable terrain relationships and landmark recognition.

### 12.4 Broad Terrain Collision

Use forgiving terrain categories such as mountains, cliffs, forests, water, marsh, desert, passes, and vehicle-specific surfaces. Movement should slide smoothly along terrain boundaries.

### 12.5 Vehicles Change Geography Permissions

Vehicles should not merely increase speed. They change which terrain classes are traversable and which regions become reachable.

Possible permissions include shallow water, deep water, air routes, cliffs, sealed ancient roads, Ruin-contaminated regions, rivers, storms, and underground transit.

---

## 13. Settlement Design

Settlements are explorable spaces rather than menu-only stops.

Possible districts include residential, market, inn, workshop, military, government, guild, research, sanctuary, industrial, agricultural, hidden-passage, and character-specific areas.

Each settlement should have:

- dominant orientation landmark;
- readable main route;
- optional side routes;
- local shortcuts;
- social or commercial hub;
- memorable entrance composition;
- authored exit toward the next region;
- dialogue and activity that change after major events.

NPC placement should reinforce spatial function: merchants near trade routes, guards at thresholds, workers near machinery, officials in controlled districts, residents in lived-in spaces, and Black Host presence changing normal circulation.

---

## 14. Dungeon Structure and Pacing

A major dungeon generally targets 45–90 minutes and may include:

1. memorable entrance;
2. initial statement of place and threat;
3. central environmental mechanic;
4. connected route network;
5. optional rooms and rewards;
6. midpoint recovery or shelter;
7. story discovery;
8. elite or miniboss escalation;
9. clear boss approach;
10. final boss or climax;
11. clear exit, return route, or state change.

This is a framework, not an identical formula.

### 14.1 Alternating Rhythm

Alternate danger, shelter, spectacle, quiet, puzzle, story, encounter pressure, open travel, and dense interior space.

Avoid long stretches of maps with the same emotional and mechanical intensity.

### 14.2 Puzzle Integration

Puzzles should alter or explain the environment: rotate a bridge, reroute power, open a Crest path, manipulate water, align ancient architecture, predict an entity’s route, change elevation, disable a hazard, create a shortcut, or reveal history.

Avoid detached puzzles with no spatial consequence.

### 14.3 Backtracking Rule

When an earlier section changes, open a shortcut, lift, new route, safe return, or altered encounter state. Do not require excessive unchanged backtracking.

---

## 15. Encounter and Recovery Placement

Final Fantasy VII often uses random encounters, but Diyse adapts the map lessons to visible encounters.

- place encounters in authored spaces;
- allow deliberate preparation or avoidance where appropriate;
- make elites identifiable;
- respect route width and camera composition;
- do not continuously respawn enemies in a cleared section;
- place recovery points to create meaningful decisions;
- protect boss approaches from irrelevant interruption;
- do not overlap ordinary encounters unfairly with timing hazards.

Recovery spaces may be sanctuaries, camps, secure rooms, ancient restoration chambers, allied positions, field stations, or safe overlooks.

---

## 16. Revisits and Backtracking

A return should introduce changed purpose through new story, altered political control, damage, reconstruction, environmental change, new access, enemy ecology, party scenes, mechanisms, or high-level content.

The player’s memory of the old map should help, but a revisit should not be a full unchanged replay.

Possible changed-state navigation:

- destroyed wall replaces a corridor;
- occupation changes legal routes;
- repaired lift creates a shortcut;
- flooding opens boat access and closes lower paths;
- Ruin corruption changes safe zones;
- allied forces secure an old combat area.

---

## 17. Optional Areas and Secrets

Strong optional areas may be short, dangerous, vehicle-gated, character-linked, geographically hidden, mechanically singular, and high-reward.

Secrets should reward environmental understanding, route-state memory, vehicle permissions, visible inaccessible landmarks, unusual composition, cultural clues, or NPC information.

Avoid arbitrary invisible walls, random button presses, featureless maze searching, and secrets impossible to infer without external knowledge.

---

## 18. Final-Dungeon Standard

The Northern Cave provides several enduring principles.

### 18.1 Dramatic but Reversible Entry

The player may enter and explore before committing permanently.

### 18.2 Chosen Checkpoint

Allow the player to establish a meaningful recovery point within the final descent or network.

### 18.3 Distinct Split Routes

Party-split routes should differ in environment, enemies, rewards, mechanics, story tone, and party suitability.

### 18.4 Reunion

Split routes reconnect in a clearly understood reunion space.

### 18.5 Explicit Point of No Return

The irreversible final transition must be clearly communicated. Never hide it behind an ordinary-looking doorway or interaction.

### 18.6 Final Approach

Reduce irrelevant navigation friction, escalate visual and musical identity, allow final preparation, preserve narrative momentum, and avoid random interruption at the emotional climax.

---

## 19. Location-Level FFVII Synthesis

### Midgar

- layered industrial geography creates identity;
- sectors can share one city while feeling culturally and functionally different;
- linear infiltration improves when punctuated by small hubs and side rooms;
- visible vertical infrastructure implies a larger world beyond the route;
- revisits gain power through changed state and emotional meaning;
- escapes compress choice and increase forward pressure.

### Early World Map

- landmarks guide regional travel;
- terrain barriers teach world rules;
- dangerous regions may be visible before safe passage is possible;
- mines, marshes, mountains, and crossings create natural progression gates;
- broad travel should alternate with dense authored fields.

### Junon

- one location can contain radically different vertical social layers;
- hidden settlement and military superstructure can occupy the same geography;
- event spaces may temporarily replace ordinary traversal;
- lifts and transitions compress huge scale.

### Corel and Gold Saucer Region

- tonal contrast between adjacent areas strengthens both;
- transit sequences bridge radically different identities;
- settlements can embody historical consequences;
- entertainment spaces can function as multi-activity hubs.

### Cosmo Canyon and Nibelheim

- settlements can be organized around vertical landmarks;
- culture and history should be embedded in traversal;
- familiar-looking geography can create unease when details contradict memory;
- interiors can reinforce hierarchy and hidden history.

### Temple of the Ancients

- vertical complexity can use ordinary running over forgiving walkmeshes;
- layered routes remain readable through fixed-camera composition;
- foreground occlusion adds depth when supported by visibility systems;
- map objects can become bridges;
- timing hazards need generous safe pockets;
- route prediction can be a puzzle without difficult controls;
- route indicators are appropriate when art alone is ambiguous.

### Forgotten Capital and Northern Regions

- composition can communicate sacredness, grief, isolation, and disorientation;
- unusual architecture remains navigable through consistent visual rules;
- narrative tension may justify reduced optionality;
- dangerous routes still need landmarks and readable exits.

### Highwind and Late-Game Access

- a mobile headquarters changes pacing and world orientation;
- aerial access creates a parallel geography of optional destinations;
- late travel should reveal earlier visible but unreachable spaces;
- revisits should be selected for changed purpose, not repetition.

### Vehicle-Gated Optional Areas

- optional discoveries can come from geography rather than quest lists;
- isolated, underwater, forest, or island areas test world-map mastery;
- optional locations benefit from one strong identity and high-value rewards.

### Return to Midgar

- major revisits should use changed stakes, access, routes, and meaning;
- familiar geography supports climax without requiring full repetition;
- return routes emphasize urgency and purpose.

### Northern Cave

- final regions can support reversible exploration before commitment;
- branch selection creates party and reward decisions;
- split routes need distinct identity;
- a chosen checkpoint reduces frustration;
- the final point of no return must be explicit.

---

## 20. Transition Standard

Measured from the uploaded Fort Condor clip:

- fade begins around 561.8 seconds;
- full black around 562.3 seconds;
- fade-in begins around 564.2 seconds;
- the next screen is clearly visible around 564.6 seconds.

That is roughly 2.8 seconds from fade start to visibility, with about 1.9 seconds near total black.

Diyse should preserve strong spatial editing without copying long loading darkness.

Targets:

- local camera blend: about 0.15–0.35 seconds;
- local composition transition: about 0.35–0.7 seconds when performance allows;
- longer fades only for narrative tone, major location change, or technical necessity;
- safe, readable destination spawn.

Transitions preserve intended travel direction, logical entrance/exit relation, important elevation, camera-basis continuity, destination readability, and player-control expectations.

Perfect geometric continuity is not required when the spatial edit is understandable.

---

## 21. Anti-Patterns

Do not copy:

- long black loading transitions;
- binary idle/run presentation without modern blending;
- abrupt pivots with severe foot sliding;
- held-direction reversal after camera changes;
- decorative geometry used as exact collision;
- narrow-looking routes requiring precision steering;
- invisible paths without indicators or compositional clues;
- repeated unchanged backtracking;
- frequent random interruption of traversal;
- permanent follower trains;
- compositions that hide Cyanis without silhouette support;
- one spatial grammar repeated across the whole game;
- open-world scale without authored purpose;
- universal climbing that makes architecture meaningless;
- locations that exist only as biome containers;
- unclear final points of no return.

---

## 22. Binding Diyse Requirements

Future playable prototypes and production maps must preserve:

1. responsive camera-relative analog movement;
2. very short acceleration and deceleration;
3. fast turning with improved animation blending;
4. fixed or semi-fixed authored cameras for cinematic zones;
5. smooth input-basis blending across camera changes;
6. clean authored walkable lanes;
7. forgiving wall sliding;
8. stairs implemented as smooth navigation slopes;
9. perspective scaling across depth;
10. strong Cyanis silhouette readability;
11. foreground occlusion with transparency or silhouette support;
12. generous edge protection on narrow-looking routes;
13. contextual traversal rather than precision platforming;
14. readable critical path and intentional optional branches;
15. broad interaction and exit zones;
16. automatic final alignment for authored actions;
17. dynamic connectivity for mechanisms and state changes;
18. timing hazards built around readable cycles and safe pockets;
19. distinct local-field and regional-travel movement modes;
20. vehicles that change terrain permissions;
21. multi-state revisits with changed purpose and shorter return travel;
22. explicit final-dungeon commitment;
23. Cyanis as the sole normally visible controllable field character;
24. no permanent follower train;
25. traversal presentation remaining independent from combat, Card, progression, menu, and save systems.

---

## 23. Prototype-Proven Elements

### v0.06A

Proved fixed-camera courtyard exploration, low-poly Cyanis, four-direction movement, perspective scaling, walkmesh collision, edge sliding, foreground masking, interactions, and battle triggering.

### v0.06B

Proved improved depth-aware movement, masking, contextual interaction presentation, environmental polish, Cyanis-only normal exploration, and no follower logic.

### v0.09A1

Accepted as the stable traversal baseline, proving responsive camera-relative traversal, authored walkmesh, calibrated camera transitions, route accessibility, and regression-safe integration.

### v0.09B

Implements seven connected gatehouse compositions, layered vertical routes, a Crest mechanism, mechanism-controlled bridge connectivity, protected upper crossing, Ruin-pulse timing corridor, safe pockets, checkpoint reset, summit gate, and two-way return shortcut.

---

## 24. Map Review Checklist

### Identity

- What culture does the location express?
- What is its function?
- What historical layer is visible?
- What narrative emotion defines it?
- What is its signature visual idea?
- What is its traversal identity?

### Topology

- What spatial grammar is used?
- Where is the critical path?
- Which branches are optional?
- Where do routes reconnect?
- Is there a shortcut?
- Is repeated travel changed or shortened?
- Are one-way drops and irreversible transitions clear?

### Camera and Readability

- Is the forward route readable within a few seconds?
- Do camera changes preserve input intent?
- Are upper and lower paths distinguishable?
- Are exits framed?
- Does perspective scaling remain readable?
- Can Cyanis become hidden?
- Is silhouette or foreground fading available?

### Movement and Collision

- Are walkable lanes clean?
- Does wall sliding work?
- Are stairs smooth slopes?
- Are narrow routes forgiving?
- Are edge protections present?
- Are contextual actions aligned automatically?
- Does any section accidentally require precision platforming?

### Mechanisms and Hazards

- Does the mechanism visibly change the space?
- Does the navigation graph match the visual state?
- Is the timing cycle readable?
- Are safe pockets generous?
- Is reset quick and fair?
- Does challenge come from understanding or timing rather than unstable controls?

### Pacing

- Is there variation between tension and shelter?
- Are encounters deliberately placed?
- Is there a recovery opportunity where appropriate?
- Does the boss approach preserve momentum?
- Does the return route respect the player’s time?

### World Integration

- Does the location connect logically to regional geography?
- Can later vehicles or story states reveal new access?
- Would a revisit meaningfully change the space?
- Is optional content hinted before it becomes reachable?
- Does the map support the larger journey rather than existing in isolation?

---

## 25. Final Design Rule

When choosing between visual drama and movement difficulty:

- make the environment look dramatic;
- make the route authored;
- make the controls responsive;
- make collision forgiving;
- make the player’s intention clear;
- make challenge come from spatial understanding, state change, timing, or decision-making.

> **Diyse environments may look perilous, ancient, layered, and cinematic while remaining comfortable and reliable to traverse.**
