# ============================================================
# Workshop 1 — Module 7: Critique & Redesign Workshop
# R Demonstration Script
# Data Visualization for Data Scientists — UNYT Tirana
# ============================================================

library(tidyverse)
library(patchwork)
dir.create("output", showWarnings = FALSE)


# ── REDESIGN 1: Pie → Horizontal Bar ─────────────────────
df_budget <- tibble(
  dept = c("Marketing", "Engineering", "Sales", "Support", "R&D", "HR", "Legal"),
  pct  = c(22, 28, 18, 12, 10, 6, 4)
) |>
  mutate(dept = fct_reorder(dept, pct))

# BEFORE: pie (demonstrating what NOT to do)
p_pie <- ggplot(df_budget, aes(x = "", y = pct, fill = dept)) +
  geom_bar(stat = "identity", width = 1) +
  coord_polar("y") +
  theme_void() +
  labs(title = "BEFORE: Pie Chart") +
  theme(plot.title = element_text(face = "bold", color = "#C62828", size = 10))

# AFTER: sorted horizontal bar
p_bar <- ggplot(df_budget, aes(x = dept, y = pct,
                                fill = dept == "Engineering")) +
  geom_col(width = 0.55, show.legend = FALSE) +
  scale_fill_manual(values = c("FALSE" = "#1565C0", "TRUE" = "#E53935")) +
  geom_text(aes(label = paste0(pct, "%")), hjust = -0.2, size = 3.5, fontface = "bold") +
  coord_flip() +
  theme_minimal() +
  theme(panel.grid.major.y = element_blank()) +
  labs(title = "AFTER: Sorted Bar + Accent", x = NULL, y = "Budget Share (%)") +
  theme(plot.title = element_text(face = "bold", color = "#1565C0", size = 10))

p_redesign1 <- p_pie + p_bar +
  plot_annotation(title = "Redesign 1: Pie → Bar")

print(p_redesign1)
ggsave("output/redesign1_pie_to_bar.png", p_redesign1, width = 11, height = 5, dpi = 300)


# ── REDESIGN 2: Dual Y-Axis → Indexed Lines ──────────────
set.seed(11)
months <- 1:12
revenue <- cumsum(rnorm(12, 5, 8)) + 200
users <- cumsum(rnorm(12, 50, 80)) + 1000

df_ts <- tibble(
  month = rep(months, 2),
  metric = rep(c("Revenue ($K)", "Users"), each = 12),
  value = c(revenue, users)
) |>
  group_by(metric) |>
  mutate(index = value / first(value) * 100) |>
  ungroup()

# AFTER: indexed lines with direct labels
endpoints <- df_ts |> filter(month == max(month))

p_indexed <- ggplot(df_ts, aes(x = month, y = index, color = metric)) +
  geom_line(linewidth = 1.2) +
  geom_hline(yintercept = 100, linetype = "dashed", color = "grey60") +
  geom_text(data = endpoints, aes(label = metric),
            nudge_x = 0.5, size = 3, fontface = "bold", show.legend = FALSE) +
  scale_color_manual(values = c("Revenue ($K)" = "#1565C0", "Users" = "#E53935")) +
  scale_x_continuous(limits = c(1, 14)) +
  theme_minimal() +
  theme(legend.position = "none") +
  labs(title = "Redesign 2: Indexed Lines (Month 1 = 100)",
       x = "Month", y = "Index")

print(p_indexed)
ggsave("output/redesign2_indexed.png", p_indexed, width = 7, height = 4.5, dpi = 300)


# ── REDESIGN 3: Spaghetti → Small Multiples ──────────────
set.seed(33)
regions <- c("North", "South", "East", "West", "Central", "Coastal")

df_regions <- expand_grid(month = 1:12, region = regions) |>
  group_by(region) |>
  mutate(revenue = cumsum(rnorm(n(), 2, 6)) + runif(1, 30, 80)) |>
  ungroup()

p_facets <- ggplot(df_regions, aes(x = month, y = revenue)) +
  geom_line(color = "#1565C0", linewidth = 0.8) +
  geom_area(fill = "#1565C0", alpha = 0.06) +
  facet_wrap(~region, ncol = 3, scales = "fixed") +
  scale_x_continuous(breaks = c(1, 6, 12), labels = c("Jan", "Jun", "Dec")) +
  theme_minimal(base_size = 9) +
  theme(strip.text = element_text(face = "bold"),
        panel.grid.minor = element_blank()) +
  labs(title = "Redesign 3: Small Multiples Replace Spaghetti",
       x = NULL, y = "Revenue ($K)")

print(p_facets)
ggsave("output/redesign3_small_multiples.png", p_facets, width = 9, height = 5, dpi = 300)


# ── REDESIGN 4: Rainbow Scatter → Grey + Accent ──────────
set.seed(55)
n <- 120
df_scatter <- tibble(
  spend = runif(n, 10, 100),
  roi = 0.4 * spend + rnorm(n, 0, 12),
  category = sample(LETTERS[1:5], n, replace = TRUE),
  is_focal = category == "D"
)

p_grey_accent <- ggplot() +
  # Background: grey
  geom_point(data = filter(df_scatter, !is_focal),
             aes(x = spend, y = roi),
             color = "#CCCCCC", size = 1.5, alpha = 0.4) +
  # Focal: accent red
  geom_point(data = filter(df_scatter, is_focal),
             aes(x = spend, y = roi),
             color = "#E53935", size = 3, alpha = 0.85) +
  # Regression for focal only
  geom_smooth(data = filter(df_scatter, is_focal),
              aes(x = spend, y = roi),
              method = "lm", se = FALSE, color = "#E53935",
              linewidth = 0.8, linetype = "dashed") +
  theme_minimal() +
  labs(title = "Redesign 4: Grey + Accent (Category D Highlighted)",
       x = "Spend ($K)", y = "ROI (%)")

print(p_grey_accent)
ggsave("output/redesign4_grey_accent.png", p_grey_accent, width = 7, height = 5, dpi = 300)


# ── REDESIGN 5: Truncated Axis → Zero Baseline ───────────
df_scores <- tibble(
  year = as.character(2020:2024),
  score = c(96.2, 97.1, 97.8, 98.3, 99.0)
)

p_honest <- ggplot(df_scores, aes(x = year, y = score)) +
  geom_col(fill = "#1565C0", width = 0.5) +
  geom_text(aes(label = score), vjust = -0.5, size = 3.5, fontface = "bold") +
  geom_hline(yintercept = df_scores$score[1], linetype = "dashed", color = "grey60") +
  annotate("text", x = 5.4, y = df_scores$score[1],
           label = paste0("Baseline: ", df_scores$score[1]),
           size = 2.5, color = "grey50", hjust = 0) +
  coord_cartesian(ylim = c(0, 110)) +
  theme_minimal() +
  theme(panel.grid.major.x = element_blank()) +
  labs(title = "Redesign 5: Zero Baseline + Reference Line",
       x = NULL, y = "Score")

print(p_honest)
ggsave("output/redesign5_honest_axis.png", p_honest, width = 6, height = 4.5, dpi = 300)


cat("\n── All M07 plots saved to output/ ──\n")
