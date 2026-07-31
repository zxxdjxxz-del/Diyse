# Diyse — libGDX Android Prototype v0.01

This is the first non-Godot source foundation for **Diyse**, built as a pre-rendered Android JRPG using Java and libGDX.

## Included now

- Landscape Android application
- Title screen with New Game and Continue
- Layered pre-rendered-style Yahtrean courtyard
- Touch movement and interaction controls
- Three-character prototype party
- One Black Host training encounter
- Commands selected for every conscious party member before resolution
- Enemy commands locked at the legitimate beginning of the round
- Item tier first, Defend tier second, remaining actions by Speed
- Party priority on exact party-versus-enemy Speed ties
- Player selection order for exact party Speed ties
- Attack, Ability, Card, Item, and Defend commands
- Victory and defeat handling
- Individual XP and individual levels
- Full per-character XP for every active participant; XP is never divided
- Save and Continue through Android preferences
- GitHub Actions workflow that compiles and uploads an APK

All character identities, artwork, statistics, formulas, and abilities are placeholders. They do not lock Diyse canon.

## Automatic APK build

The repository contains `.github/workflows/build-android.yml`. On every push to `main` or `master`, GitHub Actions will:

1. Install Java 17.
2. Install Android API 35 and Build Tools 35.0.0.
3. Use Gradle 8.9.
4. Run the combat-order and progression tests.
5. Compile `android-debug.apk`.
6. Upload it as the artifact **Diyse-Prototype-v0.01-APK**.

## Downloading the APK from a phone

1. Open the repository on GitHub.
2. Open **Actions**.
3. Select the newest successful **Build Diyse Android APK** run.
4. Download **Diyse-Prototype-v0.01-APK** from Artifacts.
5. Extract the artifact ZIP and install `android-debug.apk`.

Android may require permission for the browser or file manager to install unknown apps.

## Current version pins

- libGDX 1.14.2
- Java 17
- Android Gradle Plugin 8.7.3
- Gradle 8.9
- compileSdk/targetSdk 35
- minSdk 23

## Package identity

`com.dj.diyse`
