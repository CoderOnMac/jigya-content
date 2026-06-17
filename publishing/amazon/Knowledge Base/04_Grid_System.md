# CSS Grid System

To create the layout on the right page, we used CSS Grid. Grid is a powerful two-dimensional layout system that allows us to define rows and columns.

## How we used it
In our `styles.css`:
```css
.main-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 30px;
}
```

### Breaking it down:
- `display: grid;` activates the grid system for the container.
- `grid-template-columns: 1fr 1fr;` creates exactly two columns. `1fr` stands for "1 fraction" of the available space. This means both columns take up equal width (50% each).
- `gap: 30px;` adds a 30-pixel gutter between the columns, preventing text from smashing together.

Inside this grid, we simply placed two div containers: `.col-left` and `.col-right`. The grid automatically puts `.col-left` in the first column and `.col-right` in the second column. It is the cleanest and most robust way to build newspaper or textbook style multi-column layouts.
