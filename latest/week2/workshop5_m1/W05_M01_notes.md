# Workshop 5 · Module 1 — Course Notes
## High-Dimensional Data: Challenges & Strategies

### 1. The Curse of Dimensionality
As the number of variables (p) increases, the volume of the data space grows exponentially. With fixed n, the data becomes increasingly sparse: each point has no close neighbours, distances converge, and patterns become invisible. For visualization, this means: 1D (histogram) → works; 2D (scatter) → works; 3D (scatter + colour) → starts cluttering; 5–10D (pairs plot with p² panels) → unwieldy; 10–100D → need algorithmic dimension reduction; 100+D → need feature selection or heavy aggregation before any visualization.

### 2. Visual Encoding Channels (Cleveland & McGill, 1984; Munzner, 2014)
Ranked by perceptual accuracy: (1) position x, y — most accurate; (2) length — second; (3) angle/slope — moderate; (4) area — weak (area doubling perceived as ~1.5×); (5) colour hue — categorical only, ≤8 distinguishable; (6) colour saturation/luminance — quantitative but limited precision; (7) shape/texture — categorical only, ≤6 distinguishable. Map the most important variable to the highest-ranked channel.

### 3. Multi-Encoded Scatter
A single scatter plot can encode ~5 variables: x-position, y-position, colour, size, and shape. Example: FICO (x) × Rate (y) × Tier (colour) × Amount (size) × Car Type (shape). Beyond 5 variables, the chart becomes cognitively overloaded. Add faceting for 1–2 more categorical variables (giving 6–7 total), then switch to a different visualization strategy.

### 4. Aesthetic Overload
The human visual system can track ~4 encoding channels simultaneously (Healey & Enns, 2012). Charts with 12 colours × 12 shapes × variable size are puzzles, not communication tools. Cognitive limits: ≤8 colour hues, ≤6 shapes, ≤5 size levels. Rule: simpler is denser. Prefer 3 well-chosen encodings to 7 overloaded ones.

### 5. Five Strategies for High-D Visualization
(1) **Reduce dimensions**: PCA, t-SNE, UMAP project to 2D/3D (M03). (2) **Encode multiple channels**: colour, size, shape on scatter (this module). (3) **Facet**: small multiples, one panel per group (W03-M08). (4) **Parallel coordinates**: each axis = one variable (M02). (5) **Heatmap + clustering**: rows × columns, colour = value (M04).

### 6. Aggregation for Large n
Five techniques: **binning** (histogram, hexbin — `geom_hex()` / `ax.hexbin()`), **grouping** (`group_by + summarise` → per-category stats), **sampling** (`slice_sample(n=2000)` → random subset for scatter), **smoothing** (`geom_smooth()` / `sns.kdeplot()` — LOESS/KDE through cloud), **marginals** (`ggExtra::ggMarginal()` / `sns.jointplot()` — histograms on scatter margins).

### References
- Cleveland, W. S. & McGill, R. (1984). Graphical Perception. *JASA*, 79(387).
- Healey, C. G. & Enns, J. T. (2012). Attention and Visual Memory. *IEEE TVCG*, 18(7).
- Munzner, T. (2014). *Visualization Analysis and Design*. CRC Press.
