# ============================================================
# Workshop 6 — Module 5: Seasonal & Calendar Visualizations
# Integrated R Script — UNYT Tirana
# ============================================================
library(tidyverse); library(patchwork); dir.create("output", showWarnings = FALSE)

# ── 1. SIMULATED DAILY DATA (2 years) ───────────────────
set.seed(42)
dates <- seq(as.Date("2022-01-01"), as.Date("2023-12-31"), by = "day")
n <- length(dates)
# Activity: higher on weekdays, seasonal peak in summer, trend
weekday_effect <- ifelse(weekdays(dates) %in% c("Saturday", "Sunday"), 0, 4)
seasonal_effect <- 3 * sin(2 * pi * as.numeric(format(dates, "%j")) / 365)
noise <- rpois(n, 5)
activity <- weekday_effect + seasonal_effect + noise + 8

daily <- tibble(
  date = dates,
  value = pmax(activity, 0),
  dow = factor(weekdays(date),
    levels = c("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")),
  dow_num = as.numeric(dow) - 1,
  week = as.numeric(format(date, "%U")),
  month = month(date, label = TRUE),
  year = year(date))

cat("Daily data:", nrow(daily), "rows\n")
cat("Range:", format(min(daily$date)), "to", format(max(daily$date)), "\n")

# ── 2. CALENDAR HEATMAP — github-style ──────────────────
# One year: 2023
cal_2023 <- daily |> filter(year == 2023)

p_calendar <- ggplot(cal_2023, aes(x = week, y = fct_rev(dow), fill = value)) +
  geom_tile(color = "white", linewidth = 0.5) +
  scale_fill_gradient(low = "#E8F5E9", high = "#1B5E20", name = "Activity") +
  scale_y_discrete(labels = c("Sun","Sat","Fri","Thu","Wed","Tue","Mon")) +
  theme_minimal(base_size = 9) +
  theme(
    panel.grid = element_blank(),
    axis.text.x = element_text(size = 5)) +
  labs(title = "Calendar Heatmap: 2023 Activity (GitHub-style)",
       subtitle = "Rows = Day of Week, Columns = Week of Year, Colour = Activity",
       x = "Week of Year", y = NULL)
ggsave("output/calendar_heatmap.png", p_calendar, width = 14, height = 3.5, dpi = 300)

# ── 3. YEAR-OVER-YEAR SEASONAL SUBSERIES ────────────────
# Netflix: monthly additions by year
nf <- read_csv("netflix.csv") |>
  mutate(date_added = mdy(str_trim(date_added)),
    year_added = year(date_added),
    month_added = month(date_added, label = TRUE)) |>
  filter(!is.na(year_added), year_added >= 2016, year_added <= 2021)

monthly_by_year <- nf |> count(year_added, month_added)

# Grey+accent: all years grey, 2021 in red
p_seasonal <- ggplot(monthly_by_year, aes(
    x = as.numeric(month_added), y = n,
    group = year_added,
    color = factor(year_added),
    alpha = factor(year_added),
    linewidth = factor(year_added))) +
  geom_line() +
  geom_point(size = 1.5) +
  scale_color_manual(values = c(
    "2016" = "#CCCCCC", "2017" = "#CCCCCC", "2018" = "#CCCCCC",
    "2019" = "#CCCCCC", "2020" = "#CCCCCC", "2021" = "#E53935"),
    name = "Year") +
  scale_alpha_manual(values = c(
    "2016"=0.3,"2017"=0.3,"2018"=0.4,"2019"=0.4,"2020"=0.5,"2021"=1.0),
    guide = "none") +
  scale_linewidth_manual(values = c(
    "2016"=0.5,"2017"=0.5,"2018"=0.5,"2019"=0.6,"2020"=0.8,"2021"=1.5),
    guide = "none") +
  scale_x_continuous(breaks = 1:12, labels = month.abb) +
  theme_minimal() +
  labs(title = "Netflix Seasonal Subseries: Year-over-Year (2016–2021)",
       subtitle = "2021 highlighted in red; all prior years in grey",
       x = "Month", y = "Titles Added")
ggsave("output/seasonal_subseries.png", p_seasonal, width = 9, height = 5, dpi = 300)

# ── 4. MONTHLY BOXPLOT — seasonal pattern summary ───────
p_boxplot <- ggplot(monthly_by_year, aes(x = month_added, y = n)) +
  geom_boxplot(fill = "#BBDEFB", color = "#1565C0", width = 0.5,
    outlier.size = 1) +
  stat_summary(fun = mean, geom = "line", group = 1,
    color = "#E53935", linewidth = 1) +
  stat_summary(fun = mean, geom = "point",
    color = "#E53935", size = 2) +
  theme_minimal() +
  labs(title = "Monthly Box: Distribution of Netflix Additions by Month",
       subtitle = "Box = IQR across years; red line = mean trend",
       x = "Month", y = "Titles Added per Month")
ggsave("output/monthly_boxplot.png", p_boxplot, width = 9, height = 5, dpi = 300)

# ── 5. POLAR TIME PLOT (12-month cycle) ─────────────────
avg_by_month <- monthly_by_year |>
  group_by(month_added) |>
  summarise(mean_n = mean(n), .groups = "drop") |>
  mutate(month_num = as.numeric(month_added))

p_polar <- ggplot(avg_by_month, aes(x = month_num, y = mean_n)) +
  geom_col(fill = "#1565C0", alpha = 0.7, width = 0.8) +
  coord_polar(start = 0) +
  scale_x_continuous(breaks = 1:12, labels = month.abb) +
  theme_minimal() +
  labs(title = "Polar: Average Monthly Netflix Additions",
       subtitle = "Clock-face layout for 12-month cycle",
       y = "Mean Titles")
ggsave("output/polar_month.png", p_polar, width = 6, height = 6, dpi = 300)

# ── 6. HEATMAP: MONTH × YEAR ────────────────────────────
# Alternative to calendar: coarser granularity
monthly_grid <- nf |> count(year_added, month_added)

p_month_year <- ggplot(monthly_grid, aes(
    x = month_added, y = factor(year_added), fill = n)) +
  geom_tile(color = "white", linewidth = 1) +
  geom_text(aes(label = n), size = 3, fontface = "bold") +
  scale_fill_gradient(low = "#E3F2FD", high = "#1565C0", name = "Titles") +
  theme_minimal() +
  labs(title = "Heatmap: Netflix Additions (Month × Year)",
       subtitle = "Colour + number = double encoding",
       x = "Month", y = "Year")
ggsave("output/month_year_heatmap.png", p_month_year, width = 10, height = 5, dpi = 300)

# ── 7. COMPARISON DASHBOARD ─────────────────────────────
p_dashboard <- (p_calendar) /
  (p_seasonal | p_boxplot) /
  (p_polar | p_month_year) +
  plot_annotation(
    title = "Seasonal & Calendar Visualizations: 6 Approaches",
    tag_levels = "a")
ggsave("output/seasonal_dashboard.png", p_dashboard, width = 14, height = 16, dpi = 300)

cat("\n── All W06-M05 R outputs saved ──\n")
cat("Figures: calendar_heatmap, seasonal_subseries, monthly_boxplot,\n")
cat("  polar_month, month_year_heatmap, seasonal_dashboard\n")
