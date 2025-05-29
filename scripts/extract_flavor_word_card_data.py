import json
import re
from pathlib import Path

# === Config ===
CARDS_PATH = Path("../data/raw/scryfall_full_cards.json")
KEYWORDS_PATH = Path("../data/raw/MTGJSON/Keywords.json")

CLEAN_OUT = Path("../data/static/flavor_words_card_level.json")
SORTED_OUT = Path("../data/static/flavor_words_card_level_sorted.json")
REJECTED_OUT = Path("../data/static/flavor_words_rejected.json")

# === Load Data ===
with open(CARDS_PATH, encoding="utf-8") as f:
    cards = json.load(f)

with open(KEYWORDS_PATH, encoding="utf-8") as f:
    keywords_data = json.load(f)["data"]

# === All known mechanic-related words (ability words, keyword abilities, actions)
mechanic_words_set = {
    w.lower()
    for section in ["abilityWords", "keywordAbilities", "keywordActions"]
    for w in keywords_data.get(section, [])
}

# Add manual exclusions if needed (e.g. "visit" missed in JSON)
mechanic_words_set.update({"visit"})

# === Filters
ROMAN_NUMERALS = {"I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"}
COST_PREFIXES = {"sacrifice", "discard", "pay", "exile", "tap", "untap"}

# === Regex for flavor-word-like headers
flavor_header_re = re.compile(r"^([A-Z][\w'’\- /]{1,40})\s*(—|:)\s+")

# === Output holders
cleaned = []
rejected = []

# === Extraction + Cleaning
for card in cards:
    if card.get("set_type", "") == "minigame":
        print(f"Skipping minigame card: {card['name']}")
        continue

    faces = card.get("card_faces", [card])
    for face in faces:
        name = face.get("name", card.get("name", ""))
        oracle = face.get("oracle_text", "")
        if not oracle:
            continue

        for line in oracle.split("\n"):
            stripped = line.strip()
            match = flavor_header_re.match(stripped)
            if not match:
                continue

            candidate = match.group(1).strip()
            candidate_lower = candidate.lower()
            reason = None

            # --- Filtering Logic ---
            if candidate_lower in mechanic_words_set:
                reason = "Mechanic word"
            elif candidate in ROMAN_NUMERALS:
                reason = "Saga chapter numeral"
            elif "{" in match.group(0):
                reason = "Contains mana cost"
            elif candidate.split()[0].lower() in COST_PREFIXES:
                reason = "Starts with cost word"
            elif candidate_lower == name.lower():
                reason = "Matches card name"
            elif len(candidate.split()) > 5:
                reason = "Too many words"
            elif re.search(r"[0-9]", candidate) or re.search(r'[^\w\s\'\-/]', candidate):
                reason = "Contains digits or bad punctuation"
            elif not candidate[0].isupper():
                reason = "Does not start with capital letter"

            if reason:
                rejected.append({**{
                    "card_name": name,
                    "flavor_word": candidate,
                    "full_line": stripped,
                    "oracle_text": oracle
                }, "reject_reason": reason})
            else:
                cleaned.append({
                    "card_name": name,
                    "flavor_word": candidate,
                    "full_line": stripped,
                    "oracle_text": oracle
                })

# === Save Outputs
CLEAN_OUT.parent.mkdir(parents=True, exist_ok=True)

with open(CLEAN_OUT, "w", encoding="utf-8") as f:
    json.dump(cleaned, f, indent=2, ensure_ascii=False)

with open(SORTED_OUT, "w", encoding="utf-8") as f:
    json.dump(sorted(cleaned, key=lambda x: (x["flavor_word"].lower(), x["card_name"].lower())), f, indent=2, ensure_ascii=False)

with open(REJECTED_OUT, "w", encoding="utf-8") as f:
    json.dump(rejected, f, indent=2, ensure_ascii=False)

# === Report
print(f"✅ Extracted {len(cleaned)} cleaned flavor word entries")
print(f"❌ Rejected {len(rejected)} entries → {REJECTED_OUT.name}")
