import json
from pathlib import Path

# === Paths ===
CARDS_PATH = Path("../data/raw/scryfall_full_cards.json")
KEYWORDS_PATH = Path("../data/raw/MTGJSON/Keywords.json")
FLAT_OUT = Path("../data/static/ability_words_card_level.json")
SORTED_OUT = Path("../data/static/ability_words_card_level_sorted.json")

# === Load Scryfall cards and MTGJSON Keywords ===
with open(CARDS_PATH, encoding="utf-8") as f:
    cards = json.load(f)

with open(KEYWORDS_PATH, encoding="utf-8") as f:
    keywords_data = json.load(f)["data"]

# Get list of official ability words (e.g. Landfall, Morbid)
ability_words_set = {w.lower() for w in keywords_data["abilityWords"]}

# === Scan cards for ability words ===
entries = []

for card in cards:
    # Use faces for double-faced cards
    faces = card.get("card_faces", [card])
    for face in faces:
        oracle = face.get("oracle_text", "")
        name = face.get("name", card.get("name", ""))
        if not oracle:
            continue
        for line in oracle.split("\n"):
            stripped = line.strip()
            # Match lines like "Landfall — Whenever a land..."
            if stripped.endswith(":") or "—" in stripped:
                header = stripped.split("—")[0].replace(":", "").strip()
                if header.lower() in ability_words_set:
                    entries.append({
                        "card_name": name,
                        "ability_word": header.title(),
                        "full_line": stripped,
                        "oracle_text": oracle
                    })

# === Write Outputs ===
FLAT_OUT.parent.mkdir(parents=True, exist_ok=True)

# Raw output
with open(FLAT_OUT, "w", encoding="utf-8") as f:
    json.dump(entries, f, indent=2, ensure_ascii=False)

# Sorted for human readability
sorted_entries = sorted(entries, key=lambda x: (x["ability_word"].lower(), x["card_name"].lower()))
with open(SORTED_OUT, "w", encoding="utf-8") as f:
    json.dump(sorted_entries, f, indent=2, ensure_ascii=False)

# === Summary ===
print(f"✅ Saved {len(entries)} ability word entries")
print(f"📁 Unsorted: {FLAT_OUT.name}")
print(f"📁 Sorted:   {SORTED_OUT.name}")
