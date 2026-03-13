# ============================================================
# Workshop 2 — Module 3: ggplot2 Deep Dive — Aesthetics & Geometries
# R Demonstration Script — UNYT Tirana
# ============================================================
library(tidyverse)
library(patchwork)
dir.create("output", showWarnings = FALSE)

# ── 1. MULTI-AESTHETIC ENCODING ───────────────────────────
set.seed(42)
df <- tibble(
  gdp = runif(80, 10, 100), life_exp = 50 + 0.3*gdp + rnorm(80, 0, 8),
  pop = runif(80, 1e6, 5e8), continent = sample(c("Africa","Asia","Europe"), 80, TRUE),
  income = sample(c("Low","Mid","High"), 80, TRUE)
)

p_bubble <- ggplot(df, aes(x = gdp, y = life_exp, color = continent,
                            size = pop, shape = income)) +
  geom_point(alpha = 0.6) +
  scale_color_manual(values = c(Africa="#1565C0", Asia="#E53935", Europe="#2E7D32")) +
  scale_size(range = c(1, 12), labels = scales::label_number(scale = 1e-6, suffix = "M")) +
  scale_shape_manual(values = c(Low=16, Mid=17, High=15)) +
  theme_minimal() +
  labs(title = "Five Variables in One Chart", x = "GDP per Capita ($K)",
       y = "Life Expectancy", size = "Population", shape = "Income")
ggsave("output/multi_aes.png", p_bubble, width = 8, height = 5, dpi = 300)

# ── 2. LAYERED GEOMS ─────────────────────────────────────
# Point + smooth
p1 <- ggplot(mpg, aes(x = displ, y = hwy)) +
  geom_point(alpha = 0.4) + geom_smooth(method = "lm", color = "#E53935") +
  theme_minimal() + labs(title = "point + smooth")

# Boxplot + jitter
p2 <- ggplot(mpg, aes(x = factor(cyl), y = hwy)) +
  geom_boxplot(outlier.shape = NA, fill = "#E3F2FD") +
  geom_jitter(width = 0.15, alpha = 0.3, size = 0.8, color = "#E53935") +
  theme_minimal() + labs(title = "boxplot + jitter", x = "Cylinders")

# Col + errorbar
mpg_summary <- mpg |> group_by(class) |>
  summarise(m = mean(hwy), se = sd(hwy)/sqrt(n()), .groups = "drop") |>
  mutate(class = fct_reorder(class, m))
p3 <- ggplot(mpg_summary, aes(x = class, y = m)) +
  geom_col(fill = "#1565C0", alpha = 0.6, width = 0.5) +
  geom_errorbar(aes(ymin = m-se, ymax = m+se), width = 0.2) +
  coord_flip() + theme_minimal() + labs(title = "col + errorbar", x = NULL, y = "Mean MPG")

p_layers <- p1 | p2 | p3
ggsave("output/geom_layers.png", p_layers, width = 12, height = 4, dpi = 300)

# ── 3. OVERPLOTTING ───────────────────────────────────────
set.seed(55)
big <- tibble(x = rnorm(5000, 50, 15), y = 0.3*x + rnorm(5000, 0, 8))

p_over <- ggplot(big, aes(x, y)) + geom_point(size = 0.5) +
  theme_minimal() + labs(title = "Overplotting (n=5000)")
p_alpha <- ggplot(big, aes(x, y)) + geom_point(alpha = 0.05, size = 0.5) +
  theme_minimal() + labs(title = "Fix: alpha = 0.05")
p_hex <- ggplot(big, aes(x, y)) + geom_hex(bins = 25) +
  scale_fill_viridis_c() + theme_minimal() + labs(title = "Fix: geom_hex()")
p_dens <- ggplot(big, aes(x, y)) + geom_density_2d_filled(alpha = 0.7) +
  theme_minimal() + labs(title = "Fix: geom_density_2d_filled()")

p_overplot <- (p_over | p_alpha) / (p_hex | p_dens) +
  plot_annotation(title = "Overplotting: Problem and Solutions")
ggsave("output/overplotting.png", p_overplot, width = 10, height = 7, dpi = 300)

# ── 4. LOLLIPOP CHART ────────────────────────────────────
p_lollipop <- mpg_summary |>
  ggplot(aes(x = class, y = m)) +
  geom_segment(aes(xend = class, y = 0, yend = m), color = "grey70") +
  geom_point(size = 3, color = "#1565C0") +
  coord_flip() + theme_minimal() +
  labs(title = "Lollipop: geom_segment + geom_point", x = NULL, y = "Mean Highway MPG")
ggsave("output/lollipop.png", p_lollipop, width = 6, height = 4, dpi = 300)

# ── 5. DUMBBELL CHART ────────────────────────────────────
df_db <- tibble(
  cat = c("Economy","Midsize","Compact","SUV","Pickup"),
  y2008 = c(26, 24, 28, 18, 16), y2024 = c(32, 30, 35, 24, 22)
) |> mutate(cat = fct_reorder(cat, y2024))

p_dumbbell <- ggplot(df_db, aes(y = cat)) +
  geom_segment(aes(x = y2008, xend = y2024, yend = cat), color = "grey80", linewidth = 1.5) +
  geom_point(aes(x = y2008), size = 3, color = "#1565C0") +
  geom_point(aes(x = y2024), size = 3, color = "#E53935") +
  theme_minimal() +
  labs(title = "Dumbbell: 2008 (blue) vs 2024 (red)", x = "MPG", y = NULL)
ggsave("output/dumbbell.png", p_dumbbell, width = 7, height = 4, dpi = 300)

cat("\n── All W02-M03 R plots saved ──\n")
