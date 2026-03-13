# Workshop 2 · Module 4 — Course Notes
## Scales & Coordinate Systems

### 1. Anatomy of a Scale
A scale is a function that maps data values (the domain) through an optional mathematical transformation to visual properties (the range). In ggplot2, every aesthetic has an implicit scale: `aes(x = displ)` invokes `scale_x_continuous()` by default. Scales control three things: the domain (input range), the transform (identity, log10, sqrt, reverse), and the range (output: pixel positions, hex colours, point sizes). Additionally, scales control axis breaks, labels, and legend formatting.

### 2. Position Scales
`scale_x_continuous()` / `scale_y_continuous()` handle numeric axes with parameters `limits`, `breaks`, `labels`, and `trans`. `scale_x_log10()` is a shortcut for `trans = "log10"` — use when data spans more than two orders of magnitude. `scale_x_discrete()` handles categorical axes with `limits` (for reordering) and `labels` (for renaming). `scale_x_date()` formats temporal axes with `date_breaks` and `date_labels` (strftime codes).

### 3. Colour Scales
Categorical variables use qualitative palettes: `scale_color_brewer(palette = "Set2")` or `scale_color_manual(values = c(...))`. Continuous variables use sequential gradients: `scale_color_viridis_c()`. When data has a meaningful midpoint (zero, average), use a diverging scale: `scale_color_gradient2(low = "blue", mid = "white", high = "red", midpoint = 0)`.

### 4. Axis Label Formatting
The `scales` package provides formatters: `scales::comma` (1,000,000), `scales::dollar` ($1.2M), `scales::percent` (45%). In Python, use `matplotlib.ticker.FuncFormatter` with a lambda.

### 5. Coordinate Systems
`coord_cartesian()` is the default. `coord_flip()` swaps x and y (horizontal bars). `coord_polar(theta = "y")` maps y to angle (pie chart). `coord_fixed(ratio = 1)` enforces equal aspect ratio (essential for maps and spatial data).

### 6. Zooming Safely
**Critical distinction**: `scale_x_continuous(limits = c(25, 75))` **filters** data outside the range — statistics are recomputed on the subset, changing regression slopes and smoothers. `coord_cartesian(xlim = c(25, 75))` **clips** the viewport without removing data — statistics remain unchanged. Always zoom with `coord_cartesian()`. In matplotlib, `ax.set_xlim()` behaves like `coord_cartesian` (safe).

### References
- Wickham, H. (2016). *ggplot2*, Chapters 6–8.
- Wickham, H. & Grolemund, G. (2023). *R for Data Science*, 2nd ed., Ch. 11.
- Wilke, C. O. (2019). *Fundamentals of Data Visualization*, Chapters 3, 7, 8.
