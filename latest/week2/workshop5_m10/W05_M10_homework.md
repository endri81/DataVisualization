# Workshop 5 — Homework (Final)
## Real Estate Dataset: Complete Multivariate + Spatial EDA

**Due**: Before Workshop 6, Module 1
**Format**: R script + Python script + HTML interactive map + PDF/HTML report (max 8 pages)
**Weight**: 5% of total grade

### The Assignment
Perform a complete multivariate + spatial EDA on the real estate dataset (simulated or real_estate.xlsx), integrating all W05 techniques. This is the summative assessment for Workshop 5.

### Required Sections

1. **Data description and cleaning** (1 page): rows, columns, types, derived variables (price_sqm), any cleaning steps.

2. **Six-panel EDA dashboard** (1 page): composed with patchwork (R) / GridSpec (Python). Must include at least: price histogram, area vs price scatter by type, price/sqm by neighbourhood, one chart of your choice. Panel labels, title, caption required.

3. **PCA biplot** (1 page): 6 numeric features, scaled, coloured by type. Interpret PC1 and PC2 in 100 words (what do the loading arrows mean?).

4. **Correlation heatmap** (0.5 page): clustered, lower triangle, diverging palette, annotated. Identify the two strongest and weakest correlations.

5. **Parallel coordinates** (0.5 page): 5 axes, coloured by type. In 100 words, what pattern distinguishes houses from apartments?

6. **Spatial point map** (1 page): static (ggplot2 + geom_sf / geopandas) and interactive (leaflet / folium). Colour = price/sqm, size = area. Popups with property details.

7. **Four numbered findings** (1 page): Finding → Evidence → Implication format. At least one must involve the spatial dimension (geography).

8. **Limitations and next steps** (0.5 page): What can't this EDA answer? What additional data or methods would you need?

### Bonus (+5 points)
- Clustered heatmap (z-scored) of a 30-property subset with annotation sidebar by type.
- Produce both static and interactive versions of the same map content.

### Submission Checklist
- [ ] `W05_homework.R` + `W05_homework.py`
- [ ] Dashboard PNG + PDF (300 dpi)
- [ ] PCA biplot, heatmap, parallel coords PNGs
- [ ] Static spatial map PNG
- [ ] Interactive map HTML (leaflet or folium)
- [ ] PDF/HTML report (max 8 pages)
