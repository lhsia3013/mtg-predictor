#!/bin/bash

set -e  # Stop immediately if a command fails
echo "🧠 Starting full mechanic extraction pipeline..."

# Step 1: Download full Scryfall card data
echo "📥 Step 1: Downloading full Scryfall data"
python download_scryfall_cards.py

# Step 2: Trim and deduplicate card data
echo "✂️ Step 2: Trimming and deduplicating card data"
python download_trimmed_scryfall_cards.py
python deduplicate_trimmed_scryfall_cards.py

# Step 3: Fetch underdetected mechanic fallback matches
echo "🐛 Step 3: Querying underdetected mechanics"
python scryfall_mechanic_subset_bug.py

# Step 4: Extract canonical keyword abilities/actions from PDF
echo "📘 Step 4: Extracting keyword rules from CompRules"
python extract_clean_split_keyword_ability_rules.py
python extract_clean_split_keyword_action_rules.py

# Step 5: Extract glossary terms from rules
echo "📓 Step 5: Extracting glossary terms"
python extract_glossary_terms.py

# Step 6: Extract ability and flavor word data from Scryfall cards
echo "🧠 Step 6: Extracting ability and flavor words"
python extract_ability_word_card_data.py
python extract_flavor_word_card_data.py

# Step 7: Generate the final ML mechanic list
echo "🏁 Step 7: Generating final mechanic dataset"
python generate_full_mechanics_list.py

echo "✅ Pipeline complete! Output written to: data/static/ml_ready_mechanics.json"
