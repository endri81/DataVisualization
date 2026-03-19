# Workshop 5 · Module 6 — Homework
## Choropleth Maps

**Due**: Before Workshop 5, Module 8
**Format**: R script + Python script + PDF report (max 5 pages)
**Weight**: Part of Workshop 5 homework (5% of total grade)

### Part A — Sequential Choropleth (25 points)
Using the simulated Albanian district data (or real administrative boundaries if available), produce a choropleth of GDP per capita with a sequential palette (Blues or viridis). Apply Jenks (natural breaks) classification with k=5. Produce in both R (`ggplot2 + geom_sf` or `tmap`) and Python (`geopandas.plot(scheme="NaturalBreaks")`). Add district labels and a properly formatted legend.

### Part B — Diverging Choropleth (25 points)
Compute the deviation of each district's unemployment rate from the national average. Produce a diverging choropleth (RdBu, centred at 0). In 100 words, explain why a diverging palette is correct here and a sequential palette would be misleading.

### Part C — Classification Comparison (25 points)
Produce a side-by-side 1×3 panel showing the same GDP data classified by: (a) equal interval, (b) quantile, (c) Jenks. In 150 words, explain which classification best reveals the pattern and why. Note: if using geopandas, install `mapclassify` for classification schemes.

### Part D — Interactive Choropleth (25 points)
Produce an interactive choropleth using `tmap_mode("view")` (R) or `folium.Choropleth()` (Python). Add hover tooltips showing district name and value. Export as HTML. Include a screenshot in your PDF report.

### Submission Checklist
- [ ] `W05_M06_homework.R` + `W05_M06_homework.py`
- [ ] Static choropleth PNGs (300 dpi)
- [ ] Interactive HTML file
- [ ] PDF report (max 5 pages)
