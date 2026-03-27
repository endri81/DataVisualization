# ============================================================
# Workshop 7 — Module 3: Advanced Annotation in Code
# Integrated R Script — UNYT Tirana
# ============================================================
library(tidyverse); library(patchwork); dir.create("output", showWarnings = FALSE)

# ── 1. LOAD DATA ────────────────────────────────────────
nf <- read_csv("netflix.csv") |>
  mutate(date_added = mdy(str_trim(date_added)),
    year_added = year(date_added),
    primary_country = str_trim(str_extract(country, "^[^,]+")))

# ── 2. ggrepel: NON-OVERLAPPING SCATTER LABELS ──────────
library(ggrepel)

top_countries <- nf |>
  filter(!is.na(primary_country), !is.na(year_added),
    year_added >= 2015, year_added <= 2021) |>
  count(primary_country, sort = TRUE) |>
  slice_max(n, n = 15)

p_repel <- ggplot(top_countries,
  aes(x = fct_reorder(primary_country, n), y = n, label = primary_country)) +
  geom_point(color = "#1565C0", size = 3) +
  geom_text_repel(size = 3, max.overlaps = 20,
    segment.color = "#888", segment.size = 0.3,
    box.padding = 0.4, force = 2, seed = 42,
    color = "#333", fontface = "bold") +
  coord_flip() +
  theme_minimal() +
  labs(title = "ggrepel: Auto-positioned, non-overlapping labels",
       subtitle = "15 countries — no manual positioning needed",
       x = NULL, y = "Total Titles (2015–2021)")
ggsave("output/ggrepel_scatter.png", p_repel, width = 9, height = 6, dpi = 300)

# ── 3. ggrepel ON TIME SERIES: Label endpoints ──────────
nf_genres <- nf |> separate_rows(listed_in, sep = ", ") |>
  mutate(genre = str_trim(listed_in))
top5 <- nf_genres |> count(genre, sort = TRUE) |> slice_max(n, n = 5) |> pull(genre)

genre_yearly <- nf_genres |>
  filter(genre %in% top5, !is.na(year_added), year_added >= 2016, year_added <= 2021) |>
  count(year_added, genre)

endpoints <- genre_yearly |>
  group_by(genre) |> filter(year_added == max(year_added))

p_repel_ts <- ggplot(genre_yearly, aes(x = year_added, y = n, color = genre)) +
  geom_line(linewidth = 1) +
  geom_point(data = endpoints, size = 2.5) +
  geom_text_repel(data = endpoints,
    aes(label = genre), direction = "y",
    nudge_x = 0.3, segment.size = 0.3,
    size = 3, fontface = "bold",
    hjust = 0, seed = 42) +
  scale_color_brewer(palette = "Set2") +
  coord_cartesian(xlim = c(2016, 2023)) +
  theme_minimal() +
  theme(legend.position = "none") +
  labs(title = "ggrepel on time series: direct labels at endpoints",
       subtitle = "Replaces legend — labels placed automatically without overlap",
       x = "Year", y = "Titles Added")
ggsave("output/ggrepel_timeseries.png", p_repel_ts, width = 10, height = 5, dpi = 300)

# ── 4. ggtext: MARKDOWN IN TITLES ────────────────────────
# Note: requires ggtext installed
# library(ggtext)
# For demonstration, we simulate the effect with standard theme
yearly_type <- nf |>
  filter(!is.na(year_added), year_added >= 2015, year_added <= 2021) |>
  count(year_added, type)

# Standard version (no ggtext)
p_title <- ggplot(yearly_type, aes(x = year_added, y = n, color = type)) +
  geom_line(linewidth = 1.5) + geom_point(size = 3) +
  scale_color_manual(values = c(Movie = "#1565C0", "TV Show" = "#E53935")) +
  theme_minimal() + theme(legend.position = "none") +
  labs(title = "Movies (blue) peaked in 2019; TV Shows (red) grew steadily",
       subtitle = "With ggtext: title words coloured to match — no legend needed")

# ggtext version (uncomment if installed)
# p_title_md <- ggplot(yearly_type, aes(x = year_added, y = n, color = type)) +
#   geom_line(linewidth = 1.5) + geom_point(size = 3) +
#   scale_color_manual(values = c(Movie = "#1565C0", "TV Show" = "#E53935")) +
#   labs(title = "**<span style='color:#1565C0'>Movies</span>** peaked in 2019;
#     **<span style='color:#E53935'>TV Shows</span>** grew steadily") +
#   theme_minimal() +
#   theme(plot.title = element_markdown(size = 14), legend.position = "none")

ggsave("output/ggtext_title.png", p_title, width = 9, height = 5, dpi = 300)

# ── 5. FULL CALLOUT ANNOTATION ───────────────────────────
movies_yr <- yearly_type |> filter(type == "Movie")
peak <- movies_yr |> slice_max(n, n = 1)
latest <- movies_yr |> filter(year_added == 2021)
decline_pct <- round((1 - latest$n / peak$n) * 100)

p_callout <- ggplot(yearly_type, aes(x = year_added, y = n, group = type)) +
  # Grey context
  geom_line(color = "#DDDDDD", linewidth = 0.8) +
  geom_line(data = movies_yr, color = "#1565C0", linewidth = 2.5) +
  geom_point(data = movies_yr, color = "#1565C0", size = 3) +
  # Reference line at peak
  geom_hline(yintercept = peak$n, linetype = "dotted", color = "#888") +
  # Shaded crisis region
  annotate("rect", xmin = 2019.5, xmax = 2021.5, ymin = -Inf, ymax = Inf,
    fill = "#E53935", alpha = 0.03) +
  # Callout box with arrow
  annotate("label",
    x = 2018, y = latest$n,
    label = paste0(decline_pct, "% decline\nfrom 2019 peak"),
    size = 3.5, fontface = "bold", color = "#E53935",
    fill = "white", label.size = 0.5) +
  annotate("segment", x = 2018.8, xend = 2020, y = latest$n, yend = latest$n + 20,
    arrow = arrow(length = unit(0.15, "cm")), color = "#E53935") +
  # Direct labels (no legend)
  geom_text(data = yearly_type |> filter(year_added == 2021),
    aes(label = type, color = type == "Movie"),
    hjust = -0.15, size = 3, fontface = "bold", show.legend = FALSE) +
  scale_color_manual(values = c("TRUE" = "#1565C0", "FALSE" = "#BBBBBB")) +
  coord_cartesian(xlim = c(2015, 2022.5)) +
  theme_minimal(base_size = 11) +
  theme(legend.position = "none",
    plot.title = element_text(face = "bold", size = 13)) +
  labs(title = paste0("Movie additions declined ", decline_pct, "% from their 2019 peak"),
       subtitle = "Shaded region marks the decline period | Dotted line = peak level",
       x = NULL, y = "Titles Added",
       caption = "Source: Netflix dataset | UNYT")
ggsave("output/fully_dressed.png", p_callout, width = 10, height = 6, dpi = 300)

# ── 6. e-Car: ANNOTATED CRISIS CHART ────────────────────
ec <- read_csv("ecar.csv") |>
  mutate(Year = year(mdy(`Approve Date`)),
    Spread = Rate - `Cost of Funds`) |>
  filter(Year >= 2002, Year <= 2012)
yearly_ec <- ec |> group_by(Year) |>
  summarise(rate = mean(Rate), spread = mean(Spread))

p_ecar_ann <- ggplot(yearly_ec) +
  # Shaded crisis window
  annotate("rect", xmin = 2007.5, xmax = 2009.5, ymin = -Inf, ymax = Inf,
    fill = "#E53935", alpha = 0.05) +
  # Lines
  geom_line(aes(x = Year, y = spread), color = "#DDDDDD", linewidth = 0.8) +
  geom_line(aes(x = Year, y = rate), color = "#1565C0", linewidth = 2.5) +
  geom_point(aes(x = Year, y = rate), color = "#1565C0", size = 2.5) +
  # Callout: Lehman
  annotate("label", x = 2008, y = max(yearly_ec$rate) * 0.95,
    label = "Lehman Brothers\ncollapse (Sep 2008)",
    size = 2.5, fontface = "bold", color = "#E53935",
    fill = "white", label.size = 0.5) +
  annotate("segment", x = 2008, xend = 2008,
    y = max(yearly_ec$rate) * 0.88, yend = yearly_ec$rate[yearly_ec$Year == 2008],
    arrow = arrow(length = unit(0.15, "cm")), color = "#E53935") +
  # Direct labels
  annotate("text", x = 2012.3, y = yearly_ec$rate[yearly_ec$Year == 2012],
    label = "Rate", color = "#1565C0", fontface = "bold", size = 3.5, hjust = 0) +
  annotate("text", x = 2012.3, y = yearly_ec$spread[yearly_ec$Year == 2012],
    label = "Spread", color = "#AAAAAA", size = 3, hjust = 0) +
  # Reference lines
  geom_hline(yintercept = 0, linetype = "solid", color = "#888", linewidth = 0.3) +
  scale_x_continuous(breaks = 2002:2012, limits = c(2002, 2013)) +
  theme_minimal(base_size = 10) +
  theme(legend.position = "none",
    plot.title = element_text(face = "bold", size = 12)) +
  labs(title = "Loan rates dropped 2pp after the 2008 financial crisis",
       subtitle = "Shaded region = crisis window | Rate recovered partially by 2012",
       x = NULL, y = "Percentage Points",
       caption = "Source: e-Car dataset | UNYT")
ggsave("output/ecar_annotated.png", p_ecar_ann, width = 10, height = 5, dpi = 300)

# ── 7. ANNOTATION HIERARCHY COMPARISON ───────────────────
# Layer 0: bare chart
p_bare <- ggplot(movies_yr, aes(x = year_added, y = n)) +
  geom_line(color = "#1565C0", linewidth = 1) + geom_point(color = "#1565C0", size = 2) +
  theme_minimal(base_size = 8) +
  labs(title = "Layer 0: Bare chart\n(no annotation)")

# Layer 1: + reference line
p_ref <- p_bare +
  geom_hline(yintercept = peak$n, linetype = "dotted", color = "#888") +
  labs(title = "Layer 1: + Reference line\n(peak level)")

# Layer 2: + direct label
p_label <- p_ref +
  annotate("text", x = 2021.2, y = latest$n, label = "Movies",
    color = "#1565C0", fontface = "bold", size = 3, hjust = 0) +
  labs(title = "Layer 2: + Direct label")

# Layer 3: + callout
p_full <- p_label +
  annotate("label", x = 2018, y = latest$n * 0.85,
    label = paste0("–", decline_pct, "%"), size = 3, fontface = "bold",
    color = "#E53935", fill = "white", label.size = 0.4) +
  labs(title = "Layer 3: + Callout box")

ggsave("output/annotation_layers.png",
  (p_bare | p_ref) / (p_label | p_full) +
  plot_annotation(title = "Annotation Hierarchy: Build in Layers"),
  width = 12, height = 8, dpi = 300)

cat("\n── All W07-M03 R outputs saved ──\n")
