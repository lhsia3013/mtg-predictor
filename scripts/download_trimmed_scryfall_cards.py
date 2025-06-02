import requests
import json
from pathlib import Path

# === Step 1: Download the full "default_cards" Scryfall bulk data set
bulk_index = requests.get("https://api.scryfall.com/bulk-data").json()
bulk_url = next(entry for entry in bulk_index["data"] if entry["type"] == "default_cards")["download_uri"]

print(f"📥 Downloading all card data from: {bulk_url}")
all_cards = requests.get(bulk_url).json()

# === Step 2: Define which fields to keep for ML and generation
def extract_trimmed_fields(card):
    """
    Extract only the fields relevant for ML model training:
    - oracle text and mechanics
    - flavor and visual features
    - basic identity and layout
    """
    trimmed = {
        "name": card["name"],
        "oracle_text": card.get("oracle_text", ""),
        "mana_cost": card.get("mana_cost", ""),
        "type_line": card.get("type_line", ""),
        "keywords": card.get("keywords", []),
        "power": card.get("power"),
        "toughness": card.get("toughness"),
        "loyalty": card.get("loyalty"),
        "flavor_text": card.get("flavor_text", ""),
        "artist": card.get("artist"),
        "illustration_id": card.get("illustration_id"),
        "rarity": card.get("rarity"),
        "set_name": card.get("set_name"),
        "layout": card.get("layout"),
        "produced_mana": card.get("produced_mana", [])
    }

    # Preserve double-faced or modal card faces
    if "card_faces" in card:
        trimmed["card_faces"] = [
            {
                "name": face.get("name"),
                "oracle_text": face.get("oracle_text", ""),
                "mana_cost": face.get("mana_cost", ""),
                "type_line": face.get("type_line", ""),
                "flavor_text": face.get("flavor_text", "")
            }
            for face in card["card_faces"]
        ]

    return trimmed

# === Step 3: Filter and trim each card
cards_for_model = [
    extract_trimmed_fields(card)
    for card in all_cards
    if "oracle_text" in card or "card_faces" in card
]

# === Step 4: Save result
output_dir = Path("../data/raw")
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / "scryfall_cards_trimmed_for_ml.json"

with open(output_file, "w") as f:
    json.dump(cards_for_model, f, indent=2)

print(f"✅ Saved {len(cards_for_model)} cards to {output_file}")
