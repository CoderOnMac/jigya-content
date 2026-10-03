import json
import os
import csv
import argparse
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description="Extract English word_display from JSON and update master list CSV/XLSX.")
    parser.add_argument("input_json", nargs="?", default="words.json", help="Path to the input JSON file (default: words.json)")
    parser.add_argument("--json", dest="json_flag", help="Alternative path to the input JSON file")
    parser.add_argument("--csv", default="words_master_list.csv", help="Path to the master CSV file (default: words_master_list.csv)")
    parser.add_argument("--xlsx", default="words_master_list.xlsx", help="Path to the master XLSX file (default: words_master_list.xlsx)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite the master list instead of appending unique new words")
    args = parser.parse_args()

    input_json_path = args.json_flag if args.json_flag else args.input_json

    base_dir = os.path.dirname(os.path.abspath(__file__))
    if not os.path.isabs(input_json_path):
        json_path = os.path.join(base_dir, input_json_path)
    else:
        json_path = input_json_path

    if not os.path.isabs(args.csv):
        csv_path = os.path.join(base_dir, args.csv)
    else:
        csv_path = args.csv

    if not os.path.isabs(args.xlsx):
        xlsx_path = os.path.join(base_dir, args.xlsx)
    else:
        xlsx_path = args.xlsx

    print(f"Reading data from {json_path}...")
    
    # Load JSON data
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {json_path}")
        return
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from {json_path}: {e}")
        return

    # Normalize items list
    items = []
    if isinstance(data, dict) and "words" in data and isinstance(data["words"], list):
        items = data["words"]
    elif isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        items = [data]

    # Extract words from current JSON file
    extracted_words = []
    for item in items:
        try:
            word_display = item["content_payload"]["languages"]["en"]["word_display"]
            if word_display and isinstance(word_display, str):
                extracted_words.append(word_display.strip())
        except KeyError:
            print(f"Warning: Missing 'en' word_display for item with ID: {item.get('id', 'Unknown')}")
            continue

    print(f"Extracted {len(extracted_words)} word(s) from {os.path.basename(json_path)}.")

    existing_words = []
    existing_lower_set = set()

    # If appending and CSV exists, load existing words
    if not args.overwrite and os.path.exists(csv_path):
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader, None)
                for row in reader:
                    if row:
                        word = row[0].strip()
                        if word:
                            existing_words.append(word)
                            existing_lower_set.add(word.lower())
            print(f"Loaded {len(existing_words)} existing word(s) from master list {os.path.basename(csv_path)}.")
        except Exception as e:
            print(f"Warning: Could not read existing {csv_path}: {e}")

    # Add new unique words
    added_count = 0
    final_words = list(existing_words)
    for word in extracted_words:
        if word.lower() not in existing_lower_set:
            existing_lower_set.add(word.lower())
            final_words.append(word)
            added_count += 1

    print(f"Added {added_count} new unique word(s) to master list. Total master words: {len(final_words)}.")

    # Create DataFrame
    df = pd.DataFrame({
        'content_payload_languages_en_word_display': final_words
    })

    # Save to CSV
    try:
        df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"Successfully updated CSV: {csv_path}")
    except Exception as e:
        print(f"Error updating CSV: {e}")

    # Save to XLSX
    try:
        df.to_excel(xlsx_path, index=False)
        print(f"Successfully updated XLSX: {xlsx_path}")
    except ModuleNotFoundError:
        print("\nError: Missing dependency for Excel files.")
        print("Please install openpyxl by running: pip install openpyxl")
    except Exception as e:
        print(f"Error updating XLSX: {e}")

if __name__ == "__main__":
    main()

