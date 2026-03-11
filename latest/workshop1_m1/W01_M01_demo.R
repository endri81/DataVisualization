# ============================================================
# Workshop 1 — Module 1: Why Visualize?
# R Demonstration Script
# Data Visualization for Data Scientists — UNYT Tirana
# ============================================================

# ── 0. Environment Setup ────────────────────────────────────
# install.packages(c("tidyverse", "datasauRus", "patchwork"))
library(tidyverse)
library(datasauRus)
library(patchwork)

# ── 1. Anscombe's Quartet ───────────────────────────────────
# Anscombe's quartet ships with base R; four datasets with
# identical summary statistics but completely different shapes.

data(anscombe)

# Compute summary statistics to prove they match
anscombe_summary <- anscombe |>
  pivot_longer(
    everything(),
    names_to  = c(".value", "set"),
    names_pattern = "(.)(.)"
  ) |>
  group_by(set) |>
  summarise(
    mean_x = round(mean(x), 2),
    mean_y = round(mean(y), 2),
    sd_x   = round(sd(x), 2),
    sd_y   = round(sd(y), 2),
    cor_xy = round(cor(x, y), 3),
    .groups = "drop"
  )

cat("── Anscombe's Quartet: Summary Statistics ──\n")
print(anscombe_summary)
# Observe: all four sets yield nearly identical values

# Reshape for faceted plotting
anscombe_long <- anscombe |>
  pivot_longer(
    everything(),
    names_to  = c(".value", "set"),
    names_pattern = "(.)(.)"
  )

# Faceted scatterplot with regression lines
p_anscombe <- ggplot(anscombe_long, aes(x = x, y = y)) +
  geom_point(size = 2.5, color = "#1565C0") +
  geom_smooth(
    method = "lm", se = FALSE,
    color = "#E53935", linewidth = 0.8
  ) +
  facet_wrap(~set, ncol = 2,
             labeller = labeller(set = c(
               "1" = "Dataset I",
               "2" = "Dataset II",
               "3" = "Dataset III",
               "4" = "Dataset IV"
             ))) +
  labs(
    title    = "Anscombe's Quartet",
    subtitle = "Same statistics, different stories",
    x = "x", y = "y"
  ) +
  theme_minimal(base_size = 12)

print(p_anscombe)
ggsave("output/anscombe_quartet.png", p_anscombe,
       width = 8, height = 6, dpi = 150)


# ── 2. Datasaurus Dozen ────────────────────────────────────
# Matejka & Fitzmaurice (2017) extended Anscombe's idea to
# 13 datasets — including a dinosaur — all with identical
# means, standard deviations, and correlations.

# Verify identical statistics
dino_stats <- datasaurus_dozen |>
  group_by(dataset) |>
  summarise(
    mean_x = round(mean(x), 1),
    mean_y = round(mean(y), 1),
    sd_x   = round(sd(x), 1),
    sd_y   = round(sd(y), 1),
    cor_xy = round(cor(x, y), 2),
    .groups = "drop"
  )

cat("\n── Datasaurus Dozen: Summary Statistics ──\n")
print(dino_stats)

# Faceted scatterplot: 13 shapes, one set of statistics
p_datasaurus <- ggplot(datasaurus_dozen,
                       aes(x = x, y = y)) +
  geom_point(alpha = 0.5, size = 0.6, color = "#2E7D32") +
  facet_wrap(~dataset, ncol = 5) +
  labs(
    title    = "The Datasaurus Dozen",
    subtitle = "13 datasets, same summary stats (Matejka & Fitzmaurice, 2017)",
    caption  = "Source: datasauRus package"
  ) +
  theme_minimal(base_size = 8) +
  theme(
    strip.text = element_text(face = "bold", size = 7),
    plot.title = element_text(face = "bold")
  )

print(p_datasaurus)
ggsave("output/datasaurus_dozen.png", p_datasaurus,
       width = 10, height = 6, dpi = 150)


# ── 3. First Plot: mpg Dataset ─────────────────────────────
# A quick preview of ggplot2's layered grammar using the
# built-in mpg dataset (fuel economy from 1999–2008).

p_mpg <- ggplot(mpg, aes(x = displ, y = hwy, color = class)) +
  geom_point(size = 2, alpha = 0.7) +
  labs(
    title = "Engine Displacement vs Highway Fuel Economy",
    x     = "Engine Displacement (litres)",
    y     = "Highway MPG",
    color = "Vehicle Class"
  ) +
  theme_minimal(base_size = 12)

print(p_mpg)
ggsave("output/mpg_scatter.png", p_mpg,
       width = 8, height = 5, dpi = 150)


# ── 4. Data-Ink Ratio: Before & After ──────────────────────
# Demonstrate chartjunk removal using the same data

# "Before" — heavy gridlines, unnecessary decoration
p_before <- ggplot(mpg, aes(x = class)) +
  geom_bar(fill = "skyblue", color = "black", linewidth = 1) +
  labs(title = "Vehicle Counts by Class (Cluttered)") +
  theme(
    panel.grid.major = element_line(color = "grey60", linewidth = 0.8),
    panel.grid.minor = element_line(color = "grey80", linewidth = 0.5),
    panel.background = element_rect(fill = "grey95"),
    axis.text.x = element_text(angle = 45, hjust = 1, size = 10)
  )

# "After" — clean, sorted, horizontal
mpg_counts <- mpg |>
  count(class) |>
  mutate(class = fct_reorder(class, n))

p_after <- ggplot(mpg_counts, aes(x = n, y = class)) +
  geom_col(fill = "#1565C0", width = 0.7) +
  geom_text(aes(label = n), hjust = -0.2, size = 3.5) +
  labs(
    title = "Vehicle Counts by Class (Clean)",
    x = "Count", y = NULL
  ) +
  theme_minimal(base_size = 12) +
  theme(panel.grid.major.y = element_blank())

# Side-by-side comparison using patchwork
p_comparison <- p_before + p_after +
  plot_annotation(
    title = "Data-Ink Ratio: Before & After",
    subtitle = "Removing chartjunk improves communication"
  )

print(p_comparison)
ggsave("output/data_ink_comparison.png", p_comparison,
       width = 12, height = 5, dpi = 150)

cat("\n── All plots saved to output/ directory ──\n")
