import json
import re
from collections import defaultdict
from pathlib import Path

# === Paths ===
ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = ROOT / "data" / "raw"
DATA_STATIC = ROOT / "data" / "static"

cards_path = DATA_RAW / "scryfall_full_cards.json"
rules_path = DATA_STATIC / "keyword_rules_structured_clean.json"
output_path = DATA_STATIC / "mechanics_full.json"

# === Load input files ===
with open(cards_path, "r", encoding="utf-8") as f:
    cards = json.load(f)

with open(rules_path, "r", encoding="utf-8") as f:
    keyword_rules = json.load(f)

# === Count keyword usage from card data ===
keyword_counts = defaultdict(int)
for card in cards:
    for kw in card.get("keywords", []):
        keyword_counts[kw.strip().lower()] += 1

# === Merge mechanics ===
mechanics = []

for entry in keyword_rules:
    name = entry["name"].strip()
    name_lc = name.lower()

    subsections = entry.get("subsections", [])
    rules_text = "\n".join(s["text"].strip() for s in subsections)

    mechanics.append({
        "name": name,
        "type": "keyword_ability",  # all 702.x entries are keyword abilities
        "category": None,
        "rules_text": rules_text,
        "regex": rf"\b{re.escape(name_lc)}\b",
        "subsections": subsections,
        "card_count": keyword_counts.get(name_lc, 0)
    })

# === Save output ===
output_path.parent.mkdir(parents=True, exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(mechanics, f, indent=2, ensure_ascii=False)

print(f"✅ Final enriched mechanics saved to {output_path}")
