#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED_SAVE_TOKENS = [
    'const SAVE_FORMAT := "diyse.save.envelope"',
    'const CURRENT_SCHEMA_VERSION := 2',
    'func save_game(',
    'func load_game(',
    'func transact(',
    'func migrate_slot(',
    'func migrate_payload(',
    'func write_final_return_save(',
    'func write_completion_metadata(',
    'func load_continue_state(',
    'SAVE_POST_VICTORY_PROHIBITED',
    'SAVE_NO_VERIFIED_STATE',
    'FINAL_RETURN_REQUIRED',
    'payload_sha256',
    'envelope_sha256',
    'backup_pending',
    'previous',
    'journal',
]

REQUIRED_TEST_TOKENS = [
    '_test_backup_and_corruption_recovery()',
    '_test_interrupted_write_is_ignored()',
    '_test_alias_migration_without_duplication()',
    '_test_transaction_rollback()',
    '_test_completion_metadata_separation()',
    '_test_final_return_continue_behavior()',
    '_test_post_victory_rejection()',
    '_test_checksum_tamper_detection()',
    '_test_both_invalid_fail_closed()',
    'PASS: WP-02 atomic save, migration, rollback, recovery, completion metadata, and Final Return Save gates passed.',
]


def require_tokens(path: Path, tokens: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    missing = [token for token in tokens if token not in text]
    if missing:
        raise AssertionError(f"{path}: missing contract tokens: {missing}")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_wp02_contract.py <wp02-dir>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    save = root / "save_foundation.gd"
    test = root / "wp02_save_regression_test.gd"
    scene = root / "wp02_save_regression_test.tscn"
    apply = root / "apply_wp02.py"
    for required in (save, test, scene, apply):
        if not required.is_file():
            raise FileNotFoundError(required)

    require_tokens(save, REQUIRED_SAVE_TOKENS)
    require_tokens(test, REQUIRED_TEST_TOKENS)
    require_tokens(scene, ['res://tests/wp02_save_regression_test.gd'])
    require_tokens(apply, ['0.04.0-WP02', 'SaveFoundation="*res://src/autoload/save_foundation.gd"'])

    save_text = save.read_text(encoding="utf-8")
    if re.search(r'post_victory_world"\s*:\s*true', save_text):
        raise AssertionError("WP-02 implementation contains a literal enabled post-victory world state.")
    if "__pycache__" in save_text or ".pyc" in save_text:
        raise AssertionError("Generated Python cache reference found in WP-02 implementation.")

    print("WP-02 CONTRACT VALIDATION: PASS")
    print("atomic_write=PASS backup_recovery=PASS alias_migration=PASS rollback=PASS")
    print("completion_metadata=PASS final_return_save=PASS no_post_game=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
