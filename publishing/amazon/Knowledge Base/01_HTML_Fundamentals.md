# HTML Fundamentals Used

Our manuscript system uses HTML5 as the structural foundation of every page. Think of HTML as the skeleton of a building, while CSS is the paint and interior design.

## Semantic Structure
We use standard HTML tags to define what content *is*, not just how it looks:
- `<h1>`, `<h2>`: Headings that establish a hierarchy. The main word is `<h1>` because it's the most important title on the page.
- `<p>`: Paragraphs for the definition, example, and trivia text.
- `<div>`: A generic container. In our project, `<div>` is our workhorse. We use it to create boxes, columns, pages, and card containers.

## Placeholders (The `{{}}` syntax)
In our `index.html`, you will see words surrounded by double curly braces, like `{{word}}` or `{{definition}}`.

These are **template variables**. HTML itself does not understand them; they are just raw text. Our Python/Node.js script searches for exactly these strings and replaces them with data from `sample_data.json` *before* rendering the PDF.

## Dynamic Injections
Some placeholders like `{{bubbles_html}}` represent entire blocks of HTML code that are generated in our script. Because the number of bubbles or Word In Action examples can change, we cannot hardcode the HTML tags for them. Instead, the generation script loops through the JSON array, builds the raw HTML string, and injects it into that spot.
