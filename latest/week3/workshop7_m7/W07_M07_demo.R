# ============================================================
# Workshop 7 — Module 7: Case Study — Netflix Data Story
# Complete 10-slide assertion-evidence deck in R
# ============================================================
library(tidyverse); library(patchwork); dir.create("output", showWarnings = FALSE)

# ── CLEAN THEME (from M06) ──────────────────────────────
theme_story <- theme_minimal(base_size = 12) +
  theme(panel.grid = element_blank(),
    axis.line = element_line(color = "#EEEEEE", linewidth = 0.3),
    plot.title = element_text(face = "bold", size = 14),
    plot.subtitle = element_text(color = "#666", size = 10),
    plot.caption = element_text(color = "#AAA", size = 7),
    legend.position = "none")
theme_set(theme_story)

# ── LOAD + PREPARE ──────────────────────────────────────
nf <- read_csv("netflix.csv") |>
  mutate(date_added = mdy(str_trim(date_added)),
    year_added = year(date_added),
    month_added = month(date_added),
    primary_country = str_trim(str_extract(country, "^[^,]+")))
nf_genres <- nf |> separate_rows(listed_in, sep = ", ") |> mutate(genre = str_trim(listed_in))

yearly_type <- nf |> filter(!is.na(year_added), year_added >= 2015, year_added <= 2021) |>
  count(year_added, type)
movies <- yearly_type |> filter(type == "Movie")
tv <- yearly_type |> filter(type == "TV Show")
peak <- movies |> slice_max(n, n = 1)
decline <- round((1 - movies$n[movies$year_added == 2021] / peak$n) * 100)

# ═══════════════════════════════════════════════════════
# SLIDE 2: CONTEXT — Cumulative catalog growth
# Story type: Zoom Out | Chart: Area
# ═══════════════════════════════════════════════════════
p2 <- nf |> filter(!is.na(date_added)) |>
  mutate(month = floor_date(date_added, "month")) |>
  count(month) |> mutate(cum = cumsum(n)) |>
  ggplot(aes(x = month, y = cum)) +
  geom_area(fill = "#1565C0", alpha = 0.15) +
  geom_line(color = "#1565C0", linewidth = 1.2) +
  scale_x_date(date_breaks = "2 years", date_labels = "%Y") +
  labs(title = "Netflix built a catalog of 8,800+ titles over a decade",
       subtitle = "Cumulative titles added to the platform (2008–2021)",
       x = NULL, y = "Cumulative Titles",
       caption = "Source: Netflix dataset | UNYT")
ggsave("output/slide02_context.png", p2, width = 10, height = 5.5, dpi = 300)

# ═══════════════════════════════════════════════════════
# SLIDE 3: COMPLICATION — Movie decline
# Story type: Change Over Time | Chart: Line (grey+accent)
# ═══════════════════════════════════════════════════════
p3 <- ggplot(yearly_type, aes(x = year_added, y = n, group = type)) +
  geom_line(color = "#DDDDDD", linewidth = 0.8) +
  geom_line(data = movies, color = "#1565C0", linewidth = 2.5) +
  geom_point(data = movies, color = "#1565C0", size = 3) +
  annotate("label", x = 2018.3, y = movies$n[movies$year_added == 2021] * 0.82,
    label = paste0("–", decline, "% from peak"),
    size = 3.5, fontface = "bold", color = "#E53935", fill = "white", label.size = 0.4) +
  geom_text(data = yearly_type |> filter(year_added == 2021),
    aes(label = type, color = type == "Movie"),
    hjust = -0.1, size = 3.5, fontface = "bold", show.legend = FALSE) +
  scale_color_manual(values = c("TRUE" = "#1565C0", "FALSE" = "#BBB")) +
  coord_cartesian(xlim = c(2015, 2022.5)) +
  labs(title = paste0("Movie additions declined ", decline, "% from their 2019 peak"),
       subtitle = "The largest content category is contracting",
       x = NULL, y = "Titles Added")
ggsave("output/slide03_complication.png", p3, width = 10, height = 5.5, dpi = 300)

# ═══════════════════════════════════════════════════════
# SLIDE 4: CONTRAST — Movie vs TV divergence
# Story type: Contrast | Chart: Dual line indexed
# ═══════════════════════════════════════════════════════
indexed <- yearly_type |>
  group_by(type) |> mutate(idx = n / first(n) * 100) |> ungroup()
p4 <- ggplot(indexed, aes(x = year_added, y = idx, color = type)) +
  geom_line(linewidth = 1.5) + geom_point(size = 2.5) +
  geom_hline(yintercept = 100, linetype = "dotted", color = "#888") +
  scale_color_manual(values = c(Movie = "#1565C0", "TV Show" = "#E53935")) +
  geom_text(data = indexed |> filter(year_added == 2021),
    aes(label = type), hjust = -0.1, size = 3, fontface = "bold", show.legend = FALSE) +
  coord_cartesian(xlim = c(2015, 2022.5)) +
  labs(title = "TV Shows grew 3× faster than Movies in relative terms",
       subtitle = "Both indexed to 100 at 2015 for fair comparison",
       x = NULL, y = "Index (2015 = 100)")
ggsave("output/slide04_contrast.png", p4, width = 10, height = 5.5, dpi = 300)

# ═══════════════════════════════════════════════════════
# SLIDE 5: ANALYSIS — Genre growth (climax)
# Story type: Change | Chart: Bar (accent)
# ═══════════════════════════════════════════════════════
genre_growth <- nf_genres |>
  filter(!is.na(year_added), year_added %in% c(2017, 2021)) |>
  count(year_added, genre) |>
  pivot_wider(names_from = year_added, values_from = n, values_fill = 0) |>
  mutate(growth = (`2021` - `2017`) / pmax(`2017`, 1) * 100) |>
  slice_max(growth, n = 7)
fastest <- genre_growth |> slice_max(growth, n = 1) |> pull(genre)

p5 <- ggplot(genre_growth,
  aes(x = fct_reorder(genre, growth), y = growth,
      fill = genre == fastest)) +
  geom_col(width = 0.5, show.legend = FALSE) +
  geom_text(aes(label = paste0("+", round(growth), "%")),
    hjust = -0.1, size = 3, fontface = "bold") +
  scale_fill_manual(values = c("TRUE" = "#2E7D32", "FALSE" = "#BBDEFB")) +
  coord_flip(clip = "off") +
  labs(title = paste0(fastest, " is the fastest-growing genre category"),
       subtitle = "Genre growth rates 2017 → 2021 (green = fastest)",
       x = NULL, y = "Growth %")
ggsave("output/slide05_analysis.png", p5, width = 10, height = 5.5, dpi = 300)

# ═══════════════════════════════════════════════════════
# SLIDE 6: DEEP DIVE — India's rise
# Story type: Zoom Out | Chart: Bump
# ═══════════════════════════════════════════════════════
country_cum <- nf |>
  filter(!is.na(primary_country), !is.na(year_added), year_added >= 2016, year_added <= 2021) |>
  count(year_added, primary_country) |>
  group_by(primary_country) |> arrange(year_added) |> mutate(cum = cumsum(n)) |> ungroup()
top5c <- country_cum |> filter(year_added == 2021) |> slice_max(cum, n = 5) |> pull(primary_country)
race <- country_cum |> filter(primary_country %in% top5c) |>
  group_by(year_added) |> mutate(rank = rank(-cum, ties.method = "first")) |> ungroup()

p6 <- ggplot(race, aes(x = year_added, y = rank, group = primary_country)) +
  geom_line(color = "#DDDDDD", linewidth = 0.8) +
  geom_line(data = race |> filter(primary_country == "India"),
    color = "#E53935", linewidth = 2.5) +
  geom_point(data = race |> filter(primary_country == "India"),
    color = "#E53935", size = 3) +
  geom_text(data = race |> filter(year_added == 2021),
    aes(label = primary_country, color = primary_country == "India"),
    hjust = -0.15, size = 3, fontface = "bold", show.legend = FALSE) +
  scale_color_manual(values = c("TRUE" = "#E53935", "FALSE" = "#AAA")) +
  scale_y_reverse(breaks = 1:5) +
  coord_cartesian(xlim = c(2016, 2022.5)) +
  labs(title = "India rose from #5 to #2 in Netflix content production",
       subtitle = "Bump chart of top 5 content-producing countries (2016–2021)",
       x = NULL, y = "Rank (1 = most titles)")
ggsave("output/slide06_deepdive.png", p6, width = 10, height = 5.5, dpi = 300)

# ═══════════════════════════════════════════════════════
# SLIDE 7: SEASONAL — Release calendar
# Story type: Drill Down | Chart: Calendar heatmap
# ═══════════════════════════════════════════════════════
daily_2020 <- nf |> filter(year_added == 2020, !is.na(date_added)) |>
  count(date_added) |>
  mutate(dow = wday(date_added, label = TRUE, week_start = 1),
    week = isoweek(date_added))

p7 <- ggplot(daily_2020, aes(x = week, y = dow, fill = n)) +
  geom_tile(color = "white", linewidth = 0.4) +
  scale_fill_gradient(low = "#E8F5E9", high = "#1B5E20", name = "Titles") +
  scale_y_discrete(limits = rev(c("Mon","Tue","Wed","Thu","Fri","Sat","Sun"))) +
  theme(panel.grid = element_blank(), legend.key.size = unit(0.4, "cm")) +
  labs(title = "Friday is Netflix's primary release day, with Q4 holiday spikes",
       subtitle = "Calendar heatmap of daily additions in 2020 (row = DOW, col = week)",
       x = "Week of Year", y = NULL)
ggsave("output/slide07_seasonal.png", p7, width = 11, height = 4, dpi = 300)

# ═══════════════════════════════════════════════════════
# SLIDE 8: RESOLUTION — Quality > Quantity
# Story type: Change | Chart: Stacked area (composition shift)
# ═══════════════════════════════════════════════════════
type_monthly <- nf |> filter(!is.na(date_added), year(date_added) >= 2015) |>
  mutate(month = floor_date(date_added, "month")) |>
  count(month, type) |>
  group_by(type) |> arrange(month) |> mutate(cum = cumsum(n)) |> ungroup() |>
  group_by(month) |> mutate(pct = cum / sum(cum) * 100) |> ungroup()

p8 <- ggplot(type_monthly, aes(x = month, y = pct, fill = type)) +
  geom_area(alpha = 0.7, color = "white", linewidth = 0.3) +
  scale_fill_manual(values = c(Movie = "#1565C0", "TV Show" = "#E53935")) +
  geom_text(data = type_monthly |> filter(month == max(month)),
    aes(label = paste0(type, " ", round(pct), "%")),
    position = position_stack(vjust = 0.5), size = 3, fontface = "bold", color = "white") +
  scale_x_date(date_breaks = "1 year", date_labels = "%Y") +
  labs(title = "TV Show share grew from 20% to 35% — the catalog is rebalancing",
       subtitle = "Proportional composition of cumulative Netflix catalog over time",
       x = NULL, y = "Share (%)")
ggsave("output/slide08_resolution.png", p8, width = 10, height = 5.5, dpi = 300)

# ═══════════════════════════════════════════════════════
# COMPOSE: Full 8-slide panel (slides 2–9 as evidence)
# ═══════════════════════════════════════════════════════
all_slides <- (p2 + labs(title = "2. Context") + theme(plot.title = element_text(size = 9))) |
  (p3 + labs(title = "3. Complication") + theme(plot.title = element_text(size = 9)))
all_slides2 <- (p4 + labs(title = "4. Contrast") + theme(plot.title = element_text(size = 9))) |
  (p5 + labs(title = "5. Analysis") + theme(plot.title = element_text(size = 9)))
all_slides3 <- (p6 + labs(title = "6. Deep Dive") + theme(plot.title = element_text(size = 9))) |
  (p7 + labs(title = "7. Seasonal") + theme(plot.title = element_text(size = 9)))
all_slides4 <- (p8 + labs(title = "8. Resolution") + theme(plot.title = element_text(size = 9))) |
  plot_spacer()

ggsave("output/netflix_story_deck.png",
  all_slides / all_slides2 / all_slides3 / all_slides4 +
  plot_annotation(title = "Netflix Data Story: 8-Slide Evidence Deck"),
  width = 16, height = 22, dpi = 200)

# ── TITLE SEQUENCE TEST ──────────────────────────────────
cat("\n── TITLE SEQUENCE TEST ──\n")
cat("Read only the titles. Does the story work?\n\n")
cat("1. Netflix Content Strategy: A Data Story\n")
cat("2. Netflix built a catalog of 8,800+ titles over a decade\n")
cat("3. Movie additions declined", decline, "% from their 2019 peak\n")
cat("4. TV Shows grew 3× faster than Movies in relative terms\n")
cat("5.", fastest, "is the fastest-growing genre category\n")
cat("6. India rose from #5 to #2 in content production\n")
cat("7. Friday is Netflix's primary release day, with Q4 spikes\n")
cat("8. TV Show share grew from 20% to 35% — the catalog is rebalancing\n")
cat("9. Four actions: originals, local content, reduce filler, language hubs\n")
cat("10. Explore the interactive dashboard for more detail\n")

cat("\n── All W07-M07 R outputs saved ──\n")
