# ============================================================
# Workshop 5 — Module 9: Snow's Cholera Map — Saving Lives with Data
# Integrated R Script — UNYT Tirana
# ============================================================
library(tidyverse); library(sf); dir.create("output", showWarnings = FALSE)

# ── 1. SIMULATED BROAD STREET DATA ──────────────────────
# (Real Snow data available at https://blog.rtwilson.com/john-snows-cholera-data/)
# Here we simulate the essential structure for demonstration
set.seed(1854)

# Pumps: Broad Street pump at centre, others scattered
pumps <- tibble(
  name = c("Broad Street", "Pump 2", "Pump 3", "Pump 4", "Pump 5"),
  lon  = c(-0.13680, -0.1400, -0.1330, -0.1355, -0.1390),
  lat  = c(51.5134,  51.5155, 51.5105, 51.5160, 51.5110))
pumps_sf <- st_as_sf(pumps, coords = c("lon", "lat"), crs = 4326)

# Deaths: 80% cluster near Broad Street, 20% scattered
n_deaths <- 500
deaths_broad <- tibble(
  lon = rnorm(400, -0.13680, 0.0008),
  lat = rnorm(400, 51.5134, 0.0006))
deaths_other <- tibble(
  lon = rnorm(100, -0.1370, 0.0025),
  lat = rnorm(100, 51.5135, 0.0020))
deaths <- bind_rows(deaths_broad, deaths_other)
deaths_sf <- st_as_sf(deaths, coords = c("lon", "lat"), crs = 4326)

# ── 2. SNOW'S MAP RECREATION (static) ───────────────────
p_snow <- ggplot() +
  # Deaths as small crosses
  geom_sf(data = deaths_sf, shape = 4, size = 0.8, alpha = 0.4, color = "#333") +
  # Pumps as red triangles
  geom_sf(data = pumps_sf, shape = 17, size = 4, color = "#E53935") +
  geom_sf_text(data = pumps_sf, aes(label = name), size = 2.5,
    nudge_y = 0.0005, color = "#E53935", fontface = "bold") +
  theme_void(base_size = 10) +
  labs(title = "Snow's Cholera Map (Simulated Recreation)",
       subtitle = "Deaths (×) cluster around the Broad Street pump (▲)",
       caption = "Based on John Snow (1854) | Simulated data for demonstration")
ggsave("output/snow_map.png", p_snow, width = 7, height = 7, dpi = 300)

# ── 3. VORONOI TESSELLATION ─────────────────────────────
# Compute Voronoi polygons around pumps
pump_union <- st_union(pumps_sf)
# st_voronoi requires a GEOMETRYCOLLECTION input
voronoi_geom <- st_voronoi(pump_union)
voronoi_sf <- st_sf(geometry = st_collection_extract(voronoi_geom, "POLYGON"), crs = 4326)

# Clip to a bounding box around the study area
bbox_poly <- st_as_sfc(st_bbox(c(
  xmin = -0.143, ymin = 51.509, xmax = -0.131, ymax = 51.518), crs = 4326))
voronoi_clipped <- st_intersection(voronoi_sf, bbox_poly)

# Count deaths per Voronoi cell
deaths_in_cells <- st_join(deaths_sf, voronoi_clipped) |>
  st_drop_geometry() |>
  count(name = "cell") |>
  mutate(cell_id = row_number())

p_voronoi <- ggplot() +
  geom_sf(data = voronoi_clipped, fill = NA, color = "#1565C0",
    linewidth = 1, linetype = "dashed") +
  geom_sf(data = deaths_sf, shape = 4, size = 0.5, alpha = 0.3, color = "#333") +
  geom_sf(data = pumps_sf, shape = 17, size = 5, color = "#E53935") +
  geom_sf_text(data = pumps_sf, aes(label = name), size = 2.5,
    nudge_y = 0.0005, color = "#E53935", fontface = "bold") +
  theme_void(base_size = 10) +
  labs(title = "Voronoi Tessellation: Nearest-Pump Assignment",
       subtitle = "Blue dashed lines partition space by closest pump",
       caption = "Broad Street cell contains disproportionate deaths")
ggsave("output/voronoi_map.png", p_voronoi, width = 7, height = 7, dpi = 300)

# ── 4. KDE DENSITY SURFACE ──────────────────────────────
p_kde <- ggplot() +
  stat_density2d(data = deaths, aes(x = lon, y = lat, fill = after_stat(level)),
    geom = "polygon", alpha = 0.5) +
  scale_fill_viridis_c(name = "Death\nDensity") +
  geom_point(data = pumps, aes(x = lon, y = lat),
    shape = 17, size = 4, color = "#E53935") +
  geom_text(data = pumps, aes(x = lon, y = lat, label = name),
    size = 2.5, nudge_y = 0.0005, color = "#E53935", fontface = "bold") +
  theme_void(base_size = 10) +
  labs(title = "KDE Density Surface: Death Hotspot",
       subtitle = "Peak density directly over the Broad Street pump")
ggsave("output/snow_kde.png", p_kde, width = 7, height = 7, dpi = 300)

# ── 5. DISTANCE ANALYSIS ────────────────────────────────
# For each death, compute distance to nearest pump
deaths_utm <- st_transform(deaths_sf, 32630)  # UTM zone 30N (London)
pumps_utm <- st_transform(pumps_sf, 32630)

# Distance matrix: deaths (rows) × pumps (cols)
dist_mat <- st_distance(deaths_utm, pumps_utm)
nearest_pump <- apply(dist_mat, 1, which.min)
nearest_name <- pumps$name[nearest_pump]
nearest_dist <- apply(dist_mat, 1, min) |> as.numeric()

deaths_analysis <- deaths |>
  mutate(nearest_pump = nearest_name, dist_m = nearest_dist)

cat("── Deaths by Nearest Pump ──\n")
deaths_analysis |> count(nearest_pump, sort = TRUE) |> print()
cat("\nMean distance to nearest pump:", round(mean(nearest_dist)), "m\n")
cat("Median distance to nearest pump:", round(median(nearest_dist)), "m\n")

# Bar chart of deaths per nearest pump
p_bar <- deaths_analysis |>
  count(nearest_pump) |>
  mutate(nearest_pump = fct_reorder(nearest_pump, n)) |>
  ggplot(aes(x = nearest_pump, y = n, fill = nearest_pump == "Broad Street")) +
  geom_col(width = 0.5, show.legend = FALSE) +
  scale_fill_manual(values = c("TRUE" = "#E53935", "FALSE" = "#BBBBBB")) +
  coord_flip() +
  theme_minimal(base_size = 10) +
  labs(title = "Deaths by Nearest Pump (Voronoi Assignment)",
       subtitle = "Broad Street pump's cell contains 80% of deaths",
       x = NULL, y = "Number of Deaths")
ggsave("output/snow_bar.png", p_bar, width = 7, height = 4, dpi = 300)

# ── 6. INTERACTIVE RECREATION ────────────────────────────
# library(leaflet); library(leaflet.extras)
# m <- leaflet() |>
#   addProviderTiles("CartoDB.Positron") |>
#   setView(lng = -0.1368, lat = 51.5134, zoom = 17) |>
#   addCircleMarkers(data = deaths_sf,
#     radius = 1, color = "#333", fillOpacity = 0.3, weight = 0,
#     group = "Deaths") |>
#   addMarkers(data = pumps_sf,
#     label = ~name, popup = ~name,
#     group = "Pumps") |>
#   addHeatmap(data = deaths_sf,
#     blur = 15, radius = 10, max = 0.05,
#     group = "Heatmap") |>
#   addLayersControl(
#     overlayGroups = c("Deaths", "Pumps", "Heatmap"),
#     options = layersControlOptions(collapsed = FALSE)) |>
#   hideGroup("Heatmap")
# htmlwidgets::saveWidget(m, "output/snow_interactive.html", selfcontained = TRUE)

cat("\n── All W05-M09 R outputs saved ──\n")
