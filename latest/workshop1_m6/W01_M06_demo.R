# ============================================================
# Workshop 1 — Module 6: The Design Process
# R Demonstration Script
# Data Visualization for Data Scientists — UNYT Tirana
# ============================================================

library(tidyverse)
library(patchwork)
dir.create("output", showWarnings = FALSE)


# ── COMPLETE PIPELINE DEMO ─────────────────────────────────
# Using a small synthetic dataset to demonstrate all 5 steps

# 1. ACQUIRE ─────────────────────────────────────────────────
# Simulating quarterly revenue data (in production: read_csv())
df_raw <- tibble(
  quarter = c("Q1", "Q2", "Q3", "Q4"),
  revenue = c(245, 310, 280, 395),
  region  = rep("East", 4)
)
cat("── Step 1: Acquire ──\n")
print(df_raw)

# 2. PARSE ───────────────────────────────────────────────────
# Ensure proper types (quarter as ordered factor)
df_parsed <- df_raw |>
  mutate(quarter = factor(quarter, levels = c("Q1","Q2","Q3","Q4"), ordered = TRUE))
cat("\n── Step 2: Parse ──\n")
str(df_parsed)

# 3. FILTER ──────────────────────────────────────────────────
# No filtering needed on this small dataset; in practice:
# df_filtered <- df_parsed |> filter(region == "East", revenue > 0)
df_filtered <- df_parsed

# 4. MINE ────────────────────────────────────────────────────
max_q <- df_filtered |> slice_max(revenue, n = 1)
cat("\n── Step 4: Mine ──\n")
cat("Best quarter:", max_q$quarter, "with $", max_q$revenue, "K\n")

# 5. REPRESENT ───────────────────────────────────────────────
p_final <- ggplot(df_filtered, aes(x = quarter, y = revenue)) +
  geom_col(aes(fill = quarter == max_q$quarter), width = 0.5, show.legend = FALSE) +
  scale_fill_manual(values = c("FALSE" = "#1565C0", "TRUE" = "#E53935")) +
  geom_text(aes(label = paste0("$", revenue, "K")),
            vjust = -0.5, size = 3.5, fontface = "bold") +
  coord_cartesian(ylim = c(0, 450)) +
  theme_minimal(base_size = 11) +
  theme(
    plot.title = element_text(size = 14, face = "bold"),
    plot.subtitle = element_text(size = 10, color = "grey50"),
    plot.caption = element_text(size = 8, face = "italic", hjust = 0),
    panel.grid.major.x = element_blank(),
    panel.grid.minor = element_blank()
  ) +
  labs(
    title = "Q4 Revenue Highest at $395K",
    subtitle = "Quarterly revenue, East region, 2024",
    caption = "Source: Internal sales database",
    x = NULL, y = "Revenue ($K)"
  )

print(p_final)
ggsave("output/pipeline_complete.png", p_final, width = 6, height = 4.5, dpi = 300)
ggsave("output/pipeline_complete.pdf", p_final, width = 6, height = 4.5)


# ── ITERATIVE REFINEMENT: 3 STAGES ────────────────────────
set.seed(42)
cats <- c("Tools", "Finance", "Games", "Social", "Photo")
vals <- c(42, 58, 35, 67, 51)
df_iter <- tibble(cat = cats, val = vals)

# Stage 1: Sketch
p1 <- ggplot(df_iter, aes(x = cat, y = val)) +
  geom_col() +
  labs(title = "Stage 1: Sketch")

# Stage 2: Draft
p2 <- ggplot(df_iter, aes(x = fct_reorder(cat, val), y = val)) +
  geom_col(fill = "#64B5F6", width = 0.6) +
  coord_flip() +
  labs(title = "Stage 2: Draft", x = NULL)

# Stage 3: Polished
p3 <- ggplot(df_iter, aes(x = fct_reorder(cat, val), y = val,
                            fill = val == max(val))) +
  geom_col(width = 0.5, show.legend = FALSE) +
  scale_fill_manual(values = c("FALSE" = "#1565C0", "TRUE" = "#E53935")) +
  geom_text(aes(label = val), hjust = -0.3, size = 3.5, fontface = "bold") +
  coord_flip() +
  theme_minimal() +
  theme(panel.grid.major.y = element_blank()) +
  labs(title = "Stage 3: Polished", x = NULL, y = "Count")

p_iteration <- p1 + p2 + p3 +
  plot_annotation(title = "Iterative Refinement: Sketch → Draft → Polished")

print(p_iteration)
ggsave("output/iteration_stages.png", p_iteration, width = 12, height = 4, dpi = 300)


# ── AUDIENCE ADAPTATION ───────────────────────────────────
# Executive version: 1 chart, grey + accent
p_exec <- ggplot(df_iter, aes(x = fct_reorder(cat, val), y = val,
                                fill = cat == "Games")) +
  geom_col(width = 0.5, show.legend = FALSE) +
  scale_fill_manual(values = c("FALSE" = "#BBBBBB", "TRUE" = "#E53935")) +
  geom_text(aes(label = val), hjust = -0.3, size = 4, fontface = "bold") +
  coord_flip() +
  theme_minimal(base_size = 12) +
  theme(
    panel.grid.major.y = element_blank(),
    plot.title = element_text(size = 16, face = "bold")
  ) +
  labs(title = "Games Lead with 67 Downloads",
       subtitle = "Top 5 categories, Google Play Store",
       x = NULL, y = "Count",
       caption = "Source: Kaggle | Executive Summary")

# Analyst version: 4-panel dashboard
p_a1 <- ggplot(df_iter, aes(x = fct_reorder(cat, val), y = val)) +
  geom_col(fill = "#1565C0", width = 0.5) + coord_flip() +
  labs(title = "(a) Counts", x = NULL, y = "n") + theme_minimal(base_size = 8)

p_a2 <- ggplot(tibble(x = rnorm(100, 4, 0.5)), aes(x = x)) +
  geom_histogram(fill = "#2E7D32", bins = 20, color = "white") +
  labs(title = "(b) Rating Distribution", x = "Rating") + theme_minimal(base_size = 8)

p_a3 <- ggplot(df_iter, aes(x = fct_reorder(cat, val), y = runif(5, 3.5, 4.5))) +
  geom_point(size = 3, color = "#E53935") +
  coord_flip() + labs(title = "(c) Mean Ratings", x = NULL, y = "Rating") +
  theme_minimal(base_size = 8)

p_a4 <- ggplot(tibble(x = 1:12, y = cumsum(rnorm(12, 5, 8)) + 50),
               aes(x = x, y = y)) +
  geom_line(color = "#1565C0", linewidth = 1) +
  labs(title = "(d) Monthly Trend", x = "Month", y = "Count") +
  theme_minimal(base_size = 8)

p_analyst <- (p_a1 | p_a2) / (p_a3 | p_a4) +
  plot_annotation(title = "Analyst Dashboard: Full Detail")

ggsave("output/exec_version.png", p_exec, width = 7, height = 5, dpi = 300)
ggsave("output/analyst_version.png", p_analyst, width = 10, height = 7, dpi = 300)

cat("\n── All M06 plots saved to output/ ──\n")
