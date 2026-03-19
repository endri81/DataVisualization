# ============================================================
# Workshop 6 — Module 7: Advanced Animation — Bar Chart Races
# Integrated R Script — UNYT Tirana
# ============================================================
library(tidyverse); library(patchwork); dir.create("output", showWarnings = FALSE)

# ── 1. LOAD AND PREPARE NETFLIX DATA ────────────────────
nf <- read_csv("netflix.csv") |>
  mutate(
    date_added = mdy(str_trim(date_added)),
    year_added = year(date_added),
    # Extract primary country (first listed)
    primary_country = str_trim(str_extract(country, "^[^,]+"))) |>
  filter(!is.na(date_added), !is.na(primary_country),
    year_added >= 2016, year_added <= 2021)

# Cumulative titles per country per year
country_yearly <- nf |>
  count(year_added, primary_country) |>
  group_by(primary_country) |>
  arrange(year_added) |>
  mutate(cumulative = cumsum(n)) |>
  ungroup()

# Top 10 countries by 2021 cumulative
top10_2021 <- country_yearly |>
  filter(year_added == 2021) |>
  slice_max(cumulative, n = 10) |>
  pull(primary_country)

race_data <- country_yearly |>
  filter(primary_country %in% top10_2021) |>
  group_by(year_added) |>
  mutate(rank = rank(-cumulative, ties.method = "first")) |>
  ungroup()

# ── 2. STATIC BAR CHART FRAME — 2021 ────────────────────
frame_2021 <- race_data |>
  filter(year_added == 2021) |>
  mutate(primary_country = fct_reorder(primary_country, cumulative))

p_frame <- ggplot(frame_2021,
  aes(x = primary_country, y = cumulative, fill = primary_country)) +
  geom_col(width = 0.6, show.legend = FALSE) +
  geom_text(aes(label = format(cumulative, big.mark = ",")),
    hjust = -0.1, size = 3, fontface = "bold") +
  coord_flip(clip = "off") +
  scale_fill_viridis_d(option = "turbo") +
  theme_minimal(base_size = 10) +
  theme(plot.margin = margin(5, 40, 5, 5)) +
  labs(title = "Netflix Titles by Country: 2021",
       subtitle = "Bar chart race: final frame (cumulative count)",
       x = NULL, y = "Cumulative Titles")
ggsave("output/bar_race_frame_2021.png", p_frame, width = 9, height = 5, dpi = 300)

# ── 3. STATIC KEY FRAMES PANEL (2017, 2019, 2021) ───────
key_frames <- race_data |>
  filter(year_added %in% c(2017, 2019, 2021)) |>
  mutate(primary_country = fct_reorder(primary_country, cumulative,
    .fun = max))

p_keyframes <- ggplot(key_frames,
  aes(x = primary_country, y = cumulative, fill = primary_country)) +
  geom_col(width = 0.6, show.legend = FALSE) +
  geom_text(aes(label = cumulative), hjust = -0.1, size = 2.5) +
  coord_flip(clip = "off") +
  facet_wrap(~year_added, ncol = 3) +
  scale_fill_viridis_d(option = "turbo") +
  theme_minimal(base_size = 8) +
  theme(plot.margin = margin(5, 30, 5, 5)) +
  labs(title = "Bar Chart Race: Key Frames (2017, 2019, 2021)",
       subtitle = "Static small-multiples alternative for reports/print",
       x = NULL, y = "Cumulative Titles")
ggsave("output/keyframes_panel.png", p_keyframes, width = 14, height = 5, dpi = 300)

# ── 4. BUMP CHART (RANK PLOT) — Static alternative ──────
p_bump <- ggplot(race_data,
  aes(x = year_added, y = rank, color = primary_country)) +
  geom_line(linewidth = 1) +
  geom_point(size = 2.5) +
  geom_text(data = race_data |> filter(year_added == 2021),
    aes(label = primary_country), hjust = -0.1, size = 2.5,
    fontface = "bold", show.legend = FALSE) +
  scale_y_reverse(breaks = 1:10) +
  scale_color_viridis_d(option = "turbo") +
  coord_cartesian(xlim = c(2016, 2022.5)) +
  theme_minimal() +
  theme(legend.position = "none") +
  labs(title = "Bump Chart: Country Rank Changes (2016–2021)",
       subtitle = "Static alternative to bar chart race — all years visible at once",
       x = "Year", y = "Rank (1 = most titles)")
ggsave("output/bump_chart.png", p_bump, width = 10, height = 6, dpi = 300)

# ── 5. SLOPE CHART (start → end comparison) ─────────────
slope_data <- race_data |>
  filter(year_added %in% c(2016, 2021)) |>
  select(year_added, primary_country, cumulative, rank)

p_slope <- ggplot(slope_data,
  aes(x = factor(year_added), y = rank, group = primary_country,
      color = primary_country)) +
  geom_line(linewidth = 1) +
  geom_point(size = 3) +
  geom_text(data = slope_data |> filter(year_added == 2016),
    aes(label = primary_country), hjust = 1.2, size = 2.5) +
  geom_text(data = slope_data |> filter(year_added == 2021),
    aes(label = paste0(primary_country, " (", cumulative, ")")),
    hjust = -0.1, size = 2.5) +
  scale_y_reverse(breaks = 1:10) +
  scale_color_viridis_d(option = "turbo") +
  coord_cartesian(xlim = c(0.5, 2.8)) +
  theme_minimal() +
  theme(legend.position = "none") +
  labs(title = "Slope Chart: Rank Shift 2016 → 2021",
       subtitle = "Who climbed? Who fell? (values show 2021 cumulative)",
       x = NULL, y = "Rank")
ggsave("output/slope_chart.png", p_slope, width = 8, height = 6, dpi = 300)

# ── 6. ANIMATED BAR CHART RACE (gganimate) ──────────────
# Uncomment to run — requires gganimate, gifski, transformr
# library(gganimate)
#
# race_smooth <- race_data |>
#   mutate(primary_country = fct_reorder(primary_country, cumulative,
#     .fun = max))
#
# p_race <- ggplot(race_smooth,
#   aes(x = rank, y = cumulative, fill = primary_country)) +
#   geom_col(width = 0.8, show.legend = FALSE) +
#   geom_text(aes(label = primary_country), x = -0.3,
#     hjust = 1, size = 3.5, fontface = "bold") +
#   geom_text(aes(label = format(cumulative, big.mark = ",")),
#     hjust = -0.1, size = 3) +
#   coord_flip(clip = "off") +
#   scale_x_reverse() +
#   scale_fill_viridis_d(option = "turbo") +
#   theme_minimal(base_size = 11) +
#   theme(
#     plot.margin = margin(5, 60, 5, 60),
#     axis.text.y = element_blank(),
#     axis.ticks.y = element_blank()) +
#   # Animation layers
#   transition_states(year_added,
#     transition_length = 4,
#     state_length = 2) +
#   ease_aes("cubic-in-out") +
#   labs(title = "Netflix Titles by Country: {closest_state}",
#        x = NULL, y = "Cumulative Titles")
#
# animate(p_race,
#   nframes = 150,
#   fps = 12,
#   width = 800,
#   height = 500,
#   renderer = gifski_renderer("output/bar_race.gif"))
#
# cat("Animated bar chart race saved to output/bar_race.gif\n")

# ── 7. ANIMATED SCATTER (GAPMINDER-STYLE) ───────────────
# Requires gganimate
# p_gap <- ggplot(gapminder::gapminder,
#   aes(x = gdpPercap, y = lifeExp, size = pop, color = continent)) +
#   geom_point(alpha = 0.5) +
#   scale_x_log10() + scale_size(range = c(2, 12), guide = "none") +
#   theme_minimal() +
#   transition_time(year) +
#   labs(title = "Year: {frame_time}") +
#   ease_aes("linear") +
#   shadow_wake(wake_length = 0.05, alpha = 0.2)
# animate(p_gap, nframes = 100, fps = 10,
#   renderer = gifski_renderer("output/gapminder.gif"))

# ── 8. KEY STATISTICS ────────────────────────────────────
cat("\n── Country Rankings ──\n")
cat("2016 top 5:\n")
race_data |> filter(year_added == 2016) |> arrange(rank) |>
  select(rank, primary_country, cumulative) |> slice_head(n = 5) |> print()
cat("\n2021 top 5:\n")
race_data |> filter(year_added == 2021) |> arrange(rank) |>
  select(rank, primary_country, cumulative) |> slice_head(n = 5) |> print()

cat("\nBiggest rank improvers (2016 → 2021):\n")
rank_change <- race_data |>
  filter(year_added %in% c(2016, 2021)) |>
  select(year_added, primary_country, rank) |>
  pivot_wider(names_from = year_added, values_from = rank, names_prefix = "rank_") |>
  mutate(improvement = rank_2016 - rank_2021) |>
  arrange(desc(improvement))
print(rank_change)

cat("\n── All W06-M07 R outputs saved ──\n")
cat("Figures: bar_race_frame_2021, keyframes_panel, bump_chart, slope_chart\n")
cat("Animation code: commented out (requires gganimate + gifski)\n")
