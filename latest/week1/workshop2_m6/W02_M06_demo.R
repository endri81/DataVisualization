# ============================================================
# Workshop 2 — Module 6: Themes & Publication-Quality Styling
# R Demonstration Script — UNYT Tirana
# ============================================================
library(tidyverse)
library(patchwork)
dir.create("output", showWarnings = FALSE)

# ── 1. FIVE BUILT-IN THEMES ─────────────────────────────
p_base <- ggplot(mpg, aes(x = displ, y = hwy)) + geom_point(alpha = 0.5, size = 1.5)

p_themes <- (
  (p_base + theme_gray() + labs(title = "theme_gray()")) |
  (p_base + theme_minimal() + labs(title = "theme_minimal()")) |
  (p_base + theme_classic() + labs(title = "theme_classic()"))
) / (
  (p_base + theme_bw() + labs(title = "theme_bw()")) |
  (p_base + theme_void() + labs(title = "theme_void()")) |
  (p_base + theme_dark() + labs(title = "theme_dark()"))
)
ggsave("output/five_themes.png", p_themes, width = 12, height = 7, dpi = 300)

# ── 2. BEFORE vs AFTER ──────────────────────────────────
df <- mpg |> count(class, sort = TRUE) |> mutate(class = fct_reorder(class, n))

p_before <- ggplot(df, aes(x = class, y = n)) +
  geom_col(fill = "steelblue") +
  coord_flip() +
  labs(title = "BEFORE: Defaults")

p_after <- ggplot(df, aes(x = class, y = n, fill = class == "suv")) +
  geom_col(width = 0.5, show.legend = FALSE) +
  scale_fill_manual(values = c("FALSE" = "#1565C0", "TRUE" = "#E53935")) +
  geom_text(aes(label = n), hjust = -0.2, size = 3.5, fontface = "bold") +
  coord_flip() +
  theme_minimal(base_size = 11) +
  theme(
    plot.title = element_text(face = "bold", size = 14),
    panel.grid.major.y = element_blank(),
    panel.grid.minor = element_blank(),
    axis.title = element_blank()
  ) +
  labs(title = "AFTER: Custom theme")

ggsave("output/before_after.png", p_before + p_after, width = 10, height = 5, dpi = 300)

# ── 3. CUSTOM THEME FUNCTION ────────────────────────────
theme_unyt <- function(base_size = 11) {
  theme_minimal(base_size = base_size) +
    theme(
      plot.title = element_text(face = "bold", size = rel(1.3), margin = margin(b = 8)),
      plot.subtitle = element_text(color = "grey50", margin = margin(b = 12)),
      plot.caption = element_text(face = "italic", size = rel(0.8), hjust = 0, color = "grey60"),
      panel.grid.major.x = element_blank(),
      panel.grid.minor = element_blank(),
      axis.title = element_text(face = "bold"),
      legend.position = "bottom",
      legend.title = element_text(face = "bold"),
      plot.margin = margin(t = 10, r = 15, b = 10, l = 10)
    )
}

p_branded <- ggplot(mpg, aes(x = displ, y = hwy, color = factor(cyl))) +
  geom_point(alpha = 0.6, size = 2) +
  geom_smooth(method = "lm", se = FALSE, linewidth = 0.8) +
  scale_color_brewer(palette = "Set2") +
  labs(
    title = "Engine Size vs Fuel Economy",
    subtitle = "Coloured by cylinder count, with per-group trend lines",
    caption = "Source: mpg dataset | UNYT Data Visualization Course",
    x = "Displacement (L)", y = "Highway MPG", color = "Cylinders"
  ) +
  theme_unyt()

ggsave("output/branded_theme.png", p_branded, width = 7, height = 5, dpi = 300)
ggsave("output/branded_theme.pdf", p_branded, width = 7, height = 5, device = cairo_pdf)

# ── 4. GGTHEMES ──────────────────────────────────────────
# install.packages("ggthemes")
# library(ggthemes)
# p_base + theme_economist() + scale_color_economist()
# p_base + theme_wsj()
# p_base + theme_fivethirtyeight()
# p_base + theme_tufte()

# ── 5. EXPORT DEMO ──────────────────────────────────────
ggsave("output/export_pdf.pdf", p_branded, width = 7, height = 5, device = cairo_pdf)
ggsave("output/export_png_300.png", p_branded, width = 7, height = 5, dpi = 300)
ggsave("output/export_png_150.png", p_branded, width = 7, height = 5, dpi = 150)
ggsave("output/export_svg.svg", p_branded, width = 7, height = 5)

cat("\n── All W02-M06 R plots saved ──\n")
cat("Compare file sizes:\n")
cat(system("ls -lh output/export_*", intern = TRUE), sep = "\n")
