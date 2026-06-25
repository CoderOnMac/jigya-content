#!/usr/bin/env python3
"""
Convert words.json into a ready-to-paste CSV.

Usage:
  python3 scripts/json_to_csv.py                # reads words.json, writes words.csv
  python3 scripts/json_to_csv.py input.json out.csv

Output columns (one row per word):
- id, date, category, type, tags
- image_url, image_prompt
- en_word_display, en_word_native, en_word_anglicized, en_definition, en_example_sentence, en_pronunciation_guide
- hi_word_display, hi_word_native, hi_word_anglicized, hi_definition, hi_example_sentence, hi_pronunciation_guide, hi_cultural_note
- fr_word_display, fr_word_native, fr_definition, fr_example_sentence, fr_pronunciation_guide, fr_cultural_note
- english_deep_dive_evolution_story, english_deep_dive_related_words, english_deep_dive_trivia

The script is defensive about missing keys and will flatten lists by joining with "; ". Newlines are collapsed to single spaces to make the CSV paste-friendly.
"""

import json
import csv
import sys
import re
from pathlib import Path


def sanitize(text):
    """Prepare text for CSV cell: ensure str, collapse whitespace/newlines."""
    if text is None:
        return ""
    if not isinstance(text, str):
        try:
            text = json.dumps(text, ensure_ascii=False)
        except Exception:
            text = str(text)
    # collapse multiple whitespace/newlines into single space
    text = re.sub(r"\s+", " ", text).strip()
    return text


def join_list(val):
    if val is None:
        return ""
    if isinstance(val, list):
        return "; ".join(sanitize(x) for x in val if x is not None)
    return sanitize(val)


def lang_field(content_payload, lang, field):
    try:
        return sanitize(content_payload.get("languages", {}).get(lang, {}).get(field))
    except Exception:
        return ""


import argparse

def main():
    parser = argparse.ArgumentParser(description="Convert words.json into a ready-to-paste CSV.")
    parser.add_argument("input", nargs="?", default="words.json", help="Input JSON file")
    parser.add_argument("output", nargs="?", default="words.csv", help="Output CSV file")
    parser.add_argument("--after-id", dest="after_id", default=None, help="Only process words that come after this specific ID")
    args = parser.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output)

    if not in_path.exists():
        print(f"Input file not found: {in_path}")
        sys.exit(1)

    data = json.loads(in_path.read_text(encoding='utf-8'))
    words = data.get('words', []) if isinstance(data, dict) else []

    if args.after_id:
        filtered_words = []
        found = False
        for w in words:
            if not isinstance(w, dict):
                continue
            if found:
                filtered_words.append(w)
            elif w.get('id') == args.after_id:
                found = True
        words = filtered_words

    headers = [
        'id','date','category','type','tags',
        'image_url','image_prompt',
        'en_word_display','en_word_native','en_word_anglicized','en_definition','en_example_sentence','en_pronunciation_guide',
        'hi_word_display','hi_word_native','hi_word_anglicized','hi_definition','hi_example_sentence','hi_pronunciation_guide','hi_cultural_note',
        'fr_word_display','fr_word_native','fr_definition','fr_example_sentence','fr_pronunciation_guide','fr_cultural_note',
        'english_deep_dive_evolution_story','english_deep_dive_related_words','english_deep_dive_trivia'
    ]

    # How many recent_references to flatten into separate columns
    MAX_RECENT = 5
    # add header columns for recent references: count + per-item fields
    headers.insert(headers.index('english_deep_dive_trivia')+1, 'english_deep_dive_recent_references_json')
    headers.insert(headers.index('english_deep_dive_recent_references_json')+1, 'english_deep_dive_recent_references_count')
    for i in range(1, MAX_RECENT+1):
        headers.extend([
            f'recent_reference_{i}_type',
            f'recent_reference_{i}_title',
            f'recent_reference_{i}_author',
            f'recent_reference_{i}_year',
            f'recent_reference_{i}_context',
        ])

    with out_path.open('w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers, extrasaction='ignore', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()

        for w in words:
            if not isinstance(w, dict):
                continue
            row = {h: '' for h in headers}
            row['id'] = sanitize(w.get('id'))
            row['date'] = sanitize(w.get('date'))
            row['category'] = sanitize(w.get('category'))
            row['type'] = sanitize(w.get('type'))
            row['tags'] = join_list(w.get('tags'))

            ca = w.get('common_assets', {}) or {}
            row['image_url'] = sanitize(ca.get('image_url'))
            row['image_prompt'] = sanitize(ca.get('image_prompt'))

            cp = w.get('content_payload', {}) or {}

            # English fields
            row['en_word_display'] = lang_field(cp, 'en', 'word_display')
            row['en_word_native'] = lang_field(cp, 'en', 'word_native')
            row['en_word_anglicized'] = lang_field(cp, 'en', 'word_anglicized')
            row['en_definition'] = lang_field(cp, 'en', 'definition')
            row['en_example_sentence'] = lang_field(cp, 'en', 'example_sentence')
            row['en_pronunciation_guide'] = lang_field(cp, 'en', 'pronunciation_guide')

            # Hindi fields
            row['hi_word_display'] = lang_field(cp, 'hi', 'word_display')
            row['hi_word_native'] = lang_field(cp, 'hi', 'word_native')
            row['hi_word_anglicized'] = lang_field(cp, 'hi', 'word_anglicized')
            row['hi_definition'] = lang_field(cp, 'hi', 'definition')
            row['hi_example_sentence'] = lang_field(cp, 'hi', 'example_sentence')
            row['hi_pronunciation_guide'] = lang_field(cp, 'hi', 'pronunciation_guide')
            row['hi_cultural_note'] = lang_field(cp, 'hi', 'cultural_note')

            # French fields
            row['fr_word_display'] = lang_field(cp, 'fr', 'word_display')
            row['fr_word_native'] = lang_field(cp, 'fr', 'word_native')
            row['fr_definition'] = lang_field(cp, 'fr', 'definition')
            row['fr_example_sentence'] = lang_field(cp, 'fr', 'example_sentence')
            row['fr_pronunciation_guide'] = lang_field(cp, 'fr', 'pronunciation_guide')
            row['fr_cultural_note'] = lang_field(cp, 'fr', 'cultural_note')

            # English deep dive
            ed = cp.get('english_deep_dive', {}) if isinstance(cp.get('english_deep_dive', {}), dict) else {}
            row['english_deep_dive_evolution_story'] = sanitize(ed.get('evolution_story'))
            row['english_deep_dive_related_words'] = join_list(ed.get('related_words'))
            row['english_deep_dive_trivia'] = sanitize(ed.get('trivia'))
            # recent_references: provide a JSON column and up to MAX_RECENT flattened columns
            recent_refs = ed.get('recent_references', []) if isinstance(ed.get('recent_references', []), list) else []
            row['english_deep_dive_recent_references_json'] = sanitize(json.dumps(recent_refs, ensure_ascii=False))
            row['english_deep_dive_recent_references_count'] = str(len(recent_refs)) if recent_refs is not None else '0'
            for i in range(1, MAX_RECENT+1):
                idx = i-1
                prefix_type = f'recent_reference_{i}_type'
                prefix_title = f'recent_reference_{i}_title'
                prefix_author = f'recent_reference_{i}_author'
                prefix_year = f'recent_reference_{i}_year'
                prefix_context = f'recent_reference_{i}_context'
                if idx < len(recent_refs):
                    ref = recent_refs[idx] or {}
                    row[prefix_type] = sanitize(ref.get('type'))
                    row[prefix_title] = sanitize(ref.get('title'))
                    row[prefix_author] = sanitize(ref.get('author'))
                    row[prefix_year] = sanitize(ref.get('year'))
                    row[prefix_context] = sanitize(ref.get('context'))
                else:
                    row[prefix_type] = ''
                    row[prefix_title] = ''
                    row[prefix_author] = ''
                    row[prefix_year] = ''
                    row[prefix_context] = ''

            writer.writerow(row)

    print(f"Wrote CSV to: {out_path.resolve()}")


if __name__ == '__main__':
    main()
