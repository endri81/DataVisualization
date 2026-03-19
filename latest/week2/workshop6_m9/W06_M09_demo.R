# ============================================================
# Workshop 6 — Module 9: Case Study — e-Car Temporal Analysis
# Integrated R Script — UNYT Tirana
# ============================================================
library(tidyverse); library(patchwork); dir.create("output", showWarnings = FALSE)

# ── 1. LOAD AND PREPARE ─────────────────────────────────
ec <- read_csv("ecar.csv")
# Clean column names (dataset has double-space in "Car  Type")
names(ec) <- str_replace_all(names(ec), "\\s+", " ") |> str_trim()

ec <- ec |>
  mutate(
    ApproveDate = mdy(`Approve Date`),
    Year = year(ApproveDate),
    Month = month(ApproveDate),
    Quarter = quarter(ApproveDate),
    YearMonth = floor_date(ApproveDate, "month"),
    Spread = Rate - `Cost of Funds`,
    Approved = Outcome == 1) |>
  filter(Year >= 2002, Year <= 2012)

cat("Dataset:", nrow(ec), "loans, Years:", min(ec$Year), "-", max(ec$Year), "\n")
cat("Columns:", paste(names(ec), collapse = ", "), "\n")

# ── 2. YEARLY RATE + SPREAD WITH 2008 ANNOTATION ────────
yearly <- ec |>
  group_by(Year) |>
  summarise(
    mean_rate = mean(Rate, na.rm = TRUE),
    mean_spread = mean(Spread, na.rm = TRUE),
    mean_cof = mean(`Cost of Funds`, na.rm = TRUE),
    volume = n(),
    approval_rate = mean(Approved, na.rm = TRUE),
    .groups = "drop")

p_rate_spread <- ggplot(yearly) +
  geom_line(aes(x = Year, y = mean_rate, color = "Offered Rate"),
    linewidth = 1.5) +
  geom_point(aes(x = Year, y = mean_rate), color = "#1565C0", size = 2.5) +
  geom_line(aes(x = Year, y = mean_spread, color = "Spread (Rate - CoF)"),
    linewidth = 1.5) +
  geom_point(aes(x = Year, y = mean_spread), color = "#E53935", size = 2.5) +
  geom_line(aes(x = Year, y = mean_cof, color = "Cost of Funds"),
    linewidth = 1, linetype = "dashed") +
  scale_color_manual(values = c(
    "Offered Rate" = "#1565C0",
    "Spread (Rate - CoF)" = "#E53935",
    "Cost of Funds" = "#2E7D32")) +
  # 2008 crisis annotation
  geom_vline(xintercept = 2008, linetype = "dashed", color = "#888", linewidth = 0.6) +
  annotate("rect", xmin = 2007.5, xmax = 2009.5, ymin = -Inf, ymax = Inf,
    fill = "#E53935", alpha = 0.05) +
  annotate("text", x = 2008, y = max(yearly$mean_rate) * 0.95,
    label = "2008\nFinancial\nCrisis", size = 2.5, color = "#888",
    fontface = "bold") +
  scale_x_continuous(breaks = 2002:2012) +
  theme_minimal() +
  labs(title = "e-Car Loans: Rate, Cost of Funds, and Spread (2002–2012)",
       subtitle = "Rate dropped post-2008 (Fed cuts); Spread compressed then recovered",
       x = "Year", y = "Percentage Points", color = NULL)
ggsave("output/rate_spread_cof.png", p_rate_spread, width = 10, height = 5, dpi = 300)

# ── 3. VOLUME AND APPROVAL RATE BAR CHARTS ──────────────
p_volume <- ggplot(yearly, aes(x = Year, y = volume / 1000)) +
  geom_col(fill = "#2E7D32", width = 0.6, alpha = 0.7) +
  geom_text(aes(label = paste0(round(volume/1000, 1), "k")),
    vjust = -0.5, size = 2.5, fontface = "bold") +
  geom_vline(xintercept = 2008, linetype = "dashed", color = "#888") +
  scale_x_continuous(breaks = 2002:2012) +
  theme_minimal() +
  labs(title = "(a) Loan Volume (thousands per year)",
       x = "Year", y = "Loans (000s)")

p_approval <- ggplot(yearly, aes(x = Year, y = approval_rate * 100)) +
  geom_line(color = "#7B1FA2", linewidth = 1.5) +
  geom_point(color = "#7B1FA2", size = 3) +
  geom_text(aes(label = paste0(round(approval_rate * 100, 1), "%")),
    vjust = -1, size = 2.5, color = "#7B1FA2") +
  geom_vline(xintercept = 2008, linetype = "dashed", color = "#888") +
  scale_x_continuous(breaks = 2002:2012) +
  theme_minimal() +
  labs(title = "(b) Approval Rate (%)",
       x = "Year", y = "Approval Rate (%)")

ggsave("output/volume_approval.png", p_volume | p_approval,
  width = 12, height = 5, dpi = 300)

# ── 4. QUARTERLY RATE WITH CONFIDENCE RIBBON ─────────────
quarterly <- ec |>
  group_by(Year, Quarter) |>
  summarise(
    mean_rate = mean(Rate, na.rm = TRUE),
    se_rate = sd(Rate, na.rm = TRUE) / sqrt(n()),
    n = n(), .groups = "drop") |>
  mutate(
    date = as.Date(paste0(Year, "-", Quarter * 3 - 2, "-01")),
    lower = mean_rate - 1.96 * se_rate,
    upper = mean_rate + 1.96 * se_rate)

p_quarterly <- ggplot(quarterly, aes(x = date)) +
  geom_ribbon(aes(ymin = lower, ymax = upper),
    fill = "#1565C0", alpha = 0.15) +
  geom_line(aes(y = mean_rate), color = "#1565C0", linewidth = 0.8) +
  geom_point(aes(y = mean_rate), color = "#1565C0", size = 1) +
  # Lehman collapse
  geom_vline(xintercept = as.Date("2008-09-15"),
    linetype = "dashed", color = "#E53935", linewidth = 0.6) +
  annotate("text", x = as.Date("2008-12-01"),
    y = max(quarterly$upper) * 0.95,
    label = "Lehman\ncollapse", size = 2.5, color = "#E53935",
    fontface = "bold", hjust = 0) +
  scale_x_date(date_breaks = "1 year", date_labels = "%Y") +
  theme_minimal() +
  labs(title = "Quarterly Mean Rate ± 95% CI",
       subtitle = "CI widens during crisis = more pricing volatility",
       x = NULL, y = "Rate (%)")
ggsave("output/quarterly_ci.png", p_quarterly, width = 10, height = 5, dpi = 300)

# ── 5. RATE BY TIER OVER TIME (small multiples) ─────────
tier_yearly <- ec |>
  group_by(Year, Tier) |>
  summarise(mean_rate = mean(Rate, na.rm = TRUE), .groups = "drop")

p_tier_multi <- ggplot(tier_yearly, aes(x = Year, y = mean_rate)) +
  geom_line(color = "#1565C0", linewidth = 1) +
  geom_point(color = "#1565C0", size = 1.5) +
  geom_vline(xintercept = 2008, linetype = "dashed", color = "#888", linewidth = 0.3) +
  facet_wrap(~paste0("Tier ", Tier), ncol = 5) +
  scale_x_continuous(breaks = c(2002, 2005, 2008, 2012)) +
  theme_minimal(base_size = 8) +
  labs(title = "Rate by Credit Tier Over Time (2002–2012)",
       subtitle = "All tiers dropped post-2008; Tier 1 dropped furthest (competitive pressure)",
       x = "Year", y = "Mean Rate (%)")
ggsave("output/tier_multiples.png", p_tier_multi, width = 14, height = 4, dpi = 300)

# Grey+accent: highlight Tier 1
p_tier_accent <- ggplot(tier_yearly, aes(x = Year, y = mean_rate, group = factor(Tier))) +
  geom_line(color = "#DDDDDD", linewidth = 0.7) +
  geom_line(data = tier_yearly |> filter(Tier == 1),
    color = "#E53935", linewidth = 2) +
  geom_text(data = tier_yearly |>
    group_by(Tier) |> filter(Year == max(Year)),
    aes(label = paste0("T", Tier),
        color = Tier == 1),
    hjust = -0.3, size = 2.5, fontface = "bold", show.legend = FALSE) +
  scale_color_manual(values = c("TRUE" = "#E53935", "FALSE" = "#AAAAAA")) +
  geom_vline(xintercept = 2008, linetype = "dashed", color = "#888") +
  scale_x_continuous(breaks = 2002:2012, limits = c(2002, 2013)) +
  theme_minimal() +
  labs(title = "Rate by Tier: Grey+Accent on Tier 1 (best credit)",
       subtitle = "Tier 1 dropped most aggressively — banks competed for safest borrowers",
       x = "Year", y = "Mean Rate (%)")
ggsave("output/tier_accent.png", p_tier_accent, width = 10, height = 5, dpi = 300)

# ── 6. SPREAD DISTRIBUTION: PRE vs POST 2008 ────────────
ec_period <- ec |>
  mutate(period = ifelse(Year < 2008, "Pre-2008 (2002–2007)", "Post-2008 (2008–2012)"))

p_spread_dist <- ggplot(ec_period, aes(x = Spread, fill = period)) +
  geom_histogram(bins = 50, alpha = 0.5, position = "identity", color = "white") +
  scale_fill_manual(values = c(
    "Pre-2008 (2002–2007)" = "#1565C0",
    "Post-2008 (2008–2012)" = "#E53935")) +
  geom_vline(data = ec_period |> group_by(period) |>
    summarise(med = median(Spread)),
    aes(xintercept = med, color = period),
    linetype = "dashed", linewidth = 1, show.legend = FALSE) +
  scale_color_manual(values = c(
    "Pre-2008 (2002–2007)" = "#1565C0",
    "Post-2008 (2008–2012)" = "#E53935")) +
  theme_minimal() +
  labs(title = "Spread Distribution: Pre vs Post 2008",
       subtitle = "Post-2008 spread compressed (dashed = median)",
       x = "Spread (pp)", y = "Count", fill = "Period")
ggsave("output/spread_pre_post.png", p_spread_dist, width = 9, height = 5, dpi = 300)

# ── 7. MONTHLY RATE DECOMPOSITION (STL) ─────────────────
# Monthly average rate
monthly_rate <- ec |>
  group_by(YearMonth) |>
  summarise(mean_rate = mean(Rate, na.rm = TRUE), .groups = "drop") |>
  arrange(YearMonth)

# STL requires ts object
ts_rate <- ts(monthly_rate$mean_rate, frequency = 12,
  start = c(year(min(monthly_rate$YearMonth)),
    month(min(monthly_rate$YearMonth))))
stl_fit <- stl(ts_rate, s.window = "periodic")

# Extract components
components <- tibble(
  date = monthly_rate$YearMonth,
  observed = as.numeric(ts_rate),
  trend = as.numeric(stl_fit$time.series[, "trend"]),
  seasonal = as.numeric(stl_fit$time.series[, "seasonal"]),
  remainder = as.numeric(stl_fit$time.series[, "remainder"]))

p_decomp <- components |>
  pivot_longer(-date, names_to = "component", values_to = "value") |>
  mutate(component = factor(component,
    levels = c("observed", "trend", "seasonal", "remainder"))) |>
  ggplot(aes(x = date, y = value)) +
  geom_line(aes(color = component), linewidth = 0.5, show.legend = FALSE) +
  scale_color_manual(values = c(
    observed = "#333", trend = "#1565C0",
    seasonal = "#2E7D32", remainder = "#E53935")) +
  facet_wrap(~component, ncol = 1, scales = "free_y") +
  geom_vline(xintercept = as.Date("2008-09-15"),
    linetype = "dashed", color = "#888", linewidth = 0.3) +
  theme_minimal(base_size = 8) +
  labs(title = "STL Decomposition: Monthly Mean Rate (2002–2012)",
       subtitle = "Trend captures the 2008 crisis; seasonal shows within-year pattern",
       x = NULL, y = NULL)
ggsave("output/rate_stl.png", p_decomp, width = 10, height = 8, dpi = 300)

# ── 8. SIX-PANEL DASHBOARD ──────────────────────────────
dashboard <- (p_rate_spread) /
  (p_volume | p_approval) /
  (p_quarterly | p_tier_accent) +
  plot_annotation(
    title = "e-Car Temporal Case Study: Six-Panel Dashboard (2002–2012)",
    subtitle = "Rate dynamics + Volume + Approval + Quarterly CI + Tier stratification",
    tag_levels = "a")
ggsave("output/ecar_dashboard.png", dashboard, width = 14, height = 14, dpi = 300)

# ── 9. KEY FINDINGS ──────────────────────────────────────
cat("\n── KEY FINDINGS ──\n")
cat("1. Rate peak:", round(max(yearly$mean_rate), 2), "% in",
  yearly$Year[which.max(yearly$mean_rate)], "\n")
cat("2. Rate trough:", round(min(yearly$mean_rate), 2), "% in",
  yearly$Year[which.min(yearly$mean_rate)], "\n")
cat("3. Spread pre-2008 median:", round(median(ec$Spread[ec$Year < 2008]), 2), "pp\n")
cat("4. Spread post-2008 median:", round(median(ec$Spread[ec$Year >= 2008]), 2), "pp\n")
cat("5. Volume peak:", format(max(yearly$volume), big.mark = ","), "in",
  yearly$Year[which.max(yearly$volume)], "\n")
cat("6. Approval rate range:", round(min(yearly$approval_rate)*100, 1), "–",
  round(max(yearly$approval_rate)*100, 1), "%\n")

cat("\n── All W06-M09 R outputs saved ──\n")
