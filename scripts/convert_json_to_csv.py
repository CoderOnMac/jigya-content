import json
import csv
import sys
import argparse

def flatten_json(y):
    out = {}
    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            for i, a in enumerate(x):
                flatten(a, name + str(i) + '_')
        else:
            out[name[:-1]] = x
    flatten(y)
    return out

def json_to_csv(json_file_path, csv_file_path, start_after_id=None):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{json_file_path}' was not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: The file '{json_file_path}' contains invalid JSON.")
        sys.exit(1)
    
    # Try to find a list of items to convert
    if isinstance(data, dict) and 'words' in data and isinstance(data['words'], list):
        items = data['words']
    elif isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        items = [data]
    else:
        print("Error: Unsupported JSON structure. Must be a list of objects or a dictionary containing a list.")
        sys.exit(1)
        
    if start_after_id:
        filtered_items = []
        found = False
        for item in items:
            if found:
                filtered_items.append(item)
            elif item.get('id') == start_after_id:
                found = True
        
        if not found:
            print(f"Warning: Start ID '{start_after_id}' was not found in the data. Proceeding with empty result.")
            items = []
        else:
            items = filtered_items

    flattened_data = [flatten_json(item) for item in items]
    
    # Post-process to combine title, author, and year into a single column for recent_references
    for item in flattened_data:
        # Find all reference prefixes and indices by checking keys
        ref_keys = set()
        for key in list(item.keys()):
            if 'recent_references_' in key and key.endswith('_title'):
                # Extract the prefix up to and including 'recent_references_'
                prefix = key.rsplit('recent_references_', 1)[0] + 'recent_references_'
                # Extract the index (e.g., '0' from '...recent_references_0_title')
                idx = key.split('_')[-2]
                ref_keys.add((prefix, idx))
                
        for prefix, idx in ref_keys:
            title_key = prefix + idx + '_title'
            author_key = prefix + idx + '_author'
            year_key = prefix + idx + '_year'
            
            parts = []
            if title_key in item and item[title_key] is not None:
                parts.append(str(item[title_key]))
            if author_key in item and item[author_key] is not None:
                parts.append(str(item[author_key]))
            if year_key in item and item[year_key] is not None:
                parts.append(str(item[year_key]))
                
            if parts:
                merged_key = prefix + idx + '_title_author_year'
                item[merged_key] = ", ".join(parts)
                
            # Remove the original columns so they don't appear in the CSV
            item.pop(title_key, None)
            item.pop(author_key, None)
            item.pop(year_key, None)
            
        # Title case the English word display
        en_display_key = 'content_payload_languages_en_word_display'
        if en_display_key in item and isinstance(item[en_display_key], str):
            item[en_display_key] = ' '.join(word.capitalize() for word in item[en_display_key].split())
            
        # Update image_url to use cloudinary
        img_key = 'common_assets_image_url'
        if img_key in item and isinstance(item[img_key], str):
            if item[img_key].startswith('images/'):
                item[img_key] = item[img_key].replace('images/', 'https://res.cloudinary.com/dk09hulbf/image/upload/', 1)
                
    if not flattened_data:
        print("No data found to convert.")
        return

    # Add an index column starting at 01, formatted to force spreadsheet apps to treat it as text
    for i, item in enumerate(flattened_data):
        item['index'] = f'="{str(i + 1).zfill(2)}"'

    # Get all unique keys across all items for CSV headers
    # Using a list to maintain order as much as possible, while ensuring uniqueness
    headers = ['index']
    for item in flattened_data:
        for key in item.keys():
            if key not in headers:
                headers.append(key)
    
    try:
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(flattened_data)
        print(f"Successfully converted '{json_file_path}' to '{csv_file_path}'.")
        print(f"Total records processed: {len(flattened_data)}")
    except IOError as e:
        print(f"Error writing to '{csv_file_path}': {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a JSON file (e.g., words.json) into a flat CSV format.")
    parser.add_argument("input_json", help="Path to the input JSON file", default="words.json", nargs="?")
    parser.add_argument("output_csv", help="Path to the output CSV file", default="words.csv", nargs="?")
    parser.add_argument("--start-after-id", help="Only convert items that appear after this specific ID")
    args = parser.parse_args()
    
    json_to_csv(args.input_json, args.output_csv, args.start_after_id)
