# ============================================================
# Workshop 2 — Module 7: seaborn & plotnine (R comparison)
# R Demonstration Script — UNYT Tirana
# ============================================================
library(tidyverse)
library(patchwork)
dir.create("output", showWarnings = FALSE)

# This module is Python-focused. The R script provides the ggplot2
# equivalents for direct comparison.

set.seed(42)
n <- 200
df <- tibble(
  displ = runif(n, 1, 7),
  hwy = 35 - 3 * displ + rnorm(n, 0, 3),
  class = sample(c("compact", "midsize", "suv", "pickup"), n, TRUE),
  cyl = sample(c(4, 6, 8), n, TRUE),
  type = sample(c("Free", "Paid"), n, TRUE, prob = c(0.9, 0.1)),
  rating = pmin(pmax(rnorm(n, 4.0, 0.5), 1), 5)
)

# ── R equivalent of sns.scatterplot(hue=) ─────────────────
p1 <- ggplot(df, aes(x = displ, y = hwy, color = class)) +
  geom_point(alpha = 0.5, size = 1.5) +
  scale_color_manual(values = c(compact="#1565C0", midsize="#E53935",
                                 suv="#2E7D32", pickup="#E65100")) +
  theme_minimal() + labs(title = "ggplot2: aes(color = class)")

# ── R equivalent of sns.boxplot() ─────────────────────────
p2 <- ggplot(df, aes(x = class, y = hwy, fill = class)) +
  geom_boxplot(width = 0.5, alpha = 0.3) +
  scale_fill_manual(values = c(compact="#1565C0", midsize="#E53935",
                                suv="#2E7D32", pickup="#E65100")) +
  theme_minimal() + theme(legend.position = "none") +
  labs(title = "ggplot2: geom_boxplot(fill = class)")

# ── R equivalent of sns.regplot() ─────────────────────────
p3 <- ggplot(df, aes(x = displ, y = hwy)) +
  geom_point(alpha = 0.3, size = 1) +
  geom_smooth(method = "lm", color = "#E53935", se = TRUE) +
  theme_minimal() + labs(title = "ggplot2: geom_smooth(method='lm')")

# ── R equivalent of sns.relplot(col='cyl') ────────────────
p4 <- ggplot(df, aes(x = displ, y = hwy, color = class)) +
  geom_point(alpha = 0.5, size = 1) +
  scale_color_manual(values = c(compact="#1565C0", midsize="#E53935",
                                 suv="#2E7D32", pickup="#E65100")) +
  facet_wrap(~cyl, ncol = 3) +
  theme_minimal(base_size = 9) +
  labs(title = "ggplot2: facet_wrap(~cyl)")

ggsave("output/ggplot2_equivalents.png",
       (p1 | p2) / (p3 | p4), width = 12, height = 8, dpi = 300)

cat("\n── R comparison plots saved ──\n")
