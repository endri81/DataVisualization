# Workshop 3 · Module 8 — Course Notes
## Small Multiples & Faceted Displays

### 1. Small Multiples Revisited
Small multiples (Tufte, 1983) are the single most powerful multi-group comparison technique. By splitting groups into separate panels with shared axes, the reader uses position (Cleveland rank 1) rather than colour (rank 5+) to discriminate groups. This module extends W02-M05's faceting mechanics to cover the broader philosophy of multi-panel composition, including heterogeneous dashboards.

### 2. Trellis Philosophy
Cleveland (1993) formalised small multiples as Trellis displays with four principles: (1) same chart type in every panel, (2) shared axes for fair comparison, (3) one variable per panel (the conditioning variable), (4) minimal strip labels identifying the panel variable. These principles ensure that cross-panel comparison is immediate and accurate.

### 3. Composition in R: patchwork
The `patchwork` package (Pedersen, 2020) provides an algebra of plot composition: `|` places plots side by side, `/` stacks them, `()` groups sub-layouts, `&` applies a modification to all panels, `+` adds annotations. Key functions: `plot_annotation(title, tag_levels = "a")` for global title and auto-labels, `plot_layout(widths, heights)` for unequal sizes, `inset_element()` for plot-within-plot. Older alternatives: `cowplot::plot_grid()` and `gridExtra::grid.arrange()`.

### 4. Composition in Python: GridSpec
`matplotlib.gridspec.GridSpec(nrows, ncols)` creates a grid; `fig.add_subplot(gs[row, col])` places axes. Spanning: `gs[0, :]` spans all columns; `gs[:, 0]` spans all rows. For named layouts, matplotlib 3.4+ offers `plt.subplot_mosaic()` with an ASCII grid definition where repeated names span cells.

### 5. Facet vs Patchwork Decision
Use **faceting** (`facet_wrap`, `facet_grid`) when all panels show the same geom and aesthetics with different data subsets (homogeneous). Use **patchwork/GridSpec** when panels show different chart types (heterogeneous) — e.g., bar + scatter + histogram + boxplot in a single figure.

### 6. Dashboard Best Practices
Every multi-panel figure needs: (a) panel labels (a, b, c) for reference in text, (b) a shared title, (c) a source caption, (d) consistent theme across panels (`& theme_minimal()` in patchwork, apply `rcParams` in Python). Limit to 4–6 panels per figure; more panels reduce individual panel readability.

### References
- Cleveland, W. S. (1993). *Visualizing Data*. Hobart Press.
- Pedersen, T. L. (2020). patchwork. https://patchwork.data-imaginist.com
- Tufte, E. R. (1983). *The Visual Display of Quantitative Information*, pp. 170–174.
- Wilke, C. O. (2019). *Fundamentals of Data Visualization*, Chapter 21.
