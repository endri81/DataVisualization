# ============================================================
# Workshop 7 — Module 9: Audience Adaptation
# Integrated R Script — UNYT Tirana
# ============================================================
# Same finding → 3 audience variants (executive, technical, public)
library(tidyverse); library(patchwork); dir.create("output", showWarnings = FALSE)

theme_story <- theme_minimal(base_size = 12) +
  theme(panel.grid = element_blank(),
    axis.line = element_line(color = "#EEE", linewidth = 0.3),
    plot.title = element_text(face = "bold", size = 14, lineheight = 1.2),
    plot.subtitle = element_text(color = "#666", size = 10),
    legend.position = "none")
theme_set(theme_story)

# ── LOAD DATA ────────────────────────────────────────────
nf <- read_csv("netflix.csv") |>
  mutate(date_added = mdy(str_trim(date_added)), year_added = year(date_added))
yearly <- nf |> filter(!is.na(year_added), year_added >= 2016, year_added <= 2021) |>
  count(year_added, type)
movies <- yearly |> filter(type == "Movie")
tv <- yearly |> filter(type == "TV Show")
peak <- movies |> slice_max(n, n = 1)
decline <- round((1 - movies$n[movies$year_added == 2021] / peak$n) * 100)

# ═══════════════════════════════════════════════════════
# VARIANT 1: EXECUTIVE
# One message, one chart, one number
# ═══════════════════════════════════════════════════════
p_exec <- ggplot(yearly, aes(x = year_added, y = n, group = type)) +
  geom_line(color = "#DDDDDD", linewidth = 0.8) +
  geom_line(data = movies, color = "#1565C0", linewidth = 2.5) +
  geom_point(data = movies, color = "#1565C0", size = 3) +
  annotate("label", x = 2018.5, y = movies$n[movies$year_added == 2021] * 0.80,
    label = paste0("–", decline, "%\nfrom 2019 peak"),
    size = 4, fontface = "bold", color = "#E53935",
    fill = "white", label.size = 0.5) +
  geom_text(data = yearly |> filter(year_added == 2021),
    aes(label = type, color = type == "Movie"),
    hjust = -0.1, size = 3.5, fontface = "bold", show.legend = FALSE) +
  scale_color_manual(values = c("TRUE" = "#1565C0", "FALSE" = "#BBB")) +
  coord_cartesian(xlim = c(2016, 2022.5)) +
  labs(title = paste0("Movie additions declined ", decline, "% from their 2019 peak"),
       subtitle = "Recommendation: reallocate content budget to originals + local markets",
       x = NULL, y = "Titles Added")
ggsave("output/exec_variant.png", p_exec, width = 10, height = 5.5, dpi = 300)

# ═══════════════════════════════════════════════════════
# VARIANT 2: TECHNICAL (Data Science Team)
# Full detail, both series, CI, methodology visible
# ═══════════════════════════════════════════════════════
# Compute monthly with CI
monthly <- nf |>
  filter(!is.na(date_added), year(date_added) >= 2016) |>
  mutate(month = floor_date(date_added, "month")) |>
  count(month, type) |>
  group_by(type) |> arrange(month) |>
  mutate(roll_mean = zoo::rollmean(n, k = 3, fill = NA, align = "right"),
    roll_sd = zoo::rollapply(n, width = 3, FUN = sd, fill = NA, align = "right")) |>
  ungroup()

p_tech <- ggplot(monthly, aes(x = month, y = n, color = type)) +
  geom_point(size = 0.8, alpha = 0.3) +
  geom_line(aes(y = roll_mean), linewidth = 1) +
  geom_ribbon(aes(ymin = pmax(roll_mean - 1.96 * roll_sd, 0),
    ymax = roll_mean + 1.96 * roll_sd, fill = type),
    alpha = 0.1, color = NA) +
  scale_color_manual(values = c(Movie = "#1565C0", "TV Show" = "#E53935")) +
  scale_fill_manual(values = c(Movie = "#1565C0", "TV Show" = "#E53935")) +
  theme_minimal(base_size = 10) +
  theme(panel.grid.major.y = element_line(color = "#F0F0F0"),
    legend.position = "bottom") +
  labs(title = "Netflix Monthly Additions by Type (2016–2021)",
       subtitle = "3-month rolling mean ± 1.96σ ribbon | Raw points shown for variance assessment",
       x = NULL, y = "Monthly Titles Added", color = NULL, fill = NULL,
       caption = "Method: rolling window k=3, align=right | Source: netflix.csv")
ggsave("output/tech_variant.png", p_tech, width = 10, height = 5.5, dpi = 300)

# ═══════════════════════════════════════════════════════
# VARIANT 3: PUBLIC (Blog / Social Media)
# Simplest possible, no jargon, big labels
# ═══════════════════════════════════════════════════════
p_public <- ggplot(movies, aes(x = factor(year_added), y = n)) +
  geom_col(fill = "#1565C0", width = 0.5, alpha = 0.8) +
  geom_text(aes(label = format(n, big.mark = ",")),
    vjust = -0.5, size = 4, fontface = "bold", color = "#1565C0") +
  theme_minimal(base_size = 14) +
  theme(panel.grid = element_blank(),
    axis.line.x = element_line(color = "#EEE"),
    plot.title = element_text(face = "bold", size = 16)) +
  labs(title = "Netflix is adding fewer movies every year since 2019",
       subtitle = "The streaming giant's movie catalog is shrinking",
       x = "Year", y = NULL)
ggsave("output/public_variant.png", p_public, width = 9, height = 5, dpi = 300)

# ═══════════════════════════════════════════════════════
# SIDE-BY-SIDE COMPARISON
# ═══════════════════════════════════════════════════════
ggsave("output/three_audiences.png",
  (p_exec + labs(title = "EXECUTIVE\n1 message, grey+accent, callout")) |
  (p_tech + labs(title = "TECHNICAL\nBoth series, CI ribbon, raw data")) |
  (p_public + labs(title = "PUBLIC\nSimple bar, big labels, no jargon")),
  width = 22, height = 6, dpi = 300)

# ═══════════════════════════════════════════════════════
# e-Car: 3 AUDIENCE VARIANTS
# ═══════════════════════════════════════════════════════
ec <- read_csv("ecar.csv") |>
  mutate(Year = year(mdy(`Approve Date`)),
    Spread = Rate - `Cost of Funds`) |>
  filter(Year >= 2002, Year <= 2012)
yr_ec <- ec |> group_by(Year) |>
  summarise(rate = mean(Rate), spread = mean(Spread))

# Executive
p_ec_exec <- ggplot(yr_ec) +
  annotate("rect", xmin = 2007.5, xmax = 2009.5, ymin = -Inf, ymax = Inf,
    fill = "#E53935", alpha = 0.04) +
  geom_line(aes(x = Year, y = spread), color = "#DDD", linewidth = 0.8) +
  geom_line(aes(x = Year, y = rate), color = "#1565C0", linewidth = 2.5) +
  annotate("label", x = 2005, y = min(yr_ec$rate) * 0.92,
    label = "–2pp\nrate drop", size = 4, fontface = "bold",
    color = "#E53935", fill = "white", label.size = 0.5) +
  annotate("text", x = 2012.3, y = yr_ec$rate[yr_ec$Year == 2012],
    label = "Rate", fontface = "bold", color = "#1565C0", size = 3.5, hjust = 0) +
  scale_x_continuous(limits = c(2002, 2013)) +
  labs(title = "Loan rates dropped 2pp after the 2008 crisis",
       subtitle = "Action: integrate CI-based early warning into pricing reviews")

# Technical
tier_yr <- ec |> group_by(Year, Tier) |> summarise(rate = mean(Rate), .groups = "drop")
p_ec_tech <- ggplot(tier_yr, aes(x = Year, y = rate, color = factor(Tier))) +
  geom_line(linewidth = 0.8) + geom_point(size = 1.5) +
  geom_vline(xintercept = 2008, linetype = "dashed", color = "#888") +
  theme_minimal(base_size = 9) +
  theme(legend.position = "bottom") +
  labs(title = "Mean Rate by Credit Tier (2002–2012)",
       subtitle = "Tier-stratified view | Vertical line = 2008 crisis onset",
       color = "Credit Tier", y = "Mean Rate (%)")

# Public
p_ec_public <- ggplot(yr_ec, aes(x = Year, y = rate)) +
  geom_col(fill = "#1565C0", width = 0.5, alpha = 0.8) +
  theme_minimal(base_size = 14) +
  theme(panel.grid = element_blank()) +
  labs(title = "Car loan rates dropped sharply\nafter the 2008 financial crisis",
       subtitle = "Average interest rate on auto loans, by year", y = "Rate (%)")

ggsave("output/ecar_three_audiences.png",
  (p_ec_exec + labs(title = "EXECUTIVE")) |
  (p_ec_tech + labs(title = "TECHNICAL")) |
  (p_ec_public + labs(title = "PUBLIC")),
  width = 22, height = 6, dpi = 300)

# ═══════════════════════════════════════════════════════
# MEDIUM ADAPTATION: same exec chart, 3 channels
# ═══════════════════════════════════════════════════════
# Presentation: large fonts, minimal
p_present <- p_exec +
  theme(text = element_text(size = 16),
    plot.title = element_text(size = 20)) +
  labs(title = "FOR PROJECTION\n(large fonts, minimal detail)")

# Email: self-contained with caption
p_email <- p_exec +
  labs(title = "FOR EMAIL\n(self-contained: title + chart tell full story)",
       caption = "Data: Netflix dataset. Analysis: Data Viz Team. Date: March 2025.")

# Social: bold, crop-friendly
p_social <- p_public +
  theme(text = element_text(size = 18),
    plot.title = element_text(size = 22),
    plot.margin = margin(20, 20, 20, 20)) +
  labs(title = "FOR SOCIAL MEDIA\n(big, bold, 3-second read)")

ggsave("output/medium_adaptation.png",
  p_present / p_email / p_social,
  width = 10, height = 16, dpi = 300)

cat("\n── All W07-M09 R outputs saved ──\n")
cat("Variants: exec, tech, public (Netflix + e-Car)\n")
cat("Medium: presentation, email, social\n")
