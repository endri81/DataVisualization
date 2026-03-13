# ============================================================
# Workshop 2 — Module 4: Scales & Coordinate Systems
# R Demonstration Script — UNYT Tirana
# ============================================================
library(tidyverse)
library(patchwork)
library(scales)
dir.create("output", showWarnings = FALSE)

apps <- read_csv("googleplaystore.csv") |>
  filter(Type %in% c("Free", "Paid")) |>
  mutate(Reviews = as.numeric(Reviews))

# ── 1. LINEAR vs LOG SCALE ───────────────────────────────
p_lin <- ggplot(apps, aes(x = Reviews, y = Rating)) +
  geom_point(alpha = 0.2, size = 0.5) +
  theme_minimal() + labs(title = "Linear x-axis", x = "Reviews")

p_log <- ggplot(apps, aes(x = Reviews, y = Rating)) +
  geom_point(alpha = 0.2, size = 0.5) +
  scale_x_log10(labels = comma) +
  theme_minimal() + labs(title = "Log x-axis", x = "Reviews (log)")

ggsave("output/lin_vs_log.png", p_lin + p_log, width = 10, height = 4, dpi = 300)

# ── 2. COLOUR SCALES ─────────────────────────────────────
# Manual
p_manual <- ggplot(apps, aes(x = Reviews, y = Rating, color = Type)) +
  geom_point(alpha = 0.3, size = 0.5) +
  scale_x_log10(labels = comma) +
  scale_color_manual(values = c(Free = "#1565C0", Paid = "#E53935")) +
  theme_minimal() + labs(title = "scale_color_manual()")

# Brewer
p_brewer <- ggplot(apps |> filter(!is.na(Rating)),
                   aes(x = Rating, fill = Type)) +
  geom_histogram(bins = 30, position = "identity", alpha = 0.6) +
  scale_fill_brewer(palette = "Set1") +
  theme_minimal() + labs(title = "scale_fill_brewer('Set1')")

ggsave("output/colour_scales.png", p_manual + p_brewer, width = 11, height = 4, dpi = 300)

# ── 3. AXIS FORMATTING ───────────────────────────────────
revenue <- tibble(quarter = c("Q1","Q2","Q3","Q4"),
                  revenue = c(1.2e6, 2.5e6, 1.8e6, 3.2e6))

p_comma <- ggplot(revenue, aes(x = quarter, y = revenue)) +
  geom_col(fill = "#1565C0", width = 0.5) +
  scale_y_continuous(labels = comma) +
  theme_minimal() + labs(title = "labels = comma")

p_dollar <- ggplot(revenue, aes(x = quarter, y = revenue)) +
  geom_col(fill = "#2E7D32", width = 0.5) +
  scale_y_continuous(labels = label_dollar(scale = 1e-6, suffix = "M")) +
  theme_minimal() + labs(title = "labels = dollar")

ggsave("output/axis_formatting.png", p_comma + p_dollar, width = 9, height = 4, dpi = 300)

# ── 4. ZOOM: coord_cartesian vs scale limits ─────────────
set.seed(55)
df_zoom <- tibble(x = runif(200, 0, 100), y = 0.4*x + rnorm(200, 0, 12))

p_full <- ggplot(df_zoom, aes(x, y)) + geom_point(alpha = 0.4) +
  geom_smooth(method = "lm", color = "#1565C0") +
  theme_minimal() + labs(title = "Full data")

p_scale_lim <- ggplot(df_zoom, aes(x, y)) + geom_point(alpha = 0.4) +
  geom_smooth(method = "lm", color = "#E53935") +
  scale_x_continuous(limits = c(25, 75)) +
  theme_minimal() + labs(title = "scale limits (FILTERS!)", subtitle = "Slope changes")

p_coord_zoom <- ggplot(df_zoom, aes(x, y)) + geom_point(alpha = 0.4) +
  geom_smooth(method = "lm", color = "#2E7D32") +
  coord_cartesian(xlim = c(25, 75)) +
  theme_minimal() + labs(title = "coord_cartesian (SAFE)", subtitle = "Slope preserved")

ggsave("output/zoom.png", p_full + p_scale_lim + p_coord_zoom, width = 12, height = 4, dpi = 300)

# ── 5. COORDINATE SYSTEMS ────────────────────────────────
market <- tibble(segment = c("Enterprise","SMB","Consumer","Startup"),
                 share = c(45, 25, 20, 10))

p_cart <- ggplot(market, aes(x = segment, y = share, fill = segment)) +
  geom_col(width = 0.6) + scale_fill_brewer(palette = "Set2") +
  theme_minimal() + theme(legend.position = "none") +
  labs(title = "coord_cartesian")

p_flip <- ggplot(market, aes(x = fct_reorder(segment, share), y = share, fill = segment)) +
  geom_col(width = 0.6) + scale_fill_brewer(palette = "Set2") +
  coord_flip() + theme_minimal() + theme(legend.position = "none") +
  labs(title = "coord_flip", x = NULL)

p_polar <- ggplot(market, aes(x = "", y = share, fill = segment)) +
  geom_col(width = 1) + coord_polar(theta = "y") +
  scale_fill_brewer(palette = "Set2") + theme_void() +
  labs(title = "coord_polar")

ggsave("output/coord_systems.png", p_cart + p_flip + p_polar, width = 12, height = 4, dpi = 300)

cat("\n── All W02-M04 R plots saved ──\n")
