import json
import pandas as pd
from datetime import datetime, timedelta
import os

# ------------------------------------------------
# CONFIGURATION
# ------------------------------------------------
INPUT_JSON = "words.json"
OUTPUT_JSON = "words.json"     # overwrite
START_DATE = "2025-12-11"
SERIAL_WIDTH = 5               # 00001 → supports up to 99,999
CATEGORY_PREFIX_MAP = {
    "english": "EN",
    "coding": "COD"
}

print("🚀 Script started")

# ------------------------------------------------
# Load JSON
# ------------------------------------------------
print("📂 Working directory:", os.getcwd())
print("📄 words.json exists:", os.path.exists(INPUT_JSON))

with open(INPUT_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

words = data.get("words", [])
print("📦 Original entries:", len(words))

# ------------------------------------------------
# Normalize JSON → DataFrame
# ------------------------------------------------
df = pd.json_normalize(words)
print("📊 DataFrame shape:", df.shape)

# ------------------------------------------------
# Deduplication (case-insensitive word key)
# ------------------------------------------------
df["word_key"] = (
    df["word_anglicized"]
    .str.lower()
    .str.strip()
)

df = (
    df.sort_values("date", na_position="last")
      .drop_duplicates(subset=["word_key"], keep="first")
      .drop(columns=["word_key"])
      .reset_index(drop=True)
)

print("🧹 After dedupe:", df.shape)

# ------------------------------------------------
# Regenerate IDs & Dates
# ------------------------------------------------
start_date = datetime.strptime(START_DATE, "%Y-%m-%d")
rebuilt_words = []

for idx, row in df.iterrows():
    current_date = start_date + timedelta(days=idx)

    category = row["category"]
    prefix = CATEGORY_PREFIX_MAP.get(category)

    if not prefix:
        raise ValueError(f"❌ Unknown category '{category}' — add it to CATEGORY_PREFIX_MAP")

    serial = str(idx + 1).zfill(SERIAL_WIDTH)

    rebuilt_words.append({
        "id": f"{current_date.strftime('%Y%m%d')}-{prefix}-{serial}",
        "date": current_date.strftime("%Y-%m-%d"),
        "category": category,
        "type": row["type"],
        "tags": row["tags"],
        "word_anglicized": row["word_anglicized"],
        "word_native": row["word_native"],
        "image_url": row["image_url"],
        "content_payload": {
            "definition": row["content_payload.definition"],
            "example_sentence": row["content_payload.example_sentence"],
            "image_prompt": row["content_payload.image_prompt"]
        }
    })

# ------------------------------------------------
# Write back JSON (overwrite)
# ------------------------------------------------
final_json = {
    "version": data.get("version", 1),
    "words": rebuilt_words
}

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(final_json, f, ensure_ascii=False, indent=2)

print(f"✅ Overwritten '{OUTPUT_JSON}' with {len(rebuilt_words)} entries")
