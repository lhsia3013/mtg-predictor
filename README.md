# 🧠 MTG Card Predictor

A machine learning and computer vision research project to generate future themed Magic: The Gathering cards using historical card data, structured rules text, design patterns, and artwork.

---

## 🎯 Project Goals

- Generate **mechanics**, **themes**, and **card types** for future sets  
- Parse and model MTG **rules text** to classify or generate new cards  
- Analyze trends in **set design** (color balance, power creep, mechanic cycles)  
- Match or generate **artwork** aligned with card concepts  
- Combine all components into a prototype **predictive engine**

---

## 🗂️ Project Structure

```plaintext
mtg-predictor/
├── data/
│   ├── raw/              # Scryfall raw card data, MTGJSON keyword files
│   ├── processed/        # Parsed & enriched CSVs and embeddings
│   └── static/           # Structured rule-based mechanic definitions
├── notebooks/            # Jupyter notebooks for parsing, modeling, visualization
├── scripts/              # Python utilities and scraping tools
├── models/               # Trained ML model files
├── visualizations/       # UMAPs, charts, similarity maps
├── venv/                 # Python virtual environment (excluded via .gitignore)
└── README.md
```

---

## ⚙️ Setup Instructions

### Prerequisites

- Python 3.10+
- `pip`
- `virtualenv` (recommended)

### Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install pandas requests tqdm notebook sentence-transformers pymupdf
```

### Launch Jupyter

```bash
jupyter notebook
```

---

## ✅ Current Progress

### 📌 Initial Setup & Embedding Pipeline

- ✅ Downloaded card dataset from Scryfall  
  → `data/processed/scryfall_cards.csv`  
- ✅ Built `mechanics_full.json` with 20+ structured mechanics  
- ✅ Parsed `oracle_text` using regex  
  → `data/processed/parsed_cards.csv`  
- ✅ Enriched card data with metadata (color, CMC, type, rarity...)  
  → `data/processed/enriched_cards.csv`  
- ✅ Embedded `oracle_text` with `all-MiniLM-L6-v2`  
  → `data/processed/text_embeddings.npy`  
- ✅ Visualized embeddings with UMAP by metadata clusters  
  → `visualizations/umap_by_*`

---

### 🔁 Full Mechanics Extraction Pipeline

This pipeline transforms Scryfall card data and the official Magic Comprehensive Rules into a machine-learning-ready list of mechanics, each tied to example cards, rule definitions, and mechanic types.

&nbsp;

| Stage | Script | Purpose | Output |
|-------|--------|---------|--------|
| 🧱 Download | `download_scryfall_cards.py` | Downloads full Scryfall default_cards set | `scryfall_full_cards.json` |
| ✂️ Trim | `download_trimmed_scryfall_cards.py` | Extracts only ML-relevant fields from raw Scryfall data | `scryfall_cards_trimmed_for_ml.json` |
| 🧼 Deduplicate | `deduplicate_trimmed_scryfall_cards.py` | Deduplicates by oracle identity (keeps alt arts/flavor) | `scryfall_cards_deduplicated_for_ml.json` |

---

#### 📘 Rule Parsing

&nbsp;

| Script | Purpose | Output |
|--------|---------|--------|
| `extract_clean_split_keyword_ability_rules.py` | Parses 702.* Keyword Abilities from CompRules PDF | `keyword_ability_rules_structured_clean.json` |
| `extract_clean_split_keyword_action_rules.py` | Parses 701.* Keyword Actions | `keyword_action_rules_structured_clean.json` |
| `extract_glossary_terms.py` | Extracts glossary terms and definitions | `glossary_terms_structured_clean.json` |

---

#### 🧠 Word Extraction

&nbsp;

| Script | Purpose | Output |
|--------|---------|--------|
| `extract_ability_word_card_data.py` | Extracts italicized ability word lines from oracle text | `ability_words_card_level.json` |
| `extract_flavor_word_card_data.py` | Extracts and filters flavor words | `flavor_words_card_level.json`, `flavor_words_rejected.json` |

---

#### 🐛 Manual Fallbacks for Under-Detected Mechanics

&nbsp;

| Script | Purpose | Output |
|--------|---------|--------|
| `scryfall_mechanic_subset_bug.py` | Patches edge cases like "convert", "endure", etc. | `scryfall_subset_patch.json` |

---

#### 🧠 Final Mechanic Generation

&nbsp;

| Script | Purpose | Output |
|--------|---------|--------|
| `generate_full_mechanics_list.py` | Combines all structured inputs into a clean ML dataset | `ml_ready_mechanics.json` |

---

### ▶️ Running the Full Mechanic Extraction Pipeline

To regenerate all structured rule data and the final `ml_ready_mechanics.json`, run:

```bash
cd scripts
./run_full_mechanic_pipeline.sh

---

## 🔮 Next Steps

- 🧱 Refactor and re-run:
  - `0_parsing_mechanics.ipynb` – now uses clean output
  - `1_feature_engineering.ipynb` – spans and token match updates
  - `2_text_embeddings.ipynb` – retrain with clean oracle text inputs
  - `3_umap_visualization.ipynb` – regenerate UMAPs with mechanic overlays

- 🧠 Train first **multi-label classifier**  
  → Input: text embeddings  
  → Output: predicted mechanics

- 🔎 Build **semantic mechanic search** with FAISS  
  → Input: oracle text  
  → Output: similar cards / tags

- 🧪 Consider reprocessing **reminder text exclusions**  
  → Separate embedded rules from "hints" and test impact

- 🧙 Begin early **card generation prototype**  
  → Condition on themes + predicted mechanics  
  → Output: name, type, rules text, flavor

---

## 🛠️ Git & Dev Notes

### Gitignore

`.gitignore` excludes:
- `venv/`
- `data/`
- `.ipynb_checkpoints/`

### Pre-commit Hook (Strip Notebook Outputs)

Create a `.git/hooks/pre-commit` file with the following:

```bash
#!/bin/bash
export PATH="$PWD/venv/bin:$PATH"
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.ipynb$')
[ -z "$STAGED_FILES" ] && exit 0
for file in $STAGED_FILES; do
  venv/bin/jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace "$file"
  git add "$file"
done
```

Make it executable:

```bash
chmod +x .git/hooks/pre-commit
```

---

## 📦 External Data Sources

### Scryfall Full Card Data
Scryfall card list and full meta data

Download with Python script:

```bash
python3 download_scryfall_cards.py
```

### MTG Comprehensive Rules
Used to extract canonical definitions for mechanics reference.

Download manually from the official WOTC page:
📄 https://magic.wizards.com/en/rules

```bash
File used: MagicCompRules 20250404.pdf
Place in: data/raw/
```

### MTGJSON: Keywords.json

Used for structured mechanic definitions and filtering.

Download with:

```bash
curl -O https://mtgjson.com/api/v5/Keywords.json
```

---

## 🧪 Optional Enhancements

### Enable `tqdm` in Jupyter

```bash
pip install ipywidgets
```

### UMAP Visualization Dependencies

```bash
pip install umap-learn seaborn
```

---

## 📝 Notebook Execution Notes

All notebooks are expected to be run from the `notebooks/` directory.  
If run elsewhere, adjust relative paths (e.g. `../data/processed/`).

---
