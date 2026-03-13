# ============================================================
# Workshop 3 — Module 2: Boxplots, Violins & Beeswarm
# R Demonstration Script — UNYT Tirana
# ============================================================
library(tidyverse)
library(patchwork)
dir.create("output", showWarnings = FALSE)
apps <- read_csv("googleplaystore.csv") |>
  filter(Type %in% c("Free","Paid"), !is.na(Rating))
top6 <- apps |> count(Category, sort=TRUE) |> slice_max(n, n=6) |> pull(Category)
df6 <- apps |> filter(Category %in% top6)

# 1. BOXPLOT + JITTER — the standard combo
p1 <- ggplot(df6, aes(x = fct_reorder(Category, Rating, .fun=median), y = Rating, fill = Category)) +
  geom_boxplot(width = 0.4, outlier.shape = NA, alpha = 0.3) +
  geom_jitter(width = 0.1, alpha = 0.15, size = 0.5, color = "#E53935") +
  stat_summary(fun = mean, geom = "point", shape = 18, size = 3, color = "#333") +
  coord_flip() + theme_minimal() + theme(legend.position = "none") +
  labs(title = "Boxplot + Jitter", x = NULL, y = "Rating")
ggsave("output/box_jitter.png", p1, width = 7, height = 5, dpi = 300)

# 2. VIOLIN + embedded box
p2 <- ggplot(apps, aes(x = Type, y = Rating, fill = Type)) +
  geom_violin(alpha = 0.3, draw_quantiles = c(0.25, 0.5, 0.75)) +
  geom_boxplot(width = 0.1, outlier.shape = NA, fill = "white") +
  scale_fill_manual(values = c(Free="#1565C0", Paid="#E53935")) +
  theme_minimal() + theme(legend.position = "none") +
  labs(title = "Violin + Box: Free vs Paid", y = "Rating", x = NULL)
ggsave("output/violin_box.png", p2, width = 5, height = 5, dpi = 300)

# 3. GROUPED NOTCHED BOXPLOT
p3 <- ggplot(df6, aes(x = Category, y = Rating, fill = Category)) +
  geom_boxplot(width = 0.5, notch = TRUE, outlier.alpha = 0.2) +
  stat_summary(fun = mean, geom = "point", shape = 18, size = 3, color = "#E53935") +
  scale_fill_brewer(palette = "Set2") +
  coord_flip() + theme_minimal() + theme(legend.position = "none") +
  labs(title = "Notched Boxplots: Rating by Category", x = NULL)
ggsave("output/notched_box.png", p3, width = 7, height = 5, dpi = 300)

# 4. COMPARISON PANEL
p_compare <- (p1 | p2) + plot_annotation(title = "Boxplot+Jitter vs Violin+Box")
ggsave("output/comparison.png", p_compare, width = 11, height = 5, dpi = 300)

cat("\n── All W03-M02 R plots saved ──\n")
