# Quick Commands

## If using Python:
**1. Setup environment & install Playwright**
```bash
python3 -m venv venv
source venv/bin/activate
pip install playwright
playwright install chromium
```

**2. Generate Single Page PDF (Using sample_data.json)**
```bash
python generate_pdf.py
```

**3. Generate Full Book PDF (Using words.json)**
```bash
python generate_book.py
```

## If using Node.js:
**1. Install Playwright**
```bash
npm install playwright
```

**2. Generate PDF**
```bash
node generate_pdf.js
```

## Preview layout in browser
You can simply open `index.html` in your browser. However, because Playwright replaces the `{{placeholder}}` variables, the raw HTML will show placeholders instead of data.

To see the real data:
1. Run the python script which generates a `temp_render.html` file before creating the PDF. You can comment out `os.remove(temp_html_path)` in `generate_pdf.py` so the file persists.
2. Open `temp_render.html` in your browser.
