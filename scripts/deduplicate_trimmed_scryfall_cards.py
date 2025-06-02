import json
from pathlib import Path

# === Step 1: Load trimmed (full printing) card set
with open("../data/raw/scryfall_cards_trimmed_for_ml.json") as f:
    all_cards = json.load(f)

# === Step 2: Deduplicate cards by rules identity, keeping alt art/flavor
def deduplicate_by_rules(cards):
    seen = {}
    deduped = []

    for card in cards:
        key = (
            card["name"],
            card.get("oracle_text", ""),
            card.get("mana_cost", ""),
            card.get("type_line", ""),
            card.get("layout", "")
        )

        if key not in seen:
            seen[key] = card
            deduped.append(card)
        else:
            existing = seen[key]
            if card.get("flavor_text") != existing.get("flavor_text") or \
               card.get("illustration_id") != existing.get("illustration_id"):
                deduped.append(card)

    return deduped

deduped_cards = deduplicate_by_rules(all_cards)

# === Step 3: Save result
output_path = Path("../data/raw/scryfall_cards_deduplicated_for_ml.json")
with open(output_path, "w") as f:
    json.dump(deduped_cards, f, indent=2)

print(f"✅ Deduplicated: reduced from {len(all_cards)} → {len(deduped_cards)} cards")
print(f"📁 Saved to {output_path}")
