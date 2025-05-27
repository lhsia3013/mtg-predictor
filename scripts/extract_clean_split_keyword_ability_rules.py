import fitz
import re
import json
from pathlib import Path

# === Paths ===
ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = ROOT / "data" / "raw"
DATA_STATIC = ROOT / "data" / "static"

pdf_path = DATA_RAW / "MagicCompRules 20250404.pdf"
output_path = DATA_STATIC / "keyword_ability_rules_structured_clean.json"

doc = fitz.open(pdf_path)
lines = []

# === Collect 702.* lines only ===
inside = False
for page in doc:
    for line in page.get_text().split("\n"):
        line = line.strip()
        if re.match(r"^702\.\d+\.\s+[A-Z]", line):  # Start of a new keyword
            inside = True
        elif re.match(r"^(703|Glossary|Credits|900|905|708|800|801|710)\.", line):
            inside = False
        if inside or re.match(r"^702\.", line):
            lines.append(line)

# === Helper to flush and format a rule entry ===
def flush(code, buffer):
    if not code or not buffer:
        return None

    entry = {"code": code, "name": None, "subsections": []}
    for line in buffer:
        header = re.match(rf"^{re.escape(code)}\.\s+([A-Z][a-zA-Z \-']+)", line)
        if header:
            entry["name"] = header.group(1).strip()
            continue

        sub = re.match(rf"^{re.escape(code)}[a-z]\s+(.*)", line)
        if sub:
            sub_id = re.match(rf"({re.escape(code)}[a-z])", line).group(1)
            text = sub.group(1).strip()
            entry["subsections"].append({"id": sub_id, "text": text})
        elif entry["subsections"]:
            # Ignore glossary-style lines like: "702.106, “Hidden Agenda.”"
            if re.fullmatch(r"702\.\d{1,3},.*", line):
                continue
            entry["subsections"][-1]["text"] += " " + line.strip()

    return entry if entry["name"] else None

# === Walk lines and build rule entries ===
entries = {}
current_code = None
buffer = []

for line in lines:
    start = re.match(r"^(702\.\d+)\.\s+[A-Z]", line)
    if start:
        if current_code and buffer:
            entry = flush(current_code, buffer)
            if entry:
                entries[current_code] = entry
        current_code = start.group(1)
        buffer = [line]
    else:
        buffer.append(line)

# Final flush
if current_code and buffer:
    entry = flush(current_code, buffer)
    if entry:
        entries[current_code] = entry

# Remove 702.1 (intro paragraph, not a mechanic)
entries.pop("702.1", None)

# Save
output_path.parent.mkdir(parents=True, exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(list(entries.values()), f, indent=2, ensure_ascii=False)

print(f"✅ Extracted and cleaned {len(entries)} keyword ability mechanics into: {output_path}")
