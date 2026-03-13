# Workshop 2 · Module 5 — Course Notes
## Faceting & Small Multiples

### 1. Small Multiples via the Grammar
Tufte's small multiples (W01-M02) are the grammar's faceting layer. Instead of encoding a grouping variable via colour (which taxes hue discrimination), faceting creates one panel per group level, exploiting Gestalt proximity for group separation.

### 2. facet_wrap(~var)
Splits data by one categorical variable into a wrapped grid. Key arguments: `ncol` / `nrow` (grid dimensions), `scales` ("fixed", "free_x", "free_y", "free"). The strip text above each panel displays the variable's level. Use when the faceting variable has 4–12 levels.

### 3. facet_grid(row ~ col)
Splits data by two categorical variables into a row × column matrix. Every combination gets its own cell. Use when two variables cross-classify observations (e.g., Type × Content Rating). For one variable on rows only: `facet_grid(Type ~ .)`. For columns only: `facet_grid(. ~ Content_Rating)`.

### 4. Fixed vs Free Scales
**Fixed** (default): all panels share the same axis range. Essential for fair cross-panel comparison. **Free**: each panel has its own range. Reveals within-group detail but destroys cross-panel comparability. Rule: default to fixed; use free only when ranges differ by orders of magnitude, and always warn the reader.

### 5. Facet + Statistic Layers
When `geom_smooth()` or `stat_summary()` appears inside a faceted plot, the statistic is computed independently within each panel. This reveals group-specific trends that would be averaged in a single-panel plot.

### 6. Facet vs Patchwork/GridSpec
Use **faceting** when all panels show the same geom/aes with different data subsets. Use **patchwork** (R) or **GridSpec** (Python) when panels show different chart types (bar + scatter + histogram + boxplot).

### 7. Python Equivalents
Three approaches in decreasing automation: (1) `plotnine.facet_wrap()` — identical syntax to ggplot2, (2) `seaborn.FacetGrid` — `g.map()` applies a function to each panel, (3) `plt.subplots()` with a manual loop — full control but more code.

### References
- Tufte, E. R. (1983). *The Visual Display of Quantitative Information*, pp. 170–174.
- Wickham, H. (2016). *ggplot2*, Chapter 7.
- Wilke, C. O. (2019). *Fundamentals of Data Visualization*, Chapter 21.
