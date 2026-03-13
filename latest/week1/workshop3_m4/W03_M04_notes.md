# Workshop 3 · Module 4 — Course Notes
## Relationships: Scatter, Bubble & Hexbin

### 1. Scatter Plot Fundamentals
The scatter plot is the default chart for two continuous variables, encoding values via position on x and y axes (Cleveland rank 1 — the most accurate visual channel). Additional variables can be encoded via colour (categorical 3rd variable), size (continuous 4th variable), and shape (categorical 5th variable, max 6 shapes). Always plot the scatter before computing correlation: Pearson's r misses non-linear relationships, as demonstrated by Anscombe's quartet (W01-M01).

### 2. Overplotting
When n exceeds ~500, points overlap and density information is lost. Four solutions in order of increasing n: (a) alpha transparency (n < 2K), (b) jitter (categorical x), (c) hexbin / 2D histogram (n < 50K), (d) 2D KDE contour (any n). In R: `geom_hex(bins=30) + scale_fill_viridis_c()` or `geom_density_2d_filled()`. In Python: `ax.hexbin(gridsize=30, cmap="YlGnBu")` or `ax.contourf()` with scipy's `gaussian_kde`.

### 3. Bubble Charts
Bubble charts encode a 3rd continuous variable via point size and a 4th categorical variable via colour — the Gapminder style (Rosling). Size must map to area, not radius (both ggplot2 and matplotlib default to area). Cap at ≤5 total encodings (x, y, color, size, and optionally shape) to avoid cognitive overload. Use interactive plotly for hover labels on individual bubbles.

### 4. Smoothers
`geom_smooth(method="lm")` fits OLS regression — use when the relationship is approximately linear. `method="loess"` (default for n < 1000) fits local polynomial regression in sliding windows — use for non-linear patterns. `method="gam"` fits a generalised additive model — use for large n or complex patterns. In Python, `sns.regplot()` handles linear; polynomial fits via `np.polyfit()` or `statsmodels.lowess`.

### 5. Marginal Distributions
Adding histograms or density curves to the top/right margins of a scatter plot reveals univariate patterns (skewness, bimodality) invisible in the scatter alone. In R: `ggExtra::ggMarginal(p, type="histogram")`. In Python: `sns.jointplot(kind="scatter")` or manual GridSpec composition.

### References
- Cleveland, W. S. & McGill, R. (1984). Graphical Perception. *JASA*, 79(387).
- Rosling, H. et al. (2018). *Factfulness*.
- Wickham, H. (2016). *ggplot2*, Chapter 5.
- Wilke, C. O. (2019). *Fundamentals of Data Visualization*, Chapters 12–13.
