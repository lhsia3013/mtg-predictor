import json
from pathlib import Path

# === Load JSON data
def load_json(path):
    with open(path) as f:
        return json.load(f)

# === Load cleaned goldilocks-deduped card data
scryfall_cards = load_json("../data/raw/scryfall_goldilocks_deduped.json")
keyword_abilities = load_json("../data/static/keyword_ability_rules_structured_clean.json")
keyword_actions = load_json("../data/static/keyword_action_rules_structured_clean.json")
glossary_terms = load_json("../data/static/glossary_terms_structured_clean.json")
ability_words = load_json("../data/static/ability_words_card_level.json")
flavor_words = load_json("../data/static/flavor_words_card_level.json")

# === Build oracle index (for fast mechanic text matching)
oracle_index = []
for card in scryfall_cards:
    if "oracle_text" in card:
        oracle_index.append({
            "name": card["name"],
            "oracle": card["oracle_text"]
        })
    elif "card_faces" in card:
        for face in card["card_faces"]:
            if face.get("oracle_text"):
                oracle_index.append({
                    "name": face["name"],
                    "oracle": face["oracle_text"]
                })

# === Phrase matcher (lowercased, newline-stripped phrase matching)
def normalize(text):
    return text.lower().replace('\n', ' ').replace('—', '-').strip()

def get_card_matches(mechanic_name):
    target = normalize(mechanic_name)
    return [
        entry["name"]
        for entry in oracle_index
        if target in normalize(entry["oracle"])
    ]

# === Output container
ml_mechanics = []

# === Add rule-backed mechanics
def add_rulebacked(entry, type_):
    name = entry["name"]
    rule = entry.get("code")
    definition = " ".join(sub["text"] for sub in entry.get("subsections", []))
    cards = get_card_matches(name)
    ml_mechanics.append({
        "name": name,
        "type": type_,
        "rule_code": rule,
        "definition": definition.strip(),
        "oracle_phrase_match": name.lower(),
        "card_count": len(cards),
        "cards": cards[:10]
    })

# === Add keyword abilities and actions
for entry in keyword_abilities:
    add_rulebacked(entry, "Keyword Ability")

for entry in keyword_actions:
    add_rulebacked(entry, "Keyword Action")

# === Ability Words (from Scryfall usage)
ability_word_map = {}
for entry in ability_words:
    ability_word_map.setdefault(entry["ability_word"], []).append(entry["card_name"])

for name, cards in ability_word_map.items():
    ml_mechanics.append({
        "name": name,
        "type": "Ability Word",
        "rule_code": None,
        "definition": "Ability words appear in italics at the beginning of an ability and have no rules meaning.",
        "oracle_phrase_match": name.lower(),
        "card_count": len(cards),
        "cards": cards[:10]
    })

# === Flavor Words (from Scryfall usage)
flavor_word_map = {}
for entry in flavor_words:
    flavor_word_map.setdefault(entry["flavor_word"], []).append(entry["card_name"])

for name, cards in flavor_word_map.items():
    ml_mechanics.append({
        "name": name,
        "type": "Flavor Word",
        "rule_code": None,
        "definition": "Flavor words appear in italics before a rule line and are purely descriptive with no rules meaning.",
        "oracle_phrase_match": name.lower(),
        "card_count": len(cards),
        "cards": cards[:10]
    })

# === Glossary Terms (filtered to only those appearing in cards)
oracle_text_blob = " ".join(normalize(c["oracle"]) for c in oracle_index)

for entry in glossary_terms:
    name = entry["term"]
    if name.lower() in oracle_text_blob:
        cards = get_card_matches(name)
        ml_mechanics.append({
            "name": name,
            "type": "Glossary Term",
            "rule_code": None,
            "definition": entry["definition(s)"],
            "oracle_phrase_match": name.lower(),
            "card_count": len(cards),
            "cards": cards[:10]
        })

# === Save output
output_path = Path("../data/static/ml_ready_mechanics.json")
output_path.parent.mkdir(parents=True, exist_ok=True)
with open(output_path, "w") as f:
    json.dump(ml_mechanics, f, indent=2)

print(f"✅ Saved {len(ml_mechanics)} mechanics to {output_path}")
