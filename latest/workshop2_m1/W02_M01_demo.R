# ============================================================
# Workshop 2 — Module 1: Wilkinson's Grammar of Graphics
# R Demonstration Script
# Data Visualization for Data Scientists — UNYT Tirana
# ============================================================

library(tidyverse)
library(patchwork)
dir.create("output", showWarnings = FALSE)


# ── 1. SAME DATA, THREE GEOMETRIES ────────────────────────
# Demonstrate: changing geom changes the chart, not the mapping

daily_sales <- tibble(
  day   = factor(c("Mon","Tue","Wed","Thu","Fri","Sat","Sun"),
                 levels = c("Mon","Tue","Wed","Thu","Fri","Sat","Sun")),
  sales = c(23, 45, 31, 58, 40, 52, 35)
)

# Base mapping (shared across all three)
base_map <- ggplot(daily_sales, aes(x = day, y = sales))

# geom_col (bar chart)
p_bar <- base_map +
  geom_col(fill = "#1565C0", width = 0.55) +
  labs(title = "geom_col()") +
  theme_minimal(base_size = 9) +
  theme(panel.grid.major.x = element_blank())

# geom_line (line chart)
p_line <- base_map +
  geom_line(group = 1, color = "#2E7D32", linewidth = 1.2) +
  geom_point(color = "#2E7D32", size = 2.5) +
  labs(title = "geom_line()") +
  theme_minimal(base_size = 9)

# geom_point (dot plot)
p_dot <- base_map +
  geom_point(color = "#E53935", size = 3) +
  labs(title = "geom_point()") +
  theme_minimal(base_size = 9)

p_three_geoms <- p_bar + p_line + p_dot +
  plot_annotation(
    title = "Same Data + Same Aesthetics, Different Geometry",
    subtitle = "aes(x = day, y = sales) — only the geom changes"
  )

print(p_three_geoms)
ggsave("output/three_geoms.png", p_three_geoms, width = 12, height = 4, dpi = 300)


# ── 2. LAYERED CONSTRUCTION — building up a ggplot ────────
# Show four progressive stages using the mpg dataset

# Stage 1: data + aesthetics only (empty canvas with axes)
p1 <- ggplot(mpg, aes(x = displ, y = hwy)) +
  labs(title = "1. Data + aes()") +
  theme_minimal(base_size = 8)

# Stage 2: + geometry
p2 <- ggplot(mpg, aes(x = displ, y = hwy)) +
  geom_point(alpha = 0.4, size = 1.5) +
  labs(title = "2. + geom_point()") +
  theme_minimal(base_size = 8)

# Stage 3: + statistic (smooth)
p3 <- ggplot(mpg, aes(x = displ, y = hwy)) +
  geom_point(alpha = 0.4, size = 1.5) +
  geom_smooth(method = "lm", color = "#E53935", se = TRUE) +
  labs(title = "3. + geom_smooth()") +
  theme_minimal(base_size = 8)

# Stage 4: + colour aesthetic + labels + theme
p4 <- ggplot(mpg, aes(x = displ, y = hwy, color = class)) +
  geom_point(alpha = 0.6, size = 1.5) +
  geom_smooth(method = "lm", se = TRUE, color = "grey40") +
  scale_color_brewer(palette = "Set2") +
  labs(title = "4. + aes(color) + labs() + theme",
       x = "Displacement (L)", y = "Highway MPG",
       color = "Vehicle Class") +
  theme_minimal(base_size = 8)

p_layered <- (p1 | p2) / (p3 | p4) +
  plot_annotation(title = "Layered Construction: Each + Adds a Component")

print(p_layered)
ggsave("output/layered_construction.png", p_layered, width = 10, height = 7, dpi = 300)


# ── 3. SAME DATA, DIFFERENT AESTHETIC STRATEGY ────────────
# Color vs Faceting for the same grouping variable

set.seed(42)
df_groups <- tibble(
  x = rnorm(150),
  y = rnorm(150),
  group = rep(c("A", "B", "C"), each = 50)
)

# Strategy A: color encodes group
p_color <- ggplot(df_groups, aes(x = x, y = y, color = group)) +
  geom_point(size = 1.5, alpha = 0.6) +
  scale_color_manual(values = c(A = "#1565C0", B = "#E53935", C = "#2E7D32")) +
  labs(title = "aes(color = group)", subtitle = "One panel, colour encodes group") +
  theme_minimal(base_size = 9)

# Strategy B: faceting separates groups
p_facet <- ggplot(df_groups, aes(x = x, y = y)) +
  geom_point(size = 1.5, alpha = 0.6, color = "#1565C0") +
  facet_wrap(~group, ncol = 3) +
  labs(title = "facet_wrap(~group)", subtitle = "Three panels, proximity encodes group") +
  theme_minimal(base_size = 9)

p_strategies <- p_color / p_facet +
  plot_annotation(title = "Same Data, Different Aesthetic Strategy")

print(p_strategies)
ggsave("output/color_vs_facet.png", p_strategies, width = 9, height = 7, dpi = 300)


# ── 4. DECOMPOSING A GROUPED BAR CHART ───────────────────
# Show that every chart is just a combination of grammar layers

sales_data <- tibble(
  quarter = rep(c("Q1", "Q2", "Q3", "Q4"), 3),
  product = rep(c("Alpha", "Beta", "Gamma"), each = 4),
  revenue = c(120, 150, 180, 200,
              90, 110, 130, 160,
              60, 80, 100, 120)
)

p_grouped <- ggplot(sales_data,
  aes(x = quarter, y = revenue, fill = product)) +
  geom_col(position = "dodge", width = 0.7) +              # geometry + position
  scale_fill_manual(values = c(Alpha = "#1565C0",           # scale
                                Beta = "#E53935",
                                Gamma = "#2E7D32")) +
  labs(title = "Grouped Bar: Grammar Decomposition",        # labels
       subtitle = "data + aes(x, y, fill) + geom_col(position='dodge') + scale_fill + theme",
       x = "Quarter", y = "Revenue ($K)", fill = "Product") +
  theme_minimal(base_size = 10) +                           # theme
  theme(panel.grid.major.x = element_blank())

print(p_grouped)
ggsave("output/grouped_bar_grammar.png", p_grouped, width = 7, height = 5, dpi = 300)


# ── 5. COORD SYSTEM SWAP: Bar → Pie ─────────────────────
# Same data + geom_bar, only the coordinate system changes

market <- tibble(
  segment = c("Enterprise", "SMB", "Consumer"),
  share   = c(45, 35, 20)
)

p_bar_coord <- ggplot(market, aes(x = segment, y = share, fill = segment)) +
  geom_col(width = 0.7) +
  scale_fill_manual(values = c(Enterprise = "#1565C0", SMB = "#2E7D32", Consumer = "#E53935")) +
  theme_minimal() +
  theme(legend.position = "none") +
  labs(title = "coord_cartesian (bar)", x = NULL, y = "Share (%)")

p_pie_coord <- ggplot(market, aes(x = "", y = share, fill = segment)) +
  geom_col(width = 1) +
  coord_polar(theta = "y") +
  scale_fill_manual(values = c(Enterprise = "#1565C0", SMB = "#2E7D32", Consumer = "#E53935")) +
  theme_void() +
  labs(title = "coord_polar (pie)", fill = "Segment")

p_coord_swap <- p_bar_coord + p_pie_coord +
  plot_annotation(
    title = "Same Data + Same Geom, Different Coordinate System",
    subtitle = "Bar chart in Cartesian = pie chart in polar"
  )

print(p_coord_swap)
ggsave("output/coord_swap.png", p_coord_swap, width = 10, height = 4, dpi = 300)


cat("\n── All W02-M01 plots saved to output/ ──\n")
