# MTG Card Predictor

An ML/CV research project to analyze and predict future Magic: The Gathering cards using historical card data, rules text, design patterns, and artwork.

---

## Project Goals

- Predict likely mechanics, themes, and card types for future sets  
- Parse and model MTG rules text to classify or generate new cards  
- Analyze trends in set design (color balance, power creep, mechanics cycles)  
- Match or generate art aligned with card concept and theme  
- Combine all components into a prototype predictive engine

---

## Project Structure

```plaintext
mtg-predictor/
├── data/                 
│   ├── raw/              → Scryfall raw card data, MTGJSON Keywords List
│   ├── processed/        → Parsed & enriched CSVs and embeddings
│   └── static/           → mechanics_full.json
├── notebooks/            → Jupyter notebooks for exploration
├── scripts/              → Python utilities and future scraping tools
├── models/               → Trained model files
├── visualizations/       → Charts, UMAPs, similarity maps
├── venv/                 → Local Python environment (excluded)
└── README.md
```

---

## Setup Instructions

### Requirements

- Python 3.10+
- pip
- virtualenv (recommended)

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
# Initial Setup and Dummy Mechanics List
- ✅ Downloaded full card dataset from Scryfall  
→ Output: `data/processed/scryfall_cards.csv`  
- ✅ Built `mechanics_full.json` with 20+ structured mechanics (type, rules, regex, category)  
- ✅ Parsed `oracle_text` using regex to extract mechanics  
  → Output: `data/processed/parsed_cards.csv`  
- ✅ Enriched parsed data with additional metadata (colors, cmc, type, rarity, etc.)  
  → Output: `data/processed/enriched_cards.csv`  
- ✅ Embedded `oracle_text` using Sentence Transformers (`all-MiniLM-L6-v2`)  
  → Output: `data/processed/text_embeddings.npy`  
- ✅ Visualized oracle text embeddings with UMAP, clustered by metadata (color, type, rarity, CMC, etc.)  
  → Output: `visualizations/umap_by_card_type, *by_cmc, *by_color, *by_color_identity, *by_mechanic_count, *by_rarity, *by_set`  

### Comprehensive Mechanic & Flavor Rules Extraction
- ✅ Downloaded and cleaned full card dataset from Scryfall  
  → Output: `data/raw/scryfall_full_cards.json`  
- ✅ Parsed and structured canonical **keyword abilities** from `MagicCompRules.pdf`  
  → Output: `data/static/keyword_ability_rules_structured_clean.json`  
- ✅ Parsed and structured canonical **keyword actions** from `MagicCompRules.pdf`  
  → Output: `data/static/keyword_action_rules_structured_clean.json`  
- ✅ Extracted and filtered **ability word** examples from Scryfall cards  
  → Output: `data/static/ability_words_card_level.json`  
- ✅ Extracted and cleaned **flavor word** examples (stylized headers)  
  → Output:  
    ✔ `flavor_words_card_level_cleaned.json`  
    ✔ `flavor_words_card_level_cleaned_sorted.json`  
    ✖ `flavor_words_rejected.json` (logged exclusions for transparency)
- ✅ Loaded **mechanic definitions** from MTGJSON’s `Keywords.json` and used to filter invalid matches in all extractions

### 🔜 Next Steps

- ✅ Rebuild full **mechanic list** from:
  - `keyword_ability_rules_structured_clean.json`
  - `keyword_action_rules_structured_clean.json`
  - `ability_words_card_level.json`  
  → Output: `data/static/mechanics_full.json`

- Refactor core notebooks for updated mechanic pipeline:  
  → `0_parsing_mechanics.ipynb` — rebuild mechanic list  
  → `1_feature_engineering.ipynb` — token features, span extraction  
  → `2_text_embeddings.ipynb` — generate oracle text embeddings  
  → `3_umap_visualization.ipynb` — project and explore embedding space

- Train first **multi-label mechanic classifier** using oracle text embeddings  
  → Predict keyword/mechanic tags per card

- Build **semantic similarity search** with FAISS or cosine distance  
  → Input: oracle text  
  → Output: closest matching cards + mechanic tags

- Begin conditioning **card generation** on theme + mechanic structure  
  → Use extracted data to influence flavor word use, mechanic choice, etc.

---

## Git & Dev Notes

- `.gitignore` excludes:
  - `venv/`
  - `data/`
  - `.ipynb_checkpoints/`

- Pre-commit hook is configured in `.git/hooks/pre-commit` to strip output cells from notebooks before commit:

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

To activate the hook:

```bash
chmod +x .git/hooks/pre-commit
```

---

## 📦 External Data Sources

### MTGJSON: Keywords.json

This project uses mechanic definitions from [MTGJSON](https://mtgjson.com/), specifically the `Keywords.json` file.

To obtain it:

```bash
curl -O https://mtgjson.com/api/v5/Keywords.json


---

## Optional Setup Enhancements

### Enable tqdm Progress Bars in Jupyter

```bash
pip install ipywidgets
```

### UMAP Visualization Requirements

To run `3_umap_visualization.ipynb`, install:

```bash
pip install umap-learn seaborn
```

### Notes on Running Notebooks

All notebooks are expected to be run from within the `notebooks/` folder.  
If run from another path, you may need to adjust relative references to `../data/processed/`.

---
