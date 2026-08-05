# WP-02 — Save, Migration, and Transaction Foundation

Godot implementation candidate built on approved WP-01R v0.2 / v0.03.1-WP01R.

## Runtime contract

- Atomic pending-file validation before primary replacement.
- Verified prior primary copied to backup before commit.
- Crash/interruption recovery from previous or backup state.
- Payload and envelope SHA-256 validation.
- Versioned schema migration with recursive alias resolution.
- Alias collisions merge without duplicating inventory, Cards, rewards, flags, or progress.
- Transaction mutations commit atomically or preserve the prior verified save.
- Completion metadata is stored separately and cannot contain playable world state.
- Continue after completion loads the pre-Act-VI Final Return Save.
- Post-victory and cleared-world saves are rejected.

Acceptance requires Python contract validation, Godot runtime regression, inherited WP-01R authority validation, inherited battle/UI regression, Android export/signature verification, and explicit device approval.
