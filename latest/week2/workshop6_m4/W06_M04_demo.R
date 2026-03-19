# ============================================================
# Workshop 6 — Module 4: Sparklines & Small Temporal Multiples
# Integrated R Script — UNYT Tirana
# ============================================================
library(tidyverse); library(patchwork); dir.create("output", showWarnings = FALSE)

# ── 1. LOAD NETFLIX DATA ────────────────────────────────
nf <- read_csv("netflix.csv") |>
  mutate(
    date_added = mdy(str_trim(date_added)),
    year_added = year(date_added),
    month_added = month(date_added))

# Get top 6 genres
nf_genres <- nf |>
  separate_rows(listed_in, sep = ", ") |>
  mutate(genre = str_trim(listed_in))
top6 <- nf_genres |> count(genre, sort = TRUE) |> slice_max(n, n = 6) |> pull(genre)

# Monthly additions per genre (2016–2021)
genre_monthly <- nf_genres |>
  filter(genre %in% top6, !is.na(date_added),
    year_added >= 2016, year_added <= 2021) |>
  mutate(month = floor_date(date_added, "month")) |>
  count(month, genre)

# ── 2. SPAGHETTI CHART (BAD: too many lines) ────────────
p_spaghetti <- ggplot(genre_monthly, aes(x = month, y = n, color = genre)) +
  geom_line(linewidth = 0.8) +
  scale_color_brewer(palette = "Set2") +
  theme_minimal() +
  labs(title = "BAD: Spaghetti Chart (6 overlapping lines)",
       subtitle = "Which genre is growing fastest? Impossible to tell.",
       x = NULL, y = "Monthly Additions")
ggsave("output/spaghetti.png", p_spaghetti, width = 10, height = 5, dpi = 300)

# ── 3. SMALL TEMPORAL MULTIPLES (GOOD) ──────────────────
# One panel per genre, shared x-axis, free y for different magnitudes
p_multiples <- ggplot(genre_monthly, aes(x = month, y = n)) +
  geom_line(color = "#1565C0", linewidth = 0.8) +
  facet_wrap(~genre, ncol = 3, scales = "free_y") +
  scale_x_date(date_breaks = "1 year", date_labels = "%Y") +
  theme_minimal(base_size = 8) +
  labs(title = "GOOD: Small Multiples — One Panel per Genre",
       subtitle = "Shared x-axis, free y-axis reveals each genre's own pattern",
       x = NULL, y = "Monthly Additions")
ggsave("output/small_multiples.png", p_multiples, width = 12, height = 7, dpi = 300)

# Fixed y-axis version for magnitude comparison
p_multiples_fixed <- ggplot(genre_monthly, aes(x = month, y = n)) +
  geom_line(color = "#1565C0", linewidth = 0.8) +
  facet_wrap(~genre, ncol = 3) +  # default scales = "fixed"
  scale_x_date(date_breaks = "1 year", date_labels = "%Y") +
  theme_minimal(base_size = 8) +
  labs(title = "Fixed Y-Axis: Compare Absolute Magnitudes",
       subtitle = "Same y-scale reveals which genres dominate in volume",
       x = NULL, y = "Monthly Additions")
ggsave("output/small_multiples_fixed.png", p_multiples_fixed,
  width = 12, height = 7, dpi = 300)

# Side-by-side: free vs fixed
ggsave("output/free_vs_fixed.png",
  (p_multiples + labs(title = "(a) Free Y")) |
  (p_multiples_fixed + labs(title = "(b) Fixed Y")),
  width = 20, height = 7, dpi = 300)

# ── 4. HIGHLIGHTED MULTIPLES ────────────────────────────
# Every panel shows all genres as grey; focal genre in colour
p_highlight <- ggplot() +
  # Grey background: all genres in every panel
  geom_line(data = genre_monthly |>
    rename(genre_bg = genre) |>
    cross_join(tibble(genre = top6)),
    aes(x = month, y = n, group = genre_bg),
    color = "#EEEEEE", linewidth = 0.3) +
  # Coloured foreground: the focal genre
  geom_line(data = genre_monthly,
    aes(x = month, y = n),
    color = "#E53935", linewidth = 1) +
  facet_wrap(~genre, ncol = 3, scales = "free_y") +
  scale_x_date(date_breaks = "1 year", date_labels = "%Y") +
  theme_minimal(base_size = 8) +
  labs(title = "Highlighted Multiples: Focal Genre (red) vs All Others (grey)",
       subtitle = "Each panel shows one genre against all others for context",
       x = NULL, y = "Monthly Additions")
ggsave("output/highlighted_multiples.png", p_highlight,
  width = 12, height = 7, dpi = 300)

# ── 5. SPARKLINE-STYLE PANEL (Tufte) ────────────────────
# Vertical stack: one row per genre, no axes, mark min/max/current
genre_summary <- genre_monthly |>
  group_by(genre) |>
  summarise(
    min_val = min(n), max_val = max(n), last_val = last(n),
    min_date = month[which.min(n)],
    max_date = month[which.max(n)],
    last_date = max(month))

p_sparklines <- ggplot(genre_monthly, aes(x = month, y = n)) +
  geom_line(color = "#1565C0", linewidth = 0.4) +
  geom_area(fill = "#1565C0", alpha = 0.08) +
  # Min point (red)
  geom_point(data = genre_monthly |>
    group_by(genre) |> filter(n == min(n)) |> slice(1),
    color = "#E53935", size = 1.5) +
  # Max point (green)
  geom_point(data = genre_monthly |>
    group_by(genre) |> filter(n == max(n)) |> slice(1),
    color = "#2E7D32", size = 1.5) +
  # Current point (blue)
  geom_point(data = genre_monthly |>
    group_by(genre) |> filter(month == max(month)),
    color = "#1565C0", size = 2) +
  facet_wrap(~genre, ncol = 1, scales = "free_y",
    strip.position = "left") +
  theme_void(base_size = 8) +
  theme(
    strip.text.y.left = element_text(angle = 0, hjust = 1,
      face = "bold", size = 7)) +
  labs(title = "Sparkline Panel: Netflix Genre Trends (Tufte-style)",
       subtitle = "Red = minimum, Green = maximum, Blue = current value")
ggsave("output/sparklines.png", p_sparklines, width = 7, height = 7, dpi = 300)

# ── 6. gt + gtExtras SPARKLINE TABLE (if available) ─────
# This creates a professional table with embedded sparklines
# Uncomment if gt and gtExtras are installed
# library(gt); library(gtExtras)
# spark_table <- genre_monthly |>
#   group_by(genre) |>
#   summarise(
#     trend = list(n),
#     total = sum(n),
#     peak = max(n),
#     current = last(n),
#     change = (last(n) - first(n)) / first(n) * 100) |>
#   arrange(desc(total)) |>
#   gt() |>
#   gt_sparkline(trend, same_limit = FALSE) |>
#   fmt_number(c(total, peak, current), decimals = 0) |>
#   fmt_number(change, decimals = 1, pattern = "{x}%") |>
#   cols_label(
#     genre = "Genre", trend = "Trend (2016–2021)",
#     total = "Total", peak = "Peak Month",
#     current = "Latest", change = "Change %") |>
#   tab_header(title = "Netflix Genre Summary with Sparklines")
# gtsave(spark_table, "output/sparkline_table.html")

# ── 7. SPAGHETTI → MULTIPLES → SPARKLINES COMPARISON ────
p_comparison <- p_spaghetti +
  labs(title = "(a) Spaghetti: 6 lines compete") +
  theme(legend.position = "bottom", legend.text = element_text(size = 5))

ggsave("output/evolution.png",
  p_comparison / p_multiples / p_sparklines +
  plot_annotation(title = "Evolution: Spaghetti → Small Multiples → Sparklines"),
  width = 12, height = 18, dpi = 300)

# ── 8. NETFLIX: TYPE SPARKLINES ──────────────────────────
type_monthly <- nf |>
  filter(!is.na(date_added), year_added >= 2016, year_added <= 2021) |>
  mutate(month = floor_date(date_added, "month")) |>
  count(month, type)

p_type_spark <- ggplot(type_monthly, aes(x = month, y = n)) +
  geom_line(color = "#1565C0", linewidth = 0.6) +
  geom_area(fill = "#1565C0", alpha = 0.08) +
  geom_point(data = type_monthly |>
    group_by(type) |> filter(n == max(n)) |> slice(1),
    color = "#2E7D32", size = 2) +
  geom_point(data = type_monthly |>
    group_by(type) |> filter(month == max(month)),
    color = "#E53935", size = 2) +
  facet_wrap(~type, ncol = 1, scales = "free_y") +
  theme_minimal(base_size = 9) +
  labs(title = "Netflix: Movie vs TV Show Sparklines (2016–2021)",
       subtitle = "Green = peak month, Red = latest month",
       x = NULL, y = "Monthly Additions")
ggsave("output/type_sparklines.png", p_type_spark,
  width = 9, height = 5, dpi = 300)

cat("\n── All W06-M04 R outputs saved ──\n")
cat("Figures: spaghetti, small_multiples, small_multiples_fixed,\n")
cat("  free_vs_fixed, highlighted_multiples, sparklines,\n")
cat("  evolution (3-panel), type_sparklines\n")
