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

### 📘 Rule-Based Mechanic & Flavor Word Extraction
- ✅ Downloaded card dataset with full metadata from Scryfall  
  → `data/processed/scryfall_full_cards.csv`  
- ✅ Parsed canonical **keyword abilities** from `MagicCompRules.pdf`  
  → `data/static/keyword_ability_rules_structured_clean.json`  
- ✅ Parsed **keyword actions** from `MagicCompRules.pdf`  
  → `data/static/keyword_action_rules_structured_clean.json`  
- ✅ Loaded mechanic definitions from MTGJSON’s `Keywords.json`  
  → `data/raw/Keywords.json`
- ✅ Extracted **ability word** examples from Scryfall cards using Keywords.json  
  → `data/static/ability_words_card_level.json` 
  → `data/static/ability_words_card_level_sorted.json`   
- ✅ Extracted and cleaned **flavor word** examples using Keywords.json  
  →  
    ✔ `flavor_words_card_level_cleaned.json`  
    ✔ `flavor_words_card_level_cleaned_sorted.json`  
    ✖ `flavor_words_rejected.json` (logged exclusions)  

---

## 🔮 Next Steps

- ✅ Rebuild **mechanic list** from:
  - `keyword_ability_rules_structured_clean.json`
  - `keyword_action_rules_structured_clean.json`
  - `ability_words_card_level.json`  
  → `data/static/mechanics_full.json`

- Refactor core notebooks:
  - `0_parsing_mechanics.ipynb` – regenerate mechanic list  
  - `1_feature_engineering.ipynb` – token-level features and spans  
  - `2_text_embeddings.ipynb` – embedding and export  
  - `3_umap_visualization.ipynb` – dimensionality reduction and cluster maps

- Train first **multi-label classifier**  
  → Input: oracle text embedding  
  → Output: predicted mechanics

- Build **semantic search** with FAISS or cosine similarity  
  → Input: oracle text  
  → Output: most similar cards and associated tags

- Start prototype **card generation**, conditioned on themes and mechanics  
  → Output: flavor text, card template, and suggested mechanics

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
