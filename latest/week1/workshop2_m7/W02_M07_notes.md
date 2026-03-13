# Workshop 2 · Module 7 — Course Notes
## seaborn & plotnine for Python

### 1. Three Python Visualization Libraries
Python's data visualization ecosystem has three primary libraries, each at a different abstraction level. **matplotlib** (W01-M09) is the low-level foundation: the Figure/Axes/Artists model gives full manual control but requires verbose code. **seaborn** sits atop matplotlib and provides statistical visualization with automatic aggregation, built-in faceting, and cleaner defaults. **plotnine** is a direct port of R's ggplot2 Grammar of Graphics, using identical syntax with `+` operator layering.

### 2. seaborn: Figure-Level vs Axes-Level
seaborn functions come in two flavours. **Figure-level** functions (`relplot`, `catplot`, `displot`) create their own figure and support built-in faceting via `col=` and `row=` parameters. They return a `FacetGrid` object. **Axes-level** functions (`scatterplot`, `boxplot`, `violinplot`, `histplot`, `heatmap`) draw onto an existing axes via the `ax=` parameter. Use axes-level functions when embedding seaborn plots into custom `plt.subplots()` or `GridSpec` layouts.

### 3. seaborn Aesthetic Mapping
seaborn maps data to visual channels via keyword arguments: `hue=` (colour), `style=` (shape/linestyle), `size=` (point/line size). These are the direct equivalents of ggplot2's `aes(color=, shape=, size=)`. Legends are generated automatically. The `palette=` argument accepts ColorBrewer names ("Set2"), named dictionaries, or lists.

### 4. seaborn Statistical Aggregation
seaborn computes statistics automatically: `catplot(kind="bar")` computes means and 95% CIs per category (equivalent to ggplot2's `stat_summary`). `regplot()` / `lmplot()` fit regression lines with confidence bands (equivalent to `geom_smooth(method="lm")`). `histplot(kde=True)` overlays a kernel density estimate on a histogram.

### 5. plotnine: ggplot2 for Python
plotnine replicates ggplot2's syntax almost character-for-character. The three differences are: (a) column names are strings (`"displ"` not `displ`), (b) `+` goes at the start of each line inside parentheses (Python continuation), (c) saving uses `.save()` instead of `ggsave()`. Everything else — `aes()`, `geom_*()`, `scale_*()`, `facet_*()`, `theme_*()`, `labs()` — is identical.

### 6. Library Selection Decision Tree
Need Grammar of Graphics syntax? → plotnine. Need built-in statistical aggregation or faceting? → seaborn figure-level. Need to embed in a custom multi-panel layout? → seaborn axes-level with `ax=`. Need maximum control? → matplotlib.

### References
- plotnine: https://plotnine.org
- seaborn tutorial: https://seaborn.pydata.org/tutorial.html
- VanderPlas, J. (2016). *Python Data Science Handbook*, Ch. 4.
- Waskom, M. (2021). seaborn: statistical data visualization. *JOSS*, 6(60), 3021.
