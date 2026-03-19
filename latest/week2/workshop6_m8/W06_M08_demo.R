# ============================================================
# Workshop 6 — Module 8: Case Study — Netflix Content Trends
# Integrated R Script — UNYT Tirana
# ============================================================
library(tidyverse); library(patchwork); dir.create("output", showWarnings = FALSE)

# ── 1. LOAD AND PREPARE ─────────────────────────────────
nf <- read_csv("netflix.csv") |>
  mutate(
    date_added = mdy(str_trim(date_added)),
    year_added = year(date_added),
    month_added = month(date_added),
    primary_country = str_trim(str_extract(country, "^[^,]+")))

# Genre expansion (one row per genre per title)
nf_genres <- nf |>
  separate_rows(listed_in, sep = ", ") |>
  mutate(genre = str_trim(listed_in))

cat("Dataset:", nrow(nf), "titles,", sum(!is.na(nf$date_added)), "with dates\n")
cat("Date range:", format(min(nf$date_added, na.rm=TRUE)), "to",
  format(max(nf$date_added, na.rm=TRUE)), "\n")

# ── 2. YEARLY ADDITIONS BY TYPE ─────────────────────────
yearly_type <- nf |>
  filter(!is.na(year_added), year_added >= 2015, year_added <= 2021) |>
  count(year_added, type)

p_yearly <- ggplot(yearly_type, aes(x = year_added, y = n, color = type)) +
  geom_line(linewidth = 1.5) +
  geom_point(size = 3) +
  geom_text(aes(label = n), vjust = -1, size = 2.5, show.legend = FALSE) +
  scale_color_manual(values = c(Movie = "#1565C0", "TV Show" = "#E53935")) +
  theme_minimal() +
  labs(title = "Netflix Yearly Additions by Type (2015–2021)",
       subtitle = "Movie additions peaked ~2019; TV Shows grew steadily",
       x = "Year", y = "Titles Added", color = NULL)
ggsave("output/yearly_type.png", p_yearly, width = 9, height = 5, dpi = 300)

# ── 3. MONTHLY ADDITIONS WITH EVENT ANNOTATIONS ─────────
monthly <- nf |>
  filter(!is.na(date_added), year(date_added) >= 2015) |>
  mutate(month = floor_date(date_added, "month")) |>
  count(month)

p_monthly <- ggplot(monthly, aes(x = month, y = n)) +
  geom_line(color = "#1565C0", linewidth = 0.8) +
  # Event annotations
  geom_vline(xintercept = as.Date("2016-01-01"),
    linetype = "dashed", color = "#2E7D32", linewidth = 0.5) +
  annotate("text", x = as.Date("2016-03-01"),
    y = max(monthly$n) * 0.95,
    label = "Global expansion\n(130 new countries)",
    size = 2, color = "#2E7D32", hjust = 0) +
  geom_vline(xintercept = as.Date("2020-03-01"),
    linetype = "dashed", color = "#E53935", linewidth = 0.5) +
  annotate("text", x = as.Date("2020-05-01"),
    y = max(monthly$n) * 0.85,
    label = "COVID-19\nlockdown",
    size = 2, color = "#E53935", hjust = 0) +
  geom_vline(xintercept = as.Date("2021-06-01"),
    linetype = "dashed", color = "#E65100", linewidth = 0.5) +
  annotate("text", x = as.Date("2021-03-01"),
    y = max(monthly$n) * 0.55,
    label = "Content\nslowdown",
    size = 2, color = "#E65100", hjust = 1) +
  scale_x_date(date_breaks = "1 year", date_labels = "%Y") +
  theme_minimal() +
  labs(title = "Netflix Monthly Additions with Event Annotations",
       subtitle = "Three key events annotated on the timeline",
       x = NULL, y = "Titles Added per Month")
ggsave("output/monthly_annotated.png", p_monthly, width = 10, height = 5, dpi = 300)

# ── 4. GENRE EVOLUTION: TOP 5 ───────────────────────────
top5_genres <- nf_genres |> count(genre, sort = TRUE) |> slice_max(n, n = 5) |> pull(genre)

genre_yearly <- nf_genres |>
  filter(genre %in% top5_genres, !is.na(year_added),
    year_added >= 2015, year_added <= 2021) |>
  count(year_added, genre)

# Grey+accent: highlight the fastest grower
fastest <- genre_yearly |>
  group_by(genre) |>
  summarise(growth = last(n) / first(n)) |>
  slice_max(growth, n = 1) |>
  pull(genre)

p_genre <- ggplot(genre_yearly, aes(x = year_added, y = n, group = genre)) +
  geom_line(color = "#DDDDDD", linewidth = 0.8) +
  geom_line(data = genre_yearly |> filter(genre == fastest),
    color = "#E53935", linewidth = 2) +
  geom_text(data = genre_yearly |> group_by(genre) |> filter(year_added == max(year_added)),
    aes(label = genre, color = genre == fastest),
    hjust = -0.05, size = 2.5, show.legend = FALSE) +
  scale_color_manual(values = c("TRUE" = "#E53935", "FALSE" = "#AAAAAA")) +
  coord_cartesian(xlim = c(2015, 2023)) +
  theme_minimal() +
  labs(title = "Top 5 Genre Trends: Grey+Accent on Fastest Grower",
       subtitle = paste0("Fastest relative growth: ", fastest),
       x = "Year", y = "Titles Added")
ggsave("output/genre_trends.png", p_genre, width = 10, height = 5, dpi = 300)

# Small multiples alternative
p_genre_multi <- ggplot(genre_yearly, aes(x = year_added, y = n)) +
  geom_line(color = "#1565C0", linewidth = 1) +
  geom_point(color = "#1565C0", size = 1.5) +
  facet_wrap(~genre, ncol = 5, scales = "free_y") +
  theme_minimal(base_size = 8) +
  labs(title = "Genre Trends: Small Multiples (free y-axis)", x = "Year", y = "Count")
ggsave("output/genre_multiples.png", p_genre_multi, width = 14, height = 4, dpi = 300)

# ── 5. CUMULATIVE STACKED AREA BY TYPE ──────────────────
type_monthly <- nf |>
  filter(!is.na(date_added), year(date_added) >= 2015) |>
  mutate(month = floor_date(date_added, "month")) |>
  count(month, type) |>
  group_by(type) |> arrange(month) |>
  mutate(cumulative = cumsum(n)) |>
  ungroup()

p_cumulative <- ggplot(type_monthly, aes(x = month, y = cumulative, fill = type)) +
  geom_area(alpha = 0.7, color = "white", linewidth = 0.3) +
  scale_fill_manual(values = c(Movie = "#1565C0", "TV Show" = "#E53935")) +
  scale_x_date(date_breaks = "1 year", date_labels = "%Y") +
  theme_minimal() +
  labs(title = "Cumulative Netflix Catalog by Type",
       subtitle = "Stacked area: total library growth (Movie + TV Show)",
       x = NULL, y = "Cumulative Titles")
ggsave("output/cumulative_stacked.png", p_cumulative, width = 10, height = 5, dpi = 300)

# 100% version (proportion)
type_monthly_pct <- type_monthly |>
  group_by(month) |>
  mutate(pct = cumulative / sum(cumulative) * 100) |>
  ungroup()

p_pct <- ggplot(type_monthly_pct, aes(x = month, y = pct, fill = type)) +
  geom_area(alpha = 0.7, color = "white", linewidth = 0.3) +
  scale_fill_manual(values = c(Movie = "#1565C0", "TV Show" = "#E53935")) +
  scale_x_date(date_breaks = "1 year", date_labels = "%Y") +
  theme_minimal() +
  labs(title = "Netflix Catalog Composition (% by Type)",
       subtitle = "TV Show share growing from ~20% to ~35%",
       x = NULL, y = "Share (%)")
ggsave("output/cumulative_pct.png", p_pct, width = 10, height = 5, dpi = 300)

# ── 6. SEASONAL SUBSERIES ───────────────────────────────
seasonal <- nf |>
  filter(!is.na(year_added), year_added >= 2016, year_added <= 2021) |>
  count(year_added, month_added) |>
  mutate(is_2021 = year_added == 2021)

p_seasonal <- ggplot(seasonal,
  aes(x = month_added, y = n, group = year_added,
      color = is_2021, alpha = is_2021, linewidth = is_2021)) +
  geom_line() + geom_point(size = 1.5) +
  scale_color_manual(values = c("TRUE" = "#E53935", "FALSE" = "#BBBBBB"), guide = "none") +
  scale_alpha_manual(values = c("TRUE" = 1, "FALSE" = 0.3), guide = "none") +
  scale_linewidth_manual(values = c("TRUE" = 1.5, "FALSE" = 0.6), guide = "none") +
  scale_x_continuous(breaks = 1:12, labels = month.abb) +
  theme_minimal() +
  labs(title = "Seasonal Pattern: Monthly Additions (2016–2021)",
       subtitle = "Grey = 2016–2020, Red = 2021",
       x = "Month", y = "Titles Added")
ggsave("output/seasonal_subseries.png", p_seasonal, width = 9, height = 5, dpi = 300)

# ── 7. TOP COUNTRIES OVER TIME ───────────────────────────
top5_countries <- nf |>
  filter(!is.na(primary_country)) |>
  count(primary_country, sort = TRUE) |>
  slice_max(n, n = 5) |> pull(primary_country)

country_yearly <- nf |>
  filter(primary_country %in% top5_countries, !is.na(year_added),
    year_added >= 2016, year_added <= 2021) |>
  count(year_added, primary_country)

p_country <- ggplot(country_yearly,
  aes(x = year_added, y = n, color = primary_country)) +
  geom_line(linewidth = 1) + geom_point(size = 2) +
  theme_minimal() +
  labs(title = "Netflix: Top 5 Countries — Yearly Additions",
       x = "Year", y = "Titles Added", color = "Country")
ggsave("output/country_trends.png", p_country, width = 9, height = 5, dpi = 300)

# ── 8. FIVE-PANEL TEMPORAL DASHBOARD ─────────────────────
dashboard <- (p_yearly | p_genre) / (p_monthly) / (p_cumulative | p_seasonal) +
  plot_annotation(
    title = "Netflix Temporal Case Study: Five-Panel Dashboard",
    subtitle = "Yearly trends + Genre evolution + Monthly events + Cumulative + Seasonal",
    tag_levels = "a")
ggsave("output/netflix_dashboard.png", dashboard, width = 14, height = 14, dpi = 300)

# ── 9. KEY FINDINGS ──────────────────────────────────────
cat("\n── KEY FINDINGS ──\n")
cat("1. Movie peak: 2019 (", yearly_type |> filter(type=="Movie") |>
  slice_max(n,n=1) |> pull(n), "titles). Declined post-2019.\n")
cat("2. TV pivot: TV Shows grew every year 2015–2020.\n")
cat("3. Fastest genre:", fastest, "(by relative growth 2015→2021)\n")
cat("4. COVID impact: visible dip in monthly additions ~mid-2020\n")
cat("5. Seasonal pattern: releases cluster in Q4 (holiday season)\n")

cat("\n── All W06-M08 R outputs saved ──\n")
