# CSS Fundamentals Used

Cascading Style Sheets (CSS) dictate exactly how our HTML elements look, providing the aesthetic design of the book.

## CSS Variables
At the top of `styles.css`, you'll see a `:root` selector with properties like `--bg-color: #F8F5F0;`. These are Custom Properties (variables). 
By defining colors and fonts here, we ensure consistency. If you want to change the off-white background to a stark white, you only change it in one place!

## Selectors
- **Class Selectors (e.g., `.card`)**: These target any HTML element with `class="card"`. They are the most common way to style elements because they are reusable.
- **Type Selectors (e.g., `body`)**: Targets all `body` tags.

## Typography Scaling
Handling long words like "Floccinaucinihilipilification" without breaking the layout is notoriously difficult in print.
We use a modern CSS feature called Container Queries (`container-type: inline-size`) and the `cqw` unit (container query width), or CSS `min()` functions.
In `styles.css`, the title uses:
```css
font-size: min(80pt, 13cqw);
```
This tells the browser: "Make the font size 13% of the container's width, but never let it go larger than 80 points." This ensures short words are large (but capped at 80pt) and extremely long words automatically shrink so they fit exactly onto one line!
