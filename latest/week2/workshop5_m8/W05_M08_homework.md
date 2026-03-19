# Workshop 5 · Module 8 — Homework
## Interactive Maps

**Due**: Before Workshop 5, Module 10
**Format**: R script + Python script + HTML exports + PDF report (max 5 pages)
**Weight**: Part of Workshop 5 homework (5% of total grade)

### Part A — Basic Interactive Map (20 points)
Create an interactive map of 8 Albanian cities using leaflet (R) and folium (Python). Each city should have: (a) a CircleMarker with radius proportional to population, (b) a popup showing name, population, and GDP per capita (formatted with commas and EUR), (c) a tooltip showing just the city name on hover. Use CartoDB Positron tiles. Export both as standalone HTML files.

### Part B — Multi-Layer Map (30 points)
Create a combined interactive map with three toggleable layers: (a) "Events" — 300 simulated seismic events as small red circle markers (radius = magnitude/2), (b) "Heatmap" — a HeatMap layer of the same events (hidden by default), (c) "Cities" — the 8 cities as larger blue markers. Add a LayerControl so users can toggle each layer on/off. Add at least two base tile options (Light and Dark). Export as HTML.

### Part C — Tile Comparison (20 points)
Produce the same city map with 4 different tile providers: CartoDB Positron, CartoDB DarkMatter, OpenStreetMap, and Esri Satellite (or Stamen Toner). Either as a single map with tile toggle or as 4 separate maps. In 100 words, explain which tile provider is best for: (a) population analysis, (b) terrain context, (c) print/screenshot.

### Part D — Static + Interactive Pair (30 points)
Produce the SAME map content as both: (a) a static PNG using ggplot2 + geom_sf (R) or geopandas.plot (Python), and (b) an interactive HTML using leaflet/folium. In 150 words, compare the two: what can you learn from the interactive version that is invisible in the static version? When would you prefer the static version?

### Submission Checklist
- [ ] `W05_M08_homework.R` + `W05_M08_homework.py`
- [ ] HTML exports: basic, multi-layer, tile comparison
- [ ] Static PNG (300 dpi)
- [ ] PDF report (max 5 pages) with screenshots of interactive maps
