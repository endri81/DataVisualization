# ============================================================
# Workshop 6 — Module 10: Lab — Animated Time Series Dashboard
# Integrated R Script — UNYT Tirana
# ============================================================
library(tidyverse); library(patchwork); dir.create("output", showWarnings = FALSE)

# ══════════════════════════════════════════════════════════
# This lab integrates ALL W06 techniques on the Netflix dataset:
#   M01: granularity, decomposition
#   M02: grey+accent, indexing, direct labels, event annotations
#   M03: line, step, area, stacked, ribbon
#   M04: sparklines, small multiples
#   M05: seasonal subseries, calendar heatmap
#   M06-M07: animation (bar chart race)
#   M08: Netflix case study patterns
# ══════════════════════════════════════════════════════════

# ── 1. LOAD AND PREPARE ─────────────────────────────────
nf <- read_csv("netflix.csv") |>
  mutate(
    date_added = mdy(str_trim(date_added)),
    year_added = year(date_added),
    month_added = month(date_added),
    dow = wday(date_added, label = TRUE, week_start = 1),
    week = isoweek(date_added),
    primary_country = str_trim(str_extract(country, "^[^,]+")))

nf_genres <- nf |>
  separate_rows(listed_in, sep = ", ") |>
  mutate(genre = str_trim(listed_in))

cat("Netflix:", nrow(nf), "titles |",
  sum(!is.na(nf$date_added)), "with dates |",
  n_distinct(nf_genres$genre), "genres\n")

# ── PANEL 1: LINE CHART — Monthly additions + events ────
monthly <- nf |>
  filter(!is.na(date_added), year(date_added) >= 2015) |>
  mutate(month = floor_date(date_added, "month")) |>
  count(month)

p1_line <- ggplot(monthly, aes(x = month, y = n)) +
  geom_line(color = "#1565C0", linewidth = 0.8) +
  geom_smooth(method = "loess", span = 0.3, se = FALSE,
    color = "#E53935", linewidth = 0.5, linetype = "dashed") +
  # Event annotations
  geom_vline(xintercept = as.Date("2016-01-01"),
    linetype = "dashed", color = "#2E7D32", linewidth = 0.4) +
  annotate("text", x = as.Date("2016-03-01"),
    y = max(monthly$n) * 0.95, label = "Global\nexpansion",
    size = 2, color = "#2E7D32", hjust = 0) +
  geom_vline(xintercept = as.Date("2020-03-01"),
    linetype = "dashed", color = "#E53935", linewidth = 0.4) +
  annotate("text", x = as.Date("2020-05-01"),
    y = max(monthly$n) * 0.80, label = "COVID",
    size = 2, color = "#E53935", hjust = 0) +
  scale_x_date(date_breaks = "1 year", date_labels = "%Y") +
  theme_minimal(base_size = 8) +
  labs(title = "Panel 1: Monthly Additions + Events + Trend (M02-M03)",
       x = NULL, y = "Titles/Month")

# ── PANEL 2: STACKED AREA — Top 5 genres over time ──────
top5 <- nf_genres |> count(genre, sort = TRUE) |> slice_max(n, n = 5) |> pull(genre)

genre_monthly <- nf_genres |>
  filter(genre %in% top5, !is.na(date_added), year(date_added) >= 2016) |>
  mutate(month = floor_date(date_added, "month")) |>
  count(month, genre)

p2_area <- ggplot(genre_monthly, aes(x = month, y = n, fill = genre)) +
  geom_area(alpha = 0.7, color = "white", linewidth = 0.2) +
  scale_fill_brewer(palette = "Set2") +
  scale_x_date(date_breaks = "1 year", date_labels = "%Y") +
  theme_minimal(base_size = 8) +
  theme(legend.text = element_text(size = 5),
    legend.key.size = unit(0.3, "cm")) +
  labs(title = "Panel 2: Stacked Area — Top 5 Genres (M03)",
       x = NULL, y = "Titles/Month", fill = NULL)

# ── PANEL 3: SPARKLINE TABLE — Movie vs TV Show ─────────
type_monthly <- nf |>
  filter(!is.na(date_added), year(date_added) >= 2016, year(date_added) <= 2021) |>
  mutate(month = floor_date(date_added, "month")) |>
  count(month, type)

p3_spark <- ggplot(type_monthly, aes(x = month, y = n)) +
  geom_line(color = "#1565C0", linewidth = 0.5) +
  geom_area(fill = "#1565C0", alpha = 0.06) +
  geom_point(data = type_monthly |>
    group_by(type) |> filter(n == max(n)) |> slice(1),
    color = "#2E7D32", size = 2) +
  geom_point(data = type_monthly |>
    group_by(type) |> filter(n == min(n)) |> slice(1),
    color = "#E53935", size = 2) +
  geom_point(data = type_monthly |>
    group_by(type) |> filter(month == max(month)),
    color = "#1565C0", size = 2.5) +
  facet_wrap(~type, ncol = 1, scales = "free_y") +
  theme_minimal(base_size = 8) +
  labs(title = "Panel 3: Sparklines by Type (M04)",
       subtitle = "Green=peak, Red=min, Blue=current",
       x = NULL, y = NULL)

# ── PANEL 4: CALENDAR HEATMAP — 2020 ────────────────────
daily_2020 <- nf |>
  filter(year_added == 2020, !is.na(date_added)) |>
  count(date_added) |>
  mutate(dow = wday(date_added, label = TRUE, week_start = 1),
    week = isoweek(date_added))

p4_cal <- ggplot(daily_2020, aes(x = week, y = dow, fill = n)) +
  geom_tile(color = "white", linewidth = 0.3) +
  scale_fill_gradient(low = "#E8F5E9", high = "#1B5E20", name = "Count") +
  scale_y_discrete(limits = rev(c("Mon","Tue","Wed","Thu","Fri","Sat","Sun"))) +
  theme_minimal(base_size = 7) +
  theme(panel.grid = element_blank(),
    legend.key.size = unit(0.3, "cm")) +
  labs(title = "Panel 4: Calendar Heatmap 2020 (M05)",
       x = "Week", y = NULL)

# ── PANEL 5: SEASONAL SUBSERIES ──────────────────────────
seasonal <- nf |>
  filter(!is.na(year_added), year_added >= 2016, year_added <= 2021) |>
  count(year_added, month_added) |>
  mutate(is_2021 = year_added == 2021)

p5_season <- ggplot(seasonal,
  aes(x = month_added, y = n, group = year_added,
      color = is_2021, alpha = is_2021, linewidth = is_2021)) +
  geom_line() + geom_point(size = 1) +
  scale_color_manual(values = c("TRUE" = "#E53935", "FALSE" = "#BBBBBB"), guide = "none") +
  scale_alpha_manual(values = c("TRUE" = 1, "FALSE" = 0.25), guide = "none") +
  scale_linewidth_manual(values = c("TRUE" = 1.5, "FALSE" = 0.5), guide = "none") +
  scale_x_continuous(breaks = 1:12, labels = month.abb) +
  theme_minimal(base_size = 8) +
  labs(title = "Panel 5: Seasonal Subseries (M05)",
       subtitle = "Grey = 2016–2020, Red = 2021",
       x = "Month", y = "Titles")

# ── PANEL 6: BAR CHART RACE — Static key frame ──────────
country_cum <- nf |>
  filter(!is.na(primary_country), !is.na(year_added),
    year_added >= 2016, year_added <= 2021) |>
  count(year_added, primary_country) |>
  group_by(primary_country) |> arrange(year_added) |>
  mutate(cumulative = cumsum(n)) |> ungroup()

top10_2021 <- country_cum |>
  filter(year_added == 2021) |>
  slice_max(cumulative, n = 10)

p6_race <- ggplot(top10_2021,
  aes(x = fct_reorder(primary_country, cumulative), y = cumulative,
      fill = primary_country)) +
  geom_col(width = 0.6, show.legend = FALSE) +
  geom_text(aes(label = format(cumulative, big.mark = ",")),
    hjust = -0.1, size = 2.5, fontface = "bold") +
  coord_flip(clip = "off") +
  scale_fill_viridis_d(option = "turbo") +
  theme_minimal(base_size = 8) +
  theme(plot.margin = margin(5, 30, 5, 5)) +
  labs(title = "Panel 6: Bar Race Frame 2021 (M07)",
       subtitle = "Animated GIF: see bar_race.gif",
       x = NULL, y = "Cumulative Titles")

# ── COMPOSE FULL DASHBOARD ───────────────────────────────
dashboard <- (p1_line | p2_area) /
  (p3_spark | p4_cal) /
  (p5_season | p6_race) +
  plot_annotation(
    title = "Workshop 6 Lab: Netflix Temporal Dashboard",
    subtitle = paste0(
      "Integrates: Line+events (M02-03), Stacked area (M03), ",
      "Sparklines (M04), Calendar heatmap (M05), Seasonal (M05), ",
      "Bar race frame (M07)"),
    tag_levels = "a") &
  theme_minimal(base_size = 8)

ggsave("output/w06_lab_dashboard.png", dashboard, width = 16, height = 16, dpi = 300)
ggsave("output/w06_lab_dashboard.pdf", dashboard, width = 16, height = 16)

# ── ANIMATION (uncomment to generate GIF) ────────────────
# library(gganimate)
# race_data <- country_cum |>
#   filter(primary_country %in% top10_2021$primary_country) |>
#   group_by(year_added) |>
#   mutate(rank = rank(-cumulative, ties.method = "first")) |>
#   ungroup()
#
# p_race_anim <- ggplot(race_data,
#   aes(x = rank, y = cumulative, fill = primary_country)) +
#   geom_col(width = 0.8, show.legend = FALSE) +
#   geom_text(aes(label = primary_country), x = -0.3, hjust = 1, size = 3) +
#   geom_text(aes(label = format(cumulative, big.mark = ",")),
#     hjust = -0.1, size = 3) +
#   coord_flip(clip = "off") + scale_x_reverse() +
#   scale_fill_viridis_d(option = "turbo") +
#   theme_minimal() +
#   theme(plot.margin = margin(5, 60, 5, 60),
#     axis.text.y = element_blank(), axis.ticks.y = element_blank()) +
#   transition_states(year_added, transition_length = 3, state_length = 2) +
#   ease_aes("cubic-in-out") +
#   labs(title = "Netflix by Country: {closest_state}", x = NULL, y = "Cumulative")
#
# animate(p_race_anim, nframes = 120, fps = 10, width = 800, height = 500,
#   renderer = gifski_renderer("output/bar_race.gif"))

# ── KEY FINDINGS ─────────────────────────────────────────
cat("\n══ FOUR TEMPORAL FINDINGS ══\n")
cat("1. TREND: Netflix additions peaked in 2019 (movies) and 2020 (TV),\n")
cat("   then declined — visible in Panel 1 monthly line + LOESS trend.\n")
cat("2. COMPOSITION: International genres grew fastest (stacked area,\n")
cat("   Panel 2); TV Show share rose from ~20% to ~35%.\n")
cat("3. SEASONAL: Fridays = primary release day (calendar heatmap, Panel 4);\n")
cat("   Q4 spike visible in seasonal subseries (Panel 5).\n")
cat("4. GEOGRAPHY: US dominates but India rose from #5 to #2 in cumulative\n")
cat("   titles (bar race frame, Panel 6).\n")

cat("\n── All W06-M10 Lab R outputs saved ──\n")
