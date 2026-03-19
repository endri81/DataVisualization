# ============================================================
# Workshop 6 — Module 2: Line Charts — Theory & Best Practices
# Integrated R Script — UNYT Tirana
# ============================================================
library(tidyverse); library(patchwork); dir.create("output", showWarnings = FALSE)

# ── SIMULATED DATA: 3 product revenue series ─────────────
set.seed(42)
months <- seq(as.Date("2020-01-01"), as.Date("2023-12-01"), by = "month")
n <- length(months)

products <- tibble(
  date = rep(months, 3),
  revenue = c(
    100 * cumprod(1 + rnorm(n, 0.005, 0.03)),  # Product A: steady
    500 * cumprod(1 + rnorm(n, 0.003, 0.04)),  # Product B: high start
     50 * cumprod(1 + rnorm(n, 0.008, 0.02))   # Product C: fast growth
  ),
  product = rep(c("Product A", "Product B", "Product C"), each = n))

# ── 1. ASPECT RATIO: BANKING TO 45° ─────────────────────
# Same data, three aspect ratios
ts_data <- products |> filter(product == "Product A")

p_wide <- ggplot(ts_data, aes(x = date, y = revenue)) +
  geom_line(color = "#E53935", linewidth = 1) +
  theme_minimal(base_size = 8) +
  labs(title = "(a) Too wide: trend exaggerated")

p_bank <- ggplot(ts_data, aes(x = date, y = revenue)) +
  geom_line(color = "#1565C0", linewidth = 1) +
  theme_minimal(base_size = 8) +
  labs(title = "(b) Banked to ~45°: optimal")

p_tall <- ggplot(ts_data, aes(x = date, y = revenue)) +
  geom_line(color = "#E65100", linewidth = 1) +
  theme_minimal(base_size = 8) +
  labs(title = "(c) Too tall: noise exaggerated")

# Use different widths to simulate aspect ratio
ggsave("output/aspect_wide.png", p_wide, width = 14, height = 2, dpi = 300)
ggsave("output/aspect_banked.png", p_bank, width = 7, height = 3, dpi = 300)
ggsave("output/aspect_tall.png", p_tall, width = 4, height = 5, dpi = 300)

# ── 2. DUAL Y-AXIS PROBLEM ──────────────────────────────
# Simulated temperature and sales data
temp <- 20 + 10 * sin(2 * pi * (1:n) / 12) + rnorm(n, 0, 1)
sales <- 50000 + 20000 * sin(2 * pi * (1:n) / 12 + 0.5) + rnorm(n, 0, 3000)
dual_df <- tibble(date = months, temperature = temp, sales = sales)

# BAD: dual y-axes
p_dual_bad <- ggplot(dual_df, aes(x = date)) +
  geom_line(aes(y = temperature), color = "#E53935", linewidth = 1) +
  geom_line(aes(y = sales / 1000), color = "#1565C0", linewidth = 1) +
  scale_y_continuous(
    name = "Temperature (°C)",
    sec.axis = sec_axis(~. * 1000, name = "Sales (EUR)")) +
  theme_minimal() +
  labs(title = "BAD: Dual Y-Axes (arbitrary relationship)")

# GOOD: separate panels
p_dual_good1 <- ggplot(dual_df, aes(x = date, y = temperature)) +
  geom_line(color = "#E53935", linewidth = 1) +
  theme_minimal(base_size = 8) +
  labs(title = "(a) Temperature (°C)", y = "°C")

p_dual_good2 <- ggplot(dual_df, aes(x = date, y = sales / 1000)) +
  geom_line(color = "#1565C0", linewidth = 1) +
  theme_minimal(base_size = 8) +
  labs(title = "(b) Sales (EUR thousands)", y = "EUR (000)")

ggsave("output/dual_bad.png", p_dual_bad, width = 9, height = 5, dpi = 300)
ggsave("output/dual_good.png", p_dual_good1 / p_dual_good2, width = 9, height = 7, dpi = 300)

# ── 3. INDEXED LINES ────────────────────────────────────
# Raw vs indexed comparison
p_raw <- ggplot(products, aes(x = date, y = revenue, color = product)) +
  geom_line(linewidth = 1) +
  scale_color_manual(values = c("#1565C0", "#E53935", "#2E7D32")) +
  theme_minimal() +
  labs(title = "Raw Values: B dominates visually", y = "Revenue (EUR)")

products_idx <- products |>
  group_by(product) |>
  mutate(indexed = revenue / first(revenue) * 100) |>
  ungroup()

p_indexed <- ggplot(products_idx, aes(x = date, y = indexed, color = product)) +
  geom_line(linewidth = 1) +
  geom_hline(yintercept = 100, linetype = "dotted", color = "#888") +
  scale_color_manual(values = c("#1565C0", "#E53935", "#2E7D32")) +
  theme_minimal() +
  labs(title = "Indexed to 100: C outperforms", y = "Index (start = 100)")

ggsave("output/indexed.png", p_raw | p_indexed, width = 12, height = 5, dpi = 300)

# ── 4. GREY + ACCENT STRATEGY ───────────────────────────
p_spaghetti <- ggplot(products, aes(x = date, y = revenue, color = product)) +
  geom_line(linewidth = 1) +
  theme_minimal() +
  labs(title = "All coloured: which is the story?")

p_accent <- ggplot(products, aes(x = date, y = revenue, group = product)) +
  geom_line(color = "#DDDDDD", linewidth = 0.8) +
  geom_line(data = products |> filter(product == "Product C"),
    color = "#E53935", linewidth = 2) +
  geom_text(data = products |> filter(product == "Product C", date == max(date)),
    aes(label = " Product C"), hjust = 0, color = "#E53935",
    fontface = "bold", size = 3) +
  theme_minimal() +
  labs(title = "Grey+accent: story is clear (C outperforms)")

ggsave("output/grey_accent.png", p_spaghetti | p_accent, width = 12, height = 5, dpi = 300)

# ── 5. DIRECT LABELS + EVENT ANNOTATIONS ────────────────
p_annotated <- ggplot(products_idx, aes(x = date, y = indexed, group = product)) +
  geom_line(color = "#DDDDDD", linewidth = 0.8) +
  geom_line(data = products_idx |> filter(product == "Product C"),
    color = "#E53935", linewidth = 2) +
  # Direct label at end of line
  geom_text(data = products_idx |>
    group_by(product) |> filter(date == max(date)),
    aes(label = product, color = product == "Product C"),
    hjust = 0, nudge_x = 10, size = 2.5, fontface = "bold",
    show.legend = FALSE) +
  scale_color_manual(values = c("TRUE" = "#E53935", "FALSE" = "#AAAAAA")) +
  # Event annotation
  geom_vline(xintercept = as.Date("2020-03-11"),
    linetype = "dashed", color = "#888888", linewidth = 0.5) +
  annotate("text", x = as.Date("2020-04-01"),
    y = max(products_idx$indexed) * 0.95,
    label = "WHO declares\npandemic", size = 2.5,
    hjust = 0, color = "#888888") +
  geom_hline(yintercept = 100, linetype = "dotted", color = "#888") +
  theme_minimal() +
  labs(title = "Direct Labels + Event Annotation",
    subtitle = "Indexed to 100, grey+accent, pandemic marker",
    y = "Index (start = 100)", x = NULL) +
  theme(legend.position = "none") +
  coord_cartesian(xlim = c(min(months), max(months) + 90))  # room for labels

ggsave("output/annotated.png", p_annotated, width = 10, height = 5, dpi = 300)

# ── 6. LOG SCALE FOR GROWTH COMPARISON ───────────────────
p_log <- ggplot(products, aes(x = date, y = revenue, color = product)) +
  geom_line(linewidth = 1) +
  scale_y_log10(labels = scales::comma) +
  scale_color_manual(values = c("#1565C0", "#E53935", "#2E7D32")) +
  theme_minimal() +
  labs(title = "Log Scale: Constant growth = straight line",
    y = "Revenue (log scale)")

ggsave("output/log_scale.png", p_log, width = 8, height = 5, dpi = 300)

cat("\n── All W06-M02 R outputs saved ──\n")
cat("Figures: aspect ratio (3 versions), dual axes (bad + good),\n")
cat("  indexed (raw vs indexed), grey+accent, annotated, log scale\n")
