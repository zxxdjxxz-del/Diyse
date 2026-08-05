# WP-02R Source Freeze

The original hash-gated WP-02 source package has been published and retained.

From this point forward, `agent/godot-wp02` uses the reviewed device-integration repair layer for candidate **v0.04.1-WP02R**. The legacy payload bootstrap must not overwrite the repaired source.

Device-reported corrections:

- Connect the playable `SaveManager` API used by the title screen, traversal menu, and battle autosave to the verified `SaveFoundation` engine.
- Import structurally valid legacy prototype saves into the WP-02 format.
- Exercise Save, Continue, and Recover Backup through the actual UI-facing API.
- Remove the decorative custom outer battle frame while preserving compact battle controls.

WP-02 remains unapproved until the repaired APK passes CI and is explicitly approved on-device.
