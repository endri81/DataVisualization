# Workshop 2 · Module 6 — Course Notes
## Themes & Publication-Quality Styling

### 1. What a Theme Controls
In the Grammar of Graphics, the theme layer controls all non-data visual elements: titles (font, size, colour, alignment), axis labels and tick marks, gridlines (major, minor, presence, colour), panel backgrounds, legend styling and placement, facet strip text, and plot margins. Critically, changing a theme never changes the data, aesthetics, geometry, or statistics — it only changes appearance.

### 2. Built-In Themes
ggplot2 ships with five core themes. `theme_minimal()` (white background, subtle gridlines, no box) is the recommended starting point for most work. `theme_classic()` (white background, axis lines, no gridlines) suits traditional journal formats. `theme_bw()` (white background, panel border, gridlines) works well for print. `theme_void()` removes all non-data elements entirely — use for maps, networks, and pie charts. `theme_gray()` is the ggplot2 default but is rarely appropriate for publication.

All base themes accept `base_size` for global font scaling: `base_size = 14` for slide presentations, `base_size = 9` for journal figures with dense multi-panel layouts.

### 3. The element_*() System
Four functions control theme elements: `element_text()` (font face, size, colour, angle, hjust/vjust, margin), `element_line()` (colour, linewidth, linetype), `element_rect()` (fill, colour/border, linewidth), and `element_blank()` (removes the element entirely). `element_blank()` is the Tufte eraser — every non-data element removed increases the data-ink ratio.

### 4. Custom Theme Functions
Wrapping theme customisations into a named function (e.g., `theme_unyt()`) ensures brand consistency across all charts in a project. Define the function once in a utility script, `source()` it in every analysis. The function should start with a base theme and layer custom elements on top.

### 5. ggthemes Package
The `ggthemes` package provides themes that mimic publication styles: `theme_economist()`, `theme_wsj()`, `theme_fivethirtyeight()`, `theme_tufte()`. Each comes with matching colour scales. These are useful for matching a specific publication's visual identity.

### 6. Python Equivalents
Three approaches in Python, ordered by scope: (1) `plt.rcParams.update({...})` sets global defaults for all subsequent plots, (2) `plt.style.use("seaborn-v0_8-whitegrid")` applies a named style sheet, (3) manual per-chart styling with `ax.spines[].set_visible()`, `ax.set_facecolor()`, `ax.grid()`. In plotnine, `+ theme_minimal()` works identically to ggplot2.

### 7. Export for Publication
Vector formats (PDF, SVG) are always preferred: they scale without loss and produce sharp text at any zoom. Use `ggsave("chart.pdf", device = cairo_pdf)` in R and `fig.savefig("chart.pdf", bbox_inches="tight")` in Python. For raster, use PNG at ≥300 dpi. Never use JPEG for charts — its lossy compression creates visible artifacts around sharp edges and text.

### References
- Chang, W. (2024). *R Graphics Cookbook*, 2nd ed., Chapter 9.
- Wickham, H. (2016). *ggplot2*, Chapter 8.
- Wilke, C. O. (2019). *Fundamentals of Data Visualization*, Chapter 22.
