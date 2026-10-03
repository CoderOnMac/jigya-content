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


def main():
    in_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('words.json')
    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('words.csv')

    if not in_path.exists():
        print(f"Input file not found: {in_path}")
        sys.exit(1)

    data = json.loads(in_path.read_text(encoding='utf-8'))
    words = data.get('words', []) if isinstance(data, dict) else []

    headers = [
        'id','date','category','type','tags',
        'image_url','image_prompt',
        'en_word_display','en_word_native','en_word_anglicized','en_definition','en_example_sentence','en_pronunciation_guide',
        'hi_word_display','hi_word_native','hi_word_anglicized','hi_definition','hi_example_sentence','hi_pronunciation_guide','hi_cultural_note',
        'fr_word_display','fr_word_native','fr_definition','fr_example_sentence','fr_pronunciation_guide','fr_cultural_note',
        'english_deep_dive_evolution_story','english_deep_dive_related_words','english_deep_dive_trivia'
    ]

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

            writer.writerow(row)

    print(f"Wrote CSV to: {out_path.resolve()}")


if __name__ == '__main__':
    main()
