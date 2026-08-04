#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

EXPECTED = {
    "registries": 75,
    "records": 7800,
    "canonical_ids": 2098,
    "cards": 53,
    "primes": 18,
    "scenes": 156,
    "locations": 112,
    "travel": 206,
    "quests": 87,
    "npcs": 67,
    "services": 32,
    "world_states": 26,
    "music_tracks": 72,
    "presentation_ids": 727,
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_wp01r_authority.py <authority-root>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    errors: list[str] = []

    def load(relative: str):
        return json.loads((root / relative).read_text(encoding="utf-8"))

    manifest = load("bundle_manifest.json")
    if manifest.get("format") != "diyse.authority.bundle":
        errors.append("invalid bundle format")
    if manifest.get("canon_version") != "1.12" or manifest.get("archive_audit") != 25:
        errors.append("canon or archive version mismatch")
    if manifest.get("prototype_version") != "0.03.1-WP01R":
        errors.append("Godot WP-01R prototype version mismatch")

    registry_ids: list[str] = []
    total = 0
    registries: dict[str, list[dict]] = {}
    for descriptor in manifest.get("registries", []):
        registry_id = descriptor["registry_id"]
        registry_ids.append(registry_id)
        path = root / descriptor["path"]
        if not path.is_file():
            errors.append(f"missing registry: {descriptor['path']}")
            continue
        if sha256(path) != descriptor["sha256"]:
            errors.append(f"hash mismatch: {registry_id}")
        document = json.loads(path.read_text(encoding="utf-8"))
        records = document.get("records", [])
        if len(records) != descriptor["record_count"]:
            errors.append(f"record count mismatch: {registry_id}")
        registries[registry_id] = records
        total += len(records)

    if len(registry_ids) != EXPECTED["registries"] or len(set(registry_ids)) != len(registry_ids):
        errors.append("registry identity mismatch")
    if total != EXPECTED["records"]:
        errors.append(f"record total mismatch: {total}")

    identity = load(manifest["identity_index"])
    canonical_ids = [row["id"] for row in identity["records"]]
    if len(canonical_ids) != EXPECTED["canonical_ids"] or len(set(canonical_ids)) != len(canonical_ids):
        errors.append("canonical ID count or uniqueness mismatch")

    first_reckoning = "CARD_PRIME_CATACLYSM_FIRST_RECKONING"
    aliases = {
        row["alias"]: row["canonical"]
        for row in load(manifest["alias_registry"])["id_aliases"]
    }
    for alias in (
        "CARD_PRIME_CATACLYSM_LAST_WEAPON",
        "CARD_PRIME_CATACLYSM_STAR_OF_THE_CROWN",
    ):
        if alias in canonical_ids:
            errors.append(f"alias became canonical: {alias}")
        if aliases.get(alias) != first_reckoning:
            errors.append(f"alias does not resolve to First Reckoning: {alias}")
    if first_reckoning not in canonical_ids:
        errors.append("First Reckoning canonical ID missing")

    invariants = load(manifest["invariants"])
    if invariants.get("post_game_playable") is not False:
        errors.append("playable post-game invariant failed")
    if invariants.get("universal_battle_commands") != ["Attack", "Ability", "Card", "Item", "Defend"]:
        errors.append("universal battle commands mismatch")
    if len(invariants.get("permanent_party", [])) != 8:
        errors.append("permanent party count mismatch")

    cards = registries["C3-CARD-IDS"]
    if len(cards) != EXPECTED["cards"]:
        errors.append("Card total mismatch")
    if sum(row.get("category") == "Prime" for row in cards) != EXPECTED["primes"]:
        errors.append("Prime total mismatch")

    counts = {
        "scenes": len(registries["C4-SCENES"]),
        "locations": len(registries["C5-LOCATIONS"]),
        "travel": len(registries["C5-TRAVEL"]),
        "quests": len(registries["C5-QUESTS"]),
        "npcs": len(registries["C5-NPCS"]),
        "services": len(registries["C5-SERVICES"]),
        "world_states": len(registries["C5-WORLD-STATES"]),
        "music_tracks": len(registries["C6-MUSIC-TRACKS"]),
        "presentation_ids": len(registries["C6-RUNTIME-IDS"]),
    }
    for key, actual in counts.items():
        if actual != EXPECTED[key]:
            errors.append(f"{key} count mismatch: {actual} != {EXPECTED[key]}")

    active_text = json.dumps(
        {key: value for key, value in registries.items() if key not in {"C3-CARD-ALIASES", "C5-TERMINOLOGY"}},
        ensure_ascii=False,
    )
    if "Westreach and the Last Weapon" in active_text or "planet-scale Last Weapon" in active_text:
        errors.append("superseded Last Weapon narrative wording remains active")
    if "Westreach and the Horizon Vault" not in active_text:
        errors.append("Horizon Vault terminology is missing")


    d1 = load("lore_d1/contracts/D1_RUNTIME_LORE_CONTRACT.json")
    d1_inv = d1.get("invariants", {})
    if d1_inv.get("billions_dead_before_entity_awakening") is not True:
        errors.append("D1 chronology invariant failed")
    if d1_inv.get("entity_caused_celestial_catastrophe") is not False:
        errors.append("D1 catastrophe causation invariant failed")
    if d1_inv.get("rediscovery_approximately_years_before_story") != 500:
        errors.append("D1 magic rediscovery chronology failed")
    for lore_id in d1.get("canonical_lore_ids", []):
        if lore_id not in canonical_ids:
            errors.append(f"missing D1 canonical lore ID: {lore_id}")

    checksum_lines = (root / "CHECKSUMS_SHA256.txt").read_text(encoding="utf-8").splitlines()
    for line in checksum_lines:
        expected_hash, relative = line.split("  ", 1)
        path = root / relative
        if not path.is_file() or sha256(path) != expected_hash:
            errors.append(f"bundle checksum mismatch: {relative}")

    if errors:
        print("WP-01R VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("WP-01R VALIDATION: PASS")
    print("registries=75 records=7800 canonical_ids=2098")
    print("cards=53 primes=18 scenes=156 locations=112 travel=206 quests=87")
    print("First Reckoning aliases resolve to one canonical identity.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
