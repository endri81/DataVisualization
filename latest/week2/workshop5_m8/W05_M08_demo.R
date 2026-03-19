# ============================================================
# Workshop 5 — Module 8: Interactive Maps
# Integrated R Script — UNYT Tirana
# ============================================================
library(tidyverse); dir.create("output", showWarnings = FALSE)

# ── DATA: Albanian cities + simulated events ─────────────
cities <- tibble(
  name = c("Tirana","Durrës","Vlorë","Shkodër","Elbasan","Korçë","Fier","Berat"),
  lon  = c(19.82, 19.45, 19.49, 19.51, 20.08, 20.78, 19.55, 19.95),
  lat  = c(41.33, 41.32, 40.47, 42.07, 41.11, 40.62, 40.72, 40.70),
  pop  = c(420000, 115000, 79000, 77000, 78000, 51000, 85000, 32000),
  gdp  = c(8500, 5200, 4800, 3900, 3800, 3500, 4100, 3200))

set.seed(42)
events <- tibble(
  lon = rnorm(300, 19.82, 0.4), lat = rnorm(300, 41.0, 0.3),
  magnitude = rexp(300, 1) + 2, depth = runif(300, 1, 50))

# ── 1. BASIC LEAFLET MAP ────────────────────────────────
library(leaflet)

# Simple markers with popups
m1 <- leaflet(cities) |>
  addProviderTiles("CartoDB.Positron") |>
  setView(lng = 19.82, lat = 41.33, zoom = 7) |>
  addCircleMarkers(
    lng = ~lon, lat = ~lat,
    radius = ~sqrt(pop) / 80,
    color = "#1565C0", fillOpacity = 0.6, weight = 1,
    popup = ~paste0(
      "<b>", name, "</b><br>",
      "Population: ", format(pop, big.mark = ","), "<br>",
      "GDP/cap: EUR ", format(gdp, big.mark = ",")),
    label = ~name)
# Save as standalone HTML
htmlwidgets::saveWidget(m1, "output/m08_basic.html", selfcontained = TRUE)

# ── 2. MULTIPLE TILE PROVIDERS ───────────────────────────
m2 <- leaflet() |>
  addProviderTiles("CartoDB.Positron", group = "Light") |>
  addProviderTiles("CartoDB.DarkMatter", group = "Dark") |>
  addProviderTiles("OpenStreetMap", group = "OSM") |>
  addProviderTiles("Esri.WorldImagery", group = "Satellite") |>
  setView(lng = 19.82, lat = 41.33, zoom = 7) |>
  addCircleMarkers(data = cities,
    lng = ~lon, lat = ~lat, radius = ~sqrt(pop) / 80,
    color = "#E53935", fillOpacity = 0.5, weight = 1,
    label = ~name, group = "Cities") |>
  addLayersControl(
    baseGroups = c("Light", "Dark", "OSM", "Satellite"),
    overlayGroups = c("Cities"),
    options = layersControlOptions(collapsed = FALSE))
htmlwidgets::saveWidget(m2, "output/m08_tiles.html", selfcontained = TRUE)

# ── 3. CIRCLE MARKERS WITH MAGNITUDE ────────────────────
pal_mag <- colorNumeric("YlOrRd", domain = events$magnitude)
m3 <- leaflet(events) |>
  addProviderTiles("CartoDB.Positron") |>
  addCircleMarkers(
    lng = ~lon, lat = ~lat,
    radius = ~magnitude,
    color = ~pal_mag(magnitude),
    fillOpacity = 0.5, weight = 0.5,
    popup = ~paste0("Mag: ", round(magnitude, 1),
                    "<br>Depth: ", round(depth), " km"),
    label = ~paste0("M", round(magnitude, 1))) |>
  addLegend(pal = pal_mag, values = ~magnitude,
    title = "Magnitude", position = "bottomright")
htmlwidgets::saveWidget(m3, "output/m08_events.html", selfcontained = TRUE)

# ── 4. HEATMAP (leaflet.extras) ──────────────────────────
library(leaflet.extras)
m4 <- leaflet(events) |>
  addProviderTiles("CartoDB.DarkMatter") |>
  addHeatmap(lng = ~lon, lat = ~lat,
    intensity = ~magnitude,
    blur = 20, radius = 15, max = 0.05)
htmlwidgets::saveWidget(m4, "output/m08_heatmap.html", selfcontained = TRUE)

# ── 5. COMBINED: dots + heatmap + layer control ─────────
m5 <- leaflet() |>
  addProviderTiles("CartoDB.Positron", group = "Light") |>
  addProviderTiles("CartoDB.DarkMatter", group = "Dark") |>
  addCircleMarkers(data = events,
    lng = ~lon, lat = ~lat, radius = ~magnitude / 2,
    color = "#E53935", fillOpacity = 0.3, weight = 0.3,
    group = "Events",
    popup = ~paste0("Mag: ", round(magnitude, 1))) |>
  addHeatmap(data = events,
    lng = ~lon, lat = ~lat, intensity = ~magnitude,
    blur = 20, radius = 15, max = 0.05,
    group = "Heatmap") |>
  addCircleMarkers(data = cities,
    lng = ~lon, lat = ~lat, radius = ~sqrt(pop) / 100,
    color = "#1565C0", fillOpacity = 0.6, weight = 1.5,
    group = "Cities", label = ~name,
    popup = ~paste0("<b>", name, "</b><br>Pop: ", format(pop, big.mark=","))) |>
  addLayersControl(
    baseGroups = c("Light", "Dark"),
    overlayGroups = c("Events", "Heatmap", "Cities"),
    options = layersControlOptions(collapsed = FALSE)) |>
  hideGroup("Heatmap")  # heatmap off by default
htmlwidgets::saveWidget(m5, "output/m08_combined.html", selfcontained = TRUE)

# ── 6. tmap INSTANT INTERACTIVE ──────────────────────────
# library(tmap); library(sf)
# cities_sf <- st_as_sf(cities, coords = c("lon","lat"), crs = 4326)
# tmap_mode("view")  # one command: everything below is now interactive
# tm_shape(cities_sf) +
#   tm_dots(size = "pop", col = "#1565C0", title.size = "Population") +
#   tm_text("name", size = 0.7)
# # Switch back to static
# tmap_mode("plot")

cat("\n── All W05-M08 R outputs saved ──\n")
cat("HTML files in output/: m08_basic, m08_tiles, m08_events, m08_heatmap, m08_combined\n")
