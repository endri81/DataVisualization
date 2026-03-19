# Workshop 5 · Module 7 — Homework
## Point Maps & Spatial Patterns

**Due**: Before Workshop 5, Module 9
**Format**: R script + Python script + PDF report (max 5 pages)
**Weight**: Part of Workshop 5 homework (5% of total grade)

### Part A — Dot Map + Proportional Symbols (25 points)
Using the simulated seismic event data (500 points), produce: (a) a dot map showing all events, (b) a proportional symbol map of the 8 Albanian cities (size = population). Overlay both on the same figure. Produce in R (`geom_sf`) and Python (`ax.scatter`). In 100 words, describe the spatial pattern: where are events concentrated relative to cities?

### Part B — Overplotting Panel (30 points)
Produce a 1×3 panel comparing three overplotting solutions on the event data: (a) low alpha (0.05–0.1), (b) hexbin, (c) 2D KDE contour. Compose with patchwork (R) and subplots (Python). In 150 words, compare: which solution best reveals the event hotspot? Which loses the most information?

### Part C — KDE + Proportional Combo (20 points)
Produce a single map with the KDE density surface (filled contour, low alpha) as background and city proportional symbols (blue circles, sized by population) on top. In 100 words, interpret: does the seismic hotspot coincide with a population centre? What are the implications?

### Part D — Interactive Map (25 points)
Produce an interactive point map using leaflet (R) or folium (Python). Include: (a) circle markers for events (size = magnitude, popup = magnitude + depth), (b) city markers with population tooltips, (c) a heatmap layer toggle. Export as HTML. Include a screenshot in your report.

### Submission Checklist
- [ ] `W05_M07_homework.R` + `W05_M07_homework.py`
- [ ] Static figures as PNG (300 dpi)
- [ ] Interactive HTML file(s)
- [ ] PDF report (max 5 pages)
