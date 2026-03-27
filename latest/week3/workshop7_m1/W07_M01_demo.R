# ============================================================
# Workshop 7 — Module 1: Narrative Structure in Data Communication
# Integrated R Script — UNYT Tirana
# ============================================================
library(tidyverse); library(patchwork); dir.create("output", showWarnings = FALSE)

# This module demonstrates the TRANSITION from exploratory (W04-W06)
# to explanatory (W07) using the Netflix dataset.

# ── 1. LOAD DATA ────────────────────────────────────────
nf <- read_csv("netflix.csv") |>
  mutate(
    date_added = mdy(str_trim(date_added)),
    year_added = year(date_added),
    primary_country = str_trim(str_extract(country, "^[^,]+")))

nf_genres <- nf |>
  separate_rows(listed_in, sep = ", ") |>
  mutate(genre = str_trim(listed_in))

# ── 2. EXPLORATORY VERSION (how you found the insight) ──
# Raw EDA chart — fine for the analyst, bad for stakeholders
yearly_type <- nf |>
  filter(!is.na(year_added), year_added >= 2015, year_added <= 2021) |>
  count(year_added, type)

p_exploratory <- ggplot(yearly_type, aes(x = year_added, y = n, color = type)) +
  geom_line(linewidth = 1) + geom_point(size = 2) +
  scale_color_manual(values = c(Movie = "#1565C0", "TV Show" = "#E53935")) +
  theme_minimal() +
  labs(title = "Netflix: Yearly Additions by Type (2015–2021)",
       x = "Year", y = "Count", color = "Type")
ggsave("output/exploratory_version.png", p_exploratory, width = 8, height = 5, dpi = 300)

# ── 3. EXPLANATORY VERSION (how you tell the story) ─────
# Same data, redesigned for the audience
p_explanatory <- ggplot(yearly_type, aes(x = year_added, y = n, group = type)) +
  # Grey all, accent the story
  geom_line(color = "#DDDDDD", linewidth = 0.8) +
  geom_line(data = yearly_type |> filter(type == "Movie"),
    color = "#1565C0", linewidth = 2) +
  geom_point(data = yearly_type |> filter(type == "Movie"),
    color = "#1565C0", size = 3) +
  # Direct labels (no legend needed)
  geom_text(data = yearly_type |> filter(year_added == 2021),
    aes(label = type, color = type == "Movie"),
    hjust = -0.15, size = 3.5, fontface = "bold", show.legend = FALSE) +
  scale_color_manual(values = c("TRUE" = "#1565C0", "FALSE" = "#BBBBBB")) +
  # Declarative title = the finding
  theme_minimal(base_size = 11) +
  theme(legend.position = "none",
    plot.title = element_text(face = "bold", size = 13),
    plot.subtitle = element_text(color = "#666")) +
  coord_cartesian(xlim = c(2015, 2022.5)) +
  labs(title = "Netflix movie additions peaked in 2019 and have since declined",
       subtitle = "TV Show additions grew steadily, but movies — the larger category — are contracting",
       x = NULL, y = "Titles Added per Year",
       caption = "Source: Netflix dataset | UNYT Data Viz Course")
ggsave("output/explanatory_version.png", p_explanatory, width = 9, height = 5, dpi = 300)

# Side-by-side comparison
ggsave("output/exp_vs_expl.png",
  (p_exploratory + labs(title = "EXPLORATORY\n(descriptive title, legend, no story)")) |
  (p_explanatory + labs(title = "EXPLANATORY\n(declarative title, direct labels, focused)")),
  width = 16, height = 5, dpi = 300)

# ── 4. THE BIG IDEA EXERCISE ────────────────────────────
# Netflix Big Idea:
# "Netflix should accelerate original series investment because
#  movie additions have declined 40% since 2019 while TV Show
#  additions continue to grow."
#
# Structure: [Subject] should [action] because [evidence]

# Visualize the Big Idea as a single annotated chart
movie_peak <- yearly_type |> filter(type == "Movie") |> slice_max(n, n = 1)
movie_latest <- yearly_type |> filter(type == "Movie", year_added == 2021)
decline_pct <- round((1 - movie_latest$n / movie_peak$n) * 100)

p_big_idea <- ggplot(yearly_type |> filter(type == "Movie"),
  aes(x = year_added, y = n)) +
  geom_line(color = "#1565C0", linewidth = 2) +
  geom_point(color = "#1565C0", size = 3) +
  # Highlight the decline
  geom_segment(aes(x = movie_peak$year_added, xend = 2021,
    y = movie_peak$n, yend = movie_peak$n),
    linetype = "dotted", color = "#888") +
  annotate("text", x = 2020.5, y = (movie_peak$n + movie_latest$n) / 2,
    label = paste0(decline_pct, "% decline\nsince peak"),
    size = 4, fontface = "bold", color = "#E53935") +
  annotate("segment", x = 2020.5, xend = 2020.5,
    y = movie_peak$n - 10, yend = movie_latest$n + 10,
    arrow = arrow(ends = "both", length = unit(0.15, "cm")),
    color = "#E53935", linewidth = 0.8) +
  theme_minimal(base_size = 11) +
  theme(plot.title = element_text(face = "bold", size = 12)) +
  labs(title = paste0("Movie additions declined ", decline_pct,
    "% from peak — the content pipeline is contracting"),
       subtitle = "Netflix movie catalog growth has reversed; strategic pivot needed",
       x = NULL, y = "Movie Titles Added",
       caption = "Source: Netflix dataset")
ggsave("output/big_idea.png", p_big_idea, width = 9, height = 5, dpi = 300)

# ── 5. STORY ARC: THREE-SLIDE SEQUENCE ──────────────────
# Slide 1 — Context
p_context <- ggplot(nf |>
  filter(!is.na(date_added)) |>
  mutate(month = floor_date(date_added, "month")) |>
  count(month) |>
  mutate(cumulative = cumsum(n)),
  aes(x = month, y = cumulative)) +
  geom_area(fill = "#1565C0", alpha = 0.2) +
  geom_line(color = "#1565C0", linewidth = 1) +
  theme_minimal() +
  labs(title = "Netflix built a catalog of 8,800+ titles by 2021",
       subtitle = "Context: the platform grew rapidly over a decade",
       x = NULL, y = "Cumulative Titles")

# Slide 2 — Complication
p_complication <- p_explanatory +
  labs(title = "But movie additions have been declining since 2019",
       subtitle = "Complication: the largest content category is contracting")

# Slide 3 — Resolution
genre_growth <- nf_genres |>
  filter(!is.na(year_added), year_added %in% c(2017, 2021)) |>
  count(year_added, genre) |>
  pivot_wider(names_from = year_added, values_from = n, values_fill = 0) |>
  mutate(growth = (`2021` - `2017`) / pmax(`2017`, 1) * 100) |>
  slice_max(growth, n = 5)

p_resolution <- ggplot(genre_growth,
  aes(x = fct_reorder(genre, growth), y = growth)) +
  geom_col(fill = "#2E7D32", width = 0.5) +
  geom_text(aes(label = paste0("+", round(growth), "%")),
    hjust = -0.1, size = 3, fontface = "bold", color = "#2E7D32") +
  coord_flip(clip = "off") +
  theme_minimal() +
  labs(title = "International and niche genres are the growth engines",
       subtitle = "Resolution: pivot investment toward these categories",
       x = NULL, y = "Growth % (2017 → 2021)")

ggsave("output/story_arc_3slides.png",
  p_context / p_complication / p_resolution +
  plot_annotation(title = "Three-Slide Story Arc: Context → Complication → Resolution",
    tag_levels = "1"),
  width = 10, height = 14, dpi = 300)

# ── 6. DESCRIPTIVE vs DECLARATIVE TITLES ─────────────────
p_descriptive <- ggplot(yearly_type, aes(x = year_added, y = n, color = type)) +
  geom_line(linewidth = 1) + geom_point(size = 2) +
  scale_color_manual(values = c(Movie = "#1565C0", "TV Show" = "#E53935")) +
  theme_minimal(base_size = 9) +
  labs(title = "Descriptive: 'Netflix Additions by Type'",
       subtitle = "(What the chart shows — not what it means)")

p_declarative <- ggplot(yearly_type, aes(x = year_added, y = n, color = type)) +
  geom_line(linewidth = 1) + geom_point(size = 2) +
  scale_color_manual(values = c(Movie = "#1565C0", "TV Show" = "#E53935")) +
  theme_minimal(base_size = 9) +
  labs(title = "Declarative: 'Movie additions peaked in 2019; TV grew steadily'",
       subtitle = "(The title IS the finding — the chart is the evidence)")

ggsave("output/title_comparison.png",
  p_descriptive | p_declarative, width = 14, height = 5, dpi = 300)

cat("\n── All W07-M01 R outputs saved ──\n")
cat("Figures: exploratory_version, explanatory_version, exp_vs_expl,\n")
cat("  big_idea, story_arc_3slides, title_comparison\n")
