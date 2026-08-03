class_name BattleSimulator
extends RefCounted

var actors: Dictionary = {}
var party_ids: Array[String] = []
var enemy_ids: Array[String] = []
var round_number := 0
var battle_seed := 1
var battle_kind := "ORDINARY"
var formation_id := "FORM_VS_A"
var enemy_intents: Array[Dictionary] = []
var card_uses: Dictionary = {}
var ultimate_used: Dictionary = {}

const PARTY_BLUE := "party"
const ENEMY_RED := "enemy"

func setup(kind: String, formation: String, seed: int) -> void:
    actors.clear()
    party_ids.clear()
    enemy_ids.clear()
    round_number = 0
    battle_seed = seed
    battle_kind = kind
    formation_id = formation
    card_uses = {
        "CARD_IRON_TESTAMENT": 1,
        "CARD_SUNDER_THE_GATE": 1,
        "CARD_CINDER_JUDGMENT": 1,
        "CARD_THUNDER_CHAIN": 1,
    }
    ultimate_used = {}
    _add_party()
    _add_enemies()

func _add_party() -> void:
    _add_actor("HERO_CYANIS", "Cyanis", PARTY_BLUE, 190, 38, 24, 27, 0)
    _add_actor("HERO_ILYRA", "Ilyra", PARTY_BLUE, 145, 22, 39, 25, 1)
    _add_actor("HERO_TORREN", "Torren", PARTY_BLUE, 175, 34, 20, 23, 2)
    _add_actor("HERO_MAEVRA", "Maevra", PARTY_BLUE, 215, 32, 20, 19, 3)
    _add_actor("HERO_NIMERA", "Nimera", PARTY_BLUE, 155, 20, 36, 22, 4)

func _add_enemies() -> void:
    if battle_kind == "BOSS":
        _add_actor("BOSS_VS_CONTROL_WARDEN", "Control Warden", ENEMY_RED, 520, 43, 42, 18, 0, {"boss": true})
        _add_actor("CMP_VS_CONTROL_CORE", "Control Core", ENEMY_RED, 150, 24, 30, 16, 1, {"component": true})
        return
    match formation_id:
        "FORM_VS_B":
            _add_actor("EN_VS_RUIN_SENTINEL", "Ruin Sentinel", ENEMY_RED, 150, 28, 12, 15, 0)
            _add_actor("EN_VS_RUIN_CHANNELER", "Ruin Channeler", ENEMY_RED, 110, 18, 31, 17, 1)
            _add_actor("ENT_VS_RUIN_SEAL", "Ruin Seal", ENEMY_RED, 80, 14, 22, 12, 2, {"entity": true, "creator_id": "EN_VS_RUIN_CHANNELER"})
        "FORM_VS_C":
            _add_actor("EN_VS_RUIN_HARRIER", "Ruin Harrier", ENEMY_RED, 105, 31, 14, 29, 0)
            _add_actor("EN_VS_RUIN_MARKSMAN", "Ruin Marksman", ENEMY_RED, 115, 30, 13, 24, 1)
            _add_actor("EN_VS_RUIN_SENTINEL_REINFORCEMENT", "Sentinel Reinforcement", ENEMY_RED, 135, 27, 12, 14, 2, {"reinforcement": true})
            actors["EN_VS_RUIN_SENTINEL_REINFORCEMENT"]["active"] = false
        _:
            _add_actor("EN_VS_RUIN_SENTINEL_A", "Ruin Sentinel A", ENEMY_RED, 135, 27, 12, 15, 0)
            _add_actor("EN_VS_RUIN_SENTINEL_B", "Ruin Sentinel B", ENEMY_RED, 135, 27, 12, 14, 1)
            _add_actor("EN_VS_RUIN_MARKSMAN", "Ruin Marksman", ENEMY_RED, 105, 29, 13, 23, 2)

func _add_actor(id: String, display_name: String, team: String, hp: int, attack: int, magic: int, speed: int, order: int, tags: Dictionary = {}) -> void:
    actors[id] = {
        "id": id,
        "name": display_name,
        "team": team,
        "max_hp": hp,
        "hp": hp,
        "attack": attack,
        "magic": magic,
        "defense": 18 if team == PARTY_BLUE else 14,
        "speed": speed,
        "authored_order": order,
        "alive": true,
        "active": true,
        "defending": false,
        "barrier": 0,
        "counter": false,
        "marked": false,
        "burn": 0,
        "slow": 0,
        "tags": tags.duplicate(true),
    }
    if team == PARTY_BLUE:
        party_ids.append(id)
    else:
        enemy_ids.append(id)

func start_round() -> Array[Dictionary]:
    round_number += 1
    for id in actors:
        actors[id]["defending"] = false
    var snapshot := actors.duplicate(true)
    enemy_intents = _lock_enemy_intents(snapshot)
    return [{"type": "phase", "text": "Round %d: enemy commands locked from the beginning-of-round state." % round_number}]

func _lock_enemy_intents(snapshot: Dictionary) -> Array[Dictionary]:
    var intents: Array[Dictionary] = []
    var living_party := _living_ids(PARTY_BLUE, snapshot)
    if living_party.is_empty():
        return intents
    for enemy_id in enemy_ids:
        var enemy: Dictionary = snapshot[enemy_id]
        if not bool(enemy.get("alive", false)) or not bool(enemy.get("active", true)):
            continue
        var idx: int = absi(battle_seed + round_number * 13 + int(enemy["authored_order"]) * 5) % living_party.size()
        var target_id: String = living_party[idx]
        var action_id := "ENEMY_ATTACK"
        if enemy_id == "EN_VS_RUIN_CHANNELER" and round_number == 1:
            action_id = "ENEMY_PREPARE"
        elif enemy_id == "BOSS_VS_CONTROL_WARDEN" and round_number % 3 == 0:
            action_id = "BOSS_SWEEP"
        elif enemy_id == "CMP_VS_CONTROL_CORE":
            action_id = "CORE_PULSE"
        intents.append(_intent(enemy_id, action_id, target_id, "ABILITY", 0))
    return intents

func resolve_round(party_plans: Array[Dictionary]) -> Array[Dictionary]:
    var events: Array[Dictionary] = []
    var queue: Array[Dictionary] = []
    for plan in party_plans:
        queue.append(plan.duplicate(true))
    for intent in enemy_intents:
        queue.append(intent.duplicate(true))
    queue.sort_custom(_intent_before)
    events.append({"type": "phase", "text": "Items resolve first, Defend second, then remaining actions by priority and Speed."})
    for intent in queue:
        if not _can_act(str(intent.get("actor_id", ""))):
            events.append({"type": "skip", "text": "%s cannot act." % _name(str(intent.get("actor_id", "")))})
            continue
        events.append_array(_execute_intent(intent))
        _cleanup_creator_bound_entities(events)
        _activate_reinforcement_if_needed(events)
    events.append_array(_end_round_effects())
    return events

func _intent_before(a: Dictionary, b: Dictionary) -> bool:
    var tier_a := _tier(a)
    var tier_b := _tier(b)
    if tier_a != tier_b:
        return tier_a < tier_b
    if tier_a == 3:
        var priority_a := int(a.get("priority", 0))
        var priority_b := int(b.get("priority", 0))
        if priority_a != priority_b:
            return priority_a < priority_b
    var actor_a: Dictionary = actors.get(str(a.get("actor_id", "")), {})
    var actor_b: Dictionary = actors.get(str(b.get("actor_id", "")), {})
    var speed_a := maxi(0, int(actor_a.get("speed", 0)) - int(actor_a.get("slow", 0)))
    var speed_b := maxi(0, int(actor_b.get("speed", 0)) - int(actor_b.get("slow", 0)))
    if speed_a != speed_b:
        return speed_a > speed_b
    var team_a := str(actor_a.get("team", ENEMY_RED))
    var team_b := str(actor_b.get("team", ENEMY_RED))
    if team_a != team_b:
        return team_a == PARTY_BLUE
    if team_a == PARTY_BLUE:
        return int(a.get("tie_rank", 999)) < int(b.get("tie_rank", 999))
    return int(actor_a.get("authored_order", 999)) < int(actor_b.get("authored_order", 999))

func _tier(intent: Dictionary) -> int:
    var family := str(intent.get("family", "ABILITY"))
    if family == "ITEM":
        return 1
    if family == "DEFEND":
        return 2
    return 3

func _execute_intent(intent: Dictionary) -> Array[Dictionary]:
    var actor_id := str(intent.get("actor_id", ""))
    var action_id := str(intent.get("action_id", "ATTACK"))
    var target_id := str(intent.get("target_id", ""))
    var events: Array[Dictionary] = []
    match action_id:
        "DEFEND":
            actors[actor_id]["defending"] = true
            events.append(_event("defend", "%s braces for the round." % _name(actor_id), actor_id, actor_id, 0))
        "ITEM_FIELD_SALVE":
            if GameState.consume_item("ITM_FIELD_SALVE", 1):
                events.append(_heal(actor_id, target_id, 70, "uses Field Salve on"))
            else:
                events.append(_event("failed", "%s has no Field Salve." % _name(actor_id), actor_id, target_id, 0))
        "ITEM_TRIAGE":
            if GameState.consume_item("ITM_COMPANY_TRIAGE_KIT", 1):
                for id in party_ids:
                    if _is_alive(id):
                        events.append(_heal(actor_id, id, 38, "uses Company Triage Kit for"))
            else:
                events.append(_event("failed", "%s has no Company Triage Kit." % _name(actor_id), actor_id, target_id, 0))
        "CREST_STRIKE", "DRIVING_STRIKE", "OATH_STRIKE", "IRON_TESTAMENT":
            events.append(_damage(actor_id, target_id, 1.35 if action_id != "IRON_TESTAMENT" else 1.55, false, _pretty(action_id)))
            _consume_card_if_needed(action_id)
        "MEND":
            events.append(_heal(actor_id, target_id, 92, "casts Mend on"))
        "HARMONIZING_WARD", "RENEWAL":
            for id in party_ids:
                if _is_alive(id):
                    events.append(_heal(actor_id, id, 34 if action_id == "HARMONIZING_WARD" else 44, "restores"))
        "GUARDIAN_SIGIL", "CLEAR_WARDING", "GUARDED_OATH", "WEAVE_GUARD":
            actors[target_id]["barrier"] = int(actors[target_id]["barrier"]) + 45
            events.append(_event("barrier", "%s grants %s a 45-point barrier." % [_name(actor_id), _name(target_id)], actor_id, target_id, 45))
        "RESOLUTE_COUNTER", "OATH_COUNTER":
            actors[actor_id]["counter"] = true
            events.append(_event("counter", "%s prepares a counter." % _name(actor_id), actor_id, actor_id, 0))
        "WARDENS_VALOR":
            for id in party_ids:
                actors[id]["barrier"] = int(actors[id]["barrier"]) + 25
            events.append(_event("barrier", "Ilyra reinforces the full party.", actor_id, actor_id, 25))
        "QUARRY_APPRAISAL", "DIYSEAN_APPRAISAL":
            actors[target_id]["marked"] = true
            events.append(_event("mark", "%s marks %s for focused damage." % [_name(actor_id), _name(target_id)], actor_id, target_id, 0))
        "WATCHFUL_AIM", "PREPARED_THREAD":
            actors[actor_id]["barrier"] = int(actors[actor_id]["barrier"]) + 20
            events.append(_event("prepare", "%s prepares their next exchange." % _name(actor_id), actor_id, actor_id, 20))
        "PINNING_STRIKE":
            events.append(_damage(actor_id, target_id, 1.15, false, "Pinning Strike"))
            actors[target_id]["slow"] = 8
            events.append(_event("slow", "%s is slowed." % _name(target_id), actor_id, target_id, 8))
        "STEADFAST_CHALLENGE":
            actors[actor_id]["defending"] = true
            events.append(_event("challenge", "%s issues a steadfast challenge." % _name(actor_id), actor_id, actor_id, 0))
        "REWOVEN":
            for card_id in card_uses:
                card_uses[card_id] = maxi(int(card_uses[card_id]), 1)
            events.append(_event("card", "Nimera rewoven the party's prototype Card threads.", actor_id, actor_id, 0))
        "SUNDER_THE_GATE":
            var multiplier := 1.9 if bool(actors[target_id]["tags"].get("component", false)) or int(actors[target_id]["barrier"]) > 0 else 1.3
            events.append(_damage(actor_id, target_id, multiplier, false, "Sunder the Gate"))
            _consume_card("CARD_SUNDER_THE_GATE")
        "CINDER_JUDGMENT":
            events.append(_damage(actor_id, target_id, 1.45, true, "Cinder Judgment"))
            actors[target_id]["burn"] = 3
            _consume_card("CARD_CINDER_JUDGMENT")
        "THUNDER_CHAIN":
            var targets := _living_ids(ENEMY_RED, actors)
            var hits := 0
            for id in targets:
                if hits >= 2:
                    break
                events.append(_damage(actor_id, id, 1.05, true, "Thunder Chain"))
                hits += 1
            _consume_card("CARD_THUNDER_CHAIN")
        "CREST_OF_EIGHT":
            if bool(ultimate_used.get(actor_id, false)):
                events.append(_event("failed", "%s has already used the Ultimate." % _name(actor_id), actor_id, target_id, 0))
            else:
                ultimate_used[actor_id] = true
                for id in _living_ids(ENEMY_RED, actors):
                    events.append(_damage(actor_id, id, 1.85, true, "Crest of Eight"))
        "ENEMY_PREPARE":
            actors[actor_id]["barrier"] = int(actors[actor_id]["barrier"]) + 35
            events.append(_event("prepare", "%s channels a visible ward." % _name(actor_id), actor_id, actor_id, 35))
        "BOSS_SWEEP":
            for id in party_ids:
                if _is_alive(id):
                    events.append(_damage(actor_id, id, 0.72, true, "Control Sweep"))
        "CORE_PULSE":
            var boss_id := "BOSS_VS_CONTROL_WARDEN"
            if actors.has(boss_id) and _is_alive(boss_id):
                actors[boss_id]["barrier"] = int(actors[boss_id]["barrier"]) + 25
                events.append(_event("barrier", "The Control Core reinforces the Warden.", actor_id, boss_id, 25))
        _:
            events.append(_damage(actor_id, target_id, 1.0, false, _pretty(action_id)))
    return events

func _damage(actor_id: String, target_id: String, multiplier: float, magical: bool, label: String) -> Dictionary:
    if not actors.has(target_id) or not _is_alive(target_id):
        return _event("failed", "%s has no legal target." % _name(actor_id), actor_id, target_id, 0)
    var source: Dictionary = actors[actor_id]
    var target: Dictionary = actors[target_id]
    var offense := int(source["magic"] if magical else source["attack"])
    var defense := int(target["defense"])
    var amount := maxi(1, int(round(float(offense) * multiplier - float(defense) * 0.45)))
    if bool(target.get("marked", false)):
        amount = int(round(amount * 1.18))
    if bool(target.get("defending", false)):
        amount = int(ceil(amount * 0.5))
    var barrier := int(target.get("barrier", 0))
    if barrier > 0:
        var absorbed := mini(barrier, amount)
        target["barrier"] = barrier - absorbed
        amount -= absorbed
    target["hp"] = maxi(0, int(target["hp"]) - amount)
    if int(target["hp"]) <= 0:
        target["alive"] = false
    var text := "%s uses %s on %s for %d damage." % [_name(actor_id), label, _name(target_id), amount]
    if not bool(target["alive"]):
        text += " %s is defeated." % _name(target_id)
    var event := _event("damage", text, actor_id, target_id, amount)
    if bool(target.get("counter", false)) and _is_alive(target_id) and amount > 0:
        target["counter"] = false
        var reflected := maxi(1, int(round(float(target["attack"]) * 0.65)))
        source["hp"] = maxi(0, int(source["hp"]) - reflected)
        if int(source["hp"]) <= 0:
            source["alive"] = false
        event["follow_up"] = "%s counters for %d damage." % [_name(target_id), reflected]
    return event

func _heal(actor_id: String, target_id: String, amount: int, verb: String) -> Dictionary:
    if not actors.has(target_id) or not _is_alive(target_id):
        return _event("failed", "%s cannot heal that target." % _name(actor_id), actor_id, target_id, 0)
    var before := int(actors[target_id]["hp"])
    actors[target_id]["hp"] = mini(int(actors[target_id]["max_hp"]), before + amount)
    var restored := int(actors[target_id]["hp"]) - before
    return _event("heal", "%s %s %s for %d HP." % [_name(actor_id), verb, _name(target_id), restored], actor_id, target_id, restored)

func _end_round_effects() -> Array[Dictionary]:
    var events: Array[Dictionary] = []
    for id in actors:
        var actor: Dictionary = actors[id]
        if not bool(actor.get("alive", false)) or not bool(actor.get("active", true)):
            continue
        var burn := int(actor.get("burn", 0))
        if burn > 0:
            var damage := 12
            actor["hp"] = maxi(0, int(actor["hp"]) - damage)
            actor["burn"] = burn - 1
            if int(actor["hp"]) <= 0:
                actor["alive"] = false
            events.append(_event("burn", "%s takes %d Burn damage." % [_name(id), damage], id, id, damage))
        actor["slow"] = maxi(0, int(actor.get("slow", 0)) - 3)
    return events

func _cleanup_creator_bound_entities(events: Array[Dictionary]) -> void:
    for id in enemy_ids:
        if not actors.has(id) or not _is_alive(id):
            continue
        var tags: Dictionary = actors[id].get("tags", {})
        var creator_id := str(tags.get("creator_id", ""))
        if creator_id.is_empty():
            continue
        if not _is_alive(creator_id):
            actors[id]["hp"] = 0
            actors[id]["alive"] = false
            events.append(_event("entity_removed", "%s collapses when its creator is incapacitated." % _name(id), creator_id, id, 0))

func _activate_reinforcement_if_needed(events: Array[Dictionary]) -> void:
    var reinforcement_id := "EN_VS_RUIN_SENTINEL_REINFORCEMENT"
    if not actors.has(reinforcement_id) or bool(actors[reinforcement_id].get("active", false)):
        return
    var living_initial := 0
    for id in enemy_ids:
        if id != reinforcement_id and _is_alive(id):
            living_initial += 1
    if living_initial <= 1:
        actors[reinforcement_id]["active"] = true
        events.append(_event("reinforcement", "A Sentinel reinforcement enters the battle.", reinforcement_id, reinforcement_id, 0))

func _consume_card_if_needed(action_id: String) -> void:
    if action_id == "IRON_TESTAMENT":
        _consume_card("CARD_IRON_TESTAMENT")

func _consume_card(card_id: String) -> void:
    card_uses[card_id] = maxi(0, int(card_uses.get(card_id, 0)) - 1)

func card_available(card_id: String) -> bool:
    return int(card_uses.get(card_id, 0)) > 0

func ultimate_available(actor_id: String) -> bool:
    return actor_id == "HERO_CYANIS" and not bool(ultimate_used.get(actor_id, false))

func outcome() -> String:
    if _living_ids(PARTY_BLUE, actors).is_empty():
        return "DEFEAT"
    if _living_ids(ENEMY_RED, actors).is_empty():
        return "VICTORY"
    return "ONGOING"

func _living_ids(team: String, source: Dictionary) -> Array[String]:
    var result: Array[String] = []
    var order: Array[String] = party_ids if team == PARTY_BLUE else enemy_ids
    for id in order:
        if not source.has(id):
            continue
        var actor: Dictionary = source[id]
        if bool(actor.get("alive", false)) and bool(actor.get("active", true)):
            result.append(id)
    return result

func living_party() -> Array[String]:
    return _living_ids(PARTY_BLUE, actors)

func living_enemies() -> Array[String]:
    return _living_ids(ENEMY_RED, actors)

func actor(id: String) -> Dictionary:
    return actors.get(id, {})

func _can_act(id: String) -> bool:
    return actors.has(id) and bool(actors[id].get("alive", false)) and bool(actors[id].get("active", true))

func _is_alive(id: String) -> bool:
    return _can_act(id)

func _name(id: String) -> String:
    return str(actors.get(id, {}).get("name", id))

func _pretty(action_id: String) -> String:
    return action_id.replace("_", " ").capitalize()

func _intent(actor_id: String, action_id: String, target_id: String, family: String, tie_rank: int) -> Dictionary:
    return {
        "actor_id": actor_id,
        "action_id": action_id,
        "target_id": target_id,
        "family": family,
        "priority": 0,
        "tie_rank": tie_rank,
    }

func _event(type: String, text: String, actor_id: String, target_id: String, amount: int) -> Dictionary:
    return {
        "type": type,
        "text": text,
        "actor_id": actor_id,
        "target_id": target_id,
        "amount": amount,
    }
