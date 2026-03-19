# Workshop 5 · Module 8 — Course Notes
## Interactive Maps

### 1. Why Interactive?
Static maps are fixed: one zoom level, one view, no detail-on-demand. Interactive maps add five capabilities that are impossible in print: **pan** (move the view), **zoom** (overview → detail), **hover/tooltip** (quick preview without clicking), **click/popup** (full metadata for a single feature), and **layer toggle** (switch between dot map, heatmap, and choropleth). For exploratory spatial analysis, interactive maps are strictly superior to static. For publications and reports, static maps are still needed (reproducible, no technology dependency, print-ready).

### 2. The Tile-Map Stack
Interactive web maps are built in layers: **base tiles** (raster image tiles from a tile server — OpenStreetMap, CartoDB Positron/DarkMatter, Stamen, Esri Satellite), **vector overlays** (points, lines, polygons drawn on top of tiles — markers, GeoJSON boundaries, circles), **raster overlays** (heatmap surfaces, choropleth fills), **controls** (zoom buttons, layer switcher, scale bar, legend), **interaction handlers** (click → popup, hover → tooltip, drag → pan).

### 3. leaflet (R)
The `leaflet` package is R's primary interactive map library, wrapping Leaflet.js. The pipe-based API mirrors ggplot2's layered grammar:
```r
leaflet(data) |>
  addProviderTiles("CartoDB.Positron") |>   # base tiles
  setView(lng, lat, zoom) |>                 # initial view
  addCircleMarkers(~lon, ~lat, ...) |>       # vector overlay
  addLegend(...)                              # control
```
Key functions: `addMarkers()` (pin icons), `addCircleMarkers()` (circles with radius/colour), `addPolygons()` (choropleth fill + highlight), `addPolylines()` (routes), `addHeatmap()` (from `leaflet.extras`). Export: `htmlwidgets::saveWidget(m, "map.html", selfcontained = TRUE)` produces a standalone HTML file.

The `tmap` package offers an even simpler path: build the map in static mode (`tmap_mode("plot")`), then switch to interactive with `tmap_mode("view")` — the exact same `tm_shape() + tm_fill()` code now renders as a leaflet map in the browser. This is the fastest way to go from static ggplot-style maps to interactive exploration.

### 4. folium (Python)
`folium` wraps Leaflet.js for Python. The API uses method chaining with `.add_to()`:
```python
m = folium.Map(location=[lat, lon], zoom_start=7, tiles="CartoDB positron")
folium.CircleMarker([lat, lon], radius=5, popup="text").add_to(m)
m.save("map.html")
```
Key classes: `Marker` (pin), `CircleMarker` (circle), `Choropleth` (GeoJSON + data → filled regions), `GeoJson` (raw GeoJSON overlay), `Popup` (click content, supports HTML), `Tooltip` (hover preview). Plugins: `folium.plugins.HeatMap` (density surface), `MarkerCluster` (groups nearby markers into clusters that expand on click — essential for >1,000 points), `MiniMap` (overview inset), `MeasureControl` (distance tool).

### 5. plotly Mapbox
`plotly.express.scatter_mapbox()` (Python) and `plot_ly(type = "scattermapbox")` (R) provide an alternative interactive map engine using Mapbox vector tiles. Advantages: smoother rendering, 3D perspective, integration with plotly's hover/selection system. Disadvantage: requires a Mapbox access token for custom tiles (free tier available). For most course work, leaflet/folium is sufficient; plotly mapbox is useful for dashboards (Shiny, Dash, Streamlit integration).

### 6. deck.gl / pydeck
For very large datasets (>100K points), browser rendering via SVG (leaflet) becomes slow. `deck.gl` (and its Python wrapper `pydeck`) uses WebGL to render millions of points on the GPU. Supports 3D views, arc layers, hexagon aggregation, screen-space effects. Overkill for this course but worth knowing for professional spatial data science.

### 7. Layer Control and Composition
The most useful interactive maps combine multiple toggleable layers:
- **Base tiles**: offer 2–3 options (Light, Dark, Satellite) via `addLayersControl(baseGroups=)` or `folium.LayerControl()`.
- **Overlay groups**: separate event dots, heatmap, city markers, boundaries into named groups. Users toggle each on/off.
- **Default visibility**: hide the heatmap by default (`hideGroup("Heatmap")` in R, `show=False` in folium FeatureGroup) so the map loads clean.

### 8. Static vs Interactive: Decision Framework
**Static** (ggplot2 + geom_sf, geopandas.plot): PDF reports, journal papers, presentations, print posters, reproducibility required. **Interactive** (leaflet, folium, plotly): web dashboards, exploratory analysis, stakeholder engagement, large datasets, detail-on-demand needed. **Best practice**: produce both from the same data pipeline. In R, `tmap_mode()` toggles with one command. In Python, produce `geopandas.plot()` for static and `folium` for interactive side-by-side.

### 9. Export and Sharing
leaflet/folium maps export as **standalone HTML** files: no server needed, viewable in any browser, shareable by email or LMS. File size depends on data volume (GeoJSON embedded in HTML) — keep to <5 MB for email. For larger maps, host on GitHub Pages or embed in Quarto/Jupyter HTML output. Screenshots for PDF reports: use browser developer tools (Cmd+Shift+4 on Mac) or `webshot2::webshot()` in R.

### References
- leaflet for R: https://rstudio.github.io/leaflet/
- folium: https://python-visualization.github.io/folium/
- plotly mapbox: https://plotly.com/python/mapbox-layers/
- deck.gl: https://deck.gl/
- Lovelace, R. et al. (2019). *Geocomputation with R*, Chapter 8.
