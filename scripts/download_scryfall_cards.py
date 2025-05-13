import requests
import pandas as pd

print("Downloading Scryfall bulk data...")
url = "https://api.scryfall.com/bulk-data"
bulk_list = requests.get(url).json()["data"]
default_cards_url = next(item for item in bulk_list if item["type"] == "default_cards")["download_uri"]

print("Fetching full card list...")
cards = requests.get(default_cards_url).json()

print(f"Total cards downloaded: {len(cards)}")

filtered = []
for card in cards:
    filtered.append({
        "name": card.get("name"),
        "mana_cost": card.get("mana_cost"),
        "cmc": card.get("cmc"),
        "type_line": card.get("type_line"),
        "oracle_text": card.get("oracle_text"),
        "colors": card.get("colors"),
        "set": card.get("set_name"),
        "rarity": card.get("rarity"),
        "released_at": card.get("released_at"),
        "artist": card.get("artist"),
        "image_url": card.get("image_uris", {}).get("normal", None)
    })

df = pd.DataFrame(filtered)
df.to_csv("scryfall_cards.csv", index=False)
print("Saved to scryfall_cards.csv")
