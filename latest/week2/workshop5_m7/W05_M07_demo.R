# ============================================================
# Workshop 5 — Module 7: Point Maps & Spatial Patterns
# Integrated R Script — UNYT Tirana
# ============================================================
library(tidyverse); library(sf); dir.create("output", showWarnings = FALSE)

# ── 1. SIMULATED EVENT DATA (earthquakes near Albania) ───
set.seed(42)
n_events <- 500
events <- tibble(
  lon = rnorm(n_events, 19.82, 0.5),
  lat = rnorm(n_events, 41.00, 0.4),
  magnitude = rexp(n_events, rate = 1) + 2,  # min ~2, right-skewed
  depth_km  = runif(n_events, 1, 60))

# Convert to sf
events_sf <- st_as_sf(events, coords = c("lon", "lat"), crs = 4326)

# Albanian cities for proportional symbols
cities <- tibble(
  name = c("Tirana", "Durrës", "Vlorë", "Shkodër", "Elbasan", "Korçë",
           "Fier", "Berat"),
  lon  = c(19.82, 19.45, 19.49, 19.51, 20.08, 20.78, 19.55, 19.95),
  lat  = c(41.33, 41.32, 40.47, 42.07, 41.11, 40.62, 40.72, 40.70),
  pop  = c(420000, 115000, 79000, 77000, 78000, 51000, 85000, 32000))
cities_sf <- st_as_sf(cities, coords = c("lon", "lat"), crs = 4326)

# ── 2. DOT MAP ──────────────────────────────────────────
p_dot <- ggplot() +
  geom_sf(data = events_sf, size = 0.5, alpha = 0.3, color = "#E53935") +
  theme_void(base_size = 10) +
  labs(title = "Dot Map: 500 Simulated Seismic Events",
       subtitle = "Each point = one earthquake; no size encoding")
ggsave("output/dot_map.png", p_dot, width = 6, height = 7, dpi = 300)

# ── 3. PROPORTIONAL SYMBOL MAP ──────────────────────────
p_prop <- ggplot() +
  geom_sf(data = cities_sf, aes(size = pop), color = "#1565C0",
    alpha = 0.5, show.legend = "point") +
  geom_sf_text(data = cities_sf, aes(label = name), size = 2.5,
    nudge_y = 0.08) +
  scale_size(range = c(2, 14), name = "Population",
    labels = scales::comma) +
  theme_void(base_size = 10) +
  labs(title = "Proportional Symbol Map: Albanian Cities",
       subtitle = "Bubble size = population (2023)")
ggsave("output/prop_symbol.png", p_prop, width = 6, height = 7, dpi = 300)

# ── 4. OVERPLOTTING SOLUTIONS ────────────────────────────
# (a) Low alpha
p_alpha <- ggplot(events, aes(x = lon, y = lat)) +
  geom_point(size = 0.5, alpha = 0.08, color = "#E53935") +
  theme_minimal(base_size = 8) +
  labs(title = "(a) Low alpha (0.08)")

# (b) Hexbin
p_hex <- ggplot(events, aes(x = lon, y = lat)) +
  geom_hex(bins = 25) +
  scale_fill_viridis_c(name = "Count") +
  theme_minimal(base_size = 8) +
  labs(title = "(b) Hexbin")

# (c) 2D KDE contour
p_kde <- ggplot(events, aes(x = lon, y = lat)) +
  stat_density2d(aes(fill = after_stat(level)),
    geom = "polygon", alpha = 0.6) +
  scale_fill_viridis_c(name = "Density") +
  geom_point(size = 0.2, alpha = 0.05) +
  theme_minimal(base_size = 8) +
  labs(title = "(c) 2D KDE Contour")

# (d) Marginal distributions (ggExtra)
library(ggExtra)
p_base <- ggplot(events, aes(x = lon, y = lat)) +
  geom_point(size = 0.3, alpha = 0.1, color = "#1565C0") +
  theme_minimal(base_size = 8)
p_marg <- ggMarginal(p_base, type = "histogram",
  fill = "#1565C0", alpha = 0.3)

library(patchwork)
p_grid <- (p_alpha | p_hex | p_kde) +
  plot_annotation(title = "Overplotting Solutions: 500 Events",
    tag_levels = "a")
ggsave("output/overplotting_panel.png", p_grid, width = 12, height = 4, dpi = 300)
ggsave("output/marginal_map.png", p_marg, width = 6, height = 6, dpi = 300)

# ── 5. PROPORTIONAL + KDE OVERLAY ───────────────────────
p_combo <- ggplot() +
  stat_density2d(data = events, aes(x = lon, y = lat,
    fill = after_stat(level)), geom = "polygon", alpha = 0.5) +
  scale_fill_viridis_c(name = "Event\nDensity") +
  geom_point(data = cities, aes(x = lon, y = lat, size = pop),
    color = "#E53935", alpha = 0.7) +
  geom_text(data = cities, aes(x = lon, y = lat, label = name),
    size = 2, nudge_y = 0.07, color = "#333") +
  scale_size(range = c(2, 12), name = "Population",
    labels = scales::comma) +
  theme_void(base_size = 9) +
  labs(title = "KDE Density + Proportional Symbols",
       subtitle = "Events (density) overlaid with cities (bubble)")
ggsave("output/combo_map.png", p_combo, width = 7, height = 7, dpi = 300)

# ── 6. INTERACTIVE: leaflet dot map ─────────────────────
# library(leaflet)
# leaflet(events_sf) |>
#   addProviderTiles("CartoDB.Positron") |>
#   addCircleMarkers(
#     radius = ~magnitude / 2,
#     color = "#E53935", fillOpacity = 0.4, weight = 0.5,
#     popup = ~paste0("Mag: ", round(magnitude, 1),
#                     "<br>Depth: ", round(depth_km, 0), " km"),
#     label = ~paste0("M", round(magnitude, 1)))
#
# # Heatmap overlay
# library(leaflet.extras)
# leaflet(events_sf) |>
#   addProviderTiles("CartoDB.DarkMatter") |>
#   addHeatmap(lng = ~lon, lat = ~lat,
#     intensity = ~magnitude, blur = 20, radius = 15)

cat("\n── All W05-M07 R outputs saved ──\n")
