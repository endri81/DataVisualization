# ============================================================
# Workshop 1 — Module 3: Visual Perception & Pre-Attentive Attributes
# R Demonstration Script
# Data Visualization for Data Scientists — UNYT Tirana
# ============================================================

# ── 0. Setup ────────────────────────────────────────────────
library(tidyverse)
library(patchwork)
dir.create("output", showWarnings = FALSE)


# ── 1. Pre-Attentive Pop-Out Demo ──────────────────────────
# Generate a scatter field where one point pops out by colour

set.seed(42)
n <- 80
df_pop <- tibble(
  x = runif(n, 0, 10),
  y = runif(n, 0, 8),
  target = c(rep("distractor", 36), "target", rep("distractor", n - 37))
)

# Colour pop-out: target is immediately visible
p_popout <- ggplot(df_pop, aes(x = x, y = y, color = target, size = target)) +
  geom_point(alpha = 0.8) +
  scale_color_manual(values = c(distractor = "#1565C0", target = "#E53935")) +
  scale_size_manual(values = c(distractor = 3, target = 5)) +
  theme_void() +
  theme(legend.position = "none") +
  labs(title = "Pre-Attentive Color Pop-Out",
       subtitle = "The red point is detected in <200 ms")

print(p_popout)
ggsave("output/preattentive_popout.png", p_popout,
       width = 6, height = 4, dpi = 150)


# ── 2. Conjunction Failure ─────────────────────────────────
# Red square among red circles + blue squares = serial search

set.seed(42)
n_conj <- 60
df_conj <- tibble(
  x = runif(n_conj, 0, 10),
  y = runif(n_conj, 0, 8),
  colour = sample(c("red", "blue"), n_conj, replace = TRUE),
  shape_type = sample(c("circle", "square"), n_conj, replace = TRUE)
)
# Force one target: red square at position 33
df_conj$colour[33] <- "red"
df_conj$shape_type[33] <- "square"

p_conj <- ggplot(df_conj, aes(x = x, y = y,
                               color = colour, shape = shape_type)) +
  geom_point(size = 3, alpha = 0.8) +
  scale_color_manual(values = c(red = "#E53935", blue = "#1565C0")) +
  scale_shape_manual(values = c(circle = 16, square = 15)) +
  theme_void() +
  theme(legend.position = "none") +
  labs(title = "Conjunction Search: No Pop-Out",
       subtitle = "Find the red square — requires serial scanning (~50 ms/item)")

print(p_conj)
ggsave("output/conjunction_search.png", p_conj,
       width = 6, height = 4, dpi = 150)


# ── 3. Gestalt: Proximity via Faceting ─────────────────────
# Faceting physically separates groups, leveraging proximity

set.seed(7)
df_gestalt <- tibble(
  x = rnorm(150),
  y = rnorm(150),
  group = rep(LETTERS[1:3], each = 50)
)

p_proximity <- ggplot(df_gestalt, aes(x = x, y = y)) +
  geom_point(color = "#1565C0", alpha = 0.6, size = 2) +
  facet_wrap(~group, ncol = 3) +
  theme_minimal(base_size = 10) +
  theme(legend.position = "none",
        strip.text = element_text(face = "bold")) +
  labs(title = "Gestalt Proximity via Faceting",
       subtitle = "Physical separation creates perceptual groups")

print(p_proximity)
ggsave("output/gestalt_faceting.png", p_proximity,
       width = 9, height = 3.5, dpi = 150)


# ── 4. Gestalt: Enclosure with annotate("rect") ───────────
# Highlight a region on a time series using a shaded band

set.seed(99)
df_ts <- tibble(
  date = seq(as.Date("2023-01-01"), by = "month", length.out = 12),
  value = cumsum(rnorm(12, 3, 5)) + 50
)

p_enclosure <- ggplot(df_ts, aes(x = date, y = value)) +
  # Enclosure: shaded band for Q2

  annotate("rect",
           xmin = as.Date("2023-04-01"), xmax = as.Date("2023-06-30"),
           ymin = -Inf, ymax = Inf,
           fill = "#E3F2FD", alpha = 0.6) +
  annotate("text",
           x = as.Date("2023-05-15"), y = max(df_ts$value) + 2,
           label = "Q2 Promotion Period", fontface = "bold",
           size = 3, color = "#1565C0") +
  geom_line(color = "#1565C0", linewidth = 1) +
  geom_point(color = "#1565C0", size = 2) +
  theme_minimal(base_size = 10) +
  labs(title = "Gestalt Enclosure: Shaded Band Highlights a Period",
       x = NULL, y = "Revenue ($K)")

print(p_enclosure)
ggsave("output/gestalt_enclosure.png", p_enclosure,
       width = 7, height = 4, dpi = 150)


# ── 5. Multi-Channel Encoding ─────────────────────────────
# x = position, y = position, color = nominal, size = quantitative

set.seed(55)
n_enc <- 80
df_enc <- tibble(
  spend = runif(n_enc, 10, 100),
  roi = 0.4 * spend + rnorm(n_enc, 0, 12),
  category = sample(c("A", "B", "C"), n_enc, replace = TRUE),
  budget = runif(n_enc, 20, 200)
)

p_encoding <- ggplot(df_enc, aes(x = spend, y = roi,
                                  color = category, size = budget)) +
  geom_point(alpha = 0.6) +
  scale_color_manual(values = c(A = "#1565C0", B = "#E53935", C = "#2E7D32")) +
  scale_size_continuous(range = c(1.5, 8)) +
  theme_minimal(base_size = 10) +
  labs(title = "Four Encoding Channels: x, y, color, size",
       x = "Marketing Spend ($K)", y = "ROI (%)",
       color = "Category", size = "Budget ($K)")

print(p_encoding)
ggsave("output/multi_channel.png", p_encoding,
       width = 7, height = 5, dpi = 150)


# ── 6. Cleveland & McGill: Channel Comparison ─────────────
# Same data encoded three ways to show accuracy degradation

vals <- c(A = 42, B = 45, C = 43, D = 44)

# Position (most accurate)
p_pos <- ggplot(tibble(cat = names(vals), val = vals),
                aes(x = cat, y = val)) +
  geom_col(fill = "#1565C0", width = 0.5) +
  coord_cartesian(ylim = c(0, 50)) +
  theme_minimal(base_size = 9) +
  labs(title = "Position (Best)", y = "Value", x = NULL)

# Area (less accurate)
p_area <- ggplot(tibble(cat = names(vals), val = vals),
                 aes(x = cat, y = 1)) +
  geom_point(aes(size = val), color = "#E53935", alpha = 0.7) +
  scale_size_area(max_size = 15) +
  theme_void(base_size = 9) +
  theme(axis.text.x = element_text()) +
  labs(title = "Area (Worse)", x = NULL)

# Color saturation (worst)
p_col <- ggplot(tibble(cat = names(vals), val = vals),
                aes(x = cat, y = 1, fill = val)) +
  geom_tile(height = 2, width = 0.8) +
  scale_fill_gradient(low = "#E3F2FD", high = "#1565C0") +
  theme_void(base_size = 9) +
  theme(axis.text.x = element_text(),
        legend.position = "none") +
  labs(title = "Saturation (Worst)", x = NULL)

p_channels <- p_pos | p_area | p_col
p_channels <- p_channels +
  plot_annotation(
    title = "Cleveland & McGill: Channel Accuracy Degrades",
    subtitle = "Values: A=42, B=45, C=43, D=44 — can you tell?"
  )

print(p_channels)
ggsave("output/channel_comparison.png", p_channels,
       width = 10, height = 4, dpi = 150)


cat("\n── All M03 plots saved to output/ ──\n")
