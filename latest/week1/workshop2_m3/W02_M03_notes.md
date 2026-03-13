# Workshop 2 · Module 3 — Course Notes
## ggplot2 Deep Dive: Aesthetics & Geometries

### 1. The Five Core Aesthetic Channels
ggplot2 supports five primary aesthetic channels: **x/y position** (most precise, Cleveland rank 1), **colour** (hue for categorical ≤7 levels, gradient for continuous), **size** (area-based, for ordered quantitative data), **shape** (glyph, maximum 6 distinguishable levels), and **alpha** (transparency, primarily for managing overplotting). The channel should match the variable type: continuous → position or gradient; categorical → hue or shape; binary → two-colour or shape.

### 2. Continuous vs Discrete Colour
Continuous variables map to sequential or diverging gradients (`scale_color_viridis_c()`, `scale_color_gradient2()`). Discrete variables map to qualitative palettes (`scale_color_brewer()`, `scale_color_manual()`). Mismatching — e.g., using a qualitative palette for a continuous variable — creates false perceptual boundaries.

### 3. Layering Multiple Geometries
The `+` operator layers geoms in drawing order. Common combinations: `geom_point() + geom_smooth()` (scatter + regression), `geom_boxplot() + geom_jitter()` (summary + raw data), `geom_col() + geom_errorbar()` (bar + uncertainty). When layering, set `outlier.shape = NA` in boxplots to avoid double-plotting outliers with jitter points.

### 4. Overplotting Solutions
Overplotting occurs when too many points overlap, obscuring density. Four solutions scale with data size: alpha reduction (n < 500), jitter (discrete x), hexbin/`geom_hex()` (500 < n < 50K), and 2D density contours (n > 5K). `geom_hex()` with `scale_fill_viridis_c()` encodes local count as colour, revealing density structure invisible in raw scatter plots.

### 5. Special Geometries
**geom_text / geom_label**: direct labelling (Module W01-M05). Use `ggrepel::geom_text_repel()` for anti-overlap. **geom_segment + geom_point**: lollipop charts (cleaner than bars for small n). **Two geom_point layers + geom_segment**: dumbbell charts showing before/after or two-time-point comparisons.

### References
- Chang, W. (2024). *R Graphics Cookbook*, 2nd ed. O'Reilly.
- Wickham, H. (2016). *ggplot2*, Chapters 4–5.
- Wilke, C. O. (2019). *Fundamentals of Data Visualization*, Chapters 2, 18.
