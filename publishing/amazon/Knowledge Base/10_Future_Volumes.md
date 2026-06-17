# Generating Future Volumes and Full Books

Right now, the script reads a single `sample_data.json` object and generates a single 2-page PDF. But you want to publish whole books!

## The Batch Process
To generate a 100-page book:
1. Change `sample_data.json` to contain an **array of objects** instead of just one object.
   ```json
   [
     { "word": "Pulchritudinous", ... },
     { "word": "Sesquipedalian", ... }
   ]
   ```
2. Modify `generate_pdf.py` to loop over this array. For every word in the array, it will generate a Left Page and a Right Page block of HTML.
3. Append all these HTML pages together into one giant `<body>`.
4. Let Playwright render it. Because we used `.page { page-break-after: always; }` in our CSS, Playwright will naturally slice that giant HTML document into 100 separate PDF pages.

## Handling Pagination
When looping through the data array in Python, keep track of a counter variable.
```python
page_count = 1
for word in data:
    left_page_num = str(page_count).zfill(2) # "01"
    right_page_num = str(page_count + 1).zfill(2) # "02"
    page_count += 2
```
Inject these dynamically into `{{page_number_left}}` and `{{page_number_right}}` so your page numbers are always perfect, saving you hours of manual formatting in InDesign!
