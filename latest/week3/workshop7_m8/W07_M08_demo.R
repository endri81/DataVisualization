# ============================================================
# Workshop 7 — Module 8: Case Study — e-Car Data Story
# Integrated R Script — UNYT Tirana
# ============================================================
# Complete 6-slide assertion-evidence deck: the 2008 crisis narrative
library(tidyverse); library(patchwork); dir.create("output", showWarnings = FALSE)

# ── LOAD + CLEAN THEME ───────────────────────────────────
ec <- read_csv("ecar.csv") |>
  mutate(Year = year(mdy(`Approve Date`)),
    Quarter = quarter(mdy(`Approve Date`)),
    Spread = Rate - `Cost of Funds`,
    YearMonth = floor_date(mdy(`Approve Date`), "month")) |>
  filter(Year >= 2002, Year <= 2012)

theme_story <- theme_minimal(base_size = 12) +
  theme(panel.grid = element_blank(),
    axis.line = element_line(color = "#EEEEEE", linewidth = 0.3),
    plot.title = element_text(face = "bold", size = 14, lineheight = 1.2),
    plot.subtitle = element_text(color = "#666", size = 10),
    plot.caption = element_text(color = "#AAA", size = 7),
    legend.position = "none")
theme_set(theme_story)

yearly <- ec |> group_by(Year) |>
  summarise(rate = mean(Rate), cof = mean(`Cost of Funds`),
    spread = mean(Spread), volume = n(), approval = mean(Outcome), .groups = "drop")

# ══════════════════════════════════════════════════════════
# SLIDE 1: CONTEXT — "150K loans across five tiers"
# ══════════════════════════════════════════════════════════
s1 <- ggplot(yearly, aes(x = Year, y = volume / 1000)) +
  geom_col(fill = "#1565C0", width = 0.6, alpha = 0.7) +
  geom_text(aes(label = paste0(round(volume / 1000, 1), "k")),
    vjust = -0.5, size = 3, fontface = "bold", color = "#1565C0") +
  scale_x_continuous(breaks = 2002:2012) +
  labs(title = "150,000 auto loans processed across five credit tiers (2002–2012)",
       subtitle = "Loan volume peaked mid-decade then fluctuated with the economic cycle",
       x = NULL, y = "Loans (thousands)",
       caption = "Source: e-Car dataset | UNYT")
ggsave("output/s1_context.png", s1, width = 10, height = 5.5, dpi = 300)

# ══════════════════════════════════════════════════════════
# SLIDE 2: COMPLICATION (HERO) — "Rates dropped 2pp"
# ══════════════════════════════════════════════════════════
peak_rate <- max(yearly$rate)
trough_rate <- min(yearly$rate)
drop_pp <- round(peak_rate - trough_rate, 1)

s2 <- ggplot(yearly) +
  annotate("rect", xmin = 2007.5, xmax = 2009.5, ymin = -Inf, ymax = Inf,
    fill = "#E53935", alpha = 0.04) +
  geom_line(aes(x = Year, y = spread), color = "#DDDDDD", linewidth = 0.8) +
  geom_line(aes(x = Year, y = rate), color = "#1565C0", linewidth = 2.5) +
  geom_point(aes(x = Year, y = rate), color = "#1565C0", size = 3) +
  geom_hline(yintercept = peak_rate, linetype = "dotted", color = "#CCC") +
  # Callout
  annotate("label", x = 2004.5, y = trough_rate * 0.9,
    label = paste0("–", drop_pp, "pp rate drop\n(Fed response to crisis)"),
    size = 3.5, fontface = "bold", color = "#E53935",
    fill = "white", label.size = 0.5) +
  annotate("segment", x = 2005.5, xend = 2009,
    y = trough_rate * 0.92, yend = trough_rate + 0.2,
    arrow = arrow(length = unit(0.15, "cm")), color = "#E53935") +
  # Lehman marker
  annotate("text", x = 2008, y = peak_rate + 0.3,
    label = "Lehman\ncollapse", size = 2.5, fontface = "bold", color = "#888") +
  annotate("segment", x = 2008, xend = 2008,
    y = peak_rate + 0.1, yend = yearly$rate[yearly$Year == 2008] + 0.1,
    arrow = arrow(length = unit(0.1, "cm")), color = "#888") +
  # Direct labels
  annotate("text", x = 2012.3, y = yearly$rate[yearly$Year == 2012],
    label = "Rate", color = "#1565C0", fontface = "bold", size = 3.5, hjust = 0) +
  annotate("text", x = 2012.3, y = yearly$spread[yearly$Year == 2012],
    label = "Spread", color = "#AAAAAA", size = 3, hjust = 0) +
  scale_x_continuous(breaks = 2002:2012, limits = c(2002, 2013)) +
  labs(title = paste0("Loan rates dropped ", drop_pp, "pp after the 2008 financial crisis"),
       subtitle = "Spread (grey) also compressed as banks competed for shrinking demand",
       x = NULL, y = "Percentage Points",
       caption = "Source: e-Car dataset | UNYT")
ggsave("output/s2_hero.png", s2, width = 10, height = 5.5, dpi = 300)

# ══════════════════════════════════════════════════════════
# SLIDE 3: MECHANISM — "Rate = CoF + Spread"
# ══════════════════════════════════════════════════════════
s3 <- ggplot(yearly) +
  annotate("rect", xmin = 2007.5, xmax = 2009.5, ymin = -Inf, ymax = Inf,
    fill = "#E53935", alpha = 0.03) +
  geom_line(aes(x = Year, y = rate), color = "#1565C0", linewidth = 2) +
  geom_line(aes(x = Year, y = cof), color = "#2E7D32", linewidth = 1.5, linetype = "dashed") +
  geom_line(aes(x = Year, y = spread), color = "#E53935", linewidth = 1.5) +
  # Direct labels
  annotate("text", x = 2012.3, y = yearly$rate[yearly$Year == 2012],
    label = "Offered Rate", color = "#1565C0", fontface = "bold", size = 3, hjust = 0) +
  annotate("text", x = 2012.3, y = yearly$cof[yearly$Year == 2012],
    label = "Cost of Funds", color = "#2E7D32", size = 3, hjust = 0) +
  annotate("text", x = 2012.3, y = yearly$spread[yearly$Year == 2012],
    label = "Spread (margin)", color = "#E53935", size = 3, hjust = 0) +
  scale_x_continuous(breaks = 2002:2012, limits = c(2002, 2014)) +
  labs(title = "The mechanism: Fed cut Cost of Funds; spread compressed under competition",
       subtitle = "Rate = Cost of Funds + Spread | The drop was mechanical, not generous",
       x = NULL, y = "Percentage Points")
ggsave("output/s3_mechanism.png", s3, width = 10, height = 5.5, dpi = 300)

# ══════════════════════════════════════════════════════════
# SLIDE 4: TIER IMPACT — "Tier 1 benefited most"
# ══════════════════════════════════════════════════════════
tier_yr <- ec |> group_by(Year, Tier) |> summarise(rate = mean(Rate), .groups = "drop")

s4 <- ggplot(tier_yr, aes(x = Year, y = rate, group = factor(Tier))) +
  geom_line(color = "#DDDDDD", linewidth = 0.7) +
  geom_line(data = tier_yr |> filter(Tier == 1),
    color = "#E53935", linewidth = 2.5) +
  geom_point(data = tier_yr |> filter(Tier == 1),
    color = "#E53935", size = 2) +
  geom_vline(xintercept = 2008, linetype = "dashed", color = "#888", linewidth = 0.3) +
  # Direct labels at right end
  geom_text(data = tier_yr |>
    group_by(Tier) |> filter(Year == max(Year)),
    aes(label = paste0("T", Tier),
        color = Tier == 1),
    hjust = -0.3, size = 3, fontface = "bold", show.legend = FALSE) +
  scale_color_manual(values = c("TRUE" = "#E53935", "FALSE" = "#AAAAAA")) +
  scale_x_continuous(breaks = c(2002, 2005, 2008, 2012), limits = c(2002, 2013)) +
  labs(title = "Tier 1 borrowers received the largest rate cuts — a regressive benefit",
       subtitle = "Grey = Tiers 2–5 | Red = Tier 1 (best credit) — dropped furthest",
       x = NULL, y = "Mean Rate (%)")
ggsave("output/s4_tiers.png", s4, width = 10, height = 5.5, dpi = 300)

# ══════════════════════════════════════════════════════════
# SLIDE 5: UNCERTAINTY — "CI width as early warning"
# ══════════════════════════════════════════════════════════
quarterly <- ec |>
  group_by(Year, Quarter) |>
  summarise(rate = mean(Rate), se = sd(Rate) / sqrt(n()),
    n = n(), .groups = "drop") |>
  mutate(date = as.Date(paste0(Year, "-", Quarter * 3 - 2, "-01")),
    lower = rate - 1.96 * se, upper = rate + 1.96 * se)

s5 <- ggplot(quarterly, aes(x = date)) +
  geom_ribbon(aes(ymin = lower, ymax = upper), fill = "#1565C0", alpha = 0.15) +
  geom_line(aes(y = rate), color = "#1565C0", linewidth = 0.8) +
  geom_vline(xintercept = as.Date("2008-09-15"),
    linetype = "dashed", color = "#E53935", linewidth = 0.5) +
  annotate("label", x = as.Date("2009-06-01"),
    y = max(quarterly$upper) * 0.95,
    label = "CI widens during\ncrisis = pricing chaos",
    size = 3, fontface = "bold", color = "#E53935",
    fill = "white", label.size = 0.4) +
  annotate("segment", x = as.Date("2009-03-01"), xend = as.Date("2008-09-15"),
    y = max(quarterly$upper) * 0.90,
    yend = quarterly$upper[abs(quarterly$date - as.Date("2008-10-01")) ==
      min(abs(quarterly$date - as.Date("2008-10-01")))],
    arrow = arrow(length = unit(0.12, "cm")), color = "#E53935") +
  scale_x_date(date_breaks = "2 years", date_labels = "%Y") +
  labs(title = "Quarterly CI width is an early warning indicator of financial stress",
       subtitle = "Ribbon = ±95% CI | CI widened months before the crisis peaked, narrowed after 2010",
       x = NULL, y = "Rate (%)")
ggsave("output/s5_uncertainty.png", s5, width = 10, height = 5.5, dpi = 300)

# ══════════════════════════════════════════════════════════
# SLIDE 6: RECOVERY + CTA
# ══════════════════════════════════════════════════════════
ec_period <- ec |> mutate(period = case_when(
  Year < 2008 ~ "Pre-crisis (2002–2007)",
  Year <= 2009 ~ "Crisis (2008–2009)",
  TRUE ~ "Recovery (2010–2012)"))

spread_by_period <- ec_period |>
  group_by(period) |>
  summarise(med = median(Spread), .groups = "drop") |>
  mutate(period = fct_relevel(period, "Pre-crisis (2002–2007)",
    "Crisis (2008–2009)", "Recovery (2010–2012)"))

s6 <- ggplot(spread_by_period, aes(x = period, y = med, fill = period)) +
  geom_col(width = 0.4, show.legend = FALSE) +
  geom_text(aes(label = paste0(round(med, 1), "pp")),
    vjust = -0.5, size = 4, fontface = "bold") +
  scale_fill_manual(values = c("#1565C0", "#E53935", "#2E7D32")) +
  labs(title = "Spread recovered post-2010 but never returned to pre-crisis levels",
       subtitle = "Median spread by period — partial recovery = new equilibrium, not full restoration",
       x = NULL, y = "Median Spread (pp)")
ggsave("output/s6_recovery.png", s6, width = 10, height = 5.5, dpi = 300)

# ══════════════════════════════════════════════════════════
# COMPOSED DECK
# ══════════════════════════════════════════════════════════
deck <- (s1 + labs(title = "1. CONTEXT")) /
  (s2 + labs(title = paste0("2. HERO: –", drop_pp, "pp rate drop"))) /
  (s3 + labs(title = "3. MECHANISM: Rate = CoF + Spread")) /
  (s4 + labs(title = "4. TIER IMPACT: Tier 1 benefited most")) /
  (s5 + labs(title = "5. EARLY WARNING: CI width signal")) /
  (s6 + labs(title = "6. RECOVERY + CTA"))
ggsave("output/ecar_story_deck.png", deck, width = 10, height = 32, dpi = 200)

cat("\n── e-Car Data Story Deck ──\n")
cat("Big Idea: 'The bank should integrate CI-based pricing volatility\n")
cat("  monitoring because the 2008 crisis caused a ", drop_pp, "pp rate drop\n")
cat("  with differential tier impact and slow spread recovery.'\n")
cat("\nStory arc:\n")
cat("  1. Context: 150K loans, 5 tiers (zoom out)\n")
cat("  2. Complication: –", drop_pp, "pp rate drop (change)\n")
cat("  3. Mechanism: Rate = CoF + Spread decomposition (factors)\n")
cat("  4. Tier impact: Tier 1 largest cuts (contrast)\n")
cat("  5. Early warning: CI width signal (outlier)\n")
cat("  6. Recovery: partial, not full (change)\n")
cat("  CTA: Integrate CI monitoring into pricing review\n")

cat("\n── All W07-M08 R outputs saved ──\n")
