# ============================================================
# Workshop 5 — Module 5: Introduction to Spatial Data
# Integrated R Script — UNYT Tirana
# ============================================================
library(tidyverse); library(sf); dir.create("output", showWarnings = FALSE)

# ── 1. CREATE SPATIAL DATA FROM SCRATCH ──────────────────
# Albanian cities as a tibble with coordinates
cities <- tibble(
  name     = c("Tirana", "Durrës", "Vlorë", "Shkodër", "Elbasan", "Korçë"),
  lon      = c(19.82, 19.45, 19.49, 19.51, 20.08, 20.78),
  lat      = c(41.33, 41.32, 40.47, 42.07, 41.11, 40.62),
  pop_2023 = c(420000, 115000, 79000, 77000, 78000, 51000))

# Convert to sf POINT object (CRS = WGS 84)
cities_sf <- st_as_sf(cities, coords = c("lon", "lat"), crs = 4326)
cat("Class:", class(cities_sf), "\n")
cat("CRS:", st_crs(cities_sf)$input, "\n")
print(cities_sf)

# ── 2. PLOT WITH ggplot2 + geom_sf ──────────────────────
p_cities <- ggplot(cities_sf) +
  geom_sf(aes(size = pop_2023), color = "#E53935", alpha = 0.6) +
  geom_sf_text(aes(label = name), size = 3, nudge_y = 0.08) +
  scale_size(range = c(2, 12), name = "Population") +
  theme_void() +
  labs(title = "Albanian Cities (sf POINT, EPSG:4326)")
ggsave("output/cities_sf.png", p_cities, width = 6, height = 7, dpi = 300)

# ── 3. CRS TRANSFORMATION ───────────────────────────────
# Transform to UTM Zone 34N for distance calculations
cities_utm <- st_transform(cities_sf, crs = 32634)
cat("\nUTM CRS:", st_crs(cities_utm)$input, "\n")

# Distance matrix (in metres)
dist_mat <- st_distance(cities_utm)
rownames(dist_mat) <- cities$name; colnames(dist_mat) <- cities$name
cat("\nDistance Tirana–Vlorë:", round(dist_mat["Tirana", "Vlorë"] / 1000, 1), "km\n")
cat("Distance Tirana–Shkodër:", round(dist_mat["Tirana", "Shkodër"] / 1000, 1), "km\n")

# ── 4. READ SPATIAL FILE (GeoJSON) ──────────────────────
# If you have a GeoJSON file:
# alb <- st_read("albania_districts.geojson")
# st_crs(alb)              # check CRS
# ggplot(alb) + geom_sf()  # quick plot

# Simulated polygon (simplified Albania outline)
alb_coords <- matrix(c(
  19.3, 39.6,  19.8, 39.7,  20.1, 39.8,  20.6, 40.0,
  21.0, 40.5,  20.7, 41.0,  20.5, 41.5,  20.3, 42.0,
  20.0, 42.1,  19.5, 41.8,  19.3, 41.5,  19.0, 40.5,
  19.3, 39.6), ncol = 2, byrow = TRUE)
alb_poly <- st_sf(name = "Albania",
  geometry = st_sfc(st_polygon(list(alb_coords)), crs = 4326))

# Overlay cities on country
p_overlay <- ggplot() +
  geom_sf(data = alb_poly, fill = "#E3F2FD", color = "#1565C0", linewidth = 1) +
  geom_sf(data = cities_sf, aes(size = pop_2023), color = "#E53935", alpha = 0.6) +
  geom_sf_text(data = cities_sf, aes(label = name), size = 2.5, nudge_y = 0.08) +
  scale_size(range = c(2, 10), name = "Population") +
  theme_void() +
  labs(title = "Albania: Cities (points) on Country (polygon)")
ggsave("output/overlay.png", p_overlay, width = 6, height = 7, dpi = 300)

# ── 5. FILE FORMAT I/O ──────────────────────────────────
# GeoJSON (web-friendly, text)
st_write(cities_sf, "output/cities.geojson", delete_dsn = TRUE)
# GeoPackage (modern binary, replaces Shapefile)
st_write(cities_sf, "output/cities.gpkg", delete_dsn = TRUE)
# Read back
cities_back <- st_read("output/cities.geojson", quiet = TRUE)
cat("\nRead back:", nrow(cities_back), "features\n")

# ── 6. tmap PREVIEW ─────────────────────────────────────
# library(tmap)
# tmap_mode("plot")  # static
# tm_shape(alb_poly) +
#   tm_polygons(col = "#E3F2FD") +
#   tm_shape(cities_sf) +
#   tm_dots(size = "pop_2023", col = "#E53935",
#     title.size = "Population") +
#   tm_text("name", size = 0.7) +
#   tm_layout(title = "Albania")

# tmap_mode("view")  # switch to interactive leaflet!
# Same tm_ code now renders in browser

cat("\n── All W05-M05 R outputs saved ──\n")
