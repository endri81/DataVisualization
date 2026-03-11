# ============================================================
# Workshop 1 — Module 10: Comparative Lab
# R Script — Google Play Store EDA
# Data Visualization for Data Scientists — UNYT Tirana
# ============================================================

library(tidyverse)
library(patchwork)
library(scales)
dir.create("output", showWarnings = FALSE)

# ── 1. LOAD & CLEAN ───────────────────────────────────────
apps <- read_csv("googleplaystore.csv")
cat("Dimensions:", dim(apps), "\n")

apps_clean <- apps |>
  filter(Type %in% c("Free", "Paid")) |>
  mutate(
    Reviews = as.numeric(Reviews),
    Last_Updated = mdy(`Last Updated`),
    Year = year(Last_Updated)
  )

# ── 2. BAR CHART: Top 10 categories ──────────────────────
p_bar <- apps_clean |>
  count(Category, sort = TRUE) |>
  slice_max(n, n = 10) |>
  mutate(Category = fct_reorder(Category, n)) |>
  ggplot(aes(x = Category, y = n)) +
  geom_col(fill = "#1565C0", width = 0.6) +
  geom_text(aes(label = comma(n)), hjust = -0.15, size = 3, fontface = "bold") +
  coord_flip() +
  theme_minimal() +
  theme(panel.grid.major.y = element_blank()) +
  labs(x = NULL, y = "Count", title = "(a) Top 10 App Categories")

# ── 3. HISTOGRAM: Rating distribution ────────────────────
mean_rating <- mean(apps_clean$Rating, na.rm = TRUE)

p_hist <- ggplot(apps_clean, aes(x = Rating)) +
  geom_histogram(bins = 40, fill = "#1565C0", color = "white", linewidth = 0.3) +
  geom_vline(xintercept = mean_rating, color = "#E53935", linewidth = 1, linetype = "dashed") +
  annotate("text", x = mean_rating - 0.3, y = Inf, vjust = 1.5,
           label = paste0("Mean: ", round(mean_rating, 2)),
           fontface = "bold", color = "#E53935", size = 3) +
  theme_minimal() +
  labs(title = "(b) Rating Distribution", x = "Rating", y = "Count")

# ── 4. SCATTER: Reviews vs Rating ────────────────────────
p_scatter <- apps_clean |>
  filter(!is.na(Rating), Reviews > 0) |>
  ggplot(aes(x = Reviews, y = Rating, color = Type)) +
  geom_point(alpha = 0.3, size = 0.8) +
  scale_x_log10(labels = comma) +
  scale_color_manual(values = c(Free = "#1565C0", Paid = "#E53935")) +
  theme_minimal() +
  labs(title = "(c) Reviews vs Rating", x = "Reviews (log)", y = "Rating")

# ── 5. BOXPLOT: Rating by Type ───────────────────────────
p_box <- apps_clean |>
  filter(!is.na(Rating)) |>
  ggplot(aes(x = Type, y = Rating, fill = Type)) +
  geom_boxplot(width = 0.5, notch = TRUE, outlier.alpha = 0.2) +
  stat_summary(fun = mean, geom = "point", shape = 18, size = 3, color = "#E53935") +
  scale_fill_manual(values = c(Free = "#BBDEFB", Paid = "#FFCDD2")) +
  theme_minimal() +
  theme(legend.position = "none") +
  labs(title = "(d) Rating by Type", y = "Rating", x = NULL)

# ── 6. LINE CHART: Apps per year ─────────────────────────
p_line <- apps_clean |>
  filter(Year >= 2010, Year <= 2018) |>
  count(Year, Type) |>
  ggplot(aes(x = Year, y = n, color = Type)) +
  geom_line(linewidth = 1.2) +
  geom_point(size = 2) +
  scale_color_manual(values = c(Free = "#1565C0", Paid = "#E53935")) +
  theme_minimal() +
  theme(legend.position = "bottom") +
  labs(title = "(e) Apps Added per Year", x = "Year", y = "Count")

# ── 7. STACKED BAR: Content Rating × Type ────────────────
p_stacked <- apps_clean |>
  filter(`Content Rating` %in% c("Everyone", "Teen", "Mature 17+", "Everyone 10+")) |>
  ggplot(aes(x = `Content Rating`, fill = Type)) +
  geom_bar(position = "stack") +
  scale_fill_manual(values = c(Free = "#1565C0", Paid = "#E53935")) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 30, hjust = 1, size = 7)) +
  labs(title = "(f) Content Rating × Type", x = NULL, y = "Count")

# ── 8. DASHBOARD: Combine all 6 ─────────────────────────
dashboard <- (p_bar | p_hist | p_scatter) / (p_box | p_line | p_stacked) +
  plot_annotation(
    title = "Google Play Store: Exploratory Data Analysis Dashboard",
    subtitle = "Workshop 1, Module 10 — R (ggplot2 + patchwork)"
  )

ggsave("output/W01_M10_dashboard_R.pdf", dashboard, width = 14, height = 9)
ggsave("output/W01_M10_dashboard_R.png", dashboard, width = 14, height = 9, dpi = 300)

# Individual charts
ggsave("output/bar_R.png", p_bar, width = 6, height = 5, dpi = 300)
ggsave("output/hist_R.png", p_hist, width = 6, height = 4, dpi = 300)
ggsave("output/scatter_R.png", p_scatter, width = 6, height = 5, dpi = 300)
ggsave("output/box_R.png", p_box, width = 5, height = 4, dpi = 300)
ggsave("output/line_R.png", p_line, width = 6, height = 4, dpi = 300)
ggsave("output/stacked_R.png", p_stacked, width = 6, height = 4, dpi = 300)

cat("\n── Workshop 1 Lab Complete (R) ──\n")
