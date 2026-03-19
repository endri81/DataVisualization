# ============================================================
# Workshop 6 — Module 3: Line Charts in Code (R + Python)
# Integrated R Script — UNYT Tirana
# ============================================================
library(tidyverse); library(patchwork); dir.create("output", showWarnings = FALSE)

# ── 1. SIMULATED DATA ───────────────────────────────────
set.seed(42)
months <- seq(as.Date("2020-01-01"), as.Date("2023-12-01"), by = "month")
n <- length(months)
val <- 100 + cumsum(rnorm(n, 0.5, 3))

# ── 2. geom_line: CONTINUOUS TIME SERIES ─────────────────
# Basic line chart with proper date axis formatting
p_line <- ggplot(tibble(date = months, value = val), aes(x = date, y = value)) +
  geom_line(color = "#1565C0", linewidth = 1) +
  scale_x_date(
    date_breaks = "6 months",
    date_labels = "%b %Y",        # abbreviated month + 4-digit year
    date_minor_breaks = "1 month") +  # minor gridlines every month
  theme_minimal() +
  labs(title = "geom_line: Continuous Time Series",
       subtitle = "date_breaks = '6 months', date_labels = '%b %Y'",
       x = NULL, y = "Value")
ggsave("output/line_basic.png", p_line, width = 9, height = 4, dpi = 300)

# ── 3. geom_step: DISCRETE CHANGES ──────────────────────
# Interest rate changes (discrete jumps, constant between)
rates <- c(rep(5.5, 12), rep(4.5, 12), rep(3.0, 12), rep(3.5, 12))
p_step <- ggplot(tibble(date = months, rate = rates), aes(x = date, y = rate)) +
  geom_step(color = "#E53935", linewidth = 1.5) +
  geom_point(data = tibble(
    date = as.Date(c("2021-01-01", "2022-01-01", "2023-01-01")),
    rate = c(4.5, 3.0, 3.5)),
    color = "#E53935", size = 3) +
  scale_x_date(date_breaks = "1 year", date_labels = "%Y") +
  theme_minimal() +
  labs(title = "geom_step: Discrete Rate Changes",
       subtitle = "Value jumps at specific dates, constant between",
       x = NULL, y = "Interest Rate (%)")
ggsave("output/step_chart.png", p_step, width = 8, height = 4, dpi = 300)

# ── 4. geom_area: FILLED MAGNITUDE ──────────────────────
p_area <- ggplot(tibble(date = months, value = val), aes(x = date, y = value)) +
  geom_area(fill = "#1565C0", alpha = 0.3, color = "#1565C0", linewidth = 0.5) +
  scale_x_date(date_breaks = "6 months", date_labels = "%b\n%Y") +
  theme_minimal() +
  labs(title = "geom_area: Filled Magnitude",
       subtitle = "Like geom_line but fills below — emphasises cumulative volume",
       x = NULL, y = "Value")
ggsave("output/area_chart.png", p_area, width = 8, height = 4, dpi = 300)

# ── 5. STACKED AREA: PARTS OF A WHOLE OVER TIME ─────────
v1 <- abs(rnorm(n, 30, 5)); v2 <- abs(rnorm(n, 25, 5)); v3 <- abs(rnorm(n, 15, 5))
df_stack <- tibble(
  date = rep(months, 3),
  value = c(v1, v2, v3),
  product = rep(c("Product A", "Product B", "Product C"), each = n))

# Absolute stacked area
p_stacked <- ggplot(df_stack, aes(x = date, y = value, fill = product)) +
  geom_area(alpha = 0.7, color = "white", linewidth = 0.3) +
  scale_fill_manual(values = c("#1565C0", "#E53935", "#2E7D32")) +
  theme_minimal() +
  labs(title = "Stacked Area: Parts of a Whole Over Time",
       subtitle = "Each band = one product; total = sum of all bands",
       x = NULL, y = "Revenue (EUR)")
ggsave("output/stacked_area.png", p_stacked, width = 9, height = 5, dpi = 300)

# 100% stacked area (proportions)
df_pct <- df_stack |>
  group_by(date) |>
  mutate(pct = value / sum(value) * 100) |>
  ungroup()

p_pct <- ggplot(df_pct, aes(x = date, y = pct, fill = product)) +
  geom_area(alpha = 0.7, color = "white", linewidth = 0.3) +
  scale_fill_manual(values = c("#1565C0", "#E53935", "#2E7D32")) +
  scale_y_continuous(labels = function(x) paste0(x, "%")) +
  theme_minimal() +
  labs(title = "100% Stacked Area: Proportional Composition Over Time",
       subtitle = "Each point sums to 100% — shows relative share, not absolute",
       x = NULL, y = "Share (%)")
ggsave("output/stacked_100pct.png", p_pct, width = 9, height = 5, dpi = 300)

# ── 6. RIBBON: CONFIDENCE BAND ──────────────────────────
df_ribbon <- tibble(
  date = months,
  mean = val,
  lower = val - 8 - runif(n, 0, 3),
  upper = val + 8 + runif(n, 0, 3))

p_ribbon <- ggplot(df_ribbon, aes(x = date)) +
  geom_ribbon(aes(ymin = lower, ymax = upper),
    fill = "#1565C0", alpha = 0.15) +
  geom_line(aes(y = mean), color = "#1565C0", linewidth = 1) +
  theme_minimal() +
  labs(title = "geom_ribbon: Mean ± Confidence Band",
       subtitle = "Shaded region communicates uncertainty around the central estimate",
       x = NULL, y = "Value")
ggsave("output/ribbon.png", p_ribbon, width = 8, height = 4, dpi = 300)

# ── 7. SIX-PANEL COMPARISON DASHBOARD ───────────────────
p1 <- ggplot(tibble(date=months,value=val),aes(date,value)) +
  geom_line(color="#1565C0",linewidth=0.8) + theme_minimal(base_size=7) +
  labs(title="(a) Line")
p2 <- ggplot(tibble(date=months,rate=rates),aes(date,rate)) +
  geom_step(color="#E53935",linewidth=0.8) + theme_minimal(base_size=7) +
  labs(title="(b) Step")
p3 <- ggplot(tibble(date=months,value=val),aes(date,value)) +
  geom_area(fill="#2E7D32",alpha=0.3)+geom_line(color="#2E7D32",linewidth=0.5) +
  theme_minimal(base_size=7) + labs(title="(c) Area")
p4 <- ggplot(df_stack,aes(date,value,fill=product)) +
  geom_area(alpha=0.7,color="white",linewidth=0.2) +
  scale_fill_manual(values=c("#1565C0","#E53935","#2E7D32")) +
  theme_minimal(base_size=7) + theme(legend.position="none") +
  labs(title="(d) Stacked Area")
p5 <- ggplot(df_pct,aes(date,pct,fill=product)) +
  geom_area(alpha=0.7,color="white",linewidth=0.2) +
  scale_fill_manual(values=c("#1565C0","#E53935","#2E7D32")) +
  theme_minimal(base_size=7) + theme(legend.position="none") +
  labs(title="(e) 100% Stacked")
p6 <- ggplot(df_ribbon,aes(x=date)) +
  geom_ribbon(aes(ymin=lower,ymax=upper),fill="#1565C0",alpha=0.15) +
  geom_line(aes(y=mean),color="#1565C0",linewidth=0.8) +
  theme_minimal(base_size=7) + labs(title="(f) Ribbon (CI)")

dashboard <- (p1 | p2 | p3) / (p4 | p5 | p6) +
  plot_annotation(title = "Six Line Geometries in R",
    subtitle = "Same simulated time series, different visual encodings",
    tag_levels = "a") &
  theme_minimal(base_size = 7)
ggsave("output/six_geoms_dashboard.png", dashboard, width = 14, height = 8, dpi = 300)

# ── 8. DATE FORMATTING EXAMPLES ──────────────────────────
p_fmt1 <- ggplot(tibble(date=months[1:24],value=val[1:24]),aes(date,value)) +
  geom_line(color="#1565C0") +
  scale_x_date(date_breaks="3 months",date_labels="%b %Y") +
  theme_minimal(base_size=8) + labs(title="Format: %b %Y → Jan 2020")

p_fmt2 <- ggplot(tibble(date=months[1:24],value=val[1:24]),aes(date,value)) +
  geom_line(color="#1565C0") +
  scale_x_date(date_breaks="3 months",date_labels="%Y-%m") +
  theme_minimal(base_size=8) + labs(title="Format: %Y-%m → 2020-01")

p_fmt3 <- ggplot(tibble(date=months[1:24],value=val[1:24]),aes(date,value)) +
  geom_line(color="#1565C0") +
  scale_x_date(date_breaks="1 year",date_labels="%Y") +
  theme_minimal(base_size=8) + labs(title="Format: %Y → 2020")

p_fmt4 <- ggplot(tibble(date=months[1:24],value=val[1:24]),aes(date,value)) +
  geom_line(color="#1565C0") +
  scale_x_date(date_breaks="3 months",date_labels="%b\n%Y") +
  theme_minimal(base_size=8) + labs(title="Format: %b\\n%Y (two lines)")

ggsave("output/date_formats.png", (p_fmt1|p_fmt2)/(p_fmt3|p_fmt4),
  width=12, height=7, dpi=300)

# ── 9. REAL DATA: NETFLIX ───────────────────────────────
nf <- read_csv("netflix.csv") |>
  mutate(date_added = mdy(str_trim(date_added))) |>
  filter(!is.na(date_added), year(date_added) >= 2015)

# Monthly additions line chart
nf_monthly <- nf |>
  mutate(month = floor_date(date_added, "month")) |>
  count(month)

p_nf_line <- ggplot(nf_monthly, aes(x = month, y = n)) +
  geom_line(color = "#E53935", linewidth = 0.8) +
  scale_x_date(date_breaks = "6 months", date_labels = "%b\n%Y") +
  theme_minimal() +
  labs(title = "Netflix: Monthly Additions (2015–2021)",
       x = NULL, y = "Titles Added")

# Stacked area by type
nf_type_monthly <- nf |>
  mutate(month = floor_date(date_added, "month")) |>
  count(month, type)

p_nf_stacked <- ggplot(nf_type_monthly, aes(x = month, y = n, fill = type)) +
  geom_area(alpha = 0.7, color = "white", linewidth = 0.3) +
  scale_fill_manual(values = c(Movie = "#1565C0", "TV Show" = "#E53935")) +
  scale_x_date(date_breaks = "1 year", date_labels = "%Y") +
  theme_minimal() +
  labs(title = "Netflix: Monthly Additions by Type (stacked)",
       x = NULL, y = "Titles Added")

ggsave("output/netflix_lines.png", p_nf_line / p_nf_stacked,
  width = 10, height = 8, dpi = 300)

cat("\n── All W06-M03 R outputs saved ──\n")
cat("Figures: line_basic, step_chart, area_chart, stacked_area,\n")
cat("  stacked_100pct, ribbon, six_geoms_dashboard, date_formats,\n")
cat("  netflix_lines\n")
