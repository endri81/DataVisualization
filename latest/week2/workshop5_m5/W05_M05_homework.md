# Workshop 5 · Module 5 — Homework
## Introduction to Spatial Data

**Due**: Before Workshop 5, Module 7
**Format**: R script + Python script + PDF report (max 4 pages)
**Weight**: Part of Workshop 5 homework (5% of total grade)

### Part A — CSV to Spatial (25 points)
Create a CSV file with 8 Albanian cities: Tirana, Durrës, Vlorë, Shkodër, Elbasan, Korçë, Fier, Berat. Include name, longitude, latitude, and population. Convert to a spatial object in R (`st_as_sf()`) and Python (`gpd.GeoDataFrame()`). Verify the CRS is EPSG:4326. Plot as proportional symbols (size = population). Produce in both languages.

### Part B — CRS Transformation (25 points)
Transform the cities to UTM Zone 34N (EPSG:32634). Compute the distance matrix between all 8 cities (in km). In 100 words, explain why the distances computed in UTM differ slightly from those computed in WGS 84, and which is more accurate for Albania.

### Part C — File Format Round-Trip (20 points)
Write the cities to GeoJSON, GeoPackage, and (optionally) Shapefile. Read each back and verify the geometry and attributes are preserved. In 100 words, compare the three formats: file count, file size, and readability.

### Part D — Overlay Map (30 points)
Create a simplified Albania polygon (approximate the border with 10–15 coordinate pairs). Overlay the 8 cities as proportional symbols on the country polygon. Produce with `geom_sf()` (R) and `geopandas.plot()` (Python). Add city name labels. Export as PNG (300 dpi).

### Submission Checklist
- [ ] `cities.csv` (source data)
- [ ] `W05_M05_homework.R` + `W05_M05_homework.py`
- [ ] `cities.geojson` + `cities.gpkg` (exported spatial files)
- [ ] All figures as PNG (300 dpi)
- [ ] PDF report (max 4 pages)
