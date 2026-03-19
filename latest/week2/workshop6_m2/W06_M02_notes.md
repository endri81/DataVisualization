# Workshop 6 · Module 2 — Course Notes
## Line Charts: Theory & Best Practices

### 1. Aspect Ratio: Banking to 45 Degrees
Cleveland, McGill, and McGill (1988) demonstrated that humans perceive line slopes most accurately when the average absolute slope of segments is close to 45 degrees. If the chart is too wide (low aspect ratio), even gentle trends look dramatic because the slope is amplified. If too tall (high aspect ratio), real trends are compressed and noise dominates. The "banking to 45 degrees" principle provides a principled way to choose the chart's width-to-height ratio.

In practice, start with a standard ratio (e.g., 16:9 for slides) and adjust if the line appears either too flat or too steep. R: `coord_fixed(ratio = ...)` or adjust `ggsave(width=, height=)`. Python: `fig, ax = plt.subplots(figsize=(width, height))`. The optimal aspect ratio depends on the data, not a universal constant — it's the ratio that makes the typical slope ~45 degrees.

### 2. The Dual Y-Axis Debate
Dual y-axes place two different scales on the left and right sides of the same chart, typically for two different variables. This is almost always misleading because: (a) the two scales are **arbitrary** — changing either scale changes the apparent visual relationship; (b) viewers instinctively assume shared visual space implies a shared scale, and infer correlation from visual overlap that is entirely a product of scale choice; (c) it is trivially easy to make any two variables appear correlated or uncorrelated by adjusting the scales.

**Better alternatives**: (1) Separate panels with a shared x-axis (facet_grid in R, subplots with sharex in Python). (2) Index both series to 100 (so both start at the same point and the y-axis measures percent change). (3) Use a secondary encoding (colour, line type) for the second variable on a separate chart.

The one defensible use case: when both variables share the same unit and roughly the same range (e.g., Fahrenheit vs Celsius), a secondary axis can help readers who think in different units. Even then, a conversion note in the margin is clearer.

### 3. Indexed Lines: Fair Comparison
When comparing multiple time series that start at different levels (e.g., Product A starts at EUR 100, Product B at EUR 500), the series with the highest absolute value dominates the chart visually, even if its growth rate is slower. Indexing solves this: divide each value by the first value and multiply by 100. Now all series start at 100 and the y-axis measures **relative performance** — a 20% increase from any starting point looks the same.

Formula: indexed_t = 100 × x_t / x_0. This is standard practice in financial analysis (stock price comparison), economic reporting (GDP indices), and any context where different starting levels obscure relative performance. For different units (temperature vs sales), use z-scoring instead: z_t = (x_t − mean) / SD.

Log scale is another alternative: on a log-y axis, constant percentage growth appears as a straight line. The steeper the line, the faster the growth. This makes growth rates visually comparable regardless of absolute level.

### 4. Grey + Accent Strategy
With more than 3-4 line series, the chart becomes "spaghetti" — a tangle of coloured lines where no story is readable. The grey+accent strategy solves this: draw all lines in light grey (#DDDDDD), then redraw the one series that tells the story in a saturated colour (#E53935). This immediately directs the viewer's eye to the narrative.

Pair grey+accent with **direct labelling**: place the series name at the right end of the highlighted line, not in a separate legend. This eliminates the cognitive load of the legend-to-line lookup. In R: `geom_text(data = df |> filter(date == max(date)), aes(label = name))`. In Python: `ax.text(dates[-1], values[-1], f" {name}")`.

### 5. Five Design Principles
(1) **Direct label** lines at their endpoints — beats any legend. (2) **Grey+accent**: all lines grey, one highlighted. (3) **Max 5-7 lines** per chart; beyond that, use small multiples (facets). (4) **Bank to ~45 degrees** aspect ratio for accurate slope perception. (5) **Annotate events** on the timeline with vertical dashed lines + text labels (e.g., "2008 crisis", "COVID lockdown") — this provides the causal context that makes time series interpretable.

### 6. Log Scale for Growth
On a log-y axis, constant percentage growth appears as a straight line. Steeper = faster growth. This makes growth rates visually comparable regardless of absolute level. Use when: (a) comparing series with different orders of magnitude, (b) looking for exponential growth (straight line on log = exponential), (c) the data spans several orders of magnitude. R: `scale_y_log10()`. Python: `ax.set_yscale("log")`.

### References
- Cleveland, W. S., McGill, M. E., & McGill, R. (1988). The Shape Parameter of a Two-Variable Graph. *JASA*, 83(402).
- Schwabish, J. (2021). *Better Data Visualizations*. Columbia University Press.
- Few, S. (2006). Dual-Scaled Axes in Graphs. Visual Business Intelligence Newsletter.
- Tufte, E. (2001). *The Visual Display of Quantitative Information*, 2nd ed.
