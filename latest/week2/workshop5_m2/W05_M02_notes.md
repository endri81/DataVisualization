# Workshop 5 · Module 2 — Course Notes
## Parallel Coordinates & Radar Charts

### 1. Parallel Coordinates
Parallel coordinates (Inselberg, 1985) display p variables as p parallel vertical axes. Each observation is a polyline connecting its values across all axes. Colour encodes group membership. Patterns: parallel lines between adjacent axes indicate positive correlation; crossing lines indicate negative correlation; clusters of similarly-shaped lines reveal multivariate groups; isolated lines far from the cluster are multivariate outliers. Best for 5–20 variables with many observations. R: `GGally::ggparcoord()`. Python: manual with MinMaxScaler + `ax.plot()`, or `pandas.plotting.parallel_coordinates()`.

### 2. Reading and Design
The single most impactful design decision is **axis order**. Adjacent axes are compared most easily (Gestalt proximity). Strategies: domain order (natural sequence), correlation order (correlated pairs adjacent), variance order (highest variance at edges), algorithmic (`ggparcoord(order="anyClass")`). Always apply the **grey+accent strategy**: draw all lines in light grey, highlight one group in saturated colour. With 100+ observations, lower alpha to 0.05–0.15.

### 3. Interactive Parallel Coordinates
Plotly's `parcoords` trace (R: `plot_ly(type="parcoords")`; Python: `px.parallel_coordinates()`) enables **axis brushing**: drag on any axis to select a range, and lines outside fade. This is the most powerful exploratory use — impossible in static plots. Users can iteratively narrow subsets across multiple axes.

### 4. Radar (Spider) Charts
Radar charts arrange variables as spokes radiating from a centre, with values plotted as distances from the centre and connected to form a polygon. Effective only for ≤3 profiles with ≤8 axes. Three problems: (1) enclosed area depends on axis order (meaningless for non-sequential variables), (2) area perception is less accurate than length (Cleveland & McGill), (3) beyond 3 profiles, polygons overlap into spaghetti. Popular in sports analytics and product comparisons but statistically problematic. Default to parallel coordinates unless addressing a general audience with exactly 2–3 entity comparisons.

### 5. Decision Framework
2–3 profiles, ≤8 axes, holistic comparison → radar. Many observations, 5–20 variables, group separation → parallel coordinates. 3–8 variables, precise values → pairs plot. For all: try interactive plotly version first.

### References
- Inselberg, A. (2009). *Parallel Coordinates*. Springer.
- Few, S. (2006). Radar Graphs: Not So Useful After All.
- Wilke, C. O. (2019). *Fundamentals of Data Visualization*, Ch. 6.
