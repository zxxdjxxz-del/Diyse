# Diyse — libGDX Android JRPG Prototype

Diyse is a Java/libGDX Android prototype for an original cinematic 3D JRPG using hybrid pre-rendered fields, real-time characters, authored traversal, classic round-based combat, and touch controls.

## Current prototype line

- **Device-tested stable baseline:** v0.09C authored gatehouse visual production slice
- **Current development candidate:** v0.09D field persistence and release hardening
- **Package:** `com.dj.diyse`
- **Orientation:** landscape
- **Minimum Android API:** 23
- **Build target:** Android API 35
- **Signing:** permanent prototype certificate supporting install-over updates

The current prototype line preserves title and save flow, exploration, battle, Items, MP Abilities, Standard Card loadout interaction, progression, and signed Android builds while developing the map, traversal, authored visual-production, and field-persistence foundations.

v0.09C remains the accepted visual and traversal baseline. v0.09D adds schema migration, field-aware Continue, authored safe resume anchors, persistent bridge and shortcut states, corruption fallback, and field-aware return from battles and menus without changing accepted geometry or movement.

All placeholder artwork, statistics, formulas, abilities, encounters, and temporary prototype locations remain non-canon unless separately approved and consolidated into the newest Diyse Active Master Canon.

## Authoritative project references

Start with:

- [`docs/REFERENCE_INDEX.md`](docs/REFERENCE_INDEX.md) — authority order and repository reference routing.
- [`docs/Diyse_Final_Fantasy_VII_X_Map_and_Traversal_Design_Standard.md`](docs/Diyse_Final_Fantasy_VII_X_Map_and_Traversal_Design_Standard.md) — authoritative map and traversal standard consolidating approved lessons from Final Fantasy VII, VIII, IX, and X.
- [`docs/templates/Diyse_Map_Design_Sheet.md`](docs/templates/Diyse_Map_Design_Sheet.md) — required design and traceability template for future fields, settlements, dungeons, regional routes, vehicles, optional areas, revisits, and final regions.
- [`docs/maps/v0.09C_Authored_Gatehouse_Visual_Slice_Design_Sheet.md`](docs/maps/v0.09C_Authored_Gatehouse_Visual_Slice_Design_Sheet.md) — traced design and acceptance contract for the accepted authored visual slice.
- [`docs/maps/v0.09D_Field_Persistence_Design_Sheet.md`](docs/maps/v0.09D_Field_Persistence_Design_Sheet.md) — migration, safe-resume, mechanism-state, and Android acceptance contract for the current persistence candidate.

The older `docs/Diyse_FFVII_Map_and_Traversal_Design_Standard.md` is superseded and redirects to the combined VII–X reference.

## Map and traversal direction

Local cinematic areas use a hybrid field model:

- pre-rendered or pre-composed background plates;
- separate atmosphere and foreground-mask layers;
- real-time Cyanis using an authored field sheet;
- authored walkable surfaces and elevations;
- fixed or semi-fixed cameras;
- camera-relative analog movement;
- input-basis blending across camera changes;
- smooth stair slopes and forgiving wall sliding;
- depth-based perspective scaling;
- foreground occlusion and silhouette assistance;
- contextual traversal and broad interaction alignment;
- dynamic route mechanisms and readable timing hazards;
- authored safe resume anchors for persistence;
- no permanent follower train.

Regional and world travel remain a distinct real-time 3D mode with stable camera follow, broad terrain categories, landmark navigation, and vehicle-specific access permissions.

## Included game foundation

- Title screen with New Game and Continue
- Landscape Android application
- Touch movement and interaction controls
- Cyanis-only normal field presentation
- Seven-composition gatehouse traversal route
- Layered fixed-camera exploration
- Dynamic bridge connectivity and return shortcut
- Ruin-pulse timing corridor with safe pockets
- Field-aware Continue and return from battles or menus
- Validated gatehouse safe-spawn persistence
- Persistent bridge, shortcut, and completion state
- Schema migration and corrupted-state fallback
- Classic discrete rounds
- Commands selected for every conscious active party member before resolution
- Enemy commands locked from the legitimate beginning-of-round state
- Items first, Defend second, remaining actions by Speed
- Party priority on exact party-versus-enemy Speed ties
- Player-selected order for tied party members
- Attack, Ability, Card, Item, and Defend commands
- MP-based prototype Abilities
- Standard Card loadout interaction
- Victory and defeat handling
- Individual XP and levels
- Save and Continue through Android preferences
- GitHub Actions APK compilation and artifact upload

## Build toolchain

- libGDX 1.14.2
- Java 17
- Android Gradle Plugin 8.7.3
- Gradle 8.9
- compileSdk/targetSdk 35
- minSdk 23
- Pillow 12.2.0 and NumPy 2.3.5 for deterministic offline visual generation

## Automatic APK build

The repository workflow reconstructs the verified runtime source, applies the incremental prototype overlays, regenerates and verifies authored visual assets, verifies persistence migration and safe-resume contracts, runs the complete regression suite, compiles the Android APK, verifies the permanent prototype certificate, and uploads the installable artifact.

To retrieve a build on a phone:

1. Open the repository on GitHub.
2. Open **Actions**.
3. Select the newest successful **Build Diyse Android APK** run.
4. Download the APK artifact.
5. Extract the ZIP and install the APK.

Android may require permission for the browser or file manager to install unknown apps.

## Acceptance rule

A draft build does not replace the stable baseline until:

1. integrity, migration, persistence, visual-asset, feature, and regression tests pass;
2. the APK compiles and retains the permanent certificate;
3. existing saves migrate without losing established progress;
4. field, mechanism, shortcut, and safe-position restoration work on the user’s Android phone;
5. traversal, visuals, battle, Cards, progression, menus, saving, and performance remain accepted;
6. the implementation pull request is approved and merged.
