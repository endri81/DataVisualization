# ============================================================
# Workshop 1 — Module 2: Tufte's Principles
# R Demonstration Script
# Data Visualization for Data Scientists — UNYT Tirana
# ============================================================

# ── 0. Setup ────────────────────────────────────────────────
# install.packages(c("tidyverse", "ggthemes", "patchwork"))
library(tidyverse)
library(ggthemes)   # theme_tufte(), theme_economist(), etc.
library(patchwork)

# Create output directory
dir.create("output", showWarnings = FALSE)


# ── 1. Data-Ink Ratio: Progressive Erasure ──────────────────
# Using the mpg dataset to demonstrate four stages of
# chartjunk removal following Tufte's "erase" principle.

mpg_counts <- mpg |>
  count(class) |>
  mutate(class = fct_reorder(class, n))

# Version 1: Default ggplot2 (heavy gridlines, grey background)
p1 <- ggplot(mpg_counts, aes(x = class, y = n)) +
  geom_bar(stat = "identity", fill = "skyblue", color = "black") +
  labs(title = "V1: Default", y = "Count", x = NULL) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 7),
        plot.title = element_text(size = 9, face = "bold"))

# Version 2: Remove background fill and border
p2 <- ggplot(mpg_counts, aes(x = class, y = n)) +
  geom_col(fill = "steelblue") +
  labs(title = "V2: No Fill/Border", y = "Count", x = NULL) +
  theme_minimal(base_size = 9) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 7),
        plot.title = element_text(face = "bold"))

# Version 3: Remove gridlines, flip to horizontal
p3 <- ggplot(mpg_counts, aes(x = class, y = n)) +
  geom_col(fill = "steelblue", width = 0.6) +
  coord_flip() +
  labs(title = "V3: Horizontal, No Grid", y = "Count", x = NULL) +
  theme_minimal(base_size = 9) +
  theme(panel.grid.major.y = element_blank(),
        panel.grid.minor = element_blank(),
        plot.title = element_text(face = "bold"))

# Version 4: Tufte-style — direct labels, minimal spines
p4 <- ggplot(mpg_counts, aes(x = class, y = n)) +
  geom_col(fill = "#1565C0", width = 0.5) +
  geom_text(aes(label = n), hjust = -0.3, size = 3) +
  coord_flip() +
  theme_tufte(base_size = 9) +
  labs(title = "V4: Tufte Style", y = NULL, x = NULL) +
  theme(plot.title = element_text(face = "bold"))

# Combine with patchwork
p_combined <- (p1 | p2) / (p3 | p4) +
  plot_annotation(
    title = "Data-Ink Ratio: Progressive Erasure",
    subtitle = "Same data, four design stages"
  )

print(p_combined)
ggsave("output/data_ink_erasure.png", p_combined,
       width = 10, height = 7, dpi = 150)


# ── 2. Chartjunk: 3-D Pie vs Clean Bar ─────────────────────
# R does not natively support 3-D pies, which is itself a
# design endorsement. Compare a standard pie to a bar chart.

share_data <- tibble(
  product = c("Product A", "Product B", "Product C", "Product D"),
  share = c(35, 30, 20, 15)
) |>
  mutate(product = fct_reorder(product, share))

# Pie (not recommended, but shown for comparison)
p_pie <- ggplot(share_data, aes(x = "", y = share, fill = product)) +
  geom_bar(stat = "identity", width = 1) +
  coord_polar("y") +
  theme_void() +
  labs(title = "Pie Chart (Hard to Compare)") +
  theme(plot.title = element_text(size = 9, face = "bold"))

# Clean horizontal bar
p_bar <- ggplot(share_data, aes(x = product, y = share)) +
  geom_col(fill = "#1565C0", width = 0.6) +
  geom_text(aes(label = paste0(share, "%")), hjust = -0.2, size = 3.5) +
  coord_flip() +
  theme_tufte(base_size = 10) +
  labs(title = "Tufte Bar (Easy to Compare)",
       x = NULL, y = "Market Share (%)") +
  theme(plot.title = element_text(face = "bold"))

p_chartjunk <- p_pie + p_bar +
  plot_annotation(title = "Chartjunk Removal: Pie → Bar")

print(p_chartjunk)
ggsave("output/chartjunk_removal.png", p_chartjunk,
       width = 10, height = 4, dpi = 150)


# ── 3. Lie Factor Demonstration ─────────────────────────────
# Show truncated vs full y-axis for the same data

revenue <- tibble(
  quarter = c("Q1", "Q2", "Q3", "Q4"),
  value = c(982, 995, 1003, 1010)
)

# Truncated (lie factor >> 1)
p_trunc <- ggplot(revenue, aes(x = quarter, y = value)) +
  geom_col(fill = "#E53935", width = 0.5) +
  coord_cartesian(ylim = c(975, 1015)) +
  labs(title = "Truncated Axis (Misleading)",
       y = "Revenue ($M)", x = NULL) +
  theme_minimal(base_size = 9) +
  theme(plot.title = element_text(face = "bold", color = "#C62828"))

# Honest (lie factor ~ 1)
p_honest <- ggplot(revenue, aes(x = quarter, y = value)) +
  geom_col(fill = "#1565C0", width = 0.5) +
  geom_text(aes(label = value), vjust = -0.5, size = 3) +
  coord_cartesian(ylim = c(0, 1200)) +
  labs(title = "Full Axis (Honest)",
       y = "Revenue ($M)", x = NULL) +
  theme_minimal(base_size = 9) +
  theme(plot.title = element_text(face = "bold", color = "#1565C0"))

p_lie <- p_trunc + p_honest +
  plot_annotation(title = "Lie Factor: Truncated vs Full Baseline")

print(p_lie)
ggsave("output/lie_factor_demo.png", p_lie,
       width = 9, height = 4, dpi = 150)


# ── 4. Small Multiples ─────────────────────────────────────
# Simulate regional monthly revenue data

set.seed(7)
regions <- c("North", "South", "East", "West", "Central", "Coastal")
months <- 1:12

sm_data <- expand_grid(region = regions, month = months) |>
  group_by(region) |>
  mutate(
    base = runif(1, 50, 120),
    revenue = cumsum(rnorm(n(), 2, 8)) + base
  ) |>
  ungroup()

p_sm <- ggplot(sm_data, aes(x = month, y = revenue)) +
  geom_line(color = "#1565C0", linewidth = 0.8) +
  geom_area(fill = "#1565C0", alpha = 0.08) +
  facet_wrap(~region, ncol = 3, scales = "fixed") +
  scale_x_continuous(breaks = c(1, 6, 12),
                     labels = c("Jan", "Jun", "Dec")) +
  theme_minimal(base_size = 9) +
  theme(
    strip.text = element_text(face = "bold"),
    panel.grid.minor = element_blank()
  ) +
  labs(x = NULL, y = "Revenue ($K)",
       title = "Small Multiples: Same Scale, Easy Comparison",
       subtitle = "\"Compared to what?\" — Tufte")

print(p_sm)
ggsave("output/small_multiples.png", p_sm,
       width = 9, height = 5, dpi = 150)


# ── 5. Sparklines (using theme_void) ───────────────────────
set.seed(12)
spark_data <- tibble(
  week = rep(1:52, 4),
  metric = rep(c("Revenue", "Users", "Retention", "NPS"),
               each = 52),
  value = c(
    cumsum(rnorm(52, 0.5, 3)),
    cumsum(rnorm(52, 0.3, 2)),
    cumsum(rnorm(52, 0.1, 4)),
    cumsum(rnorm(52, 0.4, 2.5))
  )
)

p_spark <- ggplot(spark_data, aes(x = week, y = value)) +
  geom_line(color = "#1565C0", linewidth = 0.6) +
  facet_wrap(~metric, ncol = 1, scales = "free_y") +
  theme_void(base_size = 8) +
  theme(strip.text = element_text(hjust = 0, face = "bold", size = 8)) +
  labs(title = "Sparklines: Word-Sized Graphics (Tufte, 2006)")

print(p_spark)
ggsave("output/sparklines.png", p_spark,
       width = 5, height = 4, dpi = 150)

cat("\n── All M02 plots saved to output/ ──\n")
