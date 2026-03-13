# Workshop 3 · Module 9 — Course Notes
## Tables as Visualization

### 1. Table vs Chart Decision
Tables are optimal when the reader needs exact values (financial reporting, regulatory compliance), needs to look up a specific row/column intersection, or when there are few rows (≤20) with many columns. Charts are optimal when the reader needs to see patterns, trends, or magnitude comparisons. The decision rule: "Does the reader need the number itself, or the pattern the numbers form?"

### 2. Five Table Design Principles
(1) **Minimal gridlines**: remove internal borders; use whitespace and alternating row shading. (2) **Right-align numbers**: decimal alignment enables quick magnitude scanning. (3) **Bold header, light body**: visual hierarchy separates structure from data. (4) **Highlight key cells**: conditional colour or bold on extreme values draws attention. (5) **Sort by a column**: pre-sorted tables eliminate reader effort.

### 3. Conditional Formatting
Conditional formatting bridges the table-chart gap. Cells are colour-encoded by value, enabling pattern detection while preserving exact numbers. Use sequential colour (light→dark) for magnitude; diverging colour (red-white-green) for deviation from a reference value. In R: `gt::data_color()`. In Python: `df.style.background_gradient()`.

### 4. Sparklines
Tufte (2006) defined sparklines as "data-intense, design-simple, word-sized graphics." They embed a miniature trend line directly in the table row, providing temporal context without requiring a separate chart. In R: `gt::gt_plt_sparkline()` or `gtExtras::gt_sparkline()`. In Python: `great_tables` nanoplot or inline matplotlib rendering.

### 5. Package Ecosystem
**R**: `gt` (declarative grammar, most polished output — HTML, LaTeX, RTF) and `kableExtra` (knitr extensions, quick RMarkdown integration). **Python**: `great_tables` (gt-inspired port, growing since 2024) and `pandas Styler` (built-in, Jupyter-native with `.background_gradient()`, `.bar()`, `.format()`).

### References
- Tufte, E. R. (2006). *Beautiful Evidence*, Chapter 2 (Sparklines).
- Few, S. (2012). *Show Me the Numbers*, Chapters 6–7.
- Iannone, R. et al. (2024). gt package. https://gt.rstudio.com
