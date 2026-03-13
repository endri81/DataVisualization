# ============================================================
# Workshop 2 — Module 2: Wickham's Layered Grammar & ggplot2
# R Demonstration Script
# Data Visualization for Data Scientists — UNYT Tirana
# ============================================================
library(tidyverse)
dir.create("output", showWarnings = FALSE)

# ── 1. MAPPING vs SETTING ─────────────────────────────────
set.seed(22)
df <- tibble(x = runif(60, 1, 6), y = 0.5*x + rnorm(60, 0, 0.8),
             group = sample(c("A","B"), 60, replace = TRUE))

# Mapping: colour driven by data
p_map <- ggplot(df, aes(x = x, y = y, color = group)) +
  geom_point(size = 2) +
  scale_color_manual(values = c(A = "#1565C0", B = "#E53935")) +
  theme_minimal() + labs(title = "Mapping: aes(color = group)")

# Setting: colour fixed
p_set <- ggplot(df, aes(x = x, y = y)) +
  geom_point(color = "#E53935", size = 2) +
  theme_minimal() + labs(title = "Setting: color = 'red'")

ggsave("output/mapping.png", p_map, width = 5, height = 4, dpi = 300)
ggsave("output/setting.png", p_set, width = 5, height = 4, dpi = 300)

# ── 2. POSITION ADJUSTMENTS ──────────────────────────────
apps <- read_csv("googleplaystore.csv") |>
  filter(Type %in% c("Free", "Paid"),
         `Content Rating` %in% c("Everyone","Teen","Mature 17+","Everyone 10+"))

p_stack <- ggplot(apps, aes(x = `Content Rating`, fill = Type)) +
  geom_bar(position = "stack") +
  scale_fill_manual(values = c(Free="#1565C0", Paid="#E53935")) +
  theme_minimal() + labs(title = 'position = "stack"')

p_dodge <- ggplot(apps, aes(x = `Content Rating`, fill = Type)) +
  geom_bar(position = position_dodge(width = 0.8)) +
  scale_fill_manual(values = c(Free="#1565C0", Paid="#E53935")) +
  theme_minimal() + labs(title = 'position = "dodge"')

p_fill <- ggplot(apps, aes(x = `Content Rating`, fill = Type)) +
  geom_bar(position = "fill") +
  scale_fill_manual(values = c(Free="#1565C0", Paid="#E53935")) +
  scale_y_continuous(labels = scales::percent) +
  theme_minimal() + labs(title = 'position = "fill"')

p_jitter <- ggplot(apps |> filter(!is.na(Rating)),
                   aes(x = Type, y = Rating)) +
  geom_jitter(width = 0.2, height = 0, alpha = 0.2, size = 0.8, color = "#1565C0") +
  theme_minimal() + labs(title = 'position = "jitter"')

library(patchwork)
p_positions <- (p_stack | p_dodge) / (p_fill | p_jitter) +
  plot_annotation(title = "Four Position Adjustments")
ggsave("output/positions.png", p_positions, width = 10, height = 7, dpi = 300)

# ── 3. INHERITANCE — global vs local ─────────────────────
# Global: both layers inherit color
p_global <- ggplot(mpg, aes(x = displ, y = hwy, color = drv)) +
  geom_point(alpha = 0.5) +
  geom_smooth(method = "lm", se = FALSE) +
  theme_minimal() + labs(title = "Global: smooth per group")

# Local: only points use color
p_local <- ggplot(mpg, aes(x = displ, y = hwy)) +
  geom_point(aes(color = drv), alpha = 0.5) +
  geom_smooth(method = "lm", se = TRUE, color = "grey40") +
  theme_minimal() + labs(title = "Local: one overall smooth")

p_inherit <- p_global + p_local +
  plot_annotation(title = "Aesthetic Inheritance")
ggsave("output/inheritance.png", p_inherit, width = 10, height = 4, dpi = 300)

# ── 4. COMPLETE EXAMPLE ──────────────────────────────────
p_final <- ggplot(mpg, aes(x = displ, y = hwy, color = class)) +
  geom_point(size = 2, alpha = 0.6) +
  geom_smooth(aes(group = 1), method = "lm", se = TRUE, color = "grey40") +
  scale_color_brewer(palette = "Set2") +
  labs(title = "Displacement vs Highway MPG", x = "Engine (L)",
       y = "Highway MPG", color = "Class") +
  theme_minimal(base_size = 11)
ggsave("output/complete_ggplot.png", p_final, width = 7, height = 5, dpi = 300)

cat("\n── All W02-M02 R plots saved ──\n")
