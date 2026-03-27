# ============================================================
# Workshop 7 — Module 5: Assertion-Evidence Slide Design
# Integrated R Script — UNYT Tirana
# ============================================================
library(tidyverse); library(patchwork); dir.create("output", showWarnings = FALSE)

# ── LOAD DATA ────────────────────────────────────────────
nf <- read_csv("netflix.csv") |>
  mutate(date_added = mdy(str_trim(date_added)),
    year_added = year(date_added),
    primary_country = str_trim(str_extract(country, "^[^,]+")))
nf_genres <- nf |> separate_rows(listed_in, sep = ", ") |> mutate(genre = str_trim(listed_in))

# ═══════════════════════════════════════════════════════
# EXAMPLE: 5-SLIDE ASSERTION-EVIDENCE DECK (Netflix)
# Each "slide" = declarative title + one focused chart
# ═══════════════════════════════════════════════════════

# ── SLIDE 1 (Context): ──────────────────────────────────
p_s1 <- nf |>
  filter(!is.na(date_added)) |>
  mutate(month = floor_date(date_added, "month")) |>
  count(month) |> mutate(cum = cumsum(n)) |>
  ggplot(aes(x = month, y = cum)) +
  geom_area(fill = "#1565C0", alpha = 0.15) +
  geom_line(color = "#1565C0", linewidth = 1.2) +
  scale_x_date(date_breaks = "2 years", date_labels = "%Y") +
  theme_minimal(base_size = 12) +
  theme(plot.title = element_text(face = "bold", size = 14),
    plot.subtitle = element_text(color = "#666", size = 10)) +
  labs(title = "Netflix built a catalog of 8,800+ titles over a decade",
       subtitle = "Cumulative titles added to the platform (2008–2021)",
       x = NULL, y = "Cumulative Titles")
ggsave("output/slide1_context.png", p_s1, width = 10, height = 5.5, dpi = 300)

# ── SLIDE 2 (Complication): ─────────────────────────────
yearly_type <- nf |>
  filter(!is.na(year_added), year_added >= 2015, year_added <= 2021) |>
  count(year_added, type)
movies <- yearly_type |> filter(type == "Movie")
peak <- movies |> slice_max(n, n = 1)
decline <- round((1 - movies$n[movies$year_added == 2021] / peak$n) * 100)

p_s2 <- ggplot(yearly_type, aes(x = year_added, y = n, group = type)) +
  geom_line(color = "#DDDDDD", linewidth = 0.8) +
  geom_line(data = movies, color = "#1565C0", linewidth = 2.5) +
  geom_point(data = movies, color = "#1565C0", size = 3) +
  annotate("label", x = 2018.5, y = movies$n[movies$year_added == 2021] * 0.85,
    label = paste0("–", decline, "% from peak"),
    size = 4, fontface = "bold", color = "#E53935", fill = "white", label.size = 0.5) +
  geom_text(data = yearly_type |> filter(year_added == 2021),
    aes(label = type, color = type == "Movie"),
    hjust = -0.1, size = 3.5, fontface = "bold", show.legend = FALSE) +
  scale_color_manual(values = c("TRUE" = "#1565C0", "FALSE" = "#BBB")) +
  coord_cartesian(xlim = c(2015, 2022.5)) +
  theme_minimal(base_size = 12) +
  theme(legend.position = "none",
    plot.title = element_text(face = "bold", size = 14),
    plot.subtitle = element_text(color = "#666", size = 10)) +
  labs(title = paste0("But movie additions declined ", decline, "% from their 2019 peak"),
       subtitle = "TV Show additions grew steadily; Movies — the larger category — contracted",
       x = NULL, y = "Titles Added")
ggsave("output/slide2_complication.png", p_s2, width = 10, height = 5.5, dpi = 300)

# ── SLIDE 3 (Analysis): ─────────────────────────────────
top5 <- nf_genres |> count(genre, sort = TRUE) |> slice_max(n, n = 5) |> pull(genre)
genre_yr <- nf_genres |>
  filter(genre %in% top5, !is.na(year_added), year_added >= 2015, year_added <= 2021) |>
  count(year_added, genre)
fastest <- genre_yr |> group_by(genre) |>
  summarise(growth = last(n) / first(n), .groups = "drop") |>
  slice_max(growth, n = 1) |> pull(genre)

p_s3 <- ggplot(genre_yr, aes(x = year_added, y = n, group = genre)) +
  geom_line(color = "#DDDDDD", linewidth = 0.8) +
  geom_line(data = genre_yr |> filter(genre == fastest),
    color = "#2E7D32", linewidth = 2.5) +
  geom_text(data = genre_yr |> group_by(genre) |> filter(year_added == max(year_added)),
    aes(label = genre, color = genre == fastest),
    hjust = -0.05, size = 3, fontface = "bold", show.legend = FALSE) +
  scale_color_manual(values = c("TRUE" = "#2E7D32", "FALSE" = "#AAA")) +
  coord_cartesian(xlim = c(2015, 2023.5)) +
  theme_minimal(base_size = 12) +
  theme(legend.position = "none",
    plot.title = element_text(face = "bold", size = 14),
    plot.subtitle = element_text(color = "#666", size = 10)) +
  labs(title = paste0(fastest, " is the fastest-growing genre category"),
       subtitle = "Grey = other top genres | Green = fastest relative growth (2015–2021)",
       x = NULL, y = "Titles Added")
ggsave("output/slide3_analysis.png", p_s3, width = 10, height = 5.5, dpi = 300)

# ── SLIDE 4 (Resolution): ───────────────────────────────
country_cum <- nf |>
  filter(!is.na(primary_country), !is.na(year_added), year_added >= 2016, year_added <= 2021) |>
  count(year_added, primary_country) |>
  group_by(primary_country) |> arrange(year_added) |> mutate(cum = cumsum(n)) |> ungroup()
top10 <- country_cum |> filter(year_added == 2021) |> slice_max(cum, n = 10) |>
  mutate(primary_country = fct_reorder(primary_country, cum))

p_s4 <- ggplot(top10, aes(x = primary_country, y = cum, fill = primary_country == "India")) +
  geom_col(width = 0.6, show.legend = FALSE) +
  geom_text(aes(label = format(cum, big.mark = ",")),
    hjust = -0.1, size = 3, fontface = "bold") +
  scale_fill_manual(values = c("TRUE" = "#E53935", "FALSE" = "#BBDEFB")) +
  coord_flip(clip = "off") +
  theme_minimal(base_size = 12) +
  theme(plot.title = element_text(face = "bold", size = 14),
    plot.subtitle = element_text(color = "#666", size = 10),
    plot.margin = margin(5, 40, 5, 5)) +
  labs(title = "India rose to #2 in content production — invest in local-language content",
       subtitle = "Cumulative Netflix titles by country of origin (2016–2021)",
       x = NULL, y = "Cumulative Titles")
ggsave("output/slide4_resolution.png", p_s4, width = 10, height = 5.5, dpi = 300)

# ── SLIDE 5 (Call to Action): ────────────────────────────
# For CTA slides, a summary table or key metrics work well
action_data <- tibble(
  action = c("Invest in 20 flagship originals/quarter",
    "Grow Indian & Korean production 50%",
    "Reduce catalog filler acquisitions 30%",
    "Launch 5 local-language hubs"),
  metric = c("Original count", "India + Korea titles", "Licensed acquisitions", "Language hubs"),
  target = c("80/year", "+50% YoY", "–30% YoY", "5 by Q4"))

p_s5 <- ggplot(action_data, aes(x = fct_inorder(action), y = 1)) +
  geom_tile(fill = "#E3F2FD", color = "white", linewidth = 2, height = 0.6) +
  geom_text(aes(label = paste0(action, "\n[Target: ", target, "]")),
    size = 3.5, fontface = "bold", lineheight = 1.2) +
  coord_flip() +
  theme_void(base_size = 12) +
  theme(plot.title = element_text(face = "bold", size = 14, hjust = 0.5),
    plot.subtitle = element_text(color = "#666", size = 10, hjust = 0.5)) +
  labs(title = "Recommendation: Reallocate content budget toward originals and local markets",
       subtitle = "Four strategic actions with measurable targets")
ggsave("output/slide5_cta.png", p_s5, width = 10, height = 5.5, dpi = 300)

# ── COMPOSE 5-SLIDE DECK AS PANEL ────────────────────────
deck <- (p_s1 + labs(title = "1. Context")) /
  (p_s2 + labs(title = paste0("2. Complication: –", decline, "% movie decline"))) /
  (p_s3 + labs(title = paste0("3. Analysis: ", fastest, " leads"))) /
  (p_s4 + labs(title = "4. Resolution: India #2")) /
  (p_s5 + labs(title = "5. Call to Action"))
# Note: this will be very tall; save as reference only
ggsave("output/deck_5slides.png", deck, width = 10, height = 28, dpi = 200)

# ── PROGRESSIVE REVEAL DEMO ─────────────────────────────
# Build 1: axes only
p_build1 <- ggplot(movies, aes(x = year_added, y = n)) +
  scale_x_continuous(limits = c(2015, 2021)) +
  scale_y_continuous(limits = c(0, max(movies$n) * 1.1)) +
  theme_minimal(base_size = 8) +
  labs(title = "Build 1: Frame (axes only)", x = "Year", y = "Movies Added")

# Build 2: + data
p_build2 <- p_build1 +
  geom_line(color = "#1565C0", linewidth = 2) +
  geom_point(color = "#1565C0", size = 3) +
  labs(title = "Build 2: + Data line")

# Build 3: + annotation
p_build3 <- p_build2 +
  geom_hline(yintercept = peak$n, linetype = "dotted", color = "#888") +
  annotate("label", x = 2018.5, y = movies$n[movies$year_added == 2021] * 0.85,
    label = paste0("–", decline, "% decline"),
    size = 3, fontface = "bold", color = "#E53935", fill = "white", label.size = 0.4) +
  labs(title = "Build 3: + Annotation (peak reference + callout)")

# Build 4: + assertion title
p_build4 <- p_build3 +
  labs(title = paste0("Build 4: + Assertion: 'Movies declined ", decline, "%'"))

ggsave("output/progressive_reveal.png",
  (p_build1 | p_build2) / (p_build3 | p_build4) +
  plot_annotation(title = "Progressive Reveal: Build the Slide in 4 Steps"),
  width = 12, height = 8, dpi = 300)

cat("\n── All W07-M05 R outputs saved ──\n")
cat("Figures: slide1-5 individual, deck_5slides, progressive_reveal\n")
