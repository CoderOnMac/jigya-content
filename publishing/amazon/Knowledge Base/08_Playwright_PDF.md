# Playwright PDF Generation

Playwright is a framework developed by Microsoft primarily for testing web applications. However, it is the absolute best tool for HTML-to-PDF conversion.

## Why Playwright?
Historically, developers used tools like `wkhtmltopdf` (which uses a decade-old browser engine) to make PDFs. Playwright uses the **actual, modern Chromium browser engine** (the same engine powering Google Chrome and Microsoft Edge). 
This means any modern CSS feature—like CSS Grid, Flexbox, or Container Queries—works perfectly in the final PDF.

## How our script works
Whether you use the Python or Node.js script, the workflow is the same:
1. **Load Data**: It reads `sample_data.json`.
2. **String Replacement**: It reads `index.html` as a raw text string, and replaces all `{{placeholders}}` with the real data.
3. **Save Temp File**: It saves this completed HTML into a `temp_render.html` file on your hard drive.
4. **Launch Browser**: It launches a "headless" (invisible) Chromium browser.
5. **Print**: It tells the browser to load `temp_render.html` and use the built-in "Print to PDF" functionality to save it as `output_manuscript.pdf`.

```python
page.pdf(
    path='output_manuscript.pdf',
    width='8.5in',
    height='11in',
    print_background=True, # Crucial! Without this, background colors won't print.
    margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'}
)
```
