import json
import os
from playwright.sync_api import sync_playwright

def generate_pdf():
    # 1. Load data
    with open('sample_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # 2. Read HTML template
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 3. Replace simple placeholders
    html_content = html_content.replace('{{page_number_left}}', data['page_number_left'])
    html_content = html_content.replace('{{page_number_right}}', data['page_number_right'])
    html_content = html_content.replace('{{word}}', data['word'])
    html_content = html_content.replace('{{definition}}', data['definition'])
    
    # Example highlighting the target word
    example_text = data['example'].replace(data['word'].lower(), f'<span class="target-word">{data["word"].lower()}</span>')
    html_content = html_content.replace('{{example_html}}', example_text)
    
    # Evolution story highlighting target word
    evolution_text = data['evolution_story'].replace(data['word'].lower(), f'<span class="target-word">{data["word"].lower()}</span>')
    html_content = html_content.replace('{{evolution_story_html}}', evolution_text)
    
    html_content = html_content.replace('{{trivia}}', data['trivia'])
    html_content = html_content.replace('{{image_path}}', data['image_path'])

    # 4. Generate Bubbles HTML
    bubbles_html = ""
    for i, bubble in enumerate(data['bubbles']):
        bubbles_html += f'<div class="bubble bubble-{i+1}">{bubble}</div>\n'
    html_content = html_content.replace('{{bubbles_html}}', bubbles_html)

    # 5. Generate Word In Action HTML
    word_in_action_html = ""
    for item in data['word_in_action']:
        text_with_highlight = item['text'].replace(data['word'].lower(), f'<span class="target-word">{data["word"].lower()}</span>')
        word_in_action_html += f'''
        <div class="action-item">
            <p class="action-source">{item["source"]}</p>
            <p class="action-text">"{text_with_highlight}"</p>
        </div>
        '''
    html_content = html_content.replace('{{word_in_action_html}}', word_in_action_html)

    # 6. Save populated HTML to a temporary file for Playwright
    temp_html_path = os.path.abspath('temp_render.html')
    with open(temp_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # 7. Use Playwright to generate PDF
    print("Launching browser to generate PDF...")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # We navigate to the local file using absolute path
        page.goto(f'file://{temp_html_path}')
        
        # Wait for any web fonts or images to load completely
        page.wait_for_load_state('networkidle')
        
        # Generate the PDF with KDP required dimensions (8.5 x 11 in)
        output_path = 'output_manuscript.pdf'
        page.pdf(
            path=output_path,
            width='8.5in',
            height='11in',
            print_background=True,
            margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'}
        )
        browser.close()
    
    # 8. Clean up temporary file
    # if os.path.exists(temp_html_path):
    #     os.remove(temp_html_path)
        
    print(f"✅ Success! PDF generated at: {output_path}")

if __name__ == "__main__":
    generate_pdf()
