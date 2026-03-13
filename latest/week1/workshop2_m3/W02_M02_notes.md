# Workshop 2 · Module 2 — Course Notes
## Wickham's Layered Grammar & ggplot2

### 1. The ggplot2 Template
Every ggplot2 chart follows a single pattern: `ggplot(data, aes()) + geom_*() + scale_*() + facet_*() + labs() + theme_*()`. The `+` operator adds one grammar layer per call. This pattern is universal — bar charts, scatter plots, histograms, boxplots, and heatmaps all follow it. Learning ggplot2 means learning one system, not memorising separate functions.

### 2. Mapping vs Setting
The most common ggplot2 error is confusing mapping and setting. **Mapping** places a variable name inside `aes()`: `aes(color = group)`. The colour then varies with the data and generates a legend automatically. **Setting** places a fixed value outside `aes()` as a geom argument: `geom_point(color = "red")`. The colour is constant for all points. Placing a fixed string inside `aes()` — `aes(color = "red")` — creates a categorical variable with one level ("red") and a useless legend, which is almost never intended.

### 3. Default Statistics
Each geom has a default stat that transforms data before rendering. `geom_bar()` defaults to `stat_count()` — it counts rows per x category. `geom_col()` defaults to `stat_identity()` — it uses raw y values. `geom_histogram()` uses `stat_bin()` (bins continuous data). `geom_smooth()` uses `stat_smooth()` (fits LOESS or LM). Override the default with `geom_bar(stat = "identity")` or `stat_smooth(geom = "point")`.

### 4. Position Adjustments
When multiple groups share the same x position, position adjustments resolve overlap. **Stack** places bars on top of each other (default for `geom_bar` with `fill`). **Dodge** places bars side by side. **Fill** normalises stacks to 100%. **Jitter** adds random noise to prevent overplotting in scatter/strip plots. Fine-tune with `position_dodge(width = 0.8)` or `position_jitter(width = 0.2, height = 0)`.

### 5. Aesthetic Inheritance
Aesthetics in `ggplot(aes())` are **global** — all layers inherit them. Aesthetics in `geom_*(aes())` are **local** — only that layer sees them. This matters when combining geoms: global `color = class` means `geom_smooth()` fits one line per class (often too many). Moving `color` to `geom_point(aes(color = class))` and using `geom_smooth(color = "grey")` produces coloured points with a single overall trend.

### 6. plotnine Parity
The Python library `plotnine` implements ggplot2 syntax character-for-character. Differences: (a) column names are strings (`"displ"` not `displ`), (b) `+` goes at the start of each line inside parentheses (Python continuation rule), (c) `size` instead of `linewidth` for line geoms.

### References
- Wickham, H. (2010). A layered grammar of graphics. *JCGS*, 19(1), 3–28.
- Wickham, H. (2016). *ggplot2*, 2nd ed. Springer.
- Wickham, H. & Grolemund, G. (2023). *R for Data Science*, 2nd ed.
- plotnine: https://plotnine.org
