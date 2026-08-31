extends Node

signal authority_ready(summary: Dictionary)
signal authority_failed(reason: String)

const AUTHORITY_ROOT := "res://assets/authority/v1_12"
const MANIFEST_PATH := AUTHORITY_ROOT + "/bundle_manifest.json"
const EXPECTED_CANON_VERSION := "1.12"
const EXPECTED_ARCHIVE_AUDIT := 25
const EXPECTED_REGISTRY_COUNT := 75
const EXPECTED_RECORD_TOTAL := 7800
const EXPECTED_CANONICAL_IDS := 2098
const EXPECTED_CARD_TOTAL := 53
const EXPECTED_PRIME_TOTAL := 18
const FIRST_RECKONING_ID := "CARD_PRIME_CATACLYSM_FIRST_RECKONING"
const LAST_WEAPON_ALIAS := "CARD_PRIME_CATACLYSM_LAST_WEAPON"
const STAR_OF_THE_CROWN_ALIAS := "CARD_PRIME_CATACLYSM_STAR_OF_THE_CROWN"

var is_loaded := false
var failure_reason := ""
var manifest: Dictionary = {}
var identity_index: Dictionary = {}
var alias_registry: Dictionary = {}
var invariants: Dictionary = {}
var registry_descriptors: Dictionary = {}
var _canonical_ids: Dictionary = {}
var _id_aliases: Dictionary = {}
var _registry_cache: Dictionary = {}
var verified_registry_count := 0
var verified_record_total := 0

func _ready() -> void:
    if not load_authority_bundle():
        call_deferred("_quit_failed")

func load_authority_bundle() -> bool:
    if is_loaded:
        return true

    var parsed_manifest = _read_json(MANIFEST_PATH)
    if parsed_manifest == null or not (parsed_manifest is Dictionary):
        return _fail("Authority manifest is missing or invalid.")
    manifest = parsed_manifest

    if String(manifest.get("format", "")) != "diyse.authority.bundle":
        return _fail("Authority manifest format is invalid.")
    if String(manifest.get("canon_version", "")) != EXPECTED_CANON_VERSION:
        return _fail("Authority canon version does not match v1.12.")
    if int(manifest.get("archive_audit", -1)) != EXPECTED_ARCHIVE_AUDIT:
        return _fail("Authority archive audit does not match Audit 25.")
    if int(manifest.get("registry_count", -1)) != EXPECTED_REGISTRY_COUNT:
        return _fail("Authority registry count is invalid.")
    if int(manifest.get("registry_record_total", -1)) != EXPECTED_RECORD_TOTAL:
        return _fail("Authority record total is invalid.")

    verified_registry_count = 0
    verified_record_total = 0
    registry_descriptors.clear()

    var registries = manifest.get("registries", [])
    if not (registries is Array):
        return _fail("Authority registry list is invalid.")

    for raw_descriptor in registries:
        if not (raw_descriptor is Dictionary):
            return _fail("Authority registry descriptor is invalid.")
        var descriptor: Dictionary = raw_descriptor
        var registry_id := String(descriptor.get("registry_id", ""))
        var relative_path := String(descriptor.get("path", ""))
        if registry_id.is_empty() or relative_path.is_empty():
            return _fail("Authority registry descriptor is incomplete.")
        if registry_descriptors.has(registry_id):
            return _fail("Duplicate authority registry ID: %s" % registry_id)

        var registry_path := AUTHORITY_ROOT + "/" + relative_path
        if not FileAccess.file_exists(registry_path):
            return _fail("Missing authority registry: %s" % relative_path)

        var expected_hash := String(descriptor.get("sha256", ""))
        var actual_hash := _sha256_file(registry_path)
        if actual_hash.is_empty() or actual_hash != expected_hash:
            return _fail("Authority registry checksum mismatch: %s" % registry_id)

        var parsed_registry = _read_json(registry_path)
        if parsed_registry == null or not (parsed_registry is Dictionary):
            return _fail("Authority registry JSON is invalid: %s" % registry_id)
        var records = parsed_registry.get("records", [])
        if not (records is Array):
            return _fail("Authority registry has no record array: %s" % registry_id)
        var expected_records := int(descriptor.get("record_count", -1))
        if records.size() != expected_records:
            return _fail("Authority registry record count mismatch: %s" % registry_id)

        registry_descriptors[registry_id] = descriptor
        verified_registry_count += 1
        verified_record_total += records.size()

    if verified_registry_count != EXPECTED_REGISTRY_COUNT:
        return _fail("Verified authority registry count is invalid.")
    if verified_record_total != EXPECTED_RECORD_TOTAL:
        return _fail("Verified authority record total is invalid.")

    var parsed_identity = _read_json(AUTHORITY_ROOT + "/" + String(manifest.get("identity_index", "")))
    if parsed_identity == null or not (parsed_identity is Dictionary):
        return _fail("Authority identity index is invalid.")
    identity_index = parsed_identity
    if int(identity_index.get("record_count", -1)) != EXPECTED_CANONICAL_IDS:
        return _fail("Authority canonical ID count is invalid.")
    if int(identity_index.get("unique_count", -1)) != EXPECTED_CANONICAL_IDS:
        return _fail("Authority canonical IDs are not unique.")

    _canonical_ids.clear()
    var identity_records = identity_index.get("records", [])
    if not (identity_records is Array) or identity_records.size() != EXPECTED_CANONICAL_IDS:
        return _fail("Authority identity records are invalid.")
    for raw_identity in identity_records:
        if not (raw_identity is Dictionary):
            return _fail("Authority identity record is invalid.")
        var canonical_id := String(raw_identity.get("id", ""))
        if canonical_id.is_empty() or _canonical_ids.has(canonical_id):
            return _fail("Authority contains a missing or duplicate canonical ID.")
        _canonical_ids[canonical_id] = true

    var parsed_aliases = _read_json(AUTHORITY_ROOT + "/" + String(manifest.get("alias_registry", "")))
    if parsed_aliases == null or not (parsed_aliases is Dictionary):
        return _fail("Authority alias registry is invalid.")
    alias_registry = parsed_aliases
    _id_aliases.clear()
    for raw_alias in alias_registry.get("id_aliases", []):
        if not (raw_alias is Dictionary):
            return _fail("Authority ID alias record is invalid.")
        var alias_id := String(raw_alias.get("alias", ""))
        var target_id := String(raw_alias.get("canonical", ""))
        if alias_id.is_empty() or target_id.is_empty():
            return _fail("Authority ID alias is incomplete.")
        _id_aliases[alias_id] = target_id

    var parsed_invariants = _read_json(AUTHORITY_ROOT + "/" + String(manifest.get("invariants", "")))
    if parsed_invariants == null or not (parsed_invariants is Dictionary):
        return _fail("Authority invariant register is invalid.")
    invariants = parsed_invariants

    if not _validate_protected_invariants():
        return false

    is_loaded = true
    var summary := get_summary()
    print("DIYSE AUTHORITY READY: registries=%d records=%d canonical_ids=%d" % [
        verified_registry_count,
        verified_record_total,
        _canonical_ids.size(),
    ])
    authority_ready.emit(summary)
    return true

func _validate_protected_invariants() -> bool:
    if not _canonical_ids.has(FIRST_RECKONING_ID):
        return _fail("First Reckoning is missing from canonical authority.")
    if _canonical_ids.has(LAST_WEAPON_ALIAS) or _canonical_ids.has(STAR_OF_THE_CROWN_ALIAS):
        return _fail("A superseded Cataclysm Prime alias became canonical.")
    if resolve_id(LAST_WEAPON_ALIAS) != FIRST_RECKONING_ID:
        return _fail("Last Weapon alias does not resolve to First Reckoning.")
    if resolve_id(STAR_OF_THE_CROWN_ALIAS) != FIRST_RECKONING_ID:
        return _fail("Star of the Crown alias does not resolve to First Reckoning.")
    if String(invariants.get("mandatory_cataclysm_prime", "")) != FIRST_RECKONING_ID:
        return _fail("Mandatory Cataclysm Prime invariant is invalid.")
    if bool(invariants.get("post_game_playable", true)):
        return _fail("Authority incorrectly enables a playable post-game state.")

    var commands = invariants.get("universal_battle_commands", [])
    if not (commands is Array) or commands != ["Attack", "Ability", "Card", "Item", "Defend"]:
        return _fail("Universal battle command invariant is invalid.")
    var party = invariants.get("permanent_party", [])
    if not (party is Array) or party.size() != 8:
        return _fail("Permanent party invariant is invalid.")

    var card_registry = get_registry("C3-CARD-IDS")
    if card_registry.is_empty():
        return _fail("Card identity registry could not be loaded.")
    var card_records = card_registry.get("records", [])
    if not (card_records is Array) or card_records.size() != EXPECTED_CARD_TOTAL:
        return _fail("Card total invariant is invalid.")
    var prime_count := 0
    for raw_card in card_records:
        if raw_card is Dictionary and String(raw_card.get("category", "")) == "Prime":
            prime_count += 1
    if prime_count != EXPECTED_PRIME_TOTAL:
        return _fail("Prime Card total invariant is invalid.")

    var d1 = invariants.get("d1_lore_invariants", {})
    if not (d1 is Dictionary):
        return _fail("D1 lore invariants are missing.")
    if not bool(d1.get("billions_dead_before_entity_awakening", false)):
        return _fail("D1 chronology invariant is invalid.")
    if int(d1.get("rediscovery_approximately_years_before_story", 0)) != 500:
        return _fail("Magic rediscovery chronology is invalid.")
    if bool(d1.get("entity_caused_celestial_catastrophe", true)):
        return _fail("Entity catastrophe-causation invariant is invalid.")

    return true

func get_registry(registry_id: String) -> Dictionary:
    if _registry_cache.has(registry_id):
        return _registry_cache[registry_id]
    if not registry_descriptors.has(registry_id):
        return {}
    var descriptor: Dictionary = registry_descriptors[registry_id]
    var path := AUTHORITY_ROOT + "/" + String(descriptor.get("path", ""))
    var parsed = _read_json(path)
    if parsed is Dictionary:
        _registry_cache[registry_id] = parsed
        return parsed
    return {}

func resolve_id(candidate_id: String) -> String:
    if _id_aliases.has(candidate_id):
        return String(_id_aliases[candidate_id])
    return candidate_id

func has_canonical_id(candidate_id: String) -> bool:
    return _canonical_ids.has(candidate_id)

func get_summary() -> Dictionary:
    return {
        "canon_version": String(manifest.get("canon_version", "")),
        "archive_audit": int(manifest.get("archive_audit", -1)),
        "bundle_version": String(manifest.get("bundle_version", "")),
        "prototype_version": String(manifest.get("prototype_version", "")),
        "registry_count": verified_registry_count,
        "record_total": verified_record_total,
        "canonical_id_count": _canonical_ids.size(),
        "first_reckoning": FIRST_RECKONING_ID,
        "post_game_playable": bool(invariants.get("post_game_playable", true)),
    }

func _read_json(path: String):
    if not FileAccess.file_exists(path):
        return null
    var text := FileAccess.get_file_as_string(path)
    if text.is_empty():
        return null
    return JSON.parse_string(text)

func _sha256_file(path: String) -> String:
    var file := FileAccess.open(path, FileAccess.READ)
    if file == null:
        return ""
    var context := HashingContext.new()
    if context.start(HashingContext.HASH_SHA256) != OK:
        return ""
    while file.get_position() < file.get_length():
        var remaining := file.get_length() - file.get_position()
        var chunk_size := int(min(remaining, 65536))
        context.update(file.get_buffer(chunk_size))
    return context.finish().hex_encode()

func _fail(reason: String) -> bool:
    failure_reason = reason
    push_error("DIYSE AUTHORITY FAILURE: %s" % reason)
    authority_failed.emit(reason)
    return false

func _quit_failed() -> void:
    get_tree().quit(70)
