# ============================================================
# Workshop 1 — Module 4: Color Theory & Accessibility
# R Demonstration Script
# Data Visualization for Data Scientists — UNYT Tirana
# ============================================================

library(tidyverse)
# install.packages(c("viridis", "RColorBrewer", "colorspace", "patchwork"))
library(viridis)
library(RColorBrewer)
library(colorspace)
library(patchwork)

dir.create("output", showWarnings = FALSE)


# ── 1. Sequential Palette: Heatmap ─────────────────────────
set.seed(33)
heatmap_data <- expand_grid(
  day = c("Mon", "Tue", "Wed", "Thu", "Fri", "Sat"),
  week = paste0("W", 1:8)
) |>
  mutate(value = runif(n(), 10, 90))

p_heat <- ggplot(heatmap_data, aes(x = week, y = day, fill = value)) +
  geom_tile(color = "white", linewidth = 0.5) +
  scale_fill_viridis_c(option = "D", direction = 1) +
  theme_minimal(base_size = 10) +
  labs(title = "Sequential Palette: viridis",
       fill = "Value", x = NULL, y = NULL) +
  theme(plot.title = element_text(face = "bold"))

print(p_heat)
ggsave("output/heatmap_viridis.png", p_heat, width = 7, height = 4, dpi = 150)


# ── 2. Diverging Palette: Deviation from Mean ──────────────
set.seed(44)
df_div <- tibble(
  x = runif(80, 0, 10),
  y = runif(80, 0, 8),
  deviation = runif(80, -1, 1)
)

p_div <- ggplot(df_div, aes(x = x, y = y, color = deviation)) +
  geom_point(size = 3) +
  scale_color_gradient2(
    low = "#2166AC", mid = "white", high = "#B2182B",
    midpoint = 0, limits = c(-1, 1)
  ) +
  theme_minimal(base_size = 10) +
  labs(title = "Diverging Palette: RdBu Centred on Zero",
       color = "Deviation") +
  theme(plot.title = element_text(face = "bold"))

print(p_div)
ggsave("output/diverging_rdbu.png", p_div, width = 7, height = 5, dpi = 150)


# ── 3. Qualitative Palette: Categories ─────────────────────
set.seed(55)
df_qual <- tibble(
  category = sample(LETTERS[1:5], 100, replace = TRUE),
  x = rnorm(100),
  y = rnorm(100)
)

p_qual <- ggplot(df_qual, aes(x = x, y = y, color = category)) +
  geom_point(size = 2.5, alpha = 0.7) +
  scale_color_brewer(palette = "Set2") +
  theme_minimal(base_size = 10) +
  labs(title = "Qualitative Palette: ColorBrewer Set2",
       color = "Category") +
  theme(plot.title = element_text(face = "bold"))

print(p_qual)
ggsave("output/qualitative_set2.png", p_qual, width = 7, height = 5, dpi = 150)


# ── 4. Rainbow vs Viridis ─────────────────────────────────
set.seed(7)
df_rainbow <- tibble(
  x = runif(200, 0, 10),
  y = runif(200, 0, 10),
  z = sin(x) * cos(y) + rnorm(200, 0, 0.3)
)

p_rain <- ggplot(df_rainbow, aes(x = x, y = y, color = z)) +
  geom_point(size = 1.5) +
  scale_color_gradientn(colors = rainbow(20)) +
  theme_minimal(base_size = 9) +
  labs(title = "Rainbow (BAD)", color = "Value") +
  theme(plot.title = element_text(face = "bold", color = "#C62828"))

p_vir <- ggplot(df_rainbow, aes(x = x, y = y, color = z)) +
  geom_point(size = 1.5) +
  scale_color_viridis_c() +
  theme_minimal(base_size = 9) +
  labs(title = "Viridis (GOOD)", color = "Value") +
  theme(plot.title = element_text(face = "bold", color = "#1565C0"))

p_compare <- p_rain + p_vir +
  plot_annotation(title = "Never Use Rainbow")

print(p_compare)
ggsave("output/rainbow_vs_viridis.png", p_compare, width = 10, height = 4, dpi = 150)


# ── 5. CVD Simulation ─────────────────────────────────────
# The colorspace package simulates colour vision deficiency

p_original <- ggplot(df_qual, aes(x = x, y = y, color = category)) +
  geom_point(size = 2.5) +
  scale_color_manual(values = c(
    A = "#E53935", B = "#2E7D32", C = "#1565C0",
    D = "#FF9800", E = "#9C27B0"
  )) +
  theme_minimal(base_size = 9) +
  labs(title = "Normal Vision") +
  theme(plot.title = element_text(face = "bold"))

# Simulate deuteranopia
p_deutan <- deutan(p_original) +
  labs(title = "Deuteranopia Simulation") +
  theme(plot.title = element_text(face = "bold"))

p_cvd <- p_original + p_deutan +
  plot_annotation(title = "CVD Simulation with colorspace::deutan()")

print(p_cvd)
ggsave("output/cvd_simulation.png", p_cvd, width = 10, height = 4, dpi = 150)


# ── 6. Grey + Accent Strategy ─────────────────────────────
set.seed(55)
df_accent <- tibble(
  x = runif(100, 10, 100),
  y = 0.4 * x + rnorm(100, 0, 12),
  category = sample(c("A", "B", "C", "D"), 100, replace = TRUE),
  is_highlight = category == "D"
)

p_accent <- ggplot(df_accent, aes(x = x, y = y)) +
  # Background: grey
  geom_point(
    data = filter(df_accent, !is_highlight),
    color = "#BBBBBB", size = 1.5, alpha = 0.4
  ) +
  # Highlight: red accent
  geom_point(
    data = filter(df_accent, is_highlight),
    color = "#E53935", size = 3, alpha = 0.9
  ) +
  theme_minimal(base_size = 10) +
  labs(title = "Grey + Accent: Category D Highlighted",
       x = "Spend ($K)", y = "ROI (%)") +
  theme(plot.title = element_text(face = "bold"))

print(p_accent)
ggsave("output/grey_accent.png", p_accent, width = 7, height = 5, dpi = 150)


cat("\n── All M04 plots saved to output/ ──\n")
