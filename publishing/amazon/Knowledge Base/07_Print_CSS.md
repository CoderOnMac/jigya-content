# Print CSS (`@page`)

Browsers are designed for endless scrolling screens, not fixed-size pieces of paper. To generate a PDF that Amazon KDP will accept, we have to force the browser to respect physical dimensions.

## The `@page` Rule
In `styles.css`, we use:
```css
@page {
    size: 8.5in 11in;
    margin: 0;
}
```
This is a special print-only rule. It tells the browser's print engine (and Playwright):
1. Create a canvas exactly 8.5 inches wide by 11 inches tall.
2. Remove all default browser margins (browsers usually add 0.5in margins to print headers/footers with URLs and dates).

## The `@media print` Query
We also use a media query specifically for printing:
```css
@media print {
    body {
        padding: 0;
        background-color: transparent;
    }
    .page {
        box-shadow: none;
    }
}
```
When you view `index.html` on your screen, we add a gray background and drop shadows to make it look like a physical book sitting on a desk. But when we actually print it to PDF, `@media print` strips away the shadows and the gray background so only the pure page content goes into the PDF!
