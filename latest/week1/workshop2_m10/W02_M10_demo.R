# ============================================================
# Workshop 2 — Module 10: Lab — Building a Visual Report
# R Demonstration Script — UNYT Tirana
# ============================================================
library(tidyverse)
library(patchwork)
library(scales)
dir.create("output", showWarnings = FALSE)

apps <- read_csv("googleplaystore.csv") |>
  filter(Type %in% c("Free", "Paid")) |>
  mutate(Reviews = as.numeric(Reviews),
         Last_Updated = mdy(`Last Updated`),
         Year = year(Last_Updated))

# ── (a) BAR: Top 8 categories ────────────────────────────
p_bar <- apps |> count(Category, sort = TRUE) |> slice_max(n, n = 8) |>
  mutate(Category = fct_reorder(Category, n), hl = Category == "FAMILY") |>
  ggplot(aes(x = Category, y = n, fill = hl)) +
  geom_col(width = 0.5, show.legend = FALSE) +
  geom_text(aes(label = comma(n)), hjust = -0.15, size = 3, fontface = "bold") +
  scale_fill_manual(values = c("TRUE" = "#1565C0", "FALSE" = "#BBBBBB")) +
  coord_flip() + theme_minimal() +
  theme(panel.grid.major.y = element_blank()) +
  labs(title = "(a) FAMILY Leads with 1,832 Apps", x = NULL, y = NULL)

# ── (b) HISTOGRAM: Rating distribution ───────────────────
mean_r <- mean(apps$Rating, na.rm = TRUE)
p_hist <- ggplot(apps, aes(x = Rating)) +
  geom_histogram(bins = 30, fill = "#1565C0", color = "white", linewidth = 0.3) +
  geom_vline(xintercept = mean_r, color = "#E53935", linewidth = 1, linetype = "dashed") +
  annotate("text", x = mean_r + 0.1, y = Inf, vjust = 1.5,
           label = paste0("Mean: ", round(mean_r, 2)), color = "#E53935",
           fontface = "bold", size = 3) +
  theme_minimal() + labs(title = "(b) Rating Distribution", x = "Rating", y = "Count")

# ── (c) SCATTER: Reviews vs Rating ───────────────────────
p_scatter <- apps |> filter(!is.na(Rating), Reviews > 0) |>
  ggplot(aes(x = Reviews, y = Rating, color = Type)) +
  geom_point(alpha = 0.3, size = 0.8) +
  scale_x_log10(labels = comma) +
  scale_color_manual(values = c(Free = "#1565C0", Paid = "#E53935")) +
  theme_minimal() + labs(title = "(c) Reviews vs Rating", x = "Reviews (log)", y = "Rating")

# ── (d) BOXPLOT: Rating by Type ──────────────────────────
p_box <- apps |> filter(!is.na(Rating)) |>
  ggplot(aes(x = Type, y = Rating, fill = Type)) +
  geom_boxplot(width = 0.5, notch = TRUE, outlier.alpha = 0.1) +
  stat_summary(fun = mean, geom = "point", shape = 18, size = 3, color = "#E53935") +
  scale_fill_manual(values = c(Free = "#BBDEFB", Paid = "#FFCDD2")) +
  theme_minimal() + theme(legend.position = "none") +
  labs(title = "(d) Rating by Type", y = "Rating", x = NULL)

# ── (e) LINE: Apps per year ──────────────────────────────
p_line <- apps |> filter(Year >= 2010, Year <= 2018) |> count(Year, Type) |>
  ggplot(aes(x = Year, y = n, color = Type)) +
  geom_line(linewidth = 1.2) + geom_point(size = 2) +
  scale_color_manual(values = c(Free = "#1565C0", Paid = "#E53935")) +
  theme_minimal() + theme(legend.position = "bottom") +
  labs(title = "(e) Apps Added per Year", x = "Year", y = "Count")

# ── (f) STACKED: Content Rating × Type ───────────────────
p_stacked <- apps |>
  filter(`Content Rating` %in% c("Everyone","Teen","Mature 17+","Everyone 10+")) |>
  ggplot(aes(x = `Content Rating`, fill = Type)) +
  geom_bar(position = "stack") +
  scale_fill_manual(values = c(Free = "#1565C0", Paid = "#E53935")) +
  theme_minimal() + theme(axis.text.x = element_text(angle = 30, hjust = 1, size = 7)) +
  labs(title = "(f) Content Rating × Type", x = NULL, y = "Count")

# ── COMPOSE DASHBOARD ────────────────────────────────────
dashboard <- (p_bar | p_hist | p_scatter) / (p_box | p_line | p_stacked) +
  plot_annotation(
    title = "Google Play Store: Complete Visual Report",
    subtitle = "Workshop 2 Lab — Grammar of Graphics Applied",
    caption = "Source: Kaggle | UNYT Data Visualization Course | Prof.Asoc. Endri Raco"
  )

ggsave("output/W02_M10_report.pdf", dashboard, width = 14, height = 9, device = cairo_pdf)
ggsave("output/W02_M10_report.png", dashboard, width = 14, height = 9, dpi = 300)
cat("\n── Workshop 2 Lab Complete (R) ──\n")
