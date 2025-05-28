# extract_glossary_terms.py

import fitz  # PyMuPDF
import re
import json
from pathlib import Path

pdf_path = Path("../data/raw/MagicCompRules 20250404.pdf")
output_path = Path("../data/static/glossary_terms_structured_clean.json")

doc = fitz.open(pdf_path)

# helper to split numbered definitions like "1. abc 2. xyz"
def split_numbered_defs(def_text):
    parts = re.split(r"\b\d+\.\s+", def_text)
    return parts[1:] if len(parts) > 1 else [def_text]

inside_glossary = False
glossary = []
terms_to_flush = []
buffer = []

# parse glossary from bold spans
for i, page in enumerate(doc):
    page_dict = page.get_text("dict")
    for block in page_dict["blocks"]:
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                if not inside_glossary:
                   font_name = span.get("font", "").lower()
                   is_bold = "bold" in font_name
                   if is_bold and span["text"].strip() == "Abandon":
                       print(f"Found glossary start at page {i}, span: '{span['text']}'")
                       inside_glossary = True
                   else:
                       continue  # skip until we see bolded "Abandon"
                text = span["text"].strip()
                if not text:
                    continue

                font_name = span.get("font", "").lower()
                is_bold = "bold" in font_name

                if not inside_glossary and re.search(r"\bglossary\b", text, re.IGNORECASE):
                    print(f"Entered glossary on page {i}")
                    inside_glossary = True
                    continue
                if inside_glossary and text.startswith("Credits"):
                    inside_glossary = False
                    print(f"Exited glossary on page {i}")
                    continue

                if inside_glossary:
                    print(f"Page {i}: '{text}' - Bold={is_bold} - Font={span.get('font', 'N/A')}")
                    if is_bold:
                        if buffer:
                            definition_text = " ".join(buffer).strip()
                            split_defs = split_numbered_defs(definition_text)
                            for term in terms_to_flush:
                                glossary.append({
                                    "term": term,
                                    "definition(s)": split_defs if len(split_defs) > 1 else split_defs[0]
                                })
                                print(f"Added: {term}")
                            terms_to_flush = []
                            buffer = []
                        terms_to_flush.append(text)
                    else:
                        buffer.append(text)

# final flush
if terms_to_flush and buffer:
    definition_text = " ".join(buffer).strip()
    split_defs = split_numbered_defs(definition_text)
    for term in terms_to_flush:
        glossary.append({
            "term": term,
            "definitions": split_defs if len(split_defs) > 1 else split_defs[0]
        })
        print(f"Final Add: {term}")

# write to output JSON
output_path.parent.mkdir(parents=True, exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(glossary, f, indent=2, ensure_ascii=False)

print(f"✅ Extracted {len(glossary)} glossary terms to {output_path}")
