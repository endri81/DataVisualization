# Workshop 5 · Module 7 — Course Notes
## Point Maps & Spatial Patterns

### 1. Three Point Map Types
**Dot map**: each point represents one event at its geographic location. No size or colour encoding — just location. Use for event mapping: crimes, earthquakes, bird sightings, disease cases. The pattern (clustered, dispersed, random) reveals the spatial process.

**Proportional symbol map**: each point has a size proportional to a numeric variable — city population, store revenue, earthquake magnitude. The location encodes where; the size encodes how much. Keep to ≤3 size classes in the legend for readability, or use a continuous size scale with `scale_size(range = c(min, max))`. Area (not diameter) should be proportional to the data; ggplot2 and matplotlib do this correctly by default.

**KDE (kernel density estimation) map**: a continuous density surface estimating the intensity of events per unit area. Converts discrete points into a smooth heatmap. The bandwidth parameter controls smoothness: too low → noisy; too high → over-smoothed. Used for hotspot detection: where are events most concentrated? R: `stat_density2d(geom = "polygon")` or `leaflet.extras::addHeatmap()`. Python: `scipy.stats.gaussian_kde()` + `ax.contourf()` or `folium.plugins.HeatMap()`.

### 2. Overplotting
With >1,000 points on a map, individual dots merge into an opaque blob. Four solutions ranked by effectiveness:

**Alpha transparency** (cheapest): set `alpha = 0.05–0.2`. Darker areas = more points. Approximate but fast. R: `geom_sf(alpha = 0.1)`. Python: `ax.scatter(alpha=0.05)`.

**Hexbin** (aggregation): divide the map into hexagonal cells, count points per cell, colour by count. Exact, no information loss within the binning resolution. R: `geom_hex(bins = 30)`. Python: `ax.hexbin(gridsize=30)`.

**2D KDE contour** (smoothing): fit a 2D kernel density, draw contour lines or filled contour regions. Produces a continuous density surface — the most informative for hotspot analysis. R: `stat_density2d()`. Python: `scipy.stats.gaussian_kde()`.

**Marginal histograms**: add 1D histograms on the x and y margins of a scatter/map. Shows the marginal distributions of longitude and latitude separately. R: `ggExtra::ggMarginal()`. Python: `sns.jointplot()`.

### 3. Combining Layers
The most informative point maps combine multiple layers: a KDE density surface (background, low alpha) + proportional symbols (cities on top) + labels. This answers both "where are events concentrated?" and "how does that relate to population centres?" In ggplot2, layer order matters: put `stat_density2d()` first, then `geom_point()` for cities on top.

### 4. Cartograms
Cartograms distort regional boundaries so that area is proportional to a data variable rather than geographic area. This solves the choropleth's biggest problem: large, sparsely-populated regions dominating the visual. Types: **contiguous** (regions resized but stay connected — preserves topology), **Dorling** (each region replaced by a circle sized by data), **non-contiguous** (regions shrink/grow maintaining centroid position), **tile grid** (each region = equal-sized tile, e.g., US state grid maps). R: `cartogram::cartogram_cont()`, `cartogram::cartogram_dorling()`. Python: no mature library — use R via `reticulate` or export from QGIS.

### 5. Interactive Point Maps
Static point maps cannot show details on hover. Interactive maps (leaflet/folium) add: **zoom** (overview → detail on demand), **popups** (click a point → see metadata), **tooltips** (hover → quick preview), **layer toggle** (switch between dot map and heatmap), **tile switching** (light, dark, satellite basemaps). For event data, the interactive version is almost always more useful than the static version for exploration, while the static version is better for reports and publications.

### 6. Choosing the Right Point Map
≤100 points → dot map (every point visible). 100–5,000 points → dot map with low alpha or hexbin. >5,000 points → KDE density or hexbin (individual points invisible anyway). Need magnitude → proportional symbol. Need hotspot detection → KDE. Need exploration → interactive (leaflet/folium). Need publication → static (ggplot2/matplotlib).

### References
- Silverman, B. W. (1986). *Density Estimation for Statistics and Data Analysis*. Chapman & Hall.
- Dorling, D. (1996). Area Cartograms. *Concepts and Techniques in Modern Geography*.
- Lovelace, R. et al. (2019). *Geocomputation with R*, Chapter 8.
- Wilke, C. O. (2019). *Fundamentals of Data Visualization*, Chapter 15.
