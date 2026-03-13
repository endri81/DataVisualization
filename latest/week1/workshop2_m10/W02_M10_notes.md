# Workshop 2 · Module 10 — Course Notes
## Lab: Building a Visual Report

### 1. The Visual Report Workflow
A complete visual report follows six steps: (1) formulate the question, (2) wrangle the data (filter, clean, type-convert), (3) explore with individual charts, (4) polish each chart (theme, labels, annotations), (5) compose into a multi-panel layout, (6) export as vector PDF and raster PNG.

### 2. Grammar Layers in Practice
Each panel of the dashboard applies specific grammar layers. The bar chart uses `geom_col` + `coord_flip` + `scale_fill_manual` (grey-accent) + `geom_text` (direct labels) + declarative title. The histogram uses `geom_histogram` + `geom_vline` (mean reference) + `annotate("text")`. The scatter uses `geom_point` + `scale_x_log10` + `aes(color = Type)`. The boxplot uses `geom_boxplot(notch = TRUE)` + `stat_summary(fun = mean)`. The line chart uses `geom_line` + direct endpoint labels (no legend). The stacked bar uses `geom_bar(position = "stack")` + `scale_fill_manual`.

### 3. Composition
In R, `patchwork` composes plots with `|` (side-by-side) and `/` (stacked): `(p1 | p2 | p3) / (p4 | p5 | p6)`. `plot_annotation(tag_levels = "a")` adds automatic panel labels. In Python, `GridSpec(2, 3)` creates the layout with `fig.add_subplot(gs[row, col])` for each panel. `fig.suptitle()` and `fig.text()` add the overall title and caption.

### 4. Workshop 2 Summary
Across ten modules, Workshop 2 established the Grammar of Graphics as the unifying framework: Wilkinson's theory (M01), Wickham's ggplot2 implementation (M02), deep dives into aesthetics (M03), scales (M04), facets (M05), themes (M06), Python libraries (M07), annotations (M08), tidy data (M09), and this capstone lab (M10). The grammar's power is compositionality: any chart is a stack of independent, modifiable layers.

### References
- Wickham, H. (2016). *ggplot2*, all chapters.
- Wilke, C. O. (2019). *Fundamentals of Data Visualization*.
- Knaflic, C. N. (2015). *Storytelling with Data*.
