# ============================================================
# Workshop 5 — Module 10: Lab — Multivariate EDA on Real Estate
# Integrated R Script — UNYT Tirana
# ============================================================
library(tidyverse); library(patchwork); dir.create("output", showWarnings = FALSE)

# ── 1. LOAD AND CLEAN REAL ESTATE DATA ──────────────────
# If real_estate.xlsx is available:
# library(readxl)
# re <- read_excel("real_estate.xlsx")

# Simulated real estate data for demonstration
set.seed(42); n <- 200
re <- tibble(
  id = 1:n,
  price = round(rlnorm(n, log(80000), 0.6)),
  area_sqm = round(rnorm(n, 85, 30) |> pmax(25)),
  bedrooms = sample(1:5, n, replace = TRUE, prob = c(0.1, 0.3, 0.35, 0.2, 0.05)),
  bathrooms = pmin(bedrooms, sample(1:3, n, replace = TRUE, prob = c(0.3, 0.5, 0.2))),
  year_built = sample(1970:2023, n, replace = TRUE),
  floor = sample(0:12, n, replace = TRUE),
  type = sample(c("apartment", "house"), n, replace = TRUE, prob = c(0.75, 0.25)),
  condition = sample(c("new", "renovated", "original"), n, replace = TRUE, prob = c(0.3, 0.4, 0.3)),
  # Simulated Tirana coordinates

  lon = rnorm(n, 19.82, 0.025),
  lat = rnorm(n, 41.33, 0.015),
  neighbourhood = sample(c("Blloku", "Komuna e Parisit", "21 Dhjetori",
    "Ish-Blloku", "Medreseja", "Selvia"), n, replace = TRUE))

# Price adjustments (houses more expensive, newer = more, Blloku premium)
re <- re |>
  mutate(
    price = ifelse(type == "house", price * 1.5, price),
    price = ifelse(neighbourhood == "Blloku", price * 1.3, price),
    price = price + (year_built - 1990) * 200,
    price_sqm = round(price / area_sqm))

cat("Dataset:", nrow(re), "properties,", ncol(re), "variables\n")
cat("Types:", paste(unique(re$type), collapse = ", "), "\n")
cat("Neighbourhoods:", paste(unique(re$neighbourhood), collapse = ", "), "\n")

# ── 2. EDA PHASE 1: UNIVARIATE ──────────────────────────
p_price <- ggplot(re, aes(x = price / 1000)) +
  geom_histogram(bins = 30, fill = "#1565C0", color = "white") +
  geom_vline(xintercept = median(re$price) / 1000, color = "#E53935", linetype = "dashed") +
  theme_minimal(base_size = 8) +
  labs(title = "(a) Price Distribution", x = "Price (000 EUR)")

p_area <- ggplot(re, aes(x = area_sqm)) +
  geom_histogram(bins = 25, fill = "#2E7D32", color = "white") +
  theme_minimal(base_size = 8) +
  labs(title = "(b) Area (sqm)")

p_type <- ggplot(re, aes(x = type, fill = type)) +
  geom_bar(width = 0.5) +
  scale_fill_manual(values = c(apartment = "#1565C0", house = "#E53935")) +
  theme_minimal(base_size = 8) + theme(legend.position = "none") +
  labs(title = "(c) Type Split")

# ── 3. EDA PHASE 2: BIVARIATE ───────────────────────────
p_scatter <- ggplot(re, aes(x = area_sqm, y = price / 1000, color = type)) +
  geom_point(alpha = 0.4, size = 1.5) +
  geom_smooth(method = "lm", se = FALSE, linewidth = 0.8) +
  scale_color_manual(values = c(apartment = "#1565C0", house = "#E53935")) +
  theme_minimal(base_size = 8) +
  labs(title = "(d) Area vs Price by Type", x = "Area (sqm)", y = "Price (000 EUR)")

p_box_nbhd <- ggplot(re, aes(x = fct_reorder(neighbourhood, price_sqm), y = price_sqm)) +
  geom_boxplot(fill = "#BBDEFB", width = 0.5, outlier.size = 0.5) +
  coord_flip() +
  theme_minimal(base_size = 8) +
  labs(title = "(e) Price/sqm by Neighbourhood", x = NULL, y = "EUR/sqm")

p_violin <- ggplot(re, aes(x = condition, y = price / 1000, fill = condition)) +
  geom_violin(alpha = 0.3) +
  geom_boxplot(width = 0.1, outlier.shape = NA, fill = "white") +
  scale_fill_brewer(palette = "Set2") +
  theme_minimal(base_size = 8) + theme(legend.position = "none") +
  labs(title = "(f) Price by Condition", y = "Price (000 EUR)")

# ── 4. DASHBOARD COMPOSITION ────────────────────────────
dashboard <- (p_price | p_area | p_type) /
  (p_scatter | p_box_nbhd | p_violin) +
  plot_annotation(
    title = "Real Estate EDA Dashboard: 200 Properties in Tirana",
    subtitle = paste0("Median price: EUR ", format(median(re$price), big.mark = ","),
      " | Median area: ", median(re$area_sqm), " sqm"),
    caption = "Source: Simulated data | UNYT Data Viz Course",
    tag_levels = "a") &
  theme_minimal(base_size = 8)
ggsave("output/re_dashboard.png", dashboard, width = 14, height = 9, dpi = 300)
ggsave("output/re_dashboard.pdf", dashboard, width = 14, height = 9)

# ── 5. PCA BIPLOT ────────────────────────────────────────
library(ggfortify)
num_cols <- re |> select(price, area_sqm, bedrooms, bathrooms, year_built, floor)
pca <- prcomp(num_cols, scale. = TRUE)

p_pca <- autoplot(pca, data = re,
  colour = "type", alpha = 0.4, size = 1.5,
  loadings = TRUE, loadings.label = TRUE,
  loadings.colour = "#E65100", loadings.label.colour = "#E65100",
  loadings.label.size = 3) +
  scale_color_manual(values = c(apartment = "#1565C0", house = "#E53935")) +
  theme_minimal(base_size = 9) +
  labs(title = "PCA Biplot: Real Estate Features",
       subtitle = paste0("PC1 (", round(summary(pca)$importance[2,1]*100,1),
         "%) + PC2 (", round(summary(pca)$importance[2,2]*100,1), "%)"))
ggsave("output/re_pca.png", p_pca, width = 7, height = 6, dpi = 300)

# ── 6. CORRELATION HEATMAP ──────────────────────────────
library(pheatmap)
corr <- cor(num_cols)
pheatmap(corr,
  display_numbers = TRUE, number_format = "%.2f",
  color = colorRampPalette(c("#1565C0", "white", "#E53935"))(100),
  breaks = seq(-1, 1, length.out = 101),
  clustering_method = "ward.D2",
  main = "Correlation Heatmap: Real Estate Features",
  filename = "output/re_corr_heatmap.png",
  width = 7, height = 6)

# ── 7. PARALLEL COORDINATES ─────────────────────────────
library(GGally)
p_parcoord <- ggparcoord(re,
  columns = c("price", "area_sqm", "bedrooms", "bathrooms", "year_built"),
  groupColumn = "type",
  scale = "uniminmax",
  alphaLines = 0.1) +
  scale_color_manual(values = c(apartment = "#1565C0", house = "#E53935")) +
  theme_minimal(base_size = 8) +
  labs(title = "Parallel Coordinates: Real Estate by Type")
ggsave("output/re_parcoord.png", p_parcoord, width = 9, height = 4, dpi = 300)

# ── 8. SPATIAL: POINT MAP ───────────────────────────────
library(sf)
re_sf <- st_as_sf(re, coords = c("lon", "lat"), crs = 4326)

p_map <- ggplot(re_sf) +
  geom_sf(aes(color = price_sqm, size = area_sqm), alpha = 0.5) +
  scale_color_viridis_c(option = "plasma", name = "EUR/sqm") +
  scale_size(range = c(1, 6), name = "Area (sqm)") +
  theme_void(base_size = 9) +
  labs(title = "Tirana Properties: Location × Price/sqm × Area",
       subtitle = "Colour = price per sqm, Size = total area")
ggsave("output/re_spatial.png", p_map, width = 7, height = 7, dpi = 300)

# ── 9. INTERACTIVE MAP ──────────────────────────────────
# library(leaflet)
# pal <- colorNumeric("plasma", domain = re$price_sqm)
# leaflet(re) |>
#   addProviderTiles("CartoDB.Positron") |>
#   addCircleMarkers(
#     lng = ~lon, lat = ~lat,
#     radius = ~sqrt(area_sqm) / 2,
#     color = ~pal(price_sqm),
#     fillOpacity = 0.6, weight = 0.5,
#     popup = ~paste0(
#       "<b>", neighbourhood, "</b><br>",
#       "Type: ", type, "<br>",
#       "Price: EUR ", format(price, big.mark = ","), "<br>",
#       "Area: ", area_sqm, " sqm<br>",
#       "EUR/sqm: ", format(price_sqm, big.mark = ",")),
#     label = ~paste0("EUR ", format(price, big.mark = ","))) |>
#   addLegend(pal = pal, values = ~price_sqm,
#     title = "EUR/sqm", position = "bottomright")

# ── 10. KEY STATISTICS ───────────────────────────────────
cat("\n── Key Statistics ──\n")
cat("Median price:", format(median(re$price), big.mark = ","), "EUR\n")
cat("Median area:", median(re$area_sqm), "sqm\n")
cat("Median EUR/sqm:", format(median(re$price_sqm), big.mark = ","), "\n")
cat("Spearman(area, price):", round(cor(re$area_sqm, re$price, method = "spearman"), 3), "\n")
cat("PCA: PC1 explains", round(summary(pca)$importance[2,1]*100, 1), "% variance\n")

cat("\n── All W05-M10 Lab R outputs saved ──\n")
