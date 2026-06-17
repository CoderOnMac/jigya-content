# Flexbox

While CSS Grid is for 2D layouts (rows AND columns), Flexbox is designed for 1D layouts (rows OR columns).

## Vertical Stacking
Inside our Grid columns (`.col-left` and `.col-right`), we used Flexbox to vertically stack the cards.
```css
.col-left {
    display: flex;
    flex-direction: column;
    gap: 30px;
}
```
This forces all the children (Definition, Example, Bubbles, Evolution Story) to stack in a vertical column, with exactly 30px of vertical space between them.

## Centering Elements
We also use Flexbox to perfectly center elements, like text inside the page number badges:
```css
.page-number-badge {
    display: flex;
    align-items: center;      /* Centers vertically */
    justify-content: center;  /* Centers horizontally */
}
```
Before Flexbox existed, centering text vertically was incredibly frustrating in CSS. Now, it takes just three lines.
