# extract_glossary_terms.py

import fitz  # PyMuPDF
import re
import json
from pathlib import Path

pdf_path = Path("../data/raw/MagicCompRules 20250404.pdf")
output_path = Path("../data/static/glossary_terms_structured_clean.json")

doc = fitz.open(pdf_path)
lines = []
inside_glossary = False

# Step 1: Extract glossary lines
for page in doc:
    text = page.get_text("text")
    for line in text.split("\n"):
        line = line.strip()
        if not inside_glossary and line.lower().startswith("glossary"):
            inside_glossary = True
        elif inside_glossary and (line.startswith("Credits") or re.match(r"^90\\d\\.", line)):
            inside_glossary = False
            break
        elif inside_glossary:
            lines.append(line)

# Step 2: Extract terms and definitions
glossary = []
current_term = None
buffer = []

for i, line in enumerate(lines):
    is_potential_term = (
        re.match(r"^[A-Z][A-Za-z0-9 '\-]*\.?$", line)
        and not line.startswith("See rule")
        and (i + 1 < len(lines) and lines[i + 1])
    )
    if is_potential_term:
        if current_term and buffer:
            glossary.append({
                "term": current_term,
                "definition": " ".join(buffer).strip()
            })
        current_term = line.rstrip(".").strip()
        buffer = []
    else:
        buffer.append(line)

# Final flush
if current_term and buffer:
    glossary.append({
        "term": current_term,
        "definition": " ".join(buffer).strip()
    })

# Save result
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(glossary, f, indent=2, ensure_ascii=False)

print(f"✅ Extracted {len(glossary)} glossary entries to {output_path}")
