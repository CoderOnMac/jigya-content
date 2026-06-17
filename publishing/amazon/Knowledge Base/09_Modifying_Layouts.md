# How to Modify Layouts

Because everything is driven by standard HTML and CSS, changing the design is exactly like editing a website.

## Changing Colors
Open `styles.css`. Look at the very top:
```css
:root {
    --bg-color: #F8F5F0;
    --text-color: #1a1a1a;
    --accent-orange: #C96627;
}
```
Change these hex codes, save the file, and re-run the python script to generate a new PDF. The entire book will update instantly.

## Changing Fonts
1. Go to **Google Fonts** (fonts.google.com).
2. Find a font you like (e.g., `Lora`).
3. Copy the `<link>` tag they provide and replace the one in the `<head>` of `index.html`.
4. In `styles.css`, update `--font-serif: 'Lora', serif;`

## Adding a New Box
If you want to add a "Synonyms" box:
1. Add `"synonyms": "Good, Great, Awesome"` to `sample_data.json`.
2. Open `index.html`. Find the column where you want it (e.g., `<div class="col-left">`).
3. Add a new card:
```html
<div class="card synonyms-card">
    <h2 class="card-title accent">Synonyms</h2>
    <p class="card-content">{{synonyms}}</p>
</div>
```
4. Update `generate_pdf.py` to replace `{{synonyms}}` just like the other fields:
```python
html_content = html_content.replace('{{synonyms}}', data['synonyms'])
```
