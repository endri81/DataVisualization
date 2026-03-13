# Workshop 2 · Module 8 — Course Notes
## labs(), Annotations & Storytelling Layers

### 1. labs(): The Label Layer
In ggplot2, `labs()` sets five text elements in one call: `title` (bold, states the finding), `subtitle` (grey, adds context — time period, filter), `caption` (italic, credits the source), `x` and `y` (axis labels with units), and legend titles (matching aesthetic names: `color`, `fill`, `size`). In matplotlib, title and axis labels sit on the axes object (`ax.set_title()`, `ax.set_xlabel()`), but subtitle and caption require `fig.text()` with manual coordinates.

### 2. Three Title Patterns
**Descriptive** titles name the chart ("Revenue by Quarter") — neutral, suitable for exploratory contexts where the audience draws their own conclusions. **Declarative** titles state the finding as a sentence ("Q4 Revenue Surged 35% to Record $395K") — persuasive, ideal for executive communication. **Question** titles invite investigation ("Which Quarter Drove the Revenue Spike?") — engaging, useful for teaching or interactive dashboards. For most professional output, declarative titles are recommended because they front-load the insight.

### 3. Four Annotation Types
**Text callout** (arrow + label): `annotate("text")` + `annotate("segment")` in R; `ax.annotate(arrowprops=...)` in Python. Use for specific findings on the chart. **Reference line**: `geom_hline()` / `ax.axhline()` for horizontal (mean, target); `geom_vline()` / `ax.axvline()` for vertical (event dates, policy changes). **Reference band**: `annotate("rect")` / `ax.axhspan()` for target ranges or acceptable zones. **Highlight region**: `annotate("rect")` with x-bounds / `ax.axvspan()` for event periods (e.g., recession, promotion window).

### 4. annotate() vs geom_text() vs geom_text_repel()
`annotate()` places a single annotation at a fixed position — one call per annotation. `geom_text()` / `geom_label()` maps text from a data column — one label per observation. `ggrepel::geom_text_repel()` adds anti-overlap to `geom_text()` using a force-directed algorithm. In Python, `ax.annotate()` handles callouts; `ax.text()` in a loop handles data-driven labels; `adjustText.adjust_text()` provides repulsion.

### 5. Storytelling Layers: Progressive Reveal
Build meaning in four stages: (1) show the raw data (line/scatter), (2) add a trend line or smooth for context, (3) annotate key events (vertical lines, callouts), (4) add a declarative title that states the finding. This technique works for slide presentations (reveal one layer per click) and for static reports (the final chart contains all layers simultaneously).

### References
- Knaflic, C. N. (2015). *Storytelling with Data*, Ch. 4.
- Schwabish, J. (2021). *Better Data Visualizations*, Ch. 5.
- Wickham, H. (2016). *ggplot2*, Ch. 8.3.
- Wilke, C. O. (2019). *Fundamentals of Data Visualization*, Ch. 22.
