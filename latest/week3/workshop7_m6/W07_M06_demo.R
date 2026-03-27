# ============================================================
# Workshop 7 — Module 6: Declutter & Redesign
# Integrated R Script — UNYT Tirana
# ============================================================
library(tidyverse); library(patchwork); dir.create("output", showWarnings = FALSE)

# ── LOAD DATA ────────────────────────────────────────────
nf <- read_csv("netflix.csv") |>
  mutate(date_added = mdy(str_trim(date_added)), year_added = year(date_added))
yearly <- nf |> filter(!is.na(year_added), year_added >= 2016, year_added <= 2021) |>
  count(year_added, type)
movies <- yearly |> filter(type == "Movie")
tv <- yearly |> filter(type == "TV Show")

# ═══════════════════════════════════════════════════════
# 1. BEFORE: Maximum Clutter (deliberately bad)
# ═══════════════════════════════════════════════════════
p_before <- ggplot(yearly, aes(x = factor(year_added), y = n, fill = type)) +
  geom_col(position = "dodge", width = 0.7, color = "black", linewidth = 0.5) +
  geom_text(aes(label = n), position = position_dodge(0.7),
    vjust = -0.3, size = 2.5, angle = 90) +
  scale_fill_manual(values = c(Movie = "#4472C4", "TV Show" = "#ED7D31")) +
  theme_gray() +
  theme(
    panel.grid.major = element_line(color = "#CCCCCC"),
    panel.grid.minor = element_line(color = "#DDDDDD"),
    panel.border = element_rect(color = "black", fill = NA, linewidth = 2),
    legend.background = element_rect(fill = "white", color = "black"),
    legend.key = element_rect(fill = "white", color = "black"),
    plot.background = element_rect(fill = "#F5F5F5"),
    axis.text.x = element_text(angle = 45, hjust = 1)) +
  labs(title = "Netflix Additions by Type (2016-2021)",
       subtitle = "Showing the number of titles added per year by content type",
       x = "Year of Addition", y = "Number of Titles Added to the Platform",
       fill = "Content Type",
       caption = "Source: Netflix Dataset from Kaggle (Shivam Bansal, 2021). Data accessed March 2025. All rights reserved.")
ggsave("output/before_cluttered.png", p_before, width = 9, height = 6, dpi = 300)

# ═══════════════════════════════════════════════════════
# 2. AFTER: Decluttered (same data, maximum clarity)
# ═══════════════════════════════════════════════════════
decline <- round((1 - movies$n[movies$year_added == 2021] /
  max(movies$n)) * 100)

p_after <- ggplot(yearly, aes(x = year_added, y = n, group = type)) +
  geom_line(color = "#DDDDDD", linewidth = 0.8) +
  geom_line(data = movies, color = "#1565C0", linewidth = 2.5) +
  geom_point(data = movies, color = "#1565C0", size = 3) +
  # Callout
  annotate("label", x = 2018.5, y = movies$n[movies$year_added == 2021] * 0.82,
    label = paste0("–", decline, "%\nfrom peak"),
    size = 3.5, fontface = "bold", color = "#E53935",
    fill = "white", label.size = 0.4) +
  # Direct labels
  geom_text(data = yearly |> filter(year_added == 2021),
    aes(label = type, color = type == "Movie"),
    hjust = -0.1, size = 3.5, fontface = "bold", show.legend = FALSE) +
  scale_color_manual(values = c("TRUE" = "#1565C0", "FALSE" = "#BBB")) +
  coord_cartesian(xlim = c(2016, 2022.5)) +
  theme_minimal(base_size = 11) +
  theme(
    legend.position = "none",
    panel.grid = element_blank(),
    axis.line = element_line(color = "#EEEEEE", linewidth = 0.3),
    plot.title = element_text(face = "bold", size = 13),
    plot.subtitle = element_text(color = "#666", size = 10),
    axis.title.y = element_text(color = "#888")) +
  labs(title = paste0("Movie additions declined ", decline, "% from their 2019 peak"),
       subtitle = "TV Shows grew steadily but Movies — the larger category — contracted",
       x = NULL, y = "Titles Added")
ggsave("output/after_clean.png", p_after, width = 9, height = 5, dpi = 300)

# Side-by-side
ggsave("output/before_after_comparison.png",
  (p_before + labs(title = "BEFORE: 12 clutter elements")) |
  (p_after + labs(title = "AFTER: Decluttered")),
  width = 18, height = 6, dpi = 300)

# ═══════════════════════════════════════════════════════
# 3. THE 12-STEP TRANSFORMATION (annotated)
# ═══════════════════════════════════════════════════════
cat("\n── 12-Step Declutter Transformation ──\n")
steps <- tibble(
  step = 1:12,
  element = c("Chart type", "Title", "Legend", "Borders", "Gridlines", "Data labels",
    "Background", "Axis labels", "Colour", "Bar edges", "Source line", "Spines"),
  before = c("Grouped bar", "Descriptive", "Box with border", "Heavy black",
    "Both axes, grey", "On every bar", "Grey fill", "Verbose", "Two bright",
    "Black outlines", "Long, distracting", "All 4, thick"),
  after = c("Line (continuous)", "Declarative (= finding)", "Direct labels (no legend)",
    "Removed entirely", "Removed entirely", "Only the callout %",
    "White", "Minimal, muted", "Grey + one accent", "None (line chart)",
    "Removed", "Left + bottom, light #EEE"))
print(steps, n = 12)

# ═══════════════════════════════════════════════════════
# 4. CLEAN THEME TEMPLATE
# ═══════════════════════════════════════════════════════
theme_clean <- theme_minimal(base_size = 11) +
  theme(
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    axis.line = element_line(color = "#EEEEEE", linewidth = 0.3),
    plot.title = element_text(face = "bold", size = 14),
    plot.subtitle = element_text(color = "#666", size = 10),
    plot.caption = element_text(color = "#AAA", size = 7),
    legend.background = element_blank(),
    legend.key = element_blank(),
    axis.title = element_text(color = "#888"))

# Apply globally
theme_set(theme_clean)

# Demo: any plot now inherits the clean theme
p_demo <- ggplot(movies, aes(x = year_added, y = n)) +
  geom_line(color = "#1565C0", linewidth = 2) +
  geom_point(color = "#1565C0", size = 3) +
  labs(title = "With theme_set(theme_clean): every plot starts clean",
       subtitle = "No manual theme adjustments needed per chart",
       x = "Year", y = "Movies Added")
ggsave("output/theme_clean_demo.png", p_demo, width = 8, height = 4.5, dpi = 300)

# ═══════════════════════════════════════════════════════
# 5. e-Car MAKEOVER
# ═══════════════════════════════════════════════════════
ec <- read_csv("ecar.csv") |>
  mutate(Year = year(mdy(`Approve Date`)),
    Spread = Rate - `Cost of Funds`) |>
  filter(Year >= 2002, Year <= 2012)
yr_ec <- ec |> group_by(Year) |>
  summarise(rate = mean(Rate), spread = mean(Spread))

# Before: cluttered
p_ec_before <- ggplot(yr_ec) +
  geom_line(aes(x = Year, y = rate, linetype = "Rate"), color = "blue", linewidth = 1) +
  geom_line(aes(x = Year, y = spread, linetype = "Spread"), color = "red", linewidth = 1) +
  geom_point(aes(x = Year, y = rate), color = "blue", size = 3) +
  geom_point(aes(x = Year, y = spread), color = "red", size = 3) +
  scale_linetype_manual(values = c(Rate = "solid", Spread = "dashed")) +
  theme_gray() +
  theme(panel.border = element_rect(color = "black", fill = NA, linewidth = 1.5),
    panel.grid = element_line(color = "#CCC")) +
  labs(title = "e-Car Rate and Spread Over Time",
       x = "Year", y = "Value (%)", linetype = "Metric")

# After: clean
p_ec_after <- ggplot(yr_ec) +
  annotate("rect", xmin = 2007.5, xmax = 2009.5, ymin = -Inf, ymax = Inf,
    fill = "#E53935", alpha = 0.04) +
  geom_line(aes(x = Year, y = spread), color = "#DDDDDD", linewidth = 0.8) +
  geom_line(aes(x = Year, y = rate), color = "#1565C0", linewidth = 2.5) +
  geom_point(aes(x = Year, y = rate), color = "#1565C0", size = 2.5) +
  annotate("text", x = 2012.3, y = yr_ec$rate[yr_ec$Year == 2012],
    label = "Rate", color = "#1565C0", fontface = "bold", size = 3.5, hjust = 0) +
  annotate("text", x = 2012.3, y = yr_ec$spread[yr_ec$Year == 2012],
    label = "Spread", color = "#AAAAAA", size = 3, hjust = 0) +
  annotate("label", x = 2008, y = max(yr_ec$rate) * 0.92,
    label = "2008\ncrisis", size = 2.5, fontface = "bold",
    color = "#E53935", fill = "white", label.size = 0.4) +
  scale_x_continuous(limits = c(2002, 2013)) +
  labs(title = "Loan rates dropped 2pp after the 2008 financial crisis",
       subtitle = "Spread (grey) also compressed; shaded region = crisis window",
       x = NULL, y = "Percentage Points")
ggsave("output/ecar_before_after.png",
  (p_ec_before + labs(title = "BEFORE")) | (p_ec_after + labs(title = "AFTER")),
  width = 16, height = 5, dpi = 300)

# ═══════════════════════════════════════════════════════
# 6. INCREMENTAL DECLUTTER: 4 stages
# ═══════════════════════════════════════════════════════
p_stage0 <- p_before + labs(title = "Stage 0: Original (maximum clutter)")
p_stage1 <- ggplot(yearly, aes(x = factor(year_added), y = n, fill = type)) +
  geom_col(position = "dodge", width = 0.7) +
  scale_fill_manual(values = c(Movie = "#1565C0", "TV Show" = "#E53935")) +
  theme_minimal() + labs(title = "Stage 1: Remove borders, 3D, background", fill = NULL)
p_stage2 <- ggplot(yearly, aes(x = year_added, y = n, color = type)) +
  geom_line(linewidth = 1.2) + geom_point(size = 2) +
  scale_color_manual(values = c(Movie = "#1565C0", "TV Show" = "#E53935")) +
  theme_minimal() + theme(panel.grid = element_blank()) +
  labs(title = "Stage 2: Line chart, remove gridlines", color = NULL)
p_stage3 <- p_after + labs(title = "Stage 3: Grey+accent, direct labels, callout")

ggsave("output/incremental_declutter.png",
  (p_stage0 | p_stage1) / (p_stage2 | p_stage3) +
  plot_annotation(title = "Incremental Declutter: 4 Stages of Transformation"),
  width = 16, height = 10, dpi = 300)

cat("\n── All W07-M06 R outputs saved ──\n")
