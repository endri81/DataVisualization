# ============================================================
# Workshop 1 — Module 5: Typography, Layout & Composition
# R Demonstration Script
# Data Visualization for Data Scientists — UNYT Tirana
# ============================================================

library(tidyverse)
# install.packages(c("patchwork", "ggrepel", "showtext"))
library(patchwork)
library(ggrepel)
dir.create("output", showWarnings = FALSE)


# ── 1. Typographic Hierarchy ──────────────────────────────
set.seed(42)
df <- tibble(
  product = paste("Product", LETTERS[1:6]),
  revenue = c(450, 380, 520, 290, 610, 340)
) |>
  mutate(product = fct_reorder(product, revenue))

p_typo <- ggplot(df, aes(x = product, y = revenue)) +
  geom_col(fill = "#1565C0", width = 0.6) +
  geom_text(aes(label = paste0("$", revenue, "K")),
            hjust = -0.15, size = 3, fontface = "bold") +
  coord_flip() +
  theme_minimal(base_size = 11) +
  theme(
    # Title hierarchy
    plot.title = element_text(size = 16, face = "bold",
                              margin = margin(b = 6)),
    plot.subtitle = element_text(size = 11, color = "grey50",
                                  margin = margin(b = 12)),
    plot.caption = element_text(size = 8, face = "italic", hjust = 0,
                                 margin = margin(t = 10)),
    # Axis text
    axis.title = element_text(size = 10),
    axis.text = element_text(size = 9),
    # Margins
    plot.margin = margin(t = 15, r = 30, b = 10, l = 10),
    panel.grid.major.y = element_blank()
  ) +
  labs(
    title = "Product Revenue: Q4 2024",
    subtitle = "Annual revenue in thousands USD, sorted descending",
    caption = "Source: Internal sales database | Prepared: Jan 2025",
    x = NULL, y = "Revenue ($K)"
  )

print(p_typo)
ggsave("output/typographic_hierarchy.png", p_typo, width = 7, height = 5, dpi = 300)
ggsave("output/typographic_hierarchy.pdf", p_typo, width = 7, height = 5)


# ── 2. Direct Labelling vs Legend ─────────────────────────
set.seed(7)
months <- 1:12
df_lines <- tibble(
  month = rep(months, 3),
  product = rep(c("Alpha", "Beta", "Gamma"), each = 12),
  revenue = c(
    cumsum(rnorm(12, 3, 4)) + 40,
    cumsum(rnorm(12, 2, 3)) + 30,
    cumsum(rnorm(12, 1, 5)) + 20
  )
)
colors <- c(Alpha = "#1565C0", Beta = "#E53935", Gamma = "#2E7D32")

# Version A: with legend
p_legend <- ggplot(df_lines, aes(x = month, y = revenue, color = product)) +
  geom_line(linewidth = 1.2) +
  scale_color_manual(values = colors) +
  theme_minimal(base_size = 10) +
  labs(title = "Version A: Legend", x = "Month", y = "Revenue ($K)", color = "Product")

# Version B: direct labels
endpoints <- df_lines |> filter(month == max(month))

p_direct <- ggplot(df_lines, aes(x = month, y = revenue, color = product)) +
  geom_line(linewidth = 1.2) +
  geom_text_repel(
    data = endpoints,
    aes(label = product),
    nudge_x = 0.8, size = 3.5, fontface = "bold",
    direction = "y", segment.color = "grey70"
  ) +
  scale_color_manual(values = colors) +
  scale_x_continuous(limits = c(1, 14)) +
  theme_minimal(base_size = 10) +
  theme(legend.position = "none") +
  labs(title = "Version B: Direct Labels", x = "Month", y = "Revenue ($K)")

p_labelling <- p_legend + p_direct +
  plot_annotation(title = "Direct Labelling Eliminates the Legend Shuttle")

print(p_labelling)
ggsave("output/direct_vs_legend.png", p_labelling, width = 11, height = 4, dpi = 300)


# ── 3. Multi-Panel Composition with patchwork ─────────────
set.seed(55)

# Panel (a): bar
p_a <- ggplot(df, aes(x = product, y = revenue)) +
  geom_col(fill = "#1565C0", width = 0.5) +
  coord_flip() +
  theme_minimal(base_size = 8) +
  theme(panel.grid.major.y = element_blank()) +
  labs(title = "(a) Revenue by Product", x = NULL, y = "$K")

# Panel (b): scatter
p_b <- ggplot(tibble(x = rnorm(80), y = rnorm(80)),
              aes(x = x, y = y)) +
  geom_point(color = "#E53935", alpha = 0.5, size = 1.5) +
  theme_minimal(base_size = 8) +
  labs(title = "(b) Scatter")

# Panel (c): histogram
p_c <- ggplot(tibble(val = rnorm(500, 50, 15)), aes(x = val)) +
  geom_histogram(fill = "#2E7D32", bins = 25, color = "white", linewidth = 0.3) +
  theme_minimal(base_size = 8) +
  labs(title = "(c) Distribution", x = "Value", y = "Count")

# Panel (d): full-width time series
p_d <- ggplot(tibble(
  month = 1:24,
  value = cumsum(rnorm(24, 2, 5)) + 100
), aes(x = month, y = value)) +
  geom_line(color = "#1565C0", linewidth = 1) +
  geom_area(fill = "#1565C0", alpha = 0.06) +
  theme_minimal(base_size = 8) +
  labs(title = "(d) 24-Month Trend", x = "Month", y = "Value")

# Compose
p_multi <- (p_a | p_b | p_c) / p_d +
  plot_annotation(
    title = "Multi-Panel Report: patchwork Layout",
    subtitle = "Top row: three metrics | Bottom: temporal context"
  ) +
  plot_layout(heights = c(1, 1.3))

print(p_multi)
ggsave("output/multipanel_report.png", p_multi, width = 10, height = 6, dpi = 300)
ggsave("output/multipanel_report.pdf", p_multi, width = 10, height = 6)


# ── 4. Annotation Patterns ───────────────────────────────
set.seed(99)
df_anno <- tibble(
  month = 1:24,
  revenue = cumsum(rnorm(24, 2, 6)) + 100
)
df_anno$revenue[12] <- df_anno$revenue[11] - 25
df_anno$revenue[13:24] <- df_anno$revenue[13:24] + 15

p_anno <- ggplot(df_anno, aes(x = month, y = revenue)) +
  # Context band (enclosure)
  annotate("rect", xmin = 14, xmax = 18, ymin = -Inf, ymax = Inf,
           fill = "#E8F5E9", alpha = 0.6) +
  annotate("text", x = 16, y = max(df_anno$revenue) + 5,
           label = "Recovery period", size = 3, fontface = "bold", color = "#2E7D32") +
  # Reference line
  geom_hline(yintercept = mean(df_anno$revenue), linetype = "dashed", color = "grey60") +
  annotate("text", x = 24.5, y = mean(df_anno$revenue),
           label = paste0("Mean: ", round(mean(df_anno$revenue))),
           size = 2.5, color = "grey50", hjust = 0) +
  # Data line
  geom_line(color = "#1565C0", linewidth = 1) +
  # Callout
  annotate("text", x = 15, y = df_anno$revenue[12] - 12,
           label = "Product recall\n(Month 12)", size = 2.8,
           fontface = "bold", color = "#C62828") +
  annotate("segment", x = 14, xend = 12.2,
           y = df_anno$revenue[12] - 8, yend = df_anno$revenue[12] + 1,
           arrow = arrow(length = unit(0.15, "cm")), color = "#C62828") +
  theme_minimal(base_size = 10) +
  labs(title = "Three Annotation Patterns",
       subtitle = "Callout + Context Band + Reference Line",
       x = "Month", y = "Revenue ($K)")

print(p_anno)
ggsave("output/annotation_patterns.png", p_anno, width = 8, height = 5, dpi = 300)

cat("\n── All M05 plots saved to output/ ──\n")
