#!/usr/bin/env python3
from pathlib import Path

path = Path(__file__).with_name("save_foundation.gd")
text = path.read_text(encoding="utf-8")
old = '''func _sha256_variant(value) -> String:
    return _sha256_text(JSON.stringify(value, "", true))
'''
new = '''func _sha256_variant(value) -> String:
    # Godot JSON parses every number as a float. Hash the canonical JSON
    # round-trip so an in-memory integer and its persisted numeric form agree.
    var serialized := JSON.stringify(value, "", true)
    var canonical = JSON.parse_string(serialized)
    return _sha256_text(JSON.stringify(canonical, "", true))
'''
if new in text:
    print("WP-02 canonical save hashing is already installed.")
elif old in text:
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    print("Installed WP-02 canonical save hashing.")
else:
    raise SystemExit("Expected _sha256_variant implementation was not found.")
