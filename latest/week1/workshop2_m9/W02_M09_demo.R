# ============================================================
# Workshop 2 — Module 9: Tidy Data & Data Wrangling for Viz
# R Demonstration Script — UNYT Tirana
# ============================================================
library(tidyverse)
library(patchwork)
dir.create("output", showWarnings = FALSE)

# ── 1. LOAD & CLEAN (complete pipeline) ──────────────────
apps_raw <- read_csv("googleplaystore.csv")
cat("Raw dimensions:", dim(apps_raw), "\n")

apps_clean <- apps_raw |>
  distinct(App, .keep_all = TRUE) |>
  filter(Type %in% c("Free", "Paid"), !is.na(Rating)) |>
  mutate(
    Reviews = as.numeric(Reviews),
    Installs = as.numeric(str_remove_all(Installs, "[+,]")),
    Price = as.numeric(str_remove(Price, "\\$")),
    log_reviews = log10(Reviews + 1)
  )
cat("Clean dimensions:", dim(apps_clean), "\n")

# ── 2. PIVOT DEMO — wide to long ─────────────────────────
gdp_wide <- tibble(
  country = c("Albania", "Greece", "Italy"),
  `2020` = c(2.9, -9.0, -9.0),
  `2021` = c(7.5, 8.4, 6.7),
  `2022` = c(4.8, 5.9, 3.7)
)

gdp_long <- gdp_wide |>
  pivot_longer(cols = `2020`:`2022`, names_to = "year", values_to = "gdp_growth") |>
  mutate(year = as.integer(year))

p_pivot <- ggplot(gdp_long, aes(x = year, y = gdp_growth, color = country)) +
  geom_line(linewidth = 1.2) + geom_point(size = 2) +
  geom_hline(yintercept = 0, linetype = "dashed", color = "grey50") +
  scale_color_manual(values = c(Albania = "#1565C0", Greece = "#E53935", Italy = "#2E7D32")) +
  theme_minimal() +
  labs(title = "GDP Growth After pivot_longer()", subtitle = "Wide → long enables aes(color = country)",
       x = "Year", y = "GDP Growth (%)", color = "Country")
ggsave("output/pivot_demo.png", p_pivot, width = 7, height = 4.5, dpi = 300)

# ── 3. SIX VERBS → PLOT ──────────────────────────────────
summary_df <- apps_clean |>
  group_by(Category) |>
  summarise(n = n(), m = mean(Rating), se = sd(Rating) / sqrt(n()), .groups = "drop") |>
  slice_max(n, n = 8) |>
  mutate(Category = fct_reorder(Category, m))

p_verbs <- ggplot(summary_df, aes(x = Category, y = m)) +
  geom_col(fill = "#1565C0", width = 0.5, alpha = 0.6) +
  geom_errorbar(aes(ymin = m - se, ymax = m + se), width = 0.2) +
  geom_text(aes(label = round(m, 2)), hjust = -0.3, size = 3, fontface = "bold") +
  coord_flip() +
  theme_minimal() +
  theme(panel.grid.major.y = element_blank()) +
  labs(title = "Mean Rating by Category (±SE)", subtitle = "Top 8 by count, sorted by mean rating",
       x = NULL, y = "Mean Rating")
ggsave("output/wrangle_to_plot.png", p_verbs, width = 7, height = 5, dpi = 300)

# ── 4. COMPLETE PIPELINE (one chain) ─────────────────────
p_chain <- read_csv("googleplaystore.csv") |>
  filter(Type %in% c("Free", "Paid"), !is.na(Rating)) |>
  mutate(Reviews = as.numeric(Reviews)) |>
  group_by(Category) |>
  summarise(n = n(), m = mean(Rating), .groups = "drop") |>
  slice_max(n, n = 10) |>
  mutate(Category = fct_reorder(Category, n)) |>
  ggplot(aes(x = Category, y = n, fill = m)) +
  geom_col(width = 0.6) +
  scale_fill_viridis_c(option = "plasma", name = "Mean\nRating") +
  coord_flip() +
  theme_minimal() +
  labs(title = "Top 10 Categories: Count Coloured by Mean Rating",
       subtitle = "Complete read → clean → aggregate → plot in one pipe chain",
       x = NULL, y = "Number of Apps")
ggsave("output/complete_chain.png", p_chain, width = 8, height = 5, dpi = 300)

cat("\n── All W02-M09 R plots saved ──\n")
