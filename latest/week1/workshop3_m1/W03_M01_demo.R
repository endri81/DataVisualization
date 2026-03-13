# ============================================================
# Workshop 3 — Module 1: Distributions — Histograms, Density, Ridgeline
# R Demonstration Script — UNYT Tirana
# ============================================================
library(tidyverse)
library(patchwork)
dir.create("output", showWarnings = FALSE)

apps <- read_csv("googleplaystore.csv") |>
  filter(Type %in% c("Free", "Paid"), !is.na(Rating))

# ── 1. BIN WIDTH COMPARISON ─────────────────────────────
p_bins <- map(c(5, 15, 40, 100), \(b) {
  ggplot(apps, aes(x = Rating)) +
    geom_histogram(bins = b, fill = "#1565C0", color = "white", linewidth = 0.3) +
    theme_minimal(base_size = 8) + labs(title = paste0("bins = ", b))
}) |> wrap_plots(ncol = 4) +
  plot_annotation(title = "Bin Width Matters: Same Data, Four Histograms")
ggsave("output/bin_width.png", p_bins, width = 12, height = 3, dpi = 300)

# ── 2. THREE VARIANTS ────────────────────────────────────
p_freq <- ggplot(apps, aes(x = Rating)) +
  geom_histogram(bins = 30, fill = "#1565C0", color = "white") +
  theme_minimal(base_size = 9) + labs(title = "Frequency", y = "Count")

p_dens <- ggplot(apps, aes(x = Rating)) +
  geom_histogram(aes(y = after_stat(density)), bins = 30, fill = "#2E7D32", color = "white") +
  theme_minimal(base_size = 9) + labs(title = "Density", y = "Density")

p_ecdf <- ggplot(apps, aes(x = Rating)) +
  stat_ecdf(color = "#E65100", linewidth = 1) +
  theme_minimal(base_size = 9) + labs(title = "ECDF", y = "Cumulative Proportion")

ggsave("output/hist_variants.png", p_freq | p_dens | p_ecdf, width = 12, height = 3.5, dpi = 300)

# ── 3. HISTOGRAM + KDE OVERLAY ───────────────────────────
mean_r <- mean(apps$Rating, na.rm = TRUE)
median_r <- median(apps$Rating, na.rm = TRUE)

p_overlay <- ggplot(apps, aes(x = Rating)) +
  geom_histogram(aes(y = after_stat(density)), bins = 35,
                 fill = "#1565C0", color = "white", alpha = 0.5) +
  geom_density(color = "#E53935", linewidth = 1.2) +
  geom_vline(xintercept = mean_r, linetype = "dashed", color = "#2E7D32", linewidth = 1) +
  geom_vline(xintercept = median_r, linetype = "dotted", color = "#E65100", linewidth = 1) +
  annotate("text", x = mean_r - 0.2, y = 1.3,
           label = paste0("Mean: ", round(mean_r, 2)), color = "#2E7D32",
           fontface = "bold", size = 3) +
  theme_minimal() +
  labs(title = "Rating Distribution: Left-Skewed",
       subtitle = "Histogram + KDE + Mean/Median", x = "Rating", y = "Density")
ggsave("output/hist_kde_overlay.png", p_overlay, width = 7, height = 5, dpi = 300)

# ── 4. GROUPED DENSITY ───────────────────────────────────
p_grouped <- ggplot(apps, aes(x = Rating, fill = Type, color = Type)) +
  geom_density(alpha = 0.2, linewidth = 1) +
  scale_fill_manual(values = c(Free = "#1565C0", Paid = "#E53935")) +
  scale_color_manual(values = c(Free = "#1565C0", Paid = "#E53935")) +
  theme_minimal() +
  labs(title = "Grouped Density: Free vs Paid", x = "Rating", y = "Density")
ggsave("output/grouped_density.png", p_grouped, width = 7, height = 4, dpi = 300)

# ── 5. RIDGELINE PLOT ────────────────────────────────────
# install.packages("ggridges")
# library(ggridges)
# p_ridge <- ggplot(apps |> filter(`Content Rating` %in%
#     c("Everyone","Teen","Mature 17+","Everyone 10+")),
#   aes(x = Rating, y = `Content Rating`, fill = `Content Rating`)) +
#   geom_density_ridges(alpha = 0.4, scale = 1.5) +
#   scale_fill_brewer(palette = "Set2") +
#   theme_minimal() + theme(legend.position = "none") +
#   labs(title = "Ridgeline: Rating by Content Rating")
# ggsave("output/ridgeline.png", p_ridge, width = 7, height = 5, dpi = 300)

# ── 6. BANDWIDTH COMPARISON ──────────────────────────────
p_bw <- map(c(0.3, 1.0, 3.0), \(adj) {
  ggplot(apps, aes(x = Rating)) +
    geom_density(fill = "#1565C0", alpha = 0.2, adjust = adj, linewidth = 1) +
    theme_minimal(base_size = 8) + labs(title = paste0("adjust = ", adj))
}) |> wrap_plots(ncol = 3) +
  plot_annotation(title = "Bandwidth Controls Smoothness")
ggsave("output/bandwidth.png", p_bw, width = 10, height = 3, dpi = 300)

cat("\n── All W03-M01 R plots saved ──\n")
