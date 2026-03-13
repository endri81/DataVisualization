# Workshop 1 · Module 5 — Course Notes
## Typography, Layout & Composition

---

### 1. Typographic Hierarchy

Professional chart typography establishes a clear reading order through five levels of visual weight. The **title** (16–20pt bold) states the chart's main finding or question. The **subtitle** (11–13pt regular) provides context — date range, data source, units, or methodology. **Axis labels** (10–11pt) name the variables. **Annotations** (8–9pt) are direct labels placed on data points, ideally colour-matched to their series. The **caption** (7–8pt italic) records the source, caveats, and notes.

The minimum size ratio between adjacent levels should be approximately 1.2× to maintain clear visual separation. If the title is 16pt, the subtitle should not exceed 13pt, and axis labels should remain at or below 11pt. Violating this ratio collapses the hierarchy and forces the reader to infer the reading order from position alone.


### 2. Font Selection

Sans-serif typefaces (Fira Sans, Helvetica, Arial, Source Sans Pro) render crisply at small sizes on both screens and print. They are the default recommendation for all chart text. Serif typefaces (Georgia, Palatino) may appear in long-form report text but are rarely appropriate for axis labels or annotations, where they add visual bulk without improving legibility. Monospace typefaces (Fira Code, Consolas) should be reserved for code blocks and numeric tables where digit alignment is essential.

In R, the `base_family` argument to `theme_minimal()` or `theme()` sets the global font. Google Fonts can be loaded via `showtext::font_add_google()`. In Python, `plt.rcParams["font.family"]` and the `font.sans-serif` list control the fallback chain. Custom `.ttf` files are registered via `matplotlib.font_manager.fontManager.addfont()`.


### 3. Whitespace and Margins

Whitespace is structural, not decorative. Generous internal margins (between title and plot area, between facet panels, between the legend and the plot edge) reduce cognitive load by separating visual units into readable chunks. External margins (page margin, inter-chart spacing) prevent the chart from feeling confined.

In R, `theme(plot.margin = margin(t, r, b, l))` controls the outer margin in points. In Python, `plt.tight_layout(pad=2.0)` or `plt.subplots_adjust()` serves the same purpose. A common error is to leave matplotlib's default tight_layout with no padding argument, producing zero breathing room between the title and the plot area.


### 4. Alignment and Direct Labelling

Numeric labels should be right-aligned so that digits of the same place value stack vertically, enabling instant magnitude comparison. Centred numbers scatter the digits laterally, forcing serial reading.

Direct labelling — placing the series name at the line endpoint or on the bar itself — eliminates the legend-shuttle problem, where the reader's eye oscillates between the legend box and the chart trying to match colours to categories. In R, the `ggrepel` package provides `geom_text_repel()` and `geom_label_repel()` with automatic collision avoidance. In Python, the `adjustText` library performs the same function.


### 5. Annotation Patterns

Three annotation patterns cover most explanatory needs. A **callout** (arrow + text box) points to a specific data event. A **context band** (shaded vertical or horizontal region) highlights a time period or value range. A **reference line** (dashed horizontal or vertical) marks a benchmark, mean, or target.

In R, `annotate("text")`, `annotate("rect")`, and `geom_hline()` implement these three patterns. In Python, `ax.annotate()` with `arrowprops`, `ax.axvspan()`, and `ax.axhline()` serve as equivalents.


### 6. Grid Systems and Multi-Panel Composition

Single-chart layouts work for slides. Two-column layouts support comparison (before/after, R vs Python, treatment vs control). Dashboard grids combine a KPI summary row with a 2×2 or 3×2 chart grid.

In R, the `patchwork` package composes ggplot2 objects with `|` (side-by-side) and `/` (stacked) operators. `plot_layout(heights=, widths=)` controls relative panel sizes. `plot_annotation(tag_levels = "a")` auto-labels panels. In Python, `matplotlib.gridspec.GridSpec` provides arbitrary row/column spanning with `height_ratios` and `width_ratios`.


### 7. Aspect Ratio and Export

Cleveland (1993) demonstrated that line chart slopes are perceived most accurately when the average absolute slope is approximately 45°. For time series, this typically means a wider-than-tall panel (aspect ratio ~2:1 to 3:1).

Charts should be exported as **PDF or SVG** (vector formats) for publications and presentations, ensuring infinite scalability and crisp text at any zoom. **PNG** at ≥300 dpi is acceptable when vector formats are unsupported. **JPEG** should never be used for charts — its lossy compression creates visible artefacts around sharp edges and text, degrading legibility.


### References

- Butterick, M. (2015). *Practical Typography*. https://practicaltypography.com
- Cleveland, W. S. (1993). *Visualizing Data*. Hobart Press.
- Schwabish, J. (2021). *Better Data Visualizations*. Columbia University Press.
- Wilke, C. O. (2019). *Fundamentals of Data Visualization*. O'Reilly.
