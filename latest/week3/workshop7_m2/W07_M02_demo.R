# ============================================================
# Workshop 7 — Module 2: Exploratory vs Explanatory Visualization
# Integrated R Script — UNYT Tirana
# ============================================================
library(tidyverse); library(patchwork); dir.create("output", showWarnings = FALSE)

# ── 1. LOAD DATA ────────────────────────────────────────
nf <- read_csv("netflix.csv") |>
  mutate(date_added = mdy(str_trim(date_added)),
    year_added = year(date_added),
    primary_country = str_trim(str_extract(country, "^[^,]+")))

yearly_type <- nf |>
  filter(!is.na(year_added), year_added >= 2015, year_added <= 2021) |>
  count(year_added, type)

# ── 2. READER-DRIVEN (Dashboard-Style) ──────────────────
# Grouped bar chart: both types visible, legend, gridlines, descriptive title
p_dashboard <- ggplot(yearly_type, aes(x = factor(year_added), y = n, fill = type)) +
  geom_col(position = "dodge", width = 0.7) +
  scale_fill_manual(values = c(Movie = "#1565C0", "TV Show" = "#E53935")) +
  theme_minimal() +
  theme(panel.grid.major.x = element_blank()) +
  labs(title = "Netflix Additions by Type (2015–2021)",
       subtitle = "Dashboard view: user reads both series, draws own conclusions",
       x = "Year", y = "Titles Added", fill = "Type")
ggsave("output/reader_driven.png", p_dashboard, width = 9, height = 5, dpi = 300)

# ── 3. AUTHOR-DRIVEN (Story Slide) ──────────────────────
# Grey+accent, declarative title, direct labels, annotation
p_story <- ggplot(yearly_type, aes(x = year_added, y = n, group = type)) +
  geom_line(color = "#DDDDDD", linewidth = 0.8) +
  geom_line(data = yearly_type |> filter(type == "Movie"),
    color = "#1565C0", linewidth = 2.5) +
  geom_point(data = yearly_type |> filter(type == "Movie"),
    color = "#1565C0", size = 3) +
  # Direct labels
  geom_text(data = yearly_type |> filter(year_added == 2021),
    aes(label = type, color = type == "Movie"),
    hjust = -0.15, size = 3.5, fontface = "bold", show.legend = FALSE) +
  scale_color_manual(values = c("TRUE" = "#1565C0", "FALSE" = "#BBBBBB")) +
  # Decline callout
  annotate("segment", x = 2019, xend = 2021, y = 1050, yend = 1050,
    linetype = "dotted", color = "#888") +
  annotate("text", x = 2020, y = 950,
    label = "–42% since\n2019 peak", size = 3.5, fontface = "bold",
    color = "#E53935") +
  coord_cartesian(xlim = c(2015, 2022.5)) +
  theme_minimal(base_size = 11) +
  theme(legend.position = "none",
    plot.title = element_text(face = "bold", size = 13)) +
  labs(title = "Movie additions declined 42% from their 2019 peak",
       subtitle = "Author-driven: one message, annotated, no legend",
       x = NULL, y = "Titles Added per Year")
ggsave("output/author_driven.png", p_story, width = 9, height = 5, dpi = 300)

# Side-by-side comparison
ggsave("output/reader_vs_author.png",
  (p_dashboard + labs(title = "READER-DRIVEN\n(Dashboard: descriptive, interactive)")) |
  (p_story + labs(title = "AUTHOR-DRIVEN\n(Story slide: declarative, focused)")),
  width = 16, height = 5.5, dpi = 300)

# ── 4. MARTINI GLASS: Narrative → Dashboard ──────────────
# Part 1: 3-slide author-driven narrative
p_slide1 <- ggplot(nf |> filter(!is.na(date_added)) |>
  mutate(month = floor_date(date_added, "month")) |>
  count(month) |> mutate(cum = cumsum(n)),
  aes(x = month, y = cum)) +
  geom_area(fill = "#1565C0", alpha = 0.15) +
  geom_line(color = "#1565C0", linewidth = 1) +
  theme_minimal(base_size = 8) +
  labs(title = "Slide 1: Netflix built 8,800+ titles by 2021",
       x = NULL, y = "Cumulative")

p_slide2 <- p_story +
  labs(title = "Slide 2: But movies are declining since 2019") +
  theme(plot.title = element_text(size = 9))

top5_countries <- nf |> filter(!is.na(primary_country)) |>
  count(primary_country, sort = TRUE) |> slice_max(n, n = 5)
p_slide3 <- ggplot(top5_countries,
  aes(x = fct_reorder(primary_country, n), y = n)) +
  geom_col(fill = "#2E7D32", width = 0.5) +
  geom_text(aes(label = format(n, big.mark = ",")),
    hjust = -0.1, size = 2.5, fontface = "bold") +
  coord_flip(clip = "off") +
  theme_minimal(base_size = 8) +
  labs(title = "Slide 3: US dominates, but India is rising fast",
       x = NULL, y = "Total Titles")

# Part 2: dashboard (reader-driven)
monthly_all <- nf |>
  filter(!is.na(date_added), year(date_added) >= 2015) |>
  mutate(month = floor_date(date_added, "month")) |>
  count(month, type)
p_dash <- ggplot(monthly_all, aes(x = month, y = n, color = type)) +
  geom_line(linewidth = 0.5) +
  scale_color_manual(values = c(Movie = "#1565C0", "TV Show" = "#E53935")) +
  theme_minimal(base_size = 7) +
  labs(title = "TRANSITION → DASHBOARD (explore freely)",
       subtitle = "Filter by type, country, genre, date range",
       x = NULL, y = "Monthly Additions", color = "Type")

ggsave("output/martini_glass.png",
  (p_slide1 | p_slide2 | p_slide3) / p_dash +
  plot_annotation(
    title = "Martini Glass: 3 Guided Slides → Dashboard Exploration",
    tag_levels = list(c("Slide 1", "Slide 2", "Slide 3", "Dashboard"))),
  width = 14, height = 9, dpi = 300)

# ── 5. e-Car: Dashboard vs Story ────────────────────────
ec <- read_csv("ecar.csv") |>
  mutate(Year = year(mdy(`Approve Date`)),
    Spread = Rate - `Cost of Funds`) |>
  filter(Year >= 2002, Year <= 2012)

yearly_ec <- ec |> group_by(Year) |>
  summarise(rate = mean(Rate), spread = mean(Spread), n = n())

# Dashboard version
p_ec_dash <- ggplot(yearly_ec) +
  geom_line(aes(x = Year, y = rate), color = "#1565C0", linewidth = 1) +
  geom_line(aes(x = Year, y = spread), color = "#E53935", linewidth = 1) +
  theme_minimal(base_size = 9) +
  labs(title = "e-Car: Rate and Spread (Dashboard)",
       subtitle = "Descriptive — user interprets both lines",
       y = "pp")

# Story slide version
p_ec_story <- ggplot(yearly_ec) +
  geom_line(aes(x = Year, y = spread), color = "#DDDDDD", linewidth = 0.8) +
  geom_line(aes(x = Year, y = rate), color = "#1565C0", linewidth = 2.5) +
  geom_vline(xintercept = 2008, linetype = "dashed", color = "#E53935") +
  annotate("text", x = 2008.3, y = max(yearly_ec$rate) * 0.9,
    label = "2008\ncrisis", color = "#E53935", size = 3, fontface = "bold") +
  theme_minimal(base_size = 9) +
  theme(legend.position = "none") +
  labs(title = "Loan rates dropped 2pp after the 2008 crisis",
       subtitle = "Author-driven — one message: the crisis impact on rates",
       y = "Rate (pp)")

ggsave("output/ecar_dash_vs_story.png",
  p_ec_dash | p_ec_story, width = 14, height = 5, dpi = 300)

# ── 6. TRANSFORMATION CHECKLIST (printed) ────────────────
cat("\n── Transformation Checklist: Dashboard → Story Slide ──\n")
cat("1. Title: Descriptive → Declarative (state the finding)\n")
cat("2. Legend: Remove → Direct labels at line endpoints\n")
cat("3. Colour: All coloured → Grey+accent (one story line)\n")
cat("4. Gridlines: Visible → Minimal or none\n")
cat("5. Annotations: None → Callouts, arrows, % change labels\n")
cat("6. Data density: Show all → Show only the story\n")
cat("7. Interactivity: Filters/tooltips → None (static)\n")
cat("8. Subtitle: Metric description → Strategic implication\n")

cat("\n── All W07-M02 R outputs saved ──\n")
