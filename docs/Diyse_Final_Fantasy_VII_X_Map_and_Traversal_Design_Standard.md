# Diyse Map and Traversal Design Standard
## Final Fantasy VII–X Study Consolidation Edition

**Document version:** 2.0  
**Date:** 2026-08-02  
**Status:** Authoritative project reference  
**Project:** Diyse 3D JRPG

---

## 1. Authority and Purpose

This document consolidates the approved map-design and traversal lessons drawn from **Final Fantasy VII, Final Fantasy VIII, Final Fantasy IX, and Final Fantasy X** for use in Diyse.

It includes:

- the complete FFVII playable-space and world-map audit;
- direct FFVII gameplay-footage study covering regional movement, fixed-camera fields, vertical traversal, mechanisms, transitions, occlusion, and timing hazards;
- FFVIII lessons on functional architecture, institutional hubs, transportation networks, evaluated traversal, moving operations, cross-era causality, synchronized party routes, and consistent facility mechanics;
- FFIX lessons on compact dense compositions, character-circumstance routes, layered towns, rooftops, underground spaces, spatial storytelling, district transit, contextual traversal, destruction-driven topology changes, and place-based optional systems;
- FFX lessons on the pilgrimage spine, continuous regional routing, side pockets, changing spatial scale, contextual traversal verbs, the airship’s conversion of a linear journey into a return network, and the three visible time layers of a location;
- the combined binding map and traversal standards for Diyse;
- prototype-proven implementation rules from v0.06A, v0.06B, v0.09A1, and v0.09B.

This file supersedes the earlier FFVII-only consolidation and all scattered conversational notes about FFVII–FFX map design. Future Diyse field, settlement, dungeon, regional-map, vehicle, revisit, and final-dungeon work should cite this file as the single authoritative standard.

Diyse must not copy the exact locations, layouts, puzzles, visual identities, or technical limitations of these games. It adapts the underlying design principles into an original modern 3D JRPG.

> **Diyse should make the world look layered, dangerous, historical, and cinematic while keeping ordinary movement responsive, authored, and forgiving.**

---

## 2. Evidence Labels

- **Observed:** directly visible in the studied game, map, or uploaded footage.
- **Inferred:** a design conclusion supported by repeated observed patterns.
- **Diyse Standard:** a binding rule adopted for Diyse.
- **Prototype-Proven:** successfully demonstrated in a Diyse prototype build.

Where controller input was not recorded, acceleration, deceleration, and input-timing conclusions remain visual inference rather than instrumented input data.

---

## 3. Cross-Series Synthesis

The four games emphasize different strengths:

- **FFVII:** varied topology, landmark-led regional travel, layered pre-rendered fields, dynamic connectivity, vehicle permissions, meaningful revisits, optional geographic discovery, and final-dungeon commitment structure.
- **FFVIII:** locations designed as functioning systems, recurring institutional hubs, diegetic transport, missions that evaluate traversal competence, synchronized operations, moving maps, and actions whose consequences appear across time.
- **FFIX:** compact spatial density, strong screen composition, towns layered vertically and socially, route changes caused by character circumstances, environmental storytelling through nearby simultaneous events, and optional systems rooted in places.
- **FFX:** a directed pilgrimage that still feels varied through rhythm and scale, continuous regional routes, clear critical paths with side pockets, contextual movement verbs, visible historical layers, and a late-game travel system that converts the linear journey into a return network.

Combined Diyse principle:

> **Every location must be a place, a route, a system, and a piece of history at the same time.**

A Diyse map should communicate:

1. who built or controls it;
2. what natural environment shaped it;
3. what practical function it serves;
4. what older use or event remains visible;
5. what the player should feel while crossing it;
6. what landmark makes it memorable;
7. what traversal grammar makes it distinct;
8. what changes after the player acts there.

---

# Part I — Final Fantasy VII Lessons

## 4. FFVII Core Contribution

FFVII demonstrates how a game can vary traversal structure constantly while retaining very simple movement.

Its strongest lessons include:

- linear infiltration;
- small hubs and branching interiors;
- loop-and-shortcut dungeons;
- vertical climbs;
- state-changing mechanisms;
- world-map landmark navigation;
- terrain-gated regional access;
- vehicles that change geography permissions;
- multi-state revisits;
- optional areas discovered through geography;
- split-route final-dungeon structure;
- explicit commitment before the final descent.

### 4.1 Complexity in Arrangement, Not Controls

FFVII often presents:

- layered upper and lower paths;
- stairs drawn as detailed structures but traversed as smooth slopes;
- narrow-looking bridges with forgiving walkable width;
- paths hidden behind foreground architecture;
- route-changing machinery;
- timing hazards with clear safe zones;
- contextual ladders, drops, climbs, and jumps.

**Diyse Standard:** ordinary exploration challenge comes from reading the map, understanding a mechanism, selecting a route, recognizing a changed state, or timing movement—not from unreliable movement physics.

## 5. FFVII Field Movement and Camera Findings

### 5.1 Responsive Movement

The uploaded FFVII footage showed near-immediate movement and stopping. Diyse modernizes this with very short acceleration and deceleration rather than heavy inertia.

Required:

- camera-relative analog movement;
- immediate directional intent;
- fast turning;
- short animation blends;
- minimal foot sliding;
- no tank controls;
- no precision-platforming model.

### 5.2 Camera-Basis Blending

When fixed-camera orientation changes, held input must not reverse.

Required:

- preserve intended screen-space direction;
- blend old and new movement basis over roughly 0.2–0.3 seconds;
- prevent rapid camera-boundary oscillation;
- use safe transition spawn areas.

### 5.3 Walkmeshes and Collision

- decorative geometry does not define exact collision;
- stairs are smooth navigation slopes;
- wall sliding redirects movement instead of stopping it;
- narrow-looking routes receive generous invisible safe lanes;
- ordinary ledges use edge protection;
- accidental falls do not occur unless intentionally authored.

### 5.4 Perspective and Occlusion

- Cyanis scales smoothly with depth;
- minimum readable size is enforced;
- strong silhouette matters more than physical scale accuracy;
- foreground masks add depth;
- selective transparency or silhouette support activates when Cyanis is substantially hidden;
- environmental composition should not be flattened merely to keep the actor visible.

## 6. FFVII World Map and Regional Travel

The world-map clip showed Cloud held near a stable screen anchor while terrain scrolled.

Diyse regional movement should use:

- real-time 3D terrain;
- stable central camera follow;
- slight directional look-ahead;
- broad forgiving terrain collision;
- stylized avatar scale;
- landmark-led orientation;
- terrain categories rather than collision matching every visual detail.

Vehicles must change terrain permissions, not merely speed. They may unlock shallow water, deep water, air routes, sealed ancient roads, cliffs, rivers, storms, underground transit, or Ruin-contaminated regions.

## 7. FFVII Dynamic Connectivity and Timing

The Temple of the Ancients demonstrates:

- environmental objects becoming bridges;
- navigation graphs changing after mechanisms activate;
- upper and lower routes overlapping visually while remaining mechanically separate;
- timing challenges based on safe pockets rather than steering precision;
- route prediction as a spatial puzzle;
- traversal indicators when artwork alone is ambiguous.

**Diyse Standard:** meaningful mechanisms alter connectivity, elevation, hazard state, route efficiency, or visible architecture.

## 8. FFVII Revisits, Optional Areas, and Final Structure

### Revisits

A return must change purpose through story, occupation, damage, reconstruction, new routes, environmental change, or high-level content.

### Optional areas

Secrets should be hinted through visible inaccessible landmarks, terrain permissions, unusual geography, NPC information, vehicle access, or remembered route states.

### Final dungeon

- entry may remain reversible before final commitment;
- a chosen checkpoint can reduce frustration;
- split routes should differ in enemies, rewards, environment, and party suitability;
- routes reconnect clearly;
- the irreversible point must be explicit;
- final approach should reduce irrelevant navigation friction.

---

# Part II — Final Fantasy VIII Lessons

## 9. FFVIII Core Contribution: Architecture as a Functioning System

FFVIII’s strongest map lesson is that spaces often explain how an institution, city, mission, vehicle, or facility actually works.

Architecture is not decorative scenery placed around a route. The route is created by the function of the place.

Examples from the study:

- Balamb Garden as a radial educational and military institution;
- Dollet as a forward combat advance followed by reverse evacuation;
- train infiltration as movement through an active transportation system;
- Deling City using buses to compress a larger urban district network;
- the assassination operation using synchronized routes and positions;
- sewer movement using repeated wheels, gates, ladders, and water-control logic;
- Centra excavation actions producing consequences visible later in Lunatic Pandora.

**Diyse Standard:** before designing a route, define what the place does, who operates it, what systems connect its parts, and what happens when those systems fail.

## 10. Recurring Institutional Hubs

Balamb Garden demonstrates the value of a hub that is both geographically understandable and narratively evolving.

A major recurring Diyse hub should have:

- a dominant central landmark;
- radial or strongly legible district organization;
- practical institutional functions;
- clear transit between major areas;
- changing NPC populations and access permissions;
- visible consequences after story events;
- new conversations, routes, damage, repairs, or operational states;
- reasons to revisit without replaying identical navigation.

A hub should become more familiar and faster to navigate over time while gaining new meaning.

## 11. Diegetic Transportation Networks

FFVIII repeatedly uses transport as map structure:

- trains;
- buses;
- cars;
- lifts;
- mobile bases;
- military transfer routes;
- regional road and rail logic.

Diyse should use transport to:

- compress distance without breaking world logic;
- connect districts that would be tedious to cross literally;
- create infiltration or defense sequences;
- establish class, military, or political control;
- reveal how goods, soldiers, officials, and civilians move;
- change access after occupation, sabotage, repair, or liberation.

Transport should be visible in the environment before it becomes a menu or transition.

## 12. Evaluated Traversal

Dollet demonstrates that a mission can evaluate whether the player understands route reading, forward momentum, objective order, and retreat under pressure.

Diyse may use evaluated traversal in:

- military examinations;
- Crest Knight trials;
- timed evacuations;
- reconnaissance;
- pursuit;
- rescue;
- coordinated assaults;
- escape from a changing map.

Evaluation must judge understandable decisions, not arbitrary hidden scoring or difficult steering.

Possible criteria:

- reaching objectives in sensible order;
- protecting civilians or allies;
- opening shortcuts;
- noticing optional intelligence;
- avoiding unnecessary delay;
- responding correctly when the route changes.

## 13. Forward Advance and Reverse Evacuation

FFVIII’s Dollet structure shows how the same geography can support two different experiences:

- the initial advance emphasizes discovery and objective pressure;
- the return emphasizes urgency, pursuit, and route memory.

Diyse may reuse a route in reverse only when:

- threat state changes;
- shortcuts or barriers change;
- pacing accelerates;
- landmarks gain new meaning;
- the player’s prior knowledge materially helps.

An unchanged backtrack is not equivalent to an authored evacuation.

## 14. Synchronized Multi-Route Operations

The Deling City assassination demonstrates coordinated routes that converge on one objective.

Diyse multi-party operations should:

- give each group a distinct spatial role;
- show how one route affects another;
- establish shared timing or causal relationships;
- use converging landmarks;
- preserve authored party splits rather than permanent follower simulation;
- clearly communicate when control changes between groups.

Possible Diyse applications:

- one team disables a ward while another reaches a gate;
- one party holds an upper bridge while another crosses below;
- one route opens power or transit for another;
- Cyanis’s group responds to consequences created elsewhere.

## 15. Consistent Mechanical Vocabulary per Facility

FFVIII’s sewer sequence reuses a small set of mechanisms—wheels, gates, ladders, water routes—so the player learns a local language.

**Diyse Standard:** each facility or dungeon should establish a limited mechanical vocabulary and develop it rather than introducing unrelated gimmicks in every room.

A location might be built around:

- Crest locks and rotating bridges;
- pressure doors and counterweights;
- water channels and sluice gates;
- lifts and maintenance rails;
- mirrors and light conduits;
- ward pylons and sanctuary fields;
- Ruin growth and cleansing nodes.

Later rooms should combine or transform known rules.

## 16. Moving-Operation Maps

FFVIII demonstrates that a map can itself move or operate:

- trains continue along a route;
- mobile structures change location;
- bases can travel;
- mission spaces may have an external timeline.

Diyse may use:

- moving fortresses;
- river vessels;
- airborne platforms;
- convoy assaults;
- ancient walking mechanisms;
- elevators crossing multiple playable states;
- siege engines whose operation changes available paths.

The player should understand what is stationary, what is moving, and how movement affects exits, hazards, or timing.

## 17. Cross-Era Causality

The Centra excavation and later Lunatic Pandora relationship demonstrates a powerful principle: actions in an earlier era can alter the layout, hazards, or rewards encountered much later.

Diyse can use historical or memory sequences where actions affect:

- later-open or blocked routes;
- preserved items;
- damaged structures;
- enemy access;
- machinery state;
- records or evidence;
- which shortcuts remain usable.

Cross-era consequences must be readable and authored, not based on obscure unknowable flags.

## 18. Plans Disrupted by Character Behavior

FFVIII frequently places formal operations inside spaces whose outcomes are changed by personalities, mistakes, loyalties, fear, or improvisation.

Diyse maps should allow narrative character behavior to alter route structure:

- an ally opens the wrong gate;
- a civilian crowd blocks the planned route;
- a party member chooses a rescue detour;
- betrayal changes access permissions;
- a mechanism activates earlier than intended;
- a supposedly controlled operation becomes an escape.

The map should express the narrative disruption rather than merely reporting it in dialogue.

---

# Part III — Final Fantasy IX Lessons

## 19. FFIX Core Contribution: Compact Density and Character-Circumstance Routes

FFIX demonstrates how small or moderate screens can feel rich through layered composition, social detail, verticality, strong landmarks, and route changes tied to the current character and situation.

A route may differ because:

- the controlled character has different social access;
- a festival, performance, siege, evacuation, or investigation changes circulation;
- rooftops, alleys, towers, underground passages, and district transit connect the same settlement differently;
- story events temporarily open or close routes;
- nearby events are shown from other characters’ perspectives.

**Diyse Standard:** map access can reflect character circumstance, social role, disguise, authority, danger state, or current objective without requiring a completely separate map.

## 20. Compact, Dense Field Compositions

FFIX often achieves richness without enormous continuous spaces.

A strong compact screen can contain:

- one dominant landmark;
- a clear exit;
- an optional side path;
- a foreground layer;
- NPC activity;
- a vertical clue;
- environmental storytelling;
- a transition toward another district.

Diyse should not equate quality with physical size. Several carefully composed screens may produce a stronger city or dungeon than one oversized empty space.

## 21. Layered Towns

FFIX towns frequently combine:

- streets;
- plazas;
- rooftops;
- towers;
- shops and homes;
- underground passages;
- airship or district transit;
- theatrical, political, religious, or commercial spaces.

Diyse settlements should use vertical and social layering:

- official routes versus servant or maintenance routes;
- public squares versus private courts;
- wealthy upper districts versus working lower districts;
- fortified gates versus hidden passages;
- rooftops and balconies used during pursuit or infiltration;
- old foundations beneath newer construction.

The city’s hierarchy should be visible in how people move through it.

## 22. Spatial Storytelling Through Simultaneous Events

FFIX’s Active Time Event approach shows that optional scenes can reveal what other characters are doing elsewhere in the same location.

Diyse does not need to copy the ATE interface, but it should use the principle:

- entering a district may unlock an optional scene in another nearby district;
- party members may briefly separate for authored personal events;
- NPC reactions can reveal consequences beyond Cyanis’s immediate view;
- multiple small scenes can make a settlement feel active rather than frozen around the protagonist.

These events should be geographically grounded. The player should understand where the scene occurs and how it relates to the surrounding map.

## 23. District Transit and Spatial Compression

FFIX uses lifts, gates, air cabs, boats, stairs, and district transitions to imply cities larger than the directly traversable area.

Diyse may compress city scale through:

- lifts;
- trams;
- ferries;
- stair towers;
- gate tunnels;
- guarded transfers;
- short transition corridors;
- authored camera cuts.

Compression is acceptable when entrances, exits, elevation, and district relationships remain understandable.

## 24. Contextual Traversal and Temporary Routes

FFIX’s traversal is strongly authored rather than universal.

Appropriate Diyse verbs include:

- climbing a marked ladder;
- crossing a roof beam;
- squeezing through a damaged wall;
- using a rope or lift;
- descending through a well or shaft;
- boarding a vessel;
- using a temporary siege route;
- following a character-specific shortcut.

A route may exist only during a specific story state when that temporariness is clear.

## 25. Destruction Changes Topology

FFIX repeatedly allows war, collapse, attack, or catastrophe to transform known places.

Diyse destruction should change:

- available streets;
- vertical access;
- population movement;
- safe zones;
- shops and services;
- shortcuts;
- enemy entry routes;
- landmarks;
- emotional tone.

A destroyed location should not simply reuse the intact map with darker lighting. Damage must affect circulation and meaning.

## 26. Character-Circumstance Routes

Different characters or states may reveal different navigation possibilities.

Diyse may use:

- Cyanis receiving formal access as a Crest Knight;
- Seyrik recognizing Black Host infrastructure;
- Ilyra gaining access to warded sanctuaries;
- Kessara operating machinery routes;
- Nimera interpreting Diysean Card or seal systems;
- Torren knowing old defensive passages;
- Maevra using military authority;
- Vaelira detecting elemental pathways.

These should appear through authored sequences or optional interactions. Cyanis remains the normally sole visible controllable field character.

## 27. Place-Based Optional Systems

FFIX embeds optional activity in recognizable places rather than separating everything into abstract menus.

Diyse optional systems should belong somewhere:

- town Yahtzee challengers in inns, plazas, guild halls, or homes;
- crafting in workshops;
- hunts posted and discussed in settlements;
- excavation or treasure systems tied to geography;
- character scenes tied to meaningful locations;
- minigames connected to festivals, training grounds, trade routes, or local culture.

The place should explain why the activity exists and why its rewards matter.

## 28. Emotional Route Transformation

FFIX frequently changes the emotional meaning of familiar movement:

- a celebratory square becomes an evacuation route;
- a home becomes a ruined memory;
- a theatrical or civic space becomes a battlefield;
- an ordinary street becomes a farewell path.

Diyse revisits should use the player’s memory of earlier traversal to create emotional contrast.

---

# Part IV — Final Fantasy X Lessons

## 29. FFX Core Contribution: The Pilgrimage Spine

FFX demonstrates that a directed journey can feel varied and expansive without becoming open world.

The recurring structure is:

1. settlement, arrival, or social space;
2. road, wilderness, or transitional region;
3. rest point, story scene, or party conversation;
4. temple, major objective, or confrontation;
5. departure toward the next region.

This creates a clear geographic and emotional spine.

**Diyse Standard:** a directed main journey may remain highly authored while feeling free through changing route rhythm, scale, environmental identity, optional pockets, and later return access.

## 30. Continuous Regional Routes

FFX often connects settlements and objectives through sequences of adjacent regional maps rather than jumping immediately between disconnected nodes.

Diyse should use continuous regional routes when the journey itself matters:

- roads show changing culture and terrain;
- party conversations can occur during travel;
- landmarks foreshadow the destination;
- travelers, patrols, refugees, merchants, and local threats establish world conditions;
- transitions preserve geographic direction.

Continuous routes do not require literal scale. They require believable spatial progression.

## 31. Side Pockets Along a Directed Path

FFX’s linear routes frequently contain optional side spaces for treasure, NPCs, secrets, combat, or small environmental discoveries.

Diyse main routes should include:

- short lateral branches;
- visible optional rewards;
- small overlooks;
- alternate encounter pockets;
- contextual conversations;
- hidden but inferable paths;
- later-unlockable side access.

The critical path remains clear. Optionality comes from pockets rather than requiring a sprawling open field.

## 32. Changing Spatial Scale and Rhythm

FFX alternates:

- narrow paths;
- broad roads;
- settlement plazas;
- temple interiors;
- large scenic overlooks;
- underwater sections;
- enclosed ruins;
- open plains.

Diyse should vary scale deliberately:

- narrow sections create focus or tension;
- broad spaces create relief, spectacle, or choice;
- compact interiors intensify story or puzzle focus;
- open landmark fields restore orientation;
- route width and camera distance should change pacing.

A directed route becomes monotonous only when its visual and mechanical rhythm does not change.

## 33. Authored Camera Spectacle

FFX uses controlled cameras to reveal destinations, environmental scale, and narrative landmarks.

Diyse fixed and semi-fixed fields should:

- introduce the next objective visually before arrival;
- show upper and lower route relationships;
- reveal major landmarks through composition;
- use camera changes to create scale, not to disorient;
- preserve movement intent across transitions;
- frame rest points and story beats distinctly from ordinary travel.

## 34. Contextual Traversal Verbs

FFX supports varied movement without becoming a universal platformer.

Observed or derived verbs include:

- swimming and diving;
- climbing marked surfaces;
- designated jumps;
- moving sphere or pedestal mechanisms;
- chocobo riding;
- shoopuf travel;
- lifts and moving platforms;
- teleporters;
- lightning or environmental timing hazards.

Diyse should use location-specific traversal verbs that are authored, readable, forgiving, and mechanically meaningful.

## 35. Temples as Rule-Based Spatial Systems

FFX temple trials establish a local set of objects and rules, then require the player to manipulate space through them.

Diyse temple, sanctuary, or ancient-facility puzzles should:

- introduce the local vocabulary clearly;
- connect puzzle state to doors, platforms, light, wards, or routes;
- keep carried or inserted objects readable;
- avoid arbitrary combinations unrelated to the environment;
- alter the map graph visibly;
- use known rules in increasingly complex combinations.

## 36. The Airship Converts a Line into a Network

FFX’s airship changes the earlier pilgrimage from a one-direction sequence into a return-access network.

Diyse’s late-game travel system should:

- make earlier locations quickly revisitable;
- unlock optional destinations;
- reveal hidden coordinates, routes, or passwords through clues;
- support party and personal quests;
- reduce repeated regional travel without erasing world geography;
- allow the player to prepare before final commitment.

Late travel should reinterpret the journey rather than merely provide a menu of old locations.

## 37. Three Visible Time Layers

The FFX-derived historical framework for Diyse requires every major location to show three layers:

1. **Original function** — what the location was built to do.
2. **Transformation** — how war, Ruin, occupation, disaster, religious change, or political change altered it.
3. **Current adaptation** — how present users repair, misunderstand, worship, exploit, inhabit, or avoid it.

These layers should be visible through:

- materials;
- blocked and repaired routes;
- reused rooms;
- added fortifications;
- ritual markings;
- abandoned machinery;
- changed water or power systems;
- damaged landmarks;
- current furniture, trade, housing, or defenses.

History must be spatial, not confined to lore text.

## 38. Clear Direction with Navigation Support

FFX demonstrates that clear direction does not eliminate exploration.

Diyse may use:

- strong landmark direction;
- map or minimap support;
- route indicators when compositions are ambiguous;
- named regional segments;
- visible side-pocket entrances;
- destination framing.

Navigation aids should confirm readable design rather than rescue unreadable maps.

---

# Part V — Combined Diyse Standards

## 39. Traversal Grammar Library

Every major location should deliberately choose one or more route grammars.

### 39.1 Linear Infiltration

Forward pressure, limited detours, escalating danger, and authored story beats.

### 39.2 Pilgrimage Spine

Settlement → travel route → rest/story space → major objective → departure.

### 39.3 Hub-and-Spoke

A central landmark connects distinct branches whose states evolve.

### 39.4 Radial Institutional Hub

A recurring functional organization surrounds a strong center and becomes faster to navigate over time.

### 39.5 Branch-and-Rejoin

Meaningful alternate routes reconnect later.

### 39.6 Loop with Shortcut

A longer route opens a materially shorter return path.

### 39.7 Vertical Climb

Layered ascent or descent through stairs, bridges, lifts, shafts, and authored cameras.

### 39.8 Gated Network

Visible routes unlock through mechanisms, story states, equipment, vehicles, authority, or historical actions.

### 39.9 Forward Advance / Reverse Evacuation

The same geography gains urgency and altered rules on the return.

### 39.10 Synchronized Multi-Route Operation

Different groups take distinct routes whose actions affect one another.

### 39.11 Moving-Operation Map

The environment, vehicle, fortress, convoy, or platform changes position or operating state while traversed.

### 39.12 Character-Circumstance Route

Access changes because of identity, authority, knowledge, disguise, party ability, or narrative condition.

### 39.13 Open Landmark Field

A broad authored area navigated by visual anchors.

### 39.14 Rare Maze

Used only when disorientation is narratively justified and supported by landmarks and consistent rules.

### 39.15 Multi-State Revisit

A known place returns with changed routes, population, danger, function, or emotional meaning.

### 39.16 Cross-Era Causality Map

Actions in an earlier historical sequence alter a later version of the same place.

## 40. Local Field Presentation

Local cinematic maps use a hybrid system:

- pre-rendered or pre-composed environment plate;
- real-time Cyanis;
- authored invisible walkmesh;
- elevation and depth data;
- fixed or semi-fixed cameras;
- foreground masks;
- selective dynamic layers;
- interactions, exits, and route indicators;
- real-time hazards and mechanism states.

Each field composition requires:

1. background plate;
2. walkable surfaces;
3. camera definition;
4. perspective and scale behavior;
5. elevation relationships;
6. foreground masks;
7. occlusion response;
8. interaction anchors;
9. exits and safe spawns;
10. dynamic state layers;
11. collision safety margins;
12. environmental audio identity.

## 41. Movement and Collision

Binding requirements:

- responsive camera-relative analog movement;
- very short acceleration and deceleration;
- fast turns with short blending;
- minimal foot sliding;
- smooth wall sliding;
- clean authored lanes;
- stairs as navigation slopes;
- stable character footprint across visual scaling;
- generous edge protection;
- contextual traversal rather than precision platforming;
- automatic final alignment for interactions.

## 42. Camera and Transition Rules

- use authored fixed or semi-fixed compositions;
- preserve held movement intent during camera changes;
- use input-basis blending;
- frame landmarks and route relationships;
- avoid dramatic camera lag during ordinary traversal;
- use short local transitions when technically possible;
- preserve geographic direction, elevation, and entrance logic;
- use longer fades only for tone, major location changes, or necessity.

## 43. Critical-Path Readability

The player should usually identify the likely forward route within a few seconds.

Use:

- lighting;
- architecture;
- roads, stairs, doors, bridges, and sightlines;
- landmark hierarchy;
- repeated motifs;
- NPC positioning;
- environmental motion;
- visible route-state changes.

Optional branches should read as intentional through lateral placement, smaller openings, visible rewards, lower contrast, or known gating.

## 44. Settlements

Settlements are explorable, functional, socially layered places.

Major cities may include:

- residential districts;
- markets;
- inns;
- workshops;
- military areas;
- government or court spaces;
- guilds;
- research or sanctuary districts;
- industrial infrastructure;
- transit systems;
- rooftops and hidden passages;
- old foundations beneath newer construction;
- character-specific locations.

Each settlement requires:

- dominant orientation landmark;
- readable main route;
- optional side routes;
- local shortcuts;
- social or commercial center;
- memorable entrance;
- believable transit;
- changing dialogue and circulation after major events;
- place-based optional activity.

## 45. Dungeons and Facilities

A major dungeon generally targets 45–90 minutes and may include:

1. memorable entrance;
2. statement of place and threat;
3. local mechanical vocabulary;
4. connected route network;
5. optional rooms or rewards;
6. midpoint recovery;
7. story or historical discovery;
8. elite or miniboss escalation;
9. clear boss approach;
10. climax;
11. shortcut, changed state, or clear exit.

A dungeon must not introduce unrelated gimmicks in every room. It should teach, combine, and transform a coherent local system.

## 46. Puzzles and Mechanisms

Puzzles should alter or explain the environment.

Approved forms include:

- rotating or extending bridges;
- rerouting power;
- changing water levels;
- aligning Crest architecture;
- manipulating wards;
- operating lifts;
- predicting moving entities;
- opening cross-party routes;
- creating later historical consequences;
- disabling hazards;
- opening shortcuts.

A mechanism must visibly change the map state or the player’s understanding of the place.

## 47. Timing Hazards

Timing hazards require:

- visible cycle;
- clear audiovisual warning;
- simple steering;
- generous safe pockets;
- quick checkpoint reset;
- limited punishment;
- no unfair overlap with ordinary encounters;
- clear relationship between animation and collision state.

## 48. Regional Travel and Vehicles

Regional travel remains real-time 3D and distinct from local fields.

It uses:

- stable camera anchor;
- slight look-ahead;
- stylized scale;
- broad terrain categories;
- landmark navigation;
- regional road, rail, river, sea, and air logic;
- vehicle-specific access permissions.

Transport systems should exist diegetically before becoming fast-travel interfaces.

Late-game travel may convert the earlier directed journey into a return network while preserving geographic understanding.

## 49. Revisits and Destruction

A revisit must change at least one of:

- route topology;
- political control;
- population;
- danger state;
- services;
- environmental condition;
- mechanism state;
- story purpose;
- emotional meaning.

Destruction must alter circulation, not merely visual color grading.

Solved traversal should be shortened through lifts, repaired bridges, opened gates, secured roads, cleared hazards, or fast transit.

## 50. Multi-Party and Character-Specific Navigation

- Cyanis remains the normally sole visible controllable field character;
- no permanent follower train;
- party splits occur through authored sequences;
- different characters may reveal or operate different routes;
- synchronized routes must show clear cause and effect;
- party knowledge and class identity may change optional interactions without requiring Blue-equipment or other unrelated loadout restrictions.

## 51. Optional Areas and Place-Based Systems

Optional areas should be geographically or culturally grounded.

Good clues include:

- visible unreachable landmarks;
- transport permissions;
- unusual architecture;
- NPC information;
- remembered mechanism states;
- historical evidence;
- character knowledge;
- hidden coordinates or passwords inferred from the world.

Town Yahtzee challengers, hunts, crafting, personal scenes, and other optional systems should exist in believable locations rather than only abstract menus.

## 52. Final-Dungeon Standard

The final region should combine the strongest cross-series lessons:

- dramatic but reversible initial entry;
- explicit final commitment;
- chosen recovery point or preparation access;
- distinct route choices or party routes;
- clearly readable reunion space;
- strong historical and narrative layering;
- minimal irrelevant interruption during the final approach;
- late travel access for optional preparation before commitment.

---

## 53. Anti-Patterns

Do not use:

- heavy movement inertia;
- tank controls;
- held-direction reversal after camera changes;
- exact collision matching decorative geometry;
- stairs with physical collision on every step;
- narrow routes requiring balance precision;
- universal climb-anything traversal;
- large empty spaces used only to imply production value;
- hubs that never change;
- transport systems that exist only as menus with no world logic;
- unrelated puzzle gimmicks in every room;
- repeated unchanged backtracking;
- destruction that changes appearance but not routes;
- character-specific access that feels arbitrary;
- multi-party routes with unclear causal connection;
- invisible optional content impossible to infer;
- maze design based on identical corridors;
- permanent follower trains;
- long black transitions without technical or dramatic reason;
- final points of no return hidden behind ordinary interactions.

---

## 54. Binding Diyse Requirements

All future field and regional prototypes must preserve:

1. responsive camera-relative analog movement;
2. short acceleration and deceleration;
3. fast turning with modern blending;
4. authored fixed or semi-fixed cameras in cinematic fields;
5. camera-basis blending across transitions;
6. clean walkable lanes and forgiving wall sliding;
7. stairs as smooth navigation slopes;
8. perspective scaling and minimum silhouette readability;
9. foreground masking with transparency or silhouette support;
10. edge protection on narrow-looking routes;
11. contextual traversal rather than precision platforming;
12. broad interactions and automatic alignment;
13. readable critical path and intentional side pockets;
14. locations designed around culture, function, history, emotion, landmark, and traversal identity;
15. coherent mechanical vocabulary per facility;
16. mechanisms that visibly alter connectivity or state;
17. timing hazards based on readable cycles and safe pockets;
18. recurring hubs that evolve;
19. diegetic transit and transportation networks;
20. routes capable of supporting advance, evacuation, or changed-state revisits;
21. authored multi-party convergence when narratively useful;
22. character-circumstance access where appropriate;
23. compact dense screens when they serve composition better than large spaces;
24. destruction that changes topology and circulation;
25. continuous regional journeys where travel itself matters;
26. changing spatial rhythm and scale;
27. late travel converting the journey into a return network;
28. three visible historical layers in major locations;
29. vehicles that change geography permissions;
30. optional systems rooted in believable places;
31. explicit final-dungeon commitment;
32. Cyanis as the sole normally visible controllable field character;
33. no permanent follower train;
34. map systems remaining compatible with combat, Cards, progression, menus, and saving.

---

## 55. Prototype-Proven Elements

### v0.06A

Fixed-camera field presentation, perspective scaling, walkmesh collision, edge sliding, foreground masking, interactions, and battle triggering.

### v0.06B

Improved depth-aware movement, contextual interactions, Cyanis-only exploration presentation, and no follower logic.

### v0.09A1

Stable traversal baseline proving responsive camera-relative movement, connected elevation-aware surfaces, upper/lower route separation, wall sliding, foreground fading, camera-basis blending, and reliable route accessibility.

### v0.09B

Seven connected gatehouse compositions, vertical route progression, Crest mechanism, dynamic bridge connectivity, protected upper crossing, Ruin-pulse timing corridor, safe pockets, checkpoint reset, summit payoff, and two-way shortcut.

---

## 56. Per-Map Audit Template

Every proposed map should answer the following before production.

### Identity

- What culture built or occupies it?
- What biome shapes it?
- What is its original function?
- What transformed it?
- How do present users adapt it?
- What emotion should traversal produce?
- What is the signature landmark?
- What is the traversal identity?

### Functional System

- How do people, goods, soldiers, water, power, or information move?
- What transit exists?
- What mechanical vocabulary governs the facility?
- What happens when that system fails or changes?

### Topology

- Which traversal grammar is primary?
- Where is the critical path?
- Where are the side pockets?
- Which routes reconnect?
- What shortcut opens?
- Can the map support a changed-state return?
- Does any past action affect its later form?

### Camera and Readability

- Is the forward route clear within a few seconds?
- Are landmarks visible before arrival?
- Do camera changes preserve input intent?
- Are upper and lower paths distinguishable?
- Can Cyanis become hidden?
- Is occlusion support available?
- Are exits framed and broad?

### Movement and Collision

- Are walkable lanes clean?
- Does wall sliding work?
- Are stairs smooth?
- Are narrow routes forgiving?
- Are edge protections present?
- Are contextual actions automatically aligned?
- Does any section accidentally require precision platforming?

### Story and Character

- Does character circumstance alter access?
- Can optional scenes occur elsewhere in the same location?
- Does party behavior change the planned route?
- Can multiple groups affect one another spatially?
- Does the map show narrative consequences rather than merely describe them?

### Mechanisms and Hazards

- Does the mechanism visibly change space?
- Does navigation match the visible state?
- Is the local rule vocabulary consistent?
- Is the timing cycle readable?
- Are safe pockets generous?
- Is reset quick and fair?

### Pacing and Return

- Does scale and route width vary?
- Is there alternation between danger, shelter, story, spectacle, and discovery?
- Are encounters deliberately placed?
- Is recovery available where appropriate?
- Does the boss approach preserve momentum?
- Does the return route respect the player’s time?

### World Integration

- How does the location connect to regional geography?
- What transport reaches it?
- What later vehicle or authority may unlock?
- What optional area is foreshadowed?
- How does it change after war, Ruin, occupation, repair, or liberation?

---

## 57. Final Design Rule

When choosing between visual drama and physical difficulty:

- make the environment dramatic;
- make the route authored;
- make the place functionally believable;
- make its history visible;
- make controls responsive;
- make collision forgiving;
- make the critical path readable;
- make optionality intentional;
- make mechanisms alter space;
- make revisits change meaning;
- make challenge come from understanding, timing, planning, or consequence.

> **Diyse maps should feel like real places with systems, history, culture, and changing states—presented through cinematic compositions that remain comfortable and reliable to traverse.**
