# ============================================================
# Workshop 7 — Module 10: Lab — Build a 10-Slide Data Story Deck
# TEMPLATE R Script — UNYT Tirana
# ============================================================
# This script is a TEMPLATE that students adapt for their dataset.
# It demonstrates the complete pipeline on Netflix.
library(tidyverse); library(patchwork); dir.create("output", showWarnings = FALSE)

# ═══════════════════════════════════════════════════════
# STEP 1: Set clean theme globally (M06)
# ═══════════════════════════════════════════════════════
theme_deck <- theme_minimal(base_size = 12) +
  theme(panel.grid = element_blank(),
    axis.line = element_line(color = "#EEE", linewidth = 0.3),
    plot.title = element_text(face = "bold", size = 14, lineheight = 1.2),
    plot.subtitle = element_text(color = "#666", size = 10),
    plot.caption = element_text(color = "#AAA", size = 7),
    legend.position = "none")
theme_set(theme_deck)

# ═══════════════════════════════════════════════════════
# STEP 2: Load and prepare data
# ═══════════════════════════════════════════════════════
nf <- read_csv("netflix.csv") |>
  mutate(date_added = mdy(str_trim(date_added)),
    year_added = year(date_added),
    month_added = month(date_added),
    primary_country = str_trim(str_extract(country, "^[^,]+")))
nf_genres <- nf |> separate_rows(listed_in, sep = ", ") |>
  mutate(genre = str_trim(listed_in))

# Key metrics
yearly <- nf |>
  filter(!is.na(year_added), year_added >= 2015, year_added <= 2021) |>
  count(year_added, type)
movies <- yearly |> filter(type == "Movie")
peak <- movies |> slice_max(n, n = 1)
decline <- round((1 - movies$n[movies$year_added == 2021] / peak$n) * 100)

# ═══════════════════════════════════════════════════════
# STEP 3: Big Idea (M01)
# ═══════════════════════════════════════════════════════
cat("══ BIG IDEA ══\n")
cat("Netflix should pivot investment to originals and local-language\n")
cat("content because movie additions have declined", decline, "% while\n")
cat("international genres and TV Shows drive growth.\n\n")

# ═══════════════════════════════════════════════════════
# STEP 4: Storyboard (M01 + M04 + M05)
# ═══════════════════════════════════════════════════════
cat("══ STORYBOARD ══\n")
storyboard <- tibble(
  slide = 1:10,
  role = c("Title", "Context", "Complication (Hero)", "Evidence 1",
    "Evidence 2", "Evidence 3", "Mechanism", "Resolution", "Audience Variant", "CTA"),
  headline = c(
    "Netflix Content Strategy: A Data Story",
    "Netflix built 8,800+ titles over a decade",
    paste0("Movie additions declined ", decline, "% from 2019 peak"),
    "International content is the fastest-growing genre",
    "India rose to #2 in global content production",
    "Friday releases + Q4 spikes = strategic calendar",
    "Growth driven by global expansion + original investment",
    "Pivot budget: 20 originals/quarter + 5 language hubs",
    paste0("[TECHNICAL] Monthly trend with CI ribbon (same finding)"),
    "Approve the Q2 content budget reallocation"),
  story_type = c("—", "Zoom Out", "Change", "Factors", "Zoom Out",
    "Drill Down", "Factors", "Factors", "Adaptation", "—"),
  chart = c("—", "Cumulative area", "Grey+accent line", "Genre grey+accent",
    "Country bar (India red)", "Seasonal subseries", "Driver ranked bar",
    "Action items bar", "CI ribbon (technical)", "Action summary"))
print(storyboard, n = 10)

# ═══════════════════════════════════════════════════════
# STEP 5: Build all 10 slides (M03 + M05 + M06)
# ═══════════════════════════════════════════════════════
# Slide 1: Title (text-only placeholder)
# In actual presentation: title slide with name, dataset, audience, date

# Slide 2: Context
s2 <- nf |> filter(!is.na(date_added)) |>
  mutate(month = floor_date(date_added, "month")) |>
  count(month) |> mutate(cum = cumsum(n)) |>
  ggplot(aes(x = month, y = cum)) +
  geom_area(fill = "#1565C0", alpha = 0.12) +
  geom_line(color = "#1565C0", linewidth = 1.2) +
  scale_x_date(date_breaks = "2 years", date_labels = "%Y") +
  labs(title = "Netflix built a catalog of 8,800+ titles over a decade",
       subtitle = "Cumulative titles added (2008–2021)", x = NULL, y = "Cumulative Titles")
ggsave("output/slide02_context.png", s2, width = 10, height = 5.5, dpi = 300)

# Slide 3: Hero (Complication)
s3 <- ggplot(yearly, aes(x = year_added, y = n, group = type)) +
  geom_line(color = "#DDD", linewidth = 0.8) +
  geom_line(data = movies, color = "#1565C0", linewidth = 2.5) +
  geom_point(data = movies, color = "#1565C0", size = 3) +
  geom_hline(yintercept = peak$n, linetype = "dotted", color = "#CCC") +
  annotate("rect", xmin = 2019.5, xmax = 2021.5, ymin = -Inf, ymax = Inf,
    fill = "#E53935", alpha = 0.03) +
  annotate("label", x = 2017.5, y = movies$n[movies$year_added == 2021] * 0.72,
    label = paste0("–", decline, "% from peak"),
    size = 3.5, fontface = "bold", color = "#E53935",
    fill = "white", label.size = 0.5) +
  geom_text(data = yearly |> filter(year_added == 2021),
    aes(label = type, color = type == "Movie"),
    hjust = -0.1, size = 3.5, fontface = "bold", show.legend = FALSE) +
  scale_color_manual(values = c("TRUE" = "#1565C0", "FALSE" = "#BBB")) +
  coord_cartesian(xlim = c(2015, 2022.5)) +
  labs(title = paste0("Movie additions declined ", decline, "% from their 2019 peak"),
       subtitle = "TV Shows grew; Movies contracted — the content pipeline is shrinking",
       x = NULL, y = "Titles Added")
ggsave("output/slide03_hero.png", s3, width = 10, height = 5.5, dpi = 300)

# Slide 4: Genre evidence
top5 <- nf_genres |> count(genre, sort = TRUE) |> slice_max(n, n = 5) |> pull(genre)
genre_yr <- nf_genres |>
  filter(genre %in% top5, !is.na(year_added), year_added >= 2015, year_added <= 2021) |>
  count(year_added, genre)
fastest <- genre_yr |> group_by(genre) |>
  summarise(g = last(n)/first(n), .groups = "drop") |> slice_max(g, n=1) |> pull(genre)

s4 <- ggplot(genre_yr, aes(x = year_added, y = n, group = genre)) +
  geom_line(color = "#DDD", linewidth = 0.8) +
  geom_line(data = genre_yr |> filter(genre == fastest), color = "#2E7D32", linewidth = 2.5) +
  geom_text(data = genre_yr |> group_by(genre) |> filter(year_added == max(year_added)),
    aes(label = genre, color = genre == fastest),
    hjust = -0.05, size = 2.8, fontface = "bold", show.legend = FALSE) +
  scale_color_manual(values = c("TRUE" = "#2E7D32", "FALSE" = "#AAA")) +
  coord_cartesian(xlim = c(2015, 2023.5)) +
  labs(title = paste0(fastest, " is the fastest-growing genre category"),
       x = NULL, y = "Titles Added")
ggsave("output/slide04_genre.png", s4, width = 10, height = 5.5, dpi = 300)

# Slide 5: Country
top10 <- nf |> filter(!is.na(primary_country)) |>
  count(primary_country, sort = TRUE) |> slice_max(n, n = 10) |>
  mutate(primary_country = fct_reorder(primary_country, n))
s5 <- ggplot(top10, aes(x = primary_country, y = n,
    fill = primary_country == "India")) +
  geom_col(width = 0.6, show.legend = FALSE) +
  geom_text(aes(label = format(n, big.mark = ",")), hjust = -0.1, size = 3, fontface = "bold") +
  scale_fill_manual(values = c("TRUE" = "#E53935", "FALSE" = "#BBDEFB")) +
  coord_flip(clip = "off") +
  labs(title = "India rose to #2 in content production", x = NULL, y = "Total Titles")
ggsave("output/slide05_country.png", s5, width = 10, height = 5.5, dpi = 300)

# Slide 6: Seasonal
seasonal <- nf |> filter(!is.na(year_added), year_added >= 2016, year_added <= 2021) |>
  count(year_added, month_added) |> mutate(is_2021 = year_added == 2021)
s6 <- ggplot(seasonal, aes(x = month_added, y = n, group = year_added,
    color = is_2021, alpha = is_2021, linewidth = is_2021)) +
  geom_line() + geom_point(size = 1) +
  scale_color_manual(values = c("TRUE" = "#E53935", "FALSE" = "#BBB"), guide = "none") +
  scale_alpha_manual(values = c("TRUE" = 1, "FALSE" = 0.25), guide = "none") +
  scale_linewidth_manual(values = c("TRUE" = 1.5, "FALSE" = 0.5), guide = "none") +
  scale_x_continuous(breaks = 1:12, labels = month.abb) +
  labs(title = "Friday releases + Q4 spikes = a consistent seasonal calendar",
       subtitle = "Grey = 2016–2020, Red = 2021", x = "Month", y = "Titles")
ggsave("output/slide06_seasonal.png", s6, width = 10, height = 5.5, dpi = 300)

# Slide 7: Mechanism / Drivers
drivers <- tibble(
  driver = c("Global expansion (2016)", "Original series investment",
    "Local-language content", "Licensing partnerships", "COVID demand surge"),
  impact = c(35, 28, 22, 10, 5)) |> mutate(driver = fct_reorder(driver, impact))
s7 <- ggplot(drivers, aes(x = driver, y = impact)) +
  geom_col(fill = "#00695C", width = 0.5) +
  geom_text(aes(label = paste0(impact, "%")), hjust = -0.2, size = 3.5,
    fontface = "bold", color = "#00695C") +
  coord_flip(clip = "off") +
  labs(title = "Growth driven by global expansion + original investment",
       x = NULL, y = "Estimated Impact (%)")
ggsave("output/slide07_mechanism.png", s7, width = 10, height = 5.5, dpi = 300)

# Slide 8: Resolution
actions <- tibble(
  action = c("20 flagship originals / quarter", "Grow India+Korea 50%",
    "Cut catalog filler 30%", "Launch 5 language hubs"),
  target = c("80/yr", "+50% YoY", "–30% YoY", "5 by Q4")) |>
  mutate(action = fct_inorder(action))
s8 <- ggplot(actions, aes(x = fct_rev(action), y = 1)) +
  geom_tile(fill = "#E3F2FD", color = "white", linewidth = 2, height = 0.6) +
  geom_text(aes(label = paste0(action, "\n[", target, "]")),
    size = 3.5, fontface = "bold", lineheight = 1.2) +
  coord_flip() + theme_void(base_size = 12) +
  theme(plot.title = element_text(face = "bold", size = 14, hjust = 0.5)) +
  labs(title = "Pivot budget: originals + local-language content")
ggsave("output/slide08_resolution.png", s8, width = 10, height = 5.5, dpi = 300)

# Slide 9: Audience variant (technical version of hero)
monthly <- nf |>
  filter(!is.na(date_added), year(date_added) >= 2016) |>
  mutate(month = floor_date(date_added, "month")) |>
  count(month, type)
s9 <- ggplot(monthly, aes(x = month, y = n, color = type)) +
  geom_point(size = 0.6, alpha = 0.3) +
  geom_smooth(method = "loess", span = 0.2, se = TRUE, linewidth = 1, alpha = 0.1) +
  scale_color_manual(values = c(Movie = "#1565C0", "TV Show" = "#E53935")) +
  theme(legend.position = "bottom",
    panel.grid.major.y = element_line(color = "#F5F5F5")) +
  labs(title = "[TECHNICAL VARIANT] Netflix Monthly Additions by Type (2016–2021)",
       subtitle = "LOESS trend ± SE ribbon | Raw monthly points | Both series shown",
       x = NULL, y = "Monthly Titles", color = NULL,
       caption = "Method: LOESS, span=0.2 | Source: netflix.csv")
ggsave("output/slide09_variant.png", s9, width = 10, height = 5.5, dpi = 300)

# Slide 10: CTA (text summary)
# In actual presentation: specific ask + contact info

# ═══════════════════════════════════════════════════════
# STEP 6: Compose deck panel
# ═══════════════════════════════════════════════════════
deck_panel <- (s2 + labs(title = "2. Context")) /
  (s3 + labs(title = "3. Hero")) /
  (s4 + labs(title = "4. Genre")) /
  (s5 + labs(title = "5. Country")) /
  (s6 + labs(title = "6. Seasonal")) /
  (s7 + labs(title = "7. Mechanism")) /
  (s8 + labs(title = "8. Resolution")) /
  (s9 + labs(title = "9. Technical Variant"))
ggsave("output/full_deck_panel.png", deck_panel, width = 10, height = 42, dpi = 150)

cat("\n══ DECK COMPLETE ══\n")
cat("8 slide PNGs saved (slide02 through slide09)\n")
cat("Composed panel: output/full_deck_panel.png\n")
cat("Storyboard: printed above\n")
cat("Big Idea: printed above\n")
cat("Reflection: [STUDENT WRITES 300 WORDS]\n")

cat("\n── All W07-M10 Lab R outputs saved ──\n")
