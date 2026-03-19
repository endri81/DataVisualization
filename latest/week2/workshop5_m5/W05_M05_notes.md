# Workshop 5 · Module 5 — Course Notes
## Introduction to Spatial Data

### 1. Four Spatial Data Types
**Point**: a single (x, y) or (lon, lat) coordinate pair representing a discrete location — earthquakes, stores, crime incidents. **Line** (LineString): an ordered sequence of coordinates representing a path — roads, rivers, flight routes. **Polygon**: a closed ring of coordinates enclosing an area — countries, districts, building footprints. **Raster**: a regular grid of cells, each containing a value — satellite imagery, elevation models, temperature grids. In this course we focus on vector data (point, line, polygon); raster requires specialised packages (stars/terra in R, rasterio in Python).

### 2. Coordinate Reference Systems (CRS)
Every spatial dataset must have a CRS specifying how coordinates map to locations on Earth. Two types: **Geographic CRS** (units = degrees of latitude/longitude; the globe is 3D but coordinates are angular). Standard: WGS 84 (EPSG:4326) — used by GPS, web maps, and as the default storage format. **Projected CRS** (units = metres or feet; the globe is "flattened" onto a 2D plane using a mathematical projection). Examples: Web Mercator (EPSG:3857, used by Google Maps — distorts area near poles), UTM Zone 34N (EPSG:32634, appropriate for Albania — accurate area and distance within ±3° longitude), Albanian National Grid (EPSG:6870, official cadaster).

**Critical rule**: always use a geographic CRS (4326) for storage and web maps. Transform to a projected CRS (UTM) before computing distances or areas, because degrees are not equal-length units (1° longitude shrinks toward the poles). In R: `st_transform(sf_obj, 32634)`. In Python: `gdf.to_crs(epsg=32634)`.

### 3. Spatial File Formats
**GeoJSON** (.geojson): human-readable JSON text, web-friendly, GitHub renders it, lightweight for small datasets. **Shapefile** (.shp + .dbf + .shx + .prj): ESRI legacy format, requires 4+ files together, 2GB limit, column names truncated at 10 characters — still widely used but being replaced. **GeoPackage** (.gpkg): SQLite-based, single file, no size limit, supports multiple layers — the modern replacement for Shapefile. **CSV with lat/lon**: simplest format; requires manual conversion to spatial. All three spatial formats are readable by `st_read()` (R) and `gpd.read_file()` (Python) with no format-specific arguments.

### 4. The sf / geopandas Ecosystem
**R**: The `sf` (simple features) package is the modern standard, replacing the older `sp`/`rgdal`/`rgeos` stack. sf objects are tibbles with a `geometry` column — they integrate seamlessly with dplyr and ggplot2 (`geom_sf()`). Key functions: `st_read()`, `st_write()`, `st_transform()`, `st_crs()`, `st_as_sf()` (CSV → spatial), `st_distance()`, `st_buffer()`, `st_intersection()`. For mapping: `tmap` provides a layered grammar (`tm_shape() + tm_polygons() + tm_dots()`) with instant interactive toggle (`tmap_mode("view")`).

**Python**: `geopandas` extends pandas with a `geometry` column (powered by `shapely` for geometry operations and `fiona` for file I/O). GeoDataFrames support all pandas operations plus spatial: `.plot()`, `.to_crs()`, `.buffer()`, `.intersection()`. For interactive maps: `folium` wraps Leaflet.js — `folium.Map()` + `Marker()` / `CircleMarker()` / `Choropleth()`.

### 5. CSV to Spatial
The most common starting point: a CSV with latitude and longitude columns. In R: `st_as_sf(df, coords = c("lon", "lat"), crs = 4326)`. In Python: create `shapely.geometry.Point(lon, lat)` for each row, then `gpd.GeoDataFrame(df, geometry=points, crs="EPSG:4326")`. Always specify the CRS at creation time; omitting it leads to silent errors in all downstream operations.

### References
- Lovelace, R., Nowosad, J. & Muenchow, J. (2019). *Geocomputation with R*. CRC Press. https://geocompr.robinlovelace.net
- Rey, S., Arribas-Bel, D. & Wolf, L. (2020). *Geographic Data Science with Python*. https://geographicdata.science
- sf package: https://r-spatial.github.io/sf/
- geopandas: https://geopandas.org
