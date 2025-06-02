import json
import re
from pathlib import Path

# === Paths ===
STATIC = Path("../data/static")
RAW = Path("../data/raw/scryfall_cards_deduplicated_for_ml.json")

# === Helpers ===
def load_json(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def normalize(text):
    return text.lower().replace("\n", " ").replace("—", "-").strip()

# === Load inputs ===
scryfall = load_json(RAW)
keyword_abilities = load_json(STATIC / "keyword_ability_rules_structured_clean.json")
keyword_actions = load_json(STATIC / "keyword_action_rules_structured_clean.json")
glossary = load_json(STATIC / "glossary_terms_structured_clean.json")
ability_words = load_json(STATIC / "ability_words_card_level.json")
flavor_words = load_json(STATIC / "flavor_words_card_level.json")
subset_patch = load_json(STATIC / "scryfall_subset_patch.json")

# === Build Oracle text index ===
oracle_index = []
for card in scryfall:
    if "oracle_text" in card:
        oracle_index.append({"name": card["name"], "oracle": card["oracle_text"]})
    elif "card_faces" in card:
        for face in card["card_faces"]:
            if face.get("oracle_text"):
                oracle_index.append({"name": face["name"], "oracle": face["oracle_text"]})
oracle_blob = " ".join(normalize(c["oracle"]) for c in oracle_index)

# === Manual match overrides ===
manual_match_terms = {
    "tap and untap": ["tap", "untap"],
    "daybound and nightbound": ["daybound", "nightbound"],
    "endure": ["endure"],
    "convert": ["convert"]
}

# === Matching logic ===
def get_card_matches(name):
    name_lc = name.lower().strip()
    terms = manual_match_terms.get(name_lc, [name_lc])
    matches = set()

    # 1. Regex search in oracle text
    for term in terms:
        pat = re.compile(rf"(?<!\w){re.escape(term)}(?!\w)", re.IGNORECASE)
        for entry in oracle_index:
            if pat.search(normalize(entry["oracle"])):
                matches.add(entry["name"])
    if matches:
        return list(matches)

    # 2. Subset patch fallback
    fallback = subset_patch.get(name_lc)
    if fallback:
        return [c["name"] if isinstance(c, dict) else c for c in fallback]

    # 3. Special combined case
    if name_lc == "daybound and nightbound":
        merged = []
        for t in ["daybound", "nightbound"]:
            merged += subset_patch.get(t, [])
        return list({c["name"] if isinstance(c, dict) else c for c in merged})

    return []

# === Mechanic builder ===
all_mechanics = []

def get_def(entry):
    if "subsections" in entry and entry["subsections"]:
        return " ".join(s.get("text", "") for s in entry["subsections"]).strip()
    return entry.get("text", "").strip()

def add(entry, type_):
    name = entry.get("name") or entry.get("term")
    rule = entry.get("code")
    definition = get_def(entry) or f"{name} is a {type_.lower()} in Magic: The Gathering."
    cards = get_card_matches(name)
    all_mechanics.append({
        "name": name,
        "type": type_,
        "rule_code": rule,
        "definition": definition,
        "oracle_phrase_match": name.lower(),
        "card_count": len(cards),
        "cards": cards[:10]
    })

for e in keyword_abilities:
    add(e, "Keyword Ability")
for e in keyword_actions:
    add(e, "Keyword Action")

def add_words(source, key, label, desc):
    word_map = {}
    for entry in source:
        word = entry[key].strip().title()
        word_map.setdefault(word, []).append(entry["card_name"])
    for word, cards in word_map.items():
        all_mechanics.append({
            "name": word,
            "type": label,
            "rule_code": None,
            "definition": desc,
            "oracle_phrase_match": word.lower(),
            "card_count": len(cards),
            "cards": list(set(cards))[:10]
        })

add_words(ability_words, "ability_word", "Ability Word",
          "Ability words appear in italics at the beginning of an ability and have no rules meaning.")
add_words(flavor_words, "flavor_word", "Flavor Word",
          "Flavor words appear in italics before a rule line and are purely descriptive.")

# === Glossary additions ===
for entry in glossary:
    name = entry.get("term", "").strip().title()
    definition = entry.get("definition(s)") or entry.get("definitions", "") or f"{name} is a glossary term."
    if re.search(rf"\b{re.escape(name.lower())}\b", oracle_blob):
        cards = get_card_matches(name)
        all_mechanics.append({
            "name": name,
            "type": "Glossary Term",
            "rule_code": None,
            "definition": definition if isinstance(definition, str) else " ".join(definition),
            "oracle_phrase_match": name.lower(),
            "card_count": len(cards),
            "cards": cards[:10]
        })

# === Deduplication logic ===
priority = {
    "Keyword Ability": 0,
    "Keyword Action": 1,
    "Ability Word": 2,
    "Flavor Word": 3,
    "Glossary Term": 4
}
deduped = {}
for mech in all_mechanics:
    name = mech["name"]
    if name not in deduped:
        deduped[name] = mech
    else:
        existing = deduped[name]
        if priority[mech["type"]] < priority[existing["type"]] or \
           (priority[mech["type"]] == priority[existing["type"]] and len(mech["definition"]) > len(existing["definition"])):
            deduped[name] = mech

# === Write output ===
with open(STATIC / "ml_ready_mechanics.json", "w") as f:
    json.dump(list(deduped.values()), f, indent=2)

print(f"✅ Wrote {len(deduped)} deduplicated mechanics to ml_ready_mechanics.json")
