import requests
import json

search_terms = {
    "aftermath": 'o:"aftermath"',
    "convert": 'o:"convert"',
    "living metal": 'o:"living metal"',
    "More Than Meets the Eye": 'keyword:"more than meets the eye"',
    "endure": 'o:"endure"',
    "daybound": 'keyword:daybound',
    "nightbound": 'keyword:nightbound'
}

results = {}

for label, query in search_terms.items():
    url = f"https://api.scryfall.com/cards/search?q={query}"
    print(f"🔍 Querying: {query}")
    cards = []

    while url:
        response = requests.get(url)
        data = response.json()
        if "data" not in data:
            print(f"❌ Failed: {data.get('details')}")
            break
        cards.extend(data["data"])
        url = data.get("next_page")

    results[label.lower()] = cards
    print(f"✅ Found {len(cards)} cards for '{label}'")

with open("../data/static/scryfall_subset_patch.json", "w") as f:
    json.dump(results, f, indent=2)

print("✅ Saved patch data to scryfall_subset_patch.json")
