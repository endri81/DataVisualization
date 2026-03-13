# Workshop 3 · Module 3 — Course Notes
## Comparisons: Bar Charts, Lollipop & Cleveland Dot

### 1. Bar Chart Best Practices
Three rules for categorical bar charts: (a) **horizontal** — labels are readable without rotation; use vertical only for temporal x-axes, (b) **sorted by value** — alphabetical order is almost never meaningful; `fct_reorder(cat, n)` in R, `sort_values()` in Python, (c) **directly labelled** — eliminates the need to trace from bar end to axis. Add grey-accent colour to highlight the key finding.

### 2. Three Bar Variants
**Grouped (dodge)**: bars side by side, best for comparing values between groups within each category. Limited to ≤3 groups before visual clutter. **Stacked**: bars stacked, best for comparing totals across categories while showing group contributions. Limitation: only the baseline segment is easy to compare precisely. **100% stacked (fill)**: normalised to percentages, best for comparing proportions. Limitation: loses absolute magnitude.

### 3. Lollipop Charts
A lollipop chart replaces the bar's filled rectangle with a thin segment and a terminal point. This reduces data ink while preserving the position encoding (Cleveland rank 1). Produced with `geom_segment() + geom_point()` in R or `ax.hlines() + ax.scatter()` in Python. Best for 10–20 categories where bars become visually heavy.

### 4. Cleveland Dot Plots
The Cleveland dot plot (Cleveland, 1985) uses only a point per category — the absolute minimum data ink. Subtle gridlines provide alignment. A mean reference line adds context. It is the Tufte-optimal comparison chart: maximum data-ink ratio with no loss of precision.

### 5. Dumbbell Charts
Dumbbell charts show change between two time periods per category. Two coloured points connected by a line segment encode start value, end value, and magnitude of change (line length). Direct-label the change value to avoid mental arithmetic.

### 6. The Ink Reduction Cascade
Bar → lollipop → Cleveland dot is a progressive reduction of non-data ink, each producing the same position-encoded comparison with less visual weight. The choice depends on audience: bars for general audiences, dots for data-literate audiences, dumbbells for change comparisons.

### References
- Cleveland, W. S. (1985). *The Elements of Graphing Data*. Wadsworth.
- Schwabish, J. (2021). *Better Data Visualizations*, Chapter 4.
- Wilke, C. O. (2019). *Fundamentals of Data Visualization*, Chapter 6.
