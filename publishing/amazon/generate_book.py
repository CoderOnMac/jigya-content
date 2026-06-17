import json
import os
import re
from playwright.sync_api import sync_playwright

def generate_book():
    print("Loading words.json...")
    words_path = os.path.join('..', '..', 'words.json')
    if not os.path.exists(words_path):
        print(f"Error: Could not find {words_path}")
        return

    with open(words_path, 'r', encoding='utf-8') as f:
        master_data = json.load(f)

    with open('index.html', 'r', encoding='utf-8') as f:
        html_template = f.read()

    # Extract the <div class="spread">...</div> block to repeat it
    spread_match = re.search(r'(<div class="spread">.*?</div>\s*</div>\s*</div>\s*</div>\s*</div>)', html_template, re.DOTALL)
    if not spread_match:
        # Fallback regex if structure is slightly different
        spread_match = re.search(r'(<div class="spread">.*?)</body>', html_template, re.DOTALL)
        if not spread_match:
            print("Error: Could not parse index.html template properly.")
            return
            
    spread_template = spread_match.group(1)
    
    # Remove the spread block from the template so we can inject all of them back in
    base_html = html_template.replace(spread_template, '{{ALL_SPREADS}}')

    all_spreads_html = ""
    page_count = 1

    words = master_data.get('words', [])
    print(f"Found {len(words)} words. Generating pages...")

    for word_obj in words:
        payload = word_obj.get('content_payload', {})
        en_data = payload.get('languages', {}).get('en', {})
        deep_dive = payload.get('english_deep_dive', {})
        
        word = en_data.get('word_display', '')
        if not word:
            continue
            
        print(f"Processing: {word}")

        # Map the fields
        definition = en_data.get('definition', '')
        example = en_data.get('example_sentence', '')
        evolution_story = deep_dive.get('evolution_story', '')
        trivia = deep_dive.get('trivia', '')
        word_in_action_data = deep_dive.get('recent_references', [])
        bubbles_data = deep_dive.get('related_words', [])
        image_path = word_obj.get('common_assets', {}).get('image_url', '')

        # Since the image paths in words.json are relative (e.g., 'images/lions_share.jpg')
        # We need to make them absolute or relative to the html file
        # The HTML file is in publishing/amazon, so the image is at ../../images/...
        if image_path.startswith('images/'):
            image_path = f"../../{image_path}"

        # Copy the spread template for this word
        current_spread = spread_template

        # Pages
        left_page_str = str(page_count).zfill(2)
        right_page_str = str(page_count + 1).zfill(2)
        page_count += 2

        # Basic replacements
        current_spread = current_spread.replace('{{page_number_left}}', left_page_str)
        current_spread = current_spread.replace('{{page_number_right}}', right_page_str)
        current_spread = current_spread.replace('{{word}}', word)
        current_spread = current_spread.replace('{{definition}}', definition)
        current_spread = current_spread.replace('{{trivia}}', trivia)
        current_spread = current_spread.replace('{{image_path}}', image_path)

        # Highlighting the target word
        # (Handling case insensitive replace)
        word_lower = word.lower()
        target_html = f'<span class="target-word">{word_lower}</span>'
        
        # A simple case-insensitive replace for the example and evolution
        # Note: For perfect case preservation this can be complex, but for styling it is usually fine
        # We will just replace it blindly for now, or use a regex
        example_html = re.sub(re.escape(word), target_html, example, flags=re.IGNORECASE)
        evolution_html = re.sub(re.escape(word), target_html, evolution_story, flags=re.IGNORECASE)
        
        current_spread = current_spread.replace('{{example_html}}', example_html)
        current_spread = current_spread.replace('{{evolution_story_html}}', evolution_html)

        # Generate Bubbles HTML
        bubbles_html = ""
        for bubble in bubbles_data:
            bubbles_html += f'<div class="bubble">{bubble}</div>\n'
        current_spread = current_spread.replace('{{bubbles_html}}', bubbles_html)

        # Generate Word In Action HTML
        word_in_action_html = ""
        for item in word_in_action_data:
            text_with_highlight = re.sub(re.escape(word), target_html, item.get("context", ""), flags=re.IGNORECASE)
            source_text = f"{item.get('title', '')}, {item.get('author', '')}, {item.get('year', '')}"
            word_in_action_html += f'''
            <div class="action-item">
                <p class="action-source">{source_text}</p>
                <p class="action-text">"{text_with_highlight}"</p>
            </div>
            '''
        current_spread = current_spread.replace('{{word_in_action_html}}', word_in_action_html)

        all_spreads_html += current_spread + "\n"

    # Assemble final HTML
    final_html = base_html.replace('{{ALL_SPREADS}}', all_spreads_html)

    temp_html_path = os.path.abspath('temp_book_render.html')
    with open(temp_html_path, 'w', encoding='utf-8') as f:
        f.write(final_html)

    # Render PDF
    print("\nLaunching browser to generate full book PDF...")
    output_path = 'output_book.pdf'
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        page.goto(f'file://{temp_html_path}')
        page.wait_for_load_state('networkidle')
        
        page.pdf(
            path=output_path,
            width='8.5in',
            height='11in',
            print_background=True,
            margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'}
        )
        browser.close()

    print(f"✅ Success! Full book PDF generated at: {output_path}")

if __name__ == "__main__":
    generate_book()
