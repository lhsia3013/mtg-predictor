import requests
from bs4 import BeautifulSoup
import json

URL = "https://en.wikipedia.org/wiki/List_of_Magic:_The_Gathering_keywords"
response = requests.get(URL)
soup = BeautifulSoup(response.text, "lxml")

print("Page title:", soup.title.string)

# Optional: save full HTML for manual inspection
with open("wiki_dump.html", "w") as f:
    f.write(soup.prettify())

# Look at all tables and try to parse mechanic-like content
mechanics = []
tables = soup.find_all("table")
print(f"🔍 Found {len(tables)} total tables")

for i, table in enumerate(tables):
    rows = table.find_all("tr")
    if len(rows) < 2:
        continue

    print(f"\n=== Table {i+1} ===")
    for row in rows[1:4]:  # print first 3 data rows
        cells = row.find_all("td")
        cell_texts = [c.get_text(strip=True) for c in cells]
        print("  →", cell_texts)


    # Peek into first cell of first real row to guess if this is a mechanic table
    first_row = rows[1].find_all("td")
    if len(first_row) >= 2 and "damage" in first_row[1].text.lower():
        print(f"✅ Table {i+1} looks like mechanics!")

    for row in rows[1:]:
        cells = row.find_all("td")
        if len(cells) < 2:
            continue

        name = cells[0].get_text(strip=True)
        text = cells[1].get_text(strip=True)

        if not name or len(name) > 40:
            continue

        mechanics.append({
            "name": name,
            "type": "keyword",  # Placeholder
            "category": None,
            "rules_text": text,
            "regex": None
        })

# Save output
with open("mechanics_full_scraped.json", "w") as f:
    json.dump(mechanics, f, indent=2)

print(f"\n✅ Scraped {len(mechanics)} mechanics to mechanics_full_scraped.json")
if mechanics:
    print(json.dumps(mechanics[:5], indent=2))
