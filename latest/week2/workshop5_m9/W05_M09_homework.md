# Workshop 5 · Module 9 — Homework
## Snow's Cholera Map: Saving Lives with Data

**Due**: Before Workshop 5, Module 10 (Lab)
**Format**: R script + Python script + HTML export + PDF report (max 6 pages)
**Weight**: Part of Workshop 5 homework (5% of total grade)

### Part A — Static Recreation (25 points)
Using the simulated Broad Street data (or the real Snow dataset from Robin Wilson's GitHub), produce a static "Snow's map" showing deaths as small crosses and pumps as coloured triangles. Label each pump. Produce in both R (`ggplot2 + geom_sf`) and Python (`matplotlib`). The Broad Street pump should be visually distinct (e.g., red vs blue for others).

### Part B — Voronoi Tessellation (25 points)
Compute Voronoi cells around the 5 pumps. Overlay the Voronoi boundaries (dashed blue lines) on the death + pump map from Part A. Count the number of deaths in each Voronoi cell. Produce a bar chart showing deaths per pump (Broad Street highlighted in red). In 150 words, explain how the Voronoi analysis formalises Snow's visual argument.

### Part C — KDE Density Surface (25 points)
Compute a 2D KDE of the death locations and overlay as filled contours on the pump map. In 100 words, compare the KDE hotspot with the Voronoi cell boundaries: do they tell the same story? What does KDE add beyond Voronoi?

### Part D — Interactive Version (25 points)
Produce an interactive map using leaflet (R) or folium (Python) with three toggleable layers: "Deaths" (circle markers), "Pumps" (larger markers with popups), and "Heatmap" (KDE-style heat layer, hidden by default). Centre the map on the Broad Street pump at zoom 17. Export as standalone HTML. In 100 words, explain what the interactive version reveals that the static version cannot show.

### Bonus (+5 points)
Use the real Snow dataset (download from Robin Wilson's GitHub). Compare the real data pattern with your simulated version.

### Submission Checklist
- [ ] `W05_M09_homework.R` + `W05_M09_homework.py`
- [ ] Static maps: snow_map.png, voronoi_map.png, kde_map.png, bar_chart.png (300 dpi)
- [ ] Interactive HTML: snow_interactive.html
- [ ] PDF report (max 6 pages)
