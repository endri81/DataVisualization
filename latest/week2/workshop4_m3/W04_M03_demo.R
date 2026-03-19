# ============================================================
# Workshop 4 — Module 3: Data Wrangling for Visualization (Python)
# R Reference Script (for comparison) — UNYT Tirana
# ============================================================
library(tidyverse); dir.create("output",showWarnings=FALSE)

# R version of the same pipeline shown in Python slides
apps_clean <- read_csv("googleplaystore.csv") |>
  distinct(App, .keep_all = TRUE) |>
  mutate(
    Reviews  = as.numeric(Reviews),
    Installs = str_remove_all(Installs, "[+,]") |> as.numeric(),
    Size     = case_when(
      str_detect(Size, "M") ~ str_remove(Size, "M") |> as.numeric(),
      str_detect(Size, "k") ~ str_remove(Size, "k") |> as.numeric() / 1024,
      TRUE ~ NA_real_),
    Price    = str_remove(Price, "\\$") |> as.numeric()
  ) |>
  filter(!is.na(Rating), Type %in% c("Free", "Paid"), Rating >= 1, Rating <= 5)

# Pipe-to-plot
p <- apps_clean |>
  group_by(Category) |>
  summarise(mean_r = mean(Rating), n = n(), .groups = "drop") |>
  slice_max(n, n = 8) |>
  mutate(Category = fct_reorder(Category, mean_r), hl = mean_r == max(mean_r)) |>
  ggplot(aes(x = Category, y = mean_r, fill = hl)) +
  geom_col(width = 0.5, show.legend = FALSE) +
  geom_text(aes(label = round(mean_r, 2)), hjust = -0.2, size = 3, fontface = "bold") +
  scale_fill_manual(values = c("TRUE" = "#1565C0", "FALSE" = "#BBBBBB")) +
  coord_flip() + theme_minimal() +
  labs(title = "R: Mean Rating by Top 8 Categories (pipe-to-plot)", x = NULL, y = "Mean Rating")
ggsave("output/r_pipe_to_plot.png", p, width = 7, height = 5, dpi = 300)

# Reshape demo
df_wide <- tibble(region = c("Tirana","Durres","Vlore"), Q1 = c(120,90,65), Q2 = c(135,95,72), Q3 = c(128,88,70))
p_reshape <- df_wide |>
  pivot_longer(Q1:Q3, names_to = "quarter", values_to = "revenue") |>
  ggplot(aes(x = quarter, y = revenue, color = region, group = region)) +
  geom_line(linewidth = 1) + geom_point(size = 2) +
  scale_color_brewer(palette = "Set2") + theme_minimal() +
  labs(title = "R: pivot_longer() -> line chart")
ggsave("output/r_reshape.png", p_reshape, width = 6, height = 4, dpi = 300)

cat("\n── W04-M03 R reference saved ──\n")
