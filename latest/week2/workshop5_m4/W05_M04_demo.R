# ============================================================
# Workshop 5 — Module 4: Heatmaps & Clustered Displays
# Integrated R Script — UNYT Tirana
# ============================================================
library(tidyverse); library(pheatmap); dir.create("output", showWarnings = FALSE)

# ── 1. SIMULATED GENE-EXPRESSION STYLE MATRIX ──
set.seed(42)
n_samples <- 25; n_features <- 10
# 3 sample clusters with distinct feature activation patterns
g1 <- matrix(rnorm(8 * n_features, mean = 2, sd = 0.5), nrow = 8)
g1[, 1:4] <- g1[, 1:4] + 3  # cluster 1 activates features 1-4
g2 <- matrix(rnorm(9 * n_features, mean = 2, sd = 0.5), nrow = 9)
g2[, 5:7] <- g2[, 5:7] + 3  # cluster 2 activates features 5-7
g3 <- matrix(rnorm(8 * n_features, mean = 2, sd = 0.5), nrow = 8)
g3[, 8:10] <- g3[, 8:10] + 3  # cluster 3 activates features 8-10

mat <- rbind(g1, g2, g3)
rownames(mat) <- paste0("S", 1:25)
colnames(mat) <- paste0("F", 1:10)
cluster_ids <- c(rep("A", 8), rep("B", 9), rep("C", 8))
ann_row <- data.frame(Cluster = cluster_ids, row.names = rownames(mat))

# ── 2. BASIC HEATMAP (no clustering) ──
pheatmap(mat,
  cluster_rows = FALSE, cluster_cols = FALSE,
  color = colorRampPalette(c("#FFFFCC", "#FD8D3C", "#800026"))(100),
  border_color = NA, fontsize_row = 7, fontsize_col = 9,
  main = "Basic Heatmap (no clustering — patterns hidden)")

# ── 3. CLUSTERED HEATMAP (Ward linkage) ──
p_clust <- pheatmap(mat,
  clustering_method = "ward.D2",
  clustering_distance_rows = "euclidean",
  clustering_distance_cols = "euclidean",
  color = colorRampPalette(c("#1565C0", "white", "#E53935"))(100),
  border_color = NA, fontsize_row = 7, fontsize_col = 9,
  annotation_row = ann_row,
  annotation_colors = list(Cluster = c(A = "#1565C0", B = "#E53935", C = "#2E7D32")),
  main = "Clustered Heatmap (Ward, Euclidean)")
ggsave("output/clustered_heatmap.png", p_clust, width = 7, height = 8, dpi = 300)

# ── 4. Z-SCORE NORMALISED ──
p_zscore <- pheatmap(mat,
  scale = "row",  # z-score each row
  clustering_method = "ward.D2",
  color = colorRampPalette(c("#1565C0", "white", "#E53935"))(100),
  border_color = NA, fontsize_row = 7, fontsize_col = 9,
  annotation_row = ann_row,
  annotation_colors = list(Cluster = c(A = "#1565C0", B = "#E53935", C = "#2E7D32")),
  main = "Z-Scored Heatmap (row-scaled, diverging palette)")
ggsave("output/zscore_heatmap.png", p_zscore, width = 7, height = 8, dpi = 300)

# ── 5. CORRELATION HEATMAP (e-Car dataset) ──
ecar <- read_csv("ecar.csv")
ecar_clean <- ecar |>
  rename(CarType = `Car  Type`, CoF = `Cost of Funds`) |>
  mutate(Spread = Rate - CoF) |>
  select(FICO, Rate, Amount, Term, CoF, Spread) |>
  drop_na()

corr_mat <- cor(ecar_clean)
pheatmap(corr_mat,
  display_numbers = TRUE, number_format = "%.2f",
  color = colorRampPalette(c("#1565C0", "white", "#E53935"))(100),
  breaks = seq(-1, 1, length.out = 101),  # fixed [-1, 1] scale
  clustering_method = "ward.D2",
  fontsize_number = 9, border_color = "white",
  main = "e-Car: Correlation Heatmap (clustered)")

# ── 6. ComplexHeatmap (if installed) ──
# library(ComplexHeatmap)
# Heatmap(mat, name = "value",
#   row_split = 3, column_split = 2,
#   top_annotation = HeatmapAnnotation(Cluster = cluster_ids))

cat("\n── All W05-M04 R outputs saved ──\n")
