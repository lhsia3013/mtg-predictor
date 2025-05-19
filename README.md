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
│   ├── raw/              → Scryfall raw card data
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
pip install pandas requests tqdm notebook sentence-transformers beautifulsoup4 lxmlpip install pandas requests tqdm notebook sentence-transformers
```

### Launch Jupyter

```bash
jupyter notebook
```

---

## ✅ Current Progress

- ✅ Downloaded full card dataset from Scryfall  
- ✅ Built `mechanics_full.json` with 20+ structured mechanics (type, rules, regex, category)  
- ✅ Parsed `oracle_text` using regex to extract mechanics  
  → Output: `data/processed/parsed_cards.csv`  
- ✅ Enriched parsed data with additional metadata (colors, cmc, type, rarity, etc.)  
  → Output: `data/processed/enriched_cards.csv`  
- ✅ Embedded `oracle_text` using Sentence Transformers (`all-MiniLM-L6-v2`)  
  → Output: `data/processed/text_embeddings.npy`  
- ✅ Visualized oracle text embeddings with UMAP, clustered by metadata (color, type, rarity, CMC, etc.)
  → Output: `visualizations/umap_by_card_type, *by_cmc, *by_color, *by_color_identity, *by_mechanic_count, *by_rarity, *by_set`

- 🔜 Next: Expand `mechanics_full.json` to full mechanic set (~300 entries)  
- 🔜 Next: Train initial multi-label mechanic predictor from oracle text embeddings  
- 🔜 Next: Build similarity search tool using vector space + metadata

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
