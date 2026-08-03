# Godot v0.02 APK build branch

This isolated branch reconstructs and builds **The Role of the Diyse Godot Prototype v0.02** without changing the accepted libGDX prototype line on `main`.

The pull-request workflow verifies the source payload and manifest, runs static and reference tests, downloads Godot 4.7.1 and its matching Android export templates, installs the documented Android 35/JDK 17 toolchain, parses the project headlessly, exports a signed arm64 QA APK, verifies the APK signature, writes a SHA-256 checksum, and uploads the installable artifact.

The QA signing certificate is ephemeral and build-specific. It is not the preserved libGDX prototype certificate and must not be used for production distribution.
