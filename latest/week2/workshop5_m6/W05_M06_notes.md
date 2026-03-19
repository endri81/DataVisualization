# Workshop 5 · Module 6 — Course Notes
## Choropleth Maps

### 1. What Is a Choropleth?
A choropleth map colours geographic regions (countries, districts, counties) according to a data variable. Each region is filled with a colour that represents a value — population, GDP, unemployment rate, election margin. Choropleths are the most common thematic map type and the spatial equivalent of a bar chart: each region is a "bar" whose colour (instead of height) encodes the value.

### 2. Classification Methods
Raw continuous data must be classified into discrete colour bins. The choice of classification method fundamentally changes what the map communicates:

**Equal interval**: divides the data range into equally-spaced bins (e.g., 0–20, 20–40, ...). Simple to understand but ignores the data distribution — if most values cluster in one interval, most regions will share the same colour.

**Quantile**: each bin contains the same number of observations. Ensures visual variety (equal number of regions per colour) but can place very different values in the same bin or very similar values in different bins.

**Natural breaks (Jenks)**: minimises within-class variance and maximises between-class variance. Usually the best default — respects the data's natural clusters. In R: `tmap::tm_fill(style="jenks")`. In Python: `geopandas.plot(scheme="NaturalBreaks")` (requires `mapclassify` package).

**Standard deviation**: bins at mean ± 1σ, ± 2σ. Best for normally distributed data. Uses a diverging palette centred at the mean.

**Unclassed (continuous)**: no binning; a continuous colour ramp. Most precise but harder to read — the eye cannot distinguish more than ~7 colour steps. Use for exploratory work; classify for publication.

### 3. Palette Selection
The palette must match the data's semantic structure:

**Sequential** (low → high): for magnitude data where higher is "more" — population, income, count. Examples: Blues, YlOrRd, viridis, plasma. Always goes from light (low) to dark (high).

**Diverging** (negative ← centre → positive): for deviation from a reference value — change in %, residuals, z-scores, election margins. Examples: RdBu, BrBG, coolwarm. Must be centred at the reference (usually 0 or the national average). The midpoint colour (white or light grey) = "no deviation."

**Qualitative** (unordered categories): for nominal data — land use, political parties, language groups. Examples: Set2, Paired. Maximum ~8 distinguishable hues. Never use for numeric data.

### 4. Five Pitfalls
(1) **Large regions dominate**: a large, sparsely-populated region takes up more visual space than a small, dense city. Solution: normalise by area or population (use rates, not counts), or consider a cartogram. (2) **Misleading colour breaks**: equal interval classification on skewed data puts 90% of regions in one colour. Solution: use Jenks or quantile. (3) **Too many classes**: >7 colour bins are perceptually indistinguishable. Stick to 5–7. (4) **No legend or unlabelled breaks**: always include a colour bar with units. (5) **CRS mismatch**: computing area in a geographic CRS (degrees) gives nonsensical results. Always project to an equal-area CRS first.

### 5. Implementation
**R — ggplot2 + sf**: `ggplot(gdf) + geom_sf(aes(fill = variable))` + `scale_fill_viridis_c()` for sequential or `scale_fill_gradient2()` for diverging. For classification: `cut()` with manual breaks, or use `tmap` which has built-in `style = "jenks"/"quantile"/"equal"`. `tmap_mode("view")` instantly switches to interactive leaflet.

**Python — geopandas**: `gdf.plot(column="variable", cmap="Blues", scheme="NaturalBreaks", k=5)` (requires `mapclassify`). For interactive: `folium.Choropleth(geo_data=geojson, data=df, columns=["id","value"], key_on="feature.properties.id", fill_color="YlOrRd")`.

### 6. Choropleth vs Other Map Types
Choropleths are best for **rate data aggregated to administrative units**. For point events → dot map or KDE. For absolute counts → proportional symbol map (bubble size = count) avoids the large-region bias. For continuous surfaces (temperature, elevation) → raster/contour map. For comparing regions by multiple variables → small-multiple choropleths (one map per variable).

### References
- Brewer, C. A. (2005). *Designing Better Maps*. ESRI Press.
- Lovelace, R. et al. (2019). *Geocomputation with R*, Chapter 8.
- Slocum, T. et al. (2014). *Thematic Cartography and Geovisualization*, 3rd ed.
- colorbrewer2.org — Cynthia Brewer's palette selection tool.
