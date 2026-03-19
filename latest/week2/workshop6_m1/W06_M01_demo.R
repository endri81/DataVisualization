# ============================================================
# Workshop 6 — Module 1: Time as a Visual Dimension
# Integrated R Script — UNYT Tirana
# ============================================================
library(tidyverse); library(lubridate); dir.create("output", showWarnings = FALSE)

# ── 1. SIMULATED DAILY TIME SERIES ──────────────────────
set.seed(42)
dates <- seq(as.Date("2020-01-01"), as.Date("2023-12-31"), by = "day")
n <- length(dates)
trend <- 100 + 0.05 * (1:n)
seasonal <- 15 * sin(2 * pi * (1:n) / 365)
residual <- rnorm(n, 0, 5)
value <- trend + seasonal + residual

daily <- tibble(date = dates, value = value)
cat("Daily series:", nrow(daily), "observations\n")
cat("Range:", format(min(daily$date)), "to", format(max(daily$date)), "\n")

# ── 2. GRANULARITY COMPARISON ────────────────────────────
weekly  <- daily |> mutate(week  = floor_date(date, "week"))  |> group_by(week)  |> summarise(value = mean(value)) |> rename(date = week)
monthly <- daily |> mutate(month = floor_date(date, "month")) |> group_by(month) |> summarise(value = mean(value)) |> rename(date = month)
yearly  <- daily |> mutate(year  = floor_date(date, "year"))  |> group_by(year)  |> summarise(value = mean(value)) |> rename(date = year)

p_daily   <- ggplot(daily, aes(x = date, y = value)) + geom_line(color = "#BBBBBB", linewidth = 0.3) +
  theme_minimal(base_size = 8) + labs(title = "(a) Daily")
p_weekly  <- ggplot(weekly, aes(x = date, y = value)) + geom_line(color = "#1565C0", linewidth = 0.8) +
  theme_minimal(base_size = 8) + labs(title = "(b) Weekly")
p_monthly <- ggplot(monthly, aes(x = date, y = value)) + geom_line(color = "#E53935", linewidth = 1) + geom_point(color = "#E53935", size = 1.5) +
  theme_minimal(base_size = 8) + labs(title = "(c) Monthly")
p_yearly  <- ggplot(yearly, aes(x = date, y = value)) + geom_line(color = "#2E7D32", linewidth = 1.5) + geom_point(color = "#2E7D32", size = 3) +
  theme_minimal(base_size = 8) + labs(title = "(d) Yearly")

library(patchwork)
p_gran <- (p_daily | p_weekly) / (p_monthly | p_yearly) +
  plot_annotation(title = "Same Data, Four Granularities", tag_levels = "a")
ggsave("output/granularity.png", p_gran, width = 12, height = 7, dpi = 300)

# ── 3. DECOMPOSITION ────────────────────────────────────
# Convert to ts object (frequency = 365 for daily data)
ts_data <- ts(daily$value, frequency = 365)

# STL decomposition (robust)
stl_fit <- stl(ts_data, s.window = "periodic")

# Plot the four panels
png("output/decomposition.png", width = 10, height = 8, units = "in", res = 300)
plot(stl_fit, main = "STL Decomposition: Trend + Seasonal + Residual")
dev.off()

# Extract components
components <- tibble(
  date = daily$date,
  observed = daily$value,
  trend = as.numeric(stl_fit$time.series[, "trend"]),
  seasonal = as.numeric(stl_fit$time.series[, "seasonal"]),
  remainder = as.numeric(stl_fit$time.series[, "remainder"]))

# ggplot version
p_decomp <- components |>
  pivot_longer(-date, names_to = "component", values_to = "val") |>
  mutate(component = factor(component, levels = c("observed", "trend", "seasonal", "remainder"))) |>
  ggplot(aes(x = date, y = val)) +
  geom_line(color = "#1565C0", linewidth = 0.3) +
  facet_wrap(~component, ncol = 1, scales = "free_y") +
  theme_minimal(base_size = 8) +
  labs(title = "STL Decomposition (ggplot version)", y = NULL)
ggsave("output/decomposition_gg.png", p_decomp, width = 10, height = 8, dpi = 300)

# ── 4. CHART TYPE COMPARISON ────────────────────────────
# Line
p_line <- ggplot(monthly, aes(x = date, y = value)) +
  geom_line(color = "#1565C0", linewidth = 1) +
  theme_minimal(base_size = 8) + labs(title = "(a) Line Chart")

# Area
p_area <- ggplot(monthly, aes(x = date, y = value)) +
  geom_area(fill = "#1565C0", alpha = 0.3, color = "#1565C0", linewidth = 0.5) +
  theme_minimal(base_size = 8) + labs(title = "(b) Area Chart")

# Step
p_step <- ggplot(monthly, aes(x = date, y = value)) +
  geom_step(color = "#E53935", linewidth = 1) +
  theme_minimal(base_size = 8) + labs(title = "(c) Step Chart")

# Bar
p_bar <- ggplot(monthly, aes(x = date, y = value)) +
  geom_col(fill = "#7B1FA2", width = 20, alpha = 0.7) +
  theme_minimal(base_size = 8) + labs(title = "(d) Bar Chart (monthly)")

p_types <- (p_line | p_area) / (p_step | p_bar) +
  plot_annotation(title = "Four Temporal Chart Types: Same Monthly Data")
ggsave("output/chart_types.png", p_types, width = 12, height = 7, dpi = 300)

# ── 5. PITFALL: CATEGORICAL vs DATE AXIS ────────────────
# Bad: dates as factor (even spacing)
bad_dates <- c("2020-01", "2020-06", "2020-12", "2022-01", "2023-06")
bad_vals <- c(10, 15, 18, 22, 28)
p_bad <- tibble(date = bad_dates, val = bad_vals) |>
  ggplot(aes(x = date, y = val, group = 1)) +
  geom_line(color = "#E53935", linewidth = 1) + geom_point(color = "#E53935", size = 3) +
  theme_minimal(base_size = 9) +
  labs(title = "BAD: Dates as categories (even spacing)")

# Good: proper date axis
p_good <- tibble(date = ymd(paste0(bad_dates, "-01")), val = bad_vals) |>
  ggplot(aes(x = date, y = val)) +
  geom_line(color = "#1565C0", linewidth = 1) + geom_point(color = "#1565C0", size = 3) +
  scale_x_date(date_breaks = "6 months", date_labels = "%Y-%m") +
  theme_minimal(base_size = 9) +
  labs(title = "GOOD: True date axis (real spacing)")

ggsave("output/pitfall_axis.png", p_bad | p_good, width = 12, height = 4, dpi = 300)

cat("\n── All W06-M01 R outputs saved ──\n")
