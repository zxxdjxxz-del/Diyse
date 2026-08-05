#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).parent

save_path = root / "save_foundation.gd"
save_text = save_path.read_text(encoding="utf-8")
old_hash = '''func _sha256_variant(value) -> String:
    return _sha256_text(JSON.stringify(value, "", true))
'''
new_hash = '''func _sha256_variant(value) -> String:
    # Godot JSON parses every number as a float. Hash the canonical JSON
    # round-trip so an in-memory integer and its persisted numeric form agree.
    var serialized := JSON.stringify(value, "", true)
    var canonical = JSON.parse_string(serialized)
    return _sha256_text(JSON.stringify(canonical, "", true))
'''
if new_hash in save_text:
    print("WP-02 canonical save hashing is already installed.")
elif old_hash in save_text:
    save_path.write_text(save_text.replace(old_hash, new_hash, 1), encoding="utf-8")
    print("Installed WP-02 canonical save hashing.")
else:
    raise SystemExit("Expected _sha256_variant implementation was not found.")

test_path = root / "wp02_save_regression_test.gd"
test_text = test_path.read_text(encoding="utf-8")
function_marker = "func _test_interrupted_write_is_ignored() -> void:\n"
start = test_text.find(function_marker)
if start < 0:
    raise SystemExit("Interrupted-write regression function was not found.")
end = test_text.find("\nfunc ", start + len(function_marker))
if end < 0:
    end = len(test_text)
segment = test_text[start:end]
repairs = (
    ('    var before := manager.load_game("slot_a")\n', '    var before: Dictionary = manager.load_game("slot_a")\n'),
    ('    var interruption := manager.simulate_interrupted_write_for_test("slot_a", {"chapter": 99})\n', '    var interruption: Dictionary = manager.simulate_interrupted_write_for_test("slot_a", {"chapter": 99})\n'),
    ('    var loaded := manager.load_game("slot_a")\n', '    var loaded: Dictionary = manager.load_game("slot_a")\n'),
)
changed = False
for old, new in repairs:
    if new in segment:
        continue
    if old not in segment:
        raise SystemExit(f"Expected interrupted-write regression line was not found: {old.strip()}")
    segment = segment.replace(old, new, 1)
    changed = True
required = [new for _, new in repairs]
missing = [line.strip() for line in required if line not in segment]
if missing:
    raise SystemExit("Typed interrupted-write regression lines are missing: " + ", ".join(missing))
if changed:
    test_text = test_text[:start] + segment + test_text[end:]
    test_path.write_text(test_text, encoding="utf-8")
    print("Installed WP-02 Godot 4.7 regression-test typing fixes.")
else:
    print("WP-02 regression-test typing fixes are already installed.")
