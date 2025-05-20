import requests
import json
from pathlib import Path

# Get the bulk data index
bulk_info = requests.get("https://api.scryfall.com/bulk-data").json()

# Find the default_cards entry
default_entry = next(item for item in bulk_info["data"] if item["type"] == "default_cards")
download_url = default_entry["download_uri"]

print(f"📥 Downloading from {download_url}")
response = requests.get(download_url)

# Save full card data (list of dicts)
raw_cards = response.json()
output_path = Path("data/raw/scryfall_full_cards.json")
output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(raw_cards, f, indent=2)

print(f"✅ Saved full Scryfall card data to {output_path}")
