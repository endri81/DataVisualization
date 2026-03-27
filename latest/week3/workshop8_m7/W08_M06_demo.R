# ============================================================
# Workshop 8 — Module 6: Dashboard Design Principles
# Integrated R Script — UNYT Tirana
# ============================================================
library(tidyverse); library(patchwork); dir.create("output", showWarnings = FALSE)

# ── LOAD DATA ────────────────────────────────────────────
nf <- read_csv("netflix.csv") |>
  mutate(date_added = mdy(str_trim(date_added)),
    year_added = year(date_added),
    primary_country = str_trim(str_extract(country, "^[^,]+")))

# ── GLOBAL PALETTE (Rule 4: Consistent Colour) ──────────
PALETTE <- c(Movie = "#1565C0", "TV Show" = "#E53935")

theme_dash <- theme_minimal(base_size = 9) +
  theme(panel.grid.major = element_line(color = "#F5F5F5"),
    panel.grid.minor = element_blank(),
    plot.title = element_text(face = "bold", size = 10),
    legend.position = "bottom",
    legend.text = element_text(size = 7))
theme_set(theme_dash)

# ══════════════════════════════════════════════════════════
# MOCKUP: Netflix Dashboard Layout (static version)
# Demonstrates the layout grid: KPI → Primary → Secondary → Detail
# ══════════════════════════════════════════════════════════

# ── KPI ROW (Rule 2) ────────────────────────────────────
total <- nrow(nf)
movies_n <- sum(nf$type == "Movie", na.rm = TRUE)
tvshows_n <- sum(nf$type == "TV Show", na.rm = TRUE)
countries_n <- n_distinct(nf$primary_country, na.rm = TRUE)

# KPI cards as mini-plots
make_kpi <- function(label, value, delta, color) {
  ggplot() +
    annotate("text", x = 0.5, y = 0.7,
      label = format(value, big.mark = ","),
      size = 8, fontface = "bold", color = color) +
    annotate("text", x = 0.5, y = 0.35,
      label = paste0(ifelse(delta >= 0, "+", ""), delta, "%"),
      size = 4, fontface = "bold",
      color = ifelse(delta >= 0, "#2E7D32", "#C62828")) +
    annotate("text", x = 0.5, y = 0.12, label = label,
      size = 3, color = "#888") +
    xlim(0, 1) + ylim(0, 1) + theme_void() +
    theme(panel.border = element_rect(color = "#EEEEEE", fill = NA))
}

kpi1 <- make_kpi("Total Titles", total, 12.3, "#333")
kpi2 <- make_kpi("Movies", movies_n, -5.2, "#1565C0")
kpi3 <- make_kpi("TV Shows", tvshows_n, 18.7, "#E53935")
kpi4 <- make_kpi("Countries", countries_n, 3.1, "#7B1FA2")

kpi_row <- kpi1 | kpi2 | kpi3 | kpi4

# ── PRIMARY CHART (Rule 3: largest, most important) ──────
yearly <- nf |>
  filter(!is.na(year_added), year_added >= 2015, year_added <= 2021) |>
  count(year_added, type)

p_primary <- ggplot(yearly, aes(x = year_added, y = n, color = type)) +
  geom_line(linewidth = 1.2) + geom_point(size = 2) +
  scale_color_manual(values = PALETTE) +
  labs(title = "Yearly Additions by Type",
       x = "Year", y = "Titles", color = NULL)

# ── SECONDARY CHART ──────────────────────────────────────
top10 <- nf |> filter(!is.na(primary_country)) |>
  count(primary_country, sort = TRUE) |> slice_max(n, n = 10) |>
  mutate(primary_country = fct_reorder(primary_country, n))

p_secondary <- ggplot(top10, aes(x = primary_country, y = n)) +
  geom_col(fill = "#1565C0", alpha = 0.7, width = 0.6) +
  coord_flip() +
  labs(title = "Top 10 Countries", x = NULL, y = "Titles")

# ── DETAIL ROW (3 small panels) ──────────────────────────
# Detail 1: Type split
type_pct <- nf |> count(type) |> mutate(pct = round(n / sum(n) * 100))
p_detail1 <- ggplot(type_pct, aes(x = type, y = pct, fill = type)) +
  geom_col(width = 0.5, show.legend = FALSE) +
  geom_text(aes(label = paste0(pct, "%")), vjust = -0.5, size = 3, fontface = "bold") +
  scale_fill_manual(values = PALETTE) +
  labs(title = "Type Split", x = NULL, y = "%")

# Detail 2: Rating distribution
p_detail2 <- nf |> filter(!is.na(rating)) |>
  count(rating, sort = TRUE) |> slice_max(n, n = 6) |>
  mutate(rating = fct_reorder(rating, n)) |>
  ggplot(aes(x = rating, y = n)) +
  geom_col(fill = "#2E7D32", alpha = 0.7, width = 0.5) +
  coord_flip() +
  labs(title = "Top Ratings", x = NULL, y = "Count")

# Detail 3: Monthly sparkline
monthly <- nf |>
  filter(!is.na(date_added), year(date_added) >= 2018) |>
  mutate(month = floor_date(date_added, "month")) |>
  count(month)
p_detail3 <- ggplot(monthly, aes(x = month, y = n)) +
  geom_line(color = "#1565C0", linewidth = 0.5) +
  geom_area(fill = "#1565C0", alpha = 0.05) +
  scale_x_date(date_labels = "%Y") +
  labs(title = "Monthly Trend (2018–2021)", x = NULL, y = "Titles")

# ── COMPOSE FULL DASHBOARD ───────────────────────────────
dashboard <- kpi_row /
  (p_primary | p_secondary) /
  (p_detail1 | p_detail2 | p_detail3) +
  plot_annotation(
    title = "Netflix Content Dashboard",
    subtitle = "Layout: KPI row → Primary + Secondary → Detail panels (Few's grid)",
    tag_levels = list(c("", "", "", "",
      "Primary", "Secondary", "Detail 1", "Detail 2", "Detail 3")))

ggsave("output/dashboard_mockup.png", dashboard, width = 14, height = 12, dpi = 300)

# ── ANTI-PATTERN: BAD DASHBOARD ──────────────────────────
# Deliberately violate all 6 rules
p_bad1 <- ggplot(yearly, aes(x = factor(year_added), y = n, fill = type)) +
  geom_col(position = "dodge", color = "black") +
  scale_fill_manual(values = c(Movie = "#FF6347", "TV Show" = "#32CD32")) + # wrong colours!
  theme_gray() + labs(title = "ANTI-PATTERN 1: Wrong colours + borders")

p_bad2 <- ggplot(yearly, aes(x = year_added, y = n, color = type)) +
  geom_line(linewidth = 1) +
  scale_color_manual(values = c(Movie = "#4169E1", "TV Show" = "#FFD700")) + # inconsistent!
  theme_gray() + labs(title = "ANTI-PATTERN 2: Different palette same data")

ggsave("output/anti_patterns.png",
  (p_bad1 | p_bad2) +
    plot_annotation(title = "Anti-Patterns: Colour Chaos (same data, different palettes per chart)"),
  width = 14, height = 5, dpi = 300)

# ── FEW'S RULES CHECKLIST ────────────────────────────────
cat("\n── Few's Dashboard Design Rules ──\n")
rules <- tibble(
  rule = 1:6,
  name = c("One screen", "KPIs at top", "5–7 charts max",
    "Consistent colour", "Filter sidebar", "Descriptive titles"),
  check = c(
    "No scrolling required?",
    "Big numbers visible in first 2 seconds?",
    "Count of charts ≤ 7?",
    "Same colour = same meaning across all panels?",
    "All inputs in sidebar or top bar (not inline)?",
    "Titles describe the metric (not the finding)?"))
print(rules, n = 6)

cat("\n── All W08-M06 R outputs saved ──\n")
