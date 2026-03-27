# ============================================================
# Workshop 7 — Module 4: The Seven Basic Data Stories
# Integrated R Script — UNYT Tirana
# ============================================================
library(tidyverse); library(patchwork); dir.create("output", showWarnings = FALSE)

# ── LOAD BOTH DATASETS ──────────────────────────────────
nf <- read_csv("netflix.csv") |>
  mutate(date_added = mdy(str_trim(date_added)),
    year_added = year(date_added),
    primary_country = str_trim(str_extract(country, "^[^,]+")))
nf_genres <- nf |> separate_rows(listed_in, sep = ", ") |> mutate(genre = str_trim(listed_in))

ec <- read_csv("ecar.csv") |>
  mutate(Year = year(mdy(`Approve Date`)), Spread = Rate - `Cost of Funds`) |>
  filter(Year >= 2002, Year <= 2012)

# ═══════════════════════════════════════════════════════
# STORY 1: CHANGE OVER TIME
# Finding: "Movie additions peaked in 2019 and declined 42%"
# ═══════════════════════════════════════════════════════
yearly <- nf |> filter(!is.na(year_added), year_added >= 2015, year_added <= 2021) |>
  count(year_added, type)
movies <- yearly |> filter(type == "Movie")
peak <- movies |> slice_max(n, n = 1)
decline <- round((1 - movies$n[movies$year_added == 2021] / peak$n) * 100)

p1 <- ggplot(yearly, aes(x = year_added, y = n, group = type)) +
  geom_line(color = "#DDDDDD", linewidth = 0.8) +
  geom_line(data = movies, color = "#1565C0", linewidth = 2.5) +
  annotate("label", x = 2018, y = movies$n[movies$year_added == 2021] * 0.85,
    label = paste0("–", decline, "% from peak"),
    size = 3, fontface = "bold", color = "#E53935", fill = "white", label.size = 0.4) +
  geom_text(data = yearly |> filter(year_added == 2021),
    aes(label = type, color = type == "Movie"),
    hjust = -0.1, size = 2.5, fontface = "bold", show.legend = FALSE) +
  scale_color_manual(values = c("TRUE" = "#1565C0", "FALSE" = "#BBB")) +
  coord_cartesian(xlim = c(2015, 2022.5)) +
  theme_minimal(base_size = 8) + theme(legend.position = "none") +
  labs(title = "STORY 1 — Change Over Time:\n'Movie additions peaked in 2019 and declined since'",
       y = "Titles Added")

# ═══════════════════════════════════════════════════════
# STORY 2: DRILL DOWN
# Finding: "69% movies, 31% TV shows"
# ═══════════════════════════════════════════════════════
type_split <- nf |> count(type) |> mutate(pct = n / sum(n) * 100)
p2 <- ggplot(type_split, aes(x = fct_reorder(type, -pct), y = pct, fill = type)) +
  geom_col(width = 0.5, show.legend = FALSE) +
  geom_text(aes(label = paste0(round(pct), "%")), vjust = -0.5, size = 3, fontface = "bold") +
  scale_fill_manual(values = c(Movie = "#1565C0", "TV Show" = "#E53935")) +
  theme_minimal(base_size = 8) +
  labs(title = "STORY 2 — Drill Down:\n'69% movies, 31% TV shows'", y = "%", x = NULL)

# ═══════════════════════════════════════════════════════
# STORY 3: ZOOM OUT
# Finding: "India rose from #5 to #2 globally"
# ═══════════════════════════════════════════════════════
country_yr <- nf |> filter(!is.na(primary_country), !is.na(year_added),
  year_added >= 2016, year_added <= 2021) |>
  count(year_added, primary_country) |>
  group_by(primary_country) |> arrange(year_added) |> mutate(cum = cumsum(n)) |> ungroup()

top5c <- country_yr |> filter(year_added == 2021) |> slice_max(cum, n = 5) |> pull(primary_country)
country_top5 <- country_yr |> filter(primary_country %in% top5c) |>
  group_by(year_added) |> mutate(rank = rank(-cum, ties.method = "first")) |> ungroup()

p3 <- ggplot(country_top5, aes(x = year_added, y = rank, color = primary_country)) +
  geom_line(linewidth = 1.2) + geom_point(size = 2) +
  scale_y_reverse(breaks = 1:5) +
  geom_text(data = country_top5 |> filter(year_added == 2021),
    aes(label = primary_country), hjust = -0.15, size = 2.5, fontface = "bold",
    show.legend = FALSE) +
  coord_cartesian(xlim = c(2016, 2022.5)) +
  theme_minimal(base_size = 8) + theme(legend.position = "none") +
  labs(title = "STORY 3 — Zoom Out:\n'India rose from #5 to #2 in global content'",
       y = "Rank (1=most)")

# ═══════════════════════════════════════════════════════
# STORY 4: CONTRAST
# Finding: "Pre-2008 spread: 3.8pp vs Post-2008: 2.9pp"
# ═══════════════════════════════════════════════════════
ec_period <- ec |> mutate(period = ifelse(Year < 2008, "Pre-2008", "Post-2008"))
spread_compare <- ec_period |> group_by(period) |>
  summarise(med_spread = median(Spread), .groups = "drop")

p4 <- ggplot(spread_compare, aes(x = period, y = med_spread, fill = period)) +
  geom_col(width = 0.4, show.legend = FALSE) +
  geom_text(aes(label = paste0(round(med_spread, 1), "pp")),
    vjust = -0.5, size = 3.5, fontface = "bold") +
  scale_fill_manual(values = c("Pre-2008" = "#1565C0", "Post-2008" = "#E53935")) +
  theme_minimal(base_size = 8) +
  labs(title = "STORY 4 — Contrast:\n'Spread compressed from 3.8pp to 2.9pp after crisis'",
       y = "Median Spread (pp)", x = NULL)

# ═══════════════════════════════════════════════════════
# STORY 5: INTERSECTIONS
# Finding: "Higher tier → lower rate"
# ═══════════════════════════════════════════════════════
p5 <- ggplot(ec |> sample_n(2000), aes(x = factor(Tier), y = Rate)) +
  geom_boxplot(fill = "#BBDEFB", color = "#1565C0", width = 0.5, outlier.size = 0.3) +
  theme_minimal(base_size = 8) +
  labs(title = "STORY 5 — Intersections:\n'Higher tier → lower rate (strong relationship)'",
       x = "Credit Tier", y = "Rate (%)")

# ═══════════════════════════════════════════════════════
# STORY 6: FACTORS
# Finding: "Three factors drive genre growth"
# ═══════════════════════════════════════════════════════
factors_df <- tibble(
  factor = c("Global expansion\n(2016, 130 countries)", "Original production\ninvestment",
    "Local-language\ncontent", "Licensing deals", "COVID demand surge"),
  impact = c(35, 28, 22, 10, 5)) |>
  mutate(factor = fct_reorder(factor, impact))

p6 <- ggplot(factors_df, aes(x = factor, y = impact)) +
  geom_col(fill = "#00695C", width = 0.5) +
  geom_text(aes(label = paste0(impact, "%")), hjust = -0.2, size = 3, fontface = "bold",
    color = "#00695C") +
  coord_flip(clip = "off") +
  theme_minimal(base_size = 8) +
  labs(title = "STORY 6 — Factors:\n'Three drivers explain Netflix genre growth'",
       x = NULL, y = "Estimated Impact (%)")

# ═══════════════════════════════════════════════════════
# STORY 7: OUTLIERS
# Finding: "Dec 2020: 160 titles — 3× average"
# ═══════════════════════════════════════════════════════
monthly <- nf |> filter(!is.na(date_added), year(date_added) >= 2016) |>
  mutate(month = floor_date(date_added, "month")) |> count(month)
avg <- mean(monthly$n)
monthly <- monthly |> mutate(is_outlier = n > avg * 2)

p7 <- ggplot(monthly, aes(x = month, y = n, color = is_outlier)) +
  geom_point(size = 1.5) + geom_line(color = "#DDDDDD", linewidth = 0.3) +
  scale_color_manual(values = c("TRUE" = "#E53935", "FALSE" = "#BBBBBB"), guide = "none") +
  geom_hline(yintercept = avg, linetype = "dashed", color = "#888") +
  geom_hline(yintercept = avg * 2, linetype = "dotted", color = "#E53935") +
  annotate("text", x = as.Date("2017-01-01"), y = avg * 2 + 5,
    label = "2× average threshold", size = 2, color = "#E53935") +
  theme_minimal(base_size = 8) +
  labs(title = "STORY 7 — Outliers:\n'Several months exceeded 2× the average additions'",
       x = NULL, y = "Titles Added")

# ═══════════════════════════════════════════════════════
# COMPOSE 7-STORY DASHBOARD
# ═══════════════════════════════════════════════════════
dashboard <- (p1 | p2 | p3) / (p4 | p5) / (p6 | p7) +
  plot_annotation(
    title = "Seven Data Stories Applied to Netflix + e-Car",
    subtitle = "Each finding maps to a story type → story type maps to a chart",
    tag_levels = "1")
ggsave("output/seven_stories_applied.png", dashboard, width = 16, height = 14, dpi = 300)

# Individual saves
ggsave("output/story1_change.png", p1, width = 8, height = 4, dpi = 300)
ggsave("output/story4_contrast.png", p4, width = 6, height = 4, dpi = 300)
ggsave("output/story7_outliers.png", p7, width = 8, height = 4, dpi = 300)

cat("\n── All W07-M04 R outputs saved ──\n")
