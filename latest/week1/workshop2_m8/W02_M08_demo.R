# ============================================================
# Workshop 2 — Module 8: labs(), Annotations & Storytelling
# R Demonstration Script — UNYT Tirana
# ============================================================
library(tidyverse)
library(patchwork)
dir.create("output", showWarnings = FALSE)

# ── 1. LABS() — full label set ────────────────────────────
p_labs <- ggplot(mpg, aes(x = displ, y = hwy, color = factor(cyl))) +
  geom_point(alpha = 0.6, size = 2) +
  labs(
    title = "Fuel Economy Decreases with Engine Size",
    subtitle = "Highway MPG vs displacement, coloured by cylinder count",
    caption = "Source: mpg dataset (ggplot2) | UNYT Data Visualization Course",
    x = "Displacement (litres)",
    y = "Highway MPG",
    color = "Cylinders"
  ) +
  scale_color_brewer(palette = "Set2") +
  theme_minimal(base_size = 11) +
  theme(
    plot.title = element_text(face = "bold", size = 14),
    plot.subtitle = element_text(color = "grey50"),
    plot.caption = element_text(face = "italic", hjust = 0, size = 8)
  )
ggsave("output/labs_full.png", p_labs, width = 7, height = 5, dpi = 300)

# ── 2. ANNOTATION TYPES ──────────────────────────────────
set.seed(33)
ts <- tibble(month = 1:12, revenue = cumsum(rnorm(12, 5, 8)) + 200)
mean_rev <- mean(ts$revenue)
peak <- ts |> slice_max(revenue, n = 1)

p_annotated <- ggplot(ts, aes(x = month, y = revenue)) +
  geom_line(color = "#1565C0", linewidth = 1.2) +
  geom_point(color = "#1565C0", size = 2) +
  # Reference line (mean)
  geom_hline(yintercept = mean_rev, linetype = "dashed", color = "grey50") +
  annotate("text", x = 12.5, y = mean_rev, label = paste0("Mean: $", round(mean_rev), "K"),
           size = 3, color = "grey50", fontface = "bold", hjust = 0) +
  # Target band
  annotate("rect", xmin = -Inf, xmax = Inf, ymin = 210, ymax = 230,
           alpha = 0.08, fill = "#2E7D32") +
  # Event marker
  geom_vline(xintercept = 6.5, linetype = "dotted", color = "#E65100") +
  annotate("text", x = 7, y = min(ts$revenue) - 3, label = "H1 | H2",
           size = 3, color = "#E65100") +
  # Peak callout
  annotate("text", x = peak$month + 1.5, y = peak$revenue + 10,
           label = paste0("Peak: $", round(peak$revenue), "K"),
           fontface = "bold", color = "#E53935", size = 3.5) +
  annotate("segment", x = peak$month + 1, y = peak$revenue + 8,
           xend = peak$month + 0.2, yend = peak$revenue + 1,
           arrow = arrow(length = unit(0.15, "cm")), color = "#E53935") +
  theme_minimal() +
  labs(title = "Monthly Revenue with Annotations",
       subtitle = "All four annotation types: text, hline, band, vline",
       x = "Month", y = "Revenue ($K)")

ggsave("output/annotations.png", p_annotated, width = 8, height = 5, dpi = 300)

# ── 3. STORYTELLING LAYERS — progressive build ───────────
set.seed(77)
ts2 <- tibble(year = 2015:2024,
              revenue = c(120, 135, 128, 142, 155, 170, 145, 180, 195, 220))

p1 <- ggplot(ts2, aes(x = year, y = revenue)) + geom_line(color = "#1565C0", linewidth = 1.2) +
  geom_point(color = "#1565C0", size = 2) + theme_minimal() + labs(title = "1. Show the data")

p2 <- p1 + geom_smooth(method = "lm", se = FALSE, color = "grey50", linewidth = 0.8) +
  labs(title = "2. + Trend line")

p3 <- p2 + geom_vline(xintercept = 2020, linetype = "dotted", color = "#E53935") +
  annotate("text", x = 2020.3, y = 155, label = "COVID", color = "#E53935",
           fontface = "bold", size = 3) +
  labs(title = "3. + Key events")

p4 <- p3 + labs(title = "Revenue Recovered to Record $220M in 2024",
                subtitle = "Annual revenue with COVID impact and recovery trend")

p_story <- (p1 | p2) / (p3 | p4) +
  plot_annotation(title = "Storytelling Layers: Progressive Reveal")
ggsave("output/storytelling.png", p_story, width = 10, height = 7, dpi = 300)

# ── 4. ANNOTATED BAR — complete example ──────────────────
df <- mpg |> count(class) |> mutate(class = fct_reorder(class, n))
mean_n <- mean(df$n)

p_final <- df |>
  mutate(highlight = class == "suv") |>
  ggplot(aes(x = class, y = n, fill = highlight)) +
  geom_col(width = 0.5, show.legend = FALSE) +
  geom_text(aes(label = n), hjust = -0.2, size = 3.5, fontface = "bold") +
  scale_fill_manual(values = c("TRUE" = "#E53935", "FALSE" = "#BBBBBB")) +
  geom_hline(yintercept = mean_n, linetype = "dashed", color = "grey50") +
  coord_flip() +
  labs(title = "SUV Leads with 62 Models",
       subtitle = "Vehicle count by class, mpg dataset",
       caption = "Source: ggplot2::mpg | UNYT Data Visualization Course",
       x = NULL, y = NULL) +
  theme_minimal(base_size = 11) +
  theme(
    plot.title = element_text(face = "bold", size = 14),
    plot.subtitle = element_text(color = "grey50"),
    plot.caption = element_text(face = "italic", hjust = 0),
    panel.grid.major.y = element_blank()
  )
ggsave("output/annotated_bar.png", p_final, width = 7, height = 5, dpi = 300)
ggsave("output/annotated_bar.pdf", p_final, width = 7, height = 5)

cat("\n── All W02-M08 R plots saved ──\n")
