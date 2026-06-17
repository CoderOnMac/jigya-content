# CSS Positioning

Positioning allows us to take elements out of the normal document flow and place them exactly where we want them.

## Absolute vs Relative
We use this extensively for the **Page Number Badges** and the **Word Pill** on the image.

To position an element absolutely, its parent container must be set to `position: relative;`. This tells the browser: "The child's coordinates should be measured relative to the borders of this specific container, not the whole web page."

Example from our code:
```css
.page {
    position: relative;
}

.page-number-badge.top-left {
    position: absolute;
    top: 15px;
    left: 15px;
}
```
This forces the badge to sit exactly 15 pixels from the top and 15 pixels from the left of the `.page` container, floating above any text or images underneath it.

## The Bubble Tags
We used absolute positioning for the little circular bubbles ("Beautiful", "Ravishing", "Comely") so they could be placed organically, slightly overlapping each other without disrupting the grid layout around them.
