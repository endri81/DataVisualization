# ============================================================
# Workshop 5 — Module 6: Choropleth Maps
# Integrated R Script — UNYT Tirana
# ============================================================
library(tidyverse); library(sf); dir.create("output", showWarnings = FALSE)

# ── 1. SIMULATED ALBANIA DISTRICTS WITH DATA ────────────
# 12 districts (simplified) with population and GDP data
set.seed(42)
districts <- tibble(
  name = c("Tirana", "Durrës", "Elbasan", "Fier", "Korçë", "Shkodër",
           "Vlorë", "Berat", "Dibër", "Gjirokastër", "Kukës", "Lezhë"),
  population = c(420000, 115000, 78000, 85000, 51000, 77000,
                 79000, 32000, 36000, 28000, 26000, 38000),
  gdp_per_cap = c(8500, 5200, 3800, 4100, 3500, 3900,
                  4800, 3200, 2800, 3600, 2500, 3400),
  unemployment = c(12.5, 15.3, 18.7, 16.2, 19.8, 17.1,
                   14.3, 20.5, 22.1, 18.9, 24.3, 17.8),
  # Simplified centroids (for demonstration)
  lon = c(19.82, 19.45, 20.08, 19.55, 20.78, 19.51,
          19.49, 19.95, 20.24, 20.14, 20.42, 19.64),
  lat = c(41.33, 41.32, 41.11, 40.72, 40.62, 42.07,
          40.47, 40.70, 41.61, 40.08, 42.08, 41.78))

# Create simple rectangular "district" polygons around centroids
# (In real work, you'd load actual administrative boundaries)
make_rect <- function(lon, lat, dx = 0.25, dy = 0.15) {
  coords <- matrix(c(lon-dx, lat-dy, lon+dx, lat-dy,
    lon+dx, lat+dy, lon-dx, lat+dy, lon-dx, lat-dy), ncol = 2, byrow = TRUE)
  st_polygon(list(coords))
}
geom <- pmap(list(districts$lon, districts$lat), ~make_rect(..1, ..2))
districts_sf <- st_sf(districts, geometry = st_sfc(geom, crs = 4326))

# ── 2. CHOROPLETH WITH ggplot2 + geom_sf ────────────────
# Sequential palette for population (magnitude)
p_pop <- ggplot(districts_sf) +
  geom_sf(aes(fill = population), color = "white", linewidth = 0.5) +
  scale_fill_viridis_c(option = "plasma", name = "Population",
    labels = scales::comma) +
  theme_void(base_size = 10) +
  labs(title = "Albania: Population by District",
       subtitle = "Sequential palette (plasma) for magnitude data",
       caption = "Source: Simulated data | UNYT")
ggsave("output/choropleth_population.png", p_pop, width = 7, height = 8, dpi = 300)

# Diverging palette for unemployment (deviation from national average)
nat_avg <- mean(districts$unemployment)
p_unemp <- ggplot(districts_sf) +
  geom_sf(aes(fill = unemployment - nat_avg), color = "white", linewidth = 0.5) +
  scale_fill_gradient2(low = "#1565C0", mid = "white", high = "#E53935",
    midpoint = 0, name = "Above/Below\nNational Avg (pp)") +
  theme_void(base_size = 10) +
  labs(title = "Albania: Unemployment Deviation from National Average",
       subtitle = paste0("Diverging palette centred at national avg (",
                         round(nat_avg, 1), "%)"))
ggsave("output/choropleth_unemployment.png", p_unemp, width = 7, height = 8, dpi = 300)

# ── 3. CLASSIFICATION METHODS ───────────────────────────
# Equal interval
p_equal <- ggplot(districts_sf) +
  geom_sf(aes(fill = cut(gdp_per_cap, breaks = 5)), color = "white") +
  scale_fill_brewer(palette = "Blues", name = "GDP/cap\n(Equal Interval)") +
  theme_void(base_size = 9) + labs(title = "Equal Interval (5 classes)")

# Quantile (equal count per class)
brks_quant <- quantile(districts$gdp_per_cap, probs = seq(0, 1, 0.2))
p_quant <- ggplot(districts_sf) +
  geom_sf(aes(fill = cut(gdp_per_cap, breaks = brks_quant, include.lowest = TRUE)),
    color = "white") +
  scale_fill_brewer(palette = "Blues", name = "GDP/cap\n(Quantile)") +
  theme_void(base_size = 9) + labs(title = "Quantile (5 classes)")

library(patchwork)
ggsave("output/classification_comparison.png", p_equal | p_quant,
  width = 12, height = 6, dpi = 300)

# ── 4. tmap (static + interactive toggle) ───────────────
# library(tmap)
# # Static
# tmap_mode("plot")
# tm_shape(districts_sf) +
#   tm_fill("gdp_per_cap", style = "jenks", n = 5,
#     palette = "Blues", title = "GDP/cap (EUR)") +
#   tm_borders(col = "white", lwd = 0.5) +
#   tm_text("name", size = 0.5) +
#   tm_layout(title = "Albania: GDP per Capita",
#     legend.outside = TRUE)
#
# # Interactive (one command switch!)
# tmap_mode("view")
# # Same tm_ code now renders as leaflet map in browser

# ── 5. ANNOTATED CHOROPLETH (best practice) ─────────────
p_best <- ggplot(districts_sf) +
  geom_sf(aes(fill = gdp_per_cap), color = "white", linewidth = 0.5) +
  geom_sf_text(aes(label = paste0(name, "\n", scales::dollar(gdp_per_cap))),
    size = 2.2, color = "grey20") +
  scale_fill_distiller(palette = "Blues", direction = 1,
    name = "GDP per capita (EUR)", labels = scales::dollar) +
  theme_void(base_size = 10) +
  labs(title = "Albania: GDP per Capita by District",
       subtitle = "Sequential palette (Blues), annotated with values",
       caption = "Classification: continuous (no binning)")
ggsave("output/choropleth_annotated.png", p_best, width = 7, height = 8, dpi = 300)

cat("\n── All W05-M06 R outputs saved ──\n")
