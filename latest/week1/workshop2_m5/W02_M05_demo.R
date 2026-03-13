# ============================================================
# Workshop 2 — Module 5: Faceting & Small Multiples
# R Demonstration Script — UNYT Tirana
# ============================================================
library(tidyverse)
library(patchwork)
dir.create("output", showWarnings = FALSE)

apps <- read_csv("googleplaystore.csv") |>
  filter(Type %in% c("Free", "Paid"),
         `Content Rating` %in% c("Everyone","Teen","Mature 17+","Everyone 10+")) |>
  mutate(Reviews = as.numeric(Reviews))

# ── 1. FACET_WRAP — one variable ─────────────────────────
top6 <- apps |> count(Category, sort = TRUE) |> slice_max(n, n = 6) |> pull(Category)
df_top6 <- apps |> filter(Category %in% top6, !is.na(Rating))

p_wrap <- ggplot(df_top6, aes(x = Rating)) +
  geom_histogram(bins = 25, fill = "#1565C0", color = "white", linewidth = 0.3) +
  facet_wrap(~Category, ncol = 3, scales = "fixed") +
  theme_minimal(base_size = 9) +
  theme(strip.text = element_text(face = "bold")) +
  labs(title = "Rating Distribution by Category", x = "Rating", y = "Count")

ggsave("output/facet_wrap.png", p_wrap, width = 9, height = 5, dpi = 300)

# ── 2. FACET_GRID — two variables ────────────────────────
p_grid <- ggplot(df_top6, aes(x = Rating)) +
  geom_histogram(bins = 20, fill = "#1565C0", color = "white", linewidth = 0.3) +
  facet_grid(Type ~ `Content Rating`, scales = "fixed") +
  theme_minimal(base_size = 8) +
  theme(strip.text = element_text(face = "bold", size = 7)) +
  labs(title = "Rating: Type × Content Rating", y = "Count")

ggsave("output/facet_grid.png", p_grid, width = 10, height = 5, dpi = 300)

# ── 3. FIXED vs FREE SCALES ─────────────────────────────
p_fixed <- ggplot(df_top6, aes(x = Rating)) +
  geom_histogram(bins = 20, fill = "#1565C0", color = "white") +
  facet_wrap(~Category, ncol = 3, scales = "fixed") +
  theme_minimal(base_size = 8) + labs(title = 'scales = "fixed"')

p_free <- ggplot(df_top6, aes(x = Rating)) +
  geom_histogram(bins = 20, fill = "#2E7D32", color = "white") +
  facet_wrap(~Category, ncol = 3, scales = "free_y") +
  theme_minimal(base_size = 8) + labs(title = 'scales = "free_y"')

ggsave("output/fixed_vs_free.png", p_fixed / p_free, width = 9, height = 8, dpi = 300)

# ── 4. FACET + SMOOTH ────────────────────────────────────
p_smooth <- df_top6 |>
  filter(Reviews > 0) |>
  ggplot(aes(x = Reviews, y = Rating)) +
  geom_point(alpha = 0.15, size = 0.5) +
  geom_smooth(method = "lm", color = "#E53935", linewidth = 0.8) +
  scale_x_log10(labels = scales::comma) +
  facet_wrap(~Category, ncol = 3, scales = "fixed") +
  theme_minimal(base_size = 8) +
  labs(title = "facet_wrap + geom_smooth: Per-Category Trend",
       x = "Reviews (log)", y = "Rating")

ggsave("output/facet_smooth.png", p_smooth, width = 9, height = 5, dpi = 300)

# ── 5. FACET vs PATCHWORK ────────────────────────────────
# Facet: same geom across panels
p_facet_demo <- ggplot(df_top6, aes(x = Rating)) +
  geom_density(fill = "#1565C0", alpha = 0.3) +
  facet_wrap(~Category, ncol = 3) + theme_minimal(base_size = 8) +
  labs(title = "Facet: same geom, different group")

# Patchwork: different geoms
p1 <- ggplot(apps, aes(x = fct_lump_n(Category, 8) |> fct_infreq())) +
  geom_bar(fill = "#1565C0") + coord_flip() + theme_minimal(base_size = 7) + labs(x = NULL, title = "(a) Bar")
p2 <- ggplot(apps |> filter(!is.na(Rating)), aes(x = Rating)) +
  geom_histogram(bins = 30, fill = "#2E7D32") + theme_minimal(base_size = 7) + labs(title = "(b) Histogram")
p3 <- ggplot(apps |> filter(!is.na(Rating), Reviews > 0), aes(x = Reviews, y = Rating)) +
  geom_point(alpha = 0.1, size = 0.3) + scale_x_log10() + theme_minimal(base_size = 7) + labs(title = "(c) Scatter")
p4 <- ggplot(apps |> filter(!is.na(Rating)), aes(x = Type, y = Rating, fill = Type)) +
  geom_boxplot(width = 0.5) + scale_fill_manual(values = c(Free="#1565C0",Paid="#E53935")) +
  theme_minimal(base_size = 7) + theme(legend.position = "none") + labs(title = "(d) Boxplot")

p_patchwork_demo <- (p1 | p2) / (p3 | p4) +
  plot_annotation(title = "Patchwork: different geoms, composed with |  and /")

ggsave("output/facet_vs_patchwork.png", p_facet_demo / p_patchwork_demo, width = 10, height = 10, dpi = 300)

cat("\n── All W02-M05 R plots saved ──\n")
