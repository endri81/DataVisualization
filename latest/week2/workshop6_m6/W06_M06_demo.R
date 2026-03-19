# ============================================================
# Workshop 6 — Module 6: Animation Fundamentals
# Integrated R Script — UNYT Tirana
# ============================================================
library(tidyverse); library(patchwork); dir.create("output", showWarnings = FALSE)

# ── 1. SIMULATED GAPMINDER-STYLE DATA ───────────────────
set.seed(42); n_countries <- 40
base_gdp <- exp(runif(n_countries, 6, 10))
continents <- sample(c("Europe", "Asia", "Africa", "Americas"),
  n_countries, replace = TRUE, prob = c(0.25, 0.30, 0.25, 0.20))

df <- tibble()
for (yr in 2000:2020) {
  noise_gdp <- rnorm(n_countries, 0, 0.05)
  noise_life <- rnorm(n_countries, 0, 0.3)
  growth <- 1 + 0.02 + noise_gdp  # ~2% annual growth
  base_gdp <<- base_gdp * growth
  life_exp <- 45 + 8 * log(base_gdp / 1000) + noise_life
  pop <- abs(rnorm(n_countries, 5e6, 3e6)) * (1 + (yr - 2000) * 0.01)
  df <- bind_rows(df, tibble(
    country = paste0("Country_", 1:n_countries),
    year = yr,
    gdp = base_gdp,
    life_exp = pmin(life_exp, 85),
    pop = pop,
    continent = continents))
}

# ── 2. STATIC FRAME (2020) — the base plot ──────────────
p_static <- df |>
  filter(year == 2020) |>
  ggplot(aes(x = gdp, y = life_exp, size = pop, color = continent)) +
  geom_point(alpha = 0.6) +
  scale_x_log10(labels = scales::comma) +
  scale_size(range = c(2, 14), guide = "none") +
  scale_color_manual(values = c(
    Europe = "#1565C0", Asia = "#E53935",
    Africa = "#2E7D32", Americas = "#E65100")) +
  theme_minimal() +
  labs(title = "Gapminder-Style Static Frame: 2020",
       subtitle = "x = GDP/cap (log), y = life expectancy, size = population",
       x = "GDP per Capita (log scale)", y = "Life Expectancy",
       color = "Continent")
ggsave("output/gapminder_static_2020.png", p_static, width = 9, height = 6, dpi = 300)

# ── 3. FOUR KEY FRAMES (small multiples alternative) ────
key_years <- c(2000, 2007, 2014, 2020)
p_keyframes <- df |>
  filter(year %in% key_years) |>
  ggplot(aes(x = gdp, y = life_exp, size = pop, color = continent)) +
  geom_point(alpha = 0.5) +
  scale_x_log10(labels = scales::comma) +
  scale_size(range = c(1, 10), guide = "none") +
  scale_color_manual(values = c(
    Europe = "#1565C0", Asia = "#E53935",
    Africa = "#2E7D32", Americas = "#E65100")) +
  facet_wrap(~year, ncol = 4) +
  theme_minimal(base_size = 8) +
  labs(title = "Small Multiples: Static Alternative to Animation",
       subtitle = "Same data shown at 4 time points — all visible simultaneously",
       x = "GDP/cap (log)", y = "Life Exp.")
ggsave("output/gapminder_keyframes.png", p_keyframes, width = 16, height = 5, dpi = 300)

# ── 4. LINE REVEAL ANIMATION (transition_reveal) ────────
# Simulated Netflix-style cumulative data
nf_sim <- tibble(
  date = seq(as.Date("2015-01-01"), as.Date("2021-12-01"), by = "month"),
  titles = cumsum(rpois(84, 120)))

p_line_static <- ggplot(nf_sim, aes(x = date, y = titles)) +
  geom_line(color = "#1565C0", linewidth = 1.2) +
  geom_area(fill = "#1565C0", alpha = 0.08) +
  theme_minimal() +
  labs(title = "Cumulative Titles Over Time (static base for reveal animation)",
       x = NULL, y = "Cumulative Titles")
ggsave("output/line_reveal_static.png", p_line_static, width = 9, height = 4, dpi = 300)

# ANIMATED VERSION (uncomment to run — requires gganimate + gifski)
# library(gganimate)
#
# ── transition_reveal: line grows left-to-right ──
# p_reveal <- ggplot(nf_sim, aes(x = date, y = titles)) +
#   geom_line(color = "#1565C0", linewidth = 1.2) +
#   geom_area(fill = "#1565C0", alpha = 0.08) +
#   geom_point(color = "#E53935", size = 3) +  # dot at growing tip
#   theme_minimal() +
#   transition_reveal(date) +
#   labs(title = "Netflix Cumulative Titles",
#        subtitle = "Date: {frame_along}",
#        x = NULL, y = "Cumulative")
# animate(p_reveal, nframes = 84, fps = 10, width = 800, height = 400,
#   renderer = gifski_renderer("output/line_reveal.gif"))

# ── 5. gganimate: GAPMINDER (transition_time) ───────────
# p_gap <- df |>
#   ggplot(aes(x = gdp, y = life_exp, size = pop, color = continent)) +
#   geom_point(alpha = 0.6) +
#   scale_x_log10(labels = scales::comma) +
#   scale_size(range = c(2, 14), guide = "none") +
#   scale_color_manual(values = c(
#     Europe = "#1565C0", Asia = "#E53935",
#     Africa = "#2E7D32", Americas = "#E65100")) +
#   theme_minimal() +
#   # --- Animation layers ---
#   transition_time(year) +
#   labs(title = "Year: {frame_time}",
#        x = "GDP per Capita (log)", y = "Life Expectancy") +
#   ease_aes("cubic-in-out") +
#   shadow_wake(wake_length = 0.08, alpha = 0.2)
#
# animate(p_gap,
#   nframes = 120,  # total frames
#   fps = 10,       # frames per second
#   width = 800,
#   height = 600,
#   renderer = gifski_renderer("output/gapminder.gif"))

# ── 6. gganimate TRANSITIONS CHEATSHEET ─────────────────
# transition_time(year)      → continuous time (Gapminder)
# transition_states(year)    → discrete states (bar chart race)
# transition_reveal(date)    → cumulative reveal (line growing)
# transition_filter(cond)    → show/hide based on logical filter
# transition_layers()        → add layers sequentially
#
# EASING:
# ease_aes("linear")         → constant speed
# ease_aes("cubic-in-out")   → smooth acceleration/deceleration
# ease_aes("bounce-out")     → bouncing effect at end
#
# SHADOWS:
# shadow_wake(wake_length=)  → fading trail behind points
# shadow_mark(past=TRUE)     → keep all previous positions
# shadow_trail()             → dot trail following trajectory
#
# RENDERING:
# gifski_renderer()          → GIF (recommended)
# ffmpeg_renderer()          → MP4/video
# av_renderer()              → MP4 via av package

# ── 7. WHEN TO ANIMATE: DECISION FRAMEWORK ──────────────
# Create a visual reference card
decision <- tibble(
  scenario = c(
    "Show trajectory over time",
    "Presentation / keynote",
    "Social media engagement",
    "Compare exact values",
    "PDF report / journal paper",
    "Dashboard for analysis",
    "Gapminder exploration",
    "Print poster"),
  recommendation = c(
    "ANIMATE", "ANIMATE", "ANIMATE",
    "STATIC (small multiples)", "STATIC (key frames)",
    "STATIC (sparklines)", "ANIMATE", "STATIC"),
  reason = c(
    "Movement IS the story",
    "Audience captive, sequential",
    "Engagement, shareability",
    "Can't freeze animation frames",
    "Media doesn't support GIF",
    "Need random access, not sequence",
    "Trajectory + wake = insight",
    "No animation on paper"))

p_decision <- ggplot(decision,
  aes(x = fct_rev(fct_inorder(scenario)),
      y = 1, fill = recommendation)) +
  geom_tile(color = "white", linewidth = 1.5, height = 0.8) +
  geom_text(aes(label = paste0(recommendation, "\n", reason)),
    size = 2.5, lineheight = 1.1) +
  scale_fill_manual(values = c(
    ANIMATE = "#E3F2FD",
    "STATIC (small multiples)" = "#FFF3E0",
    "STATIC (key frames)" = "#FFF3E0",
    "STATIC (sparklines)" = "#FFF3E0",
    STATIC = "#FFF3E0")) +
  coord_flip() +
  theme_void(base_size = 9) +
  theme(axis.text.y = element_text(hjust = 1, face = "bold", size = 8),
        legend.position = "none") +
  labs(title = "Animation Decision Framework: When to Animate vs Static")
ggsave("output/animate_decision.png", p_decision, width = 10, height = 5, dpi = 300)

# ── 8. FRAME SEQUENCE (simulating animation as stills) ──
# Show the "animation" as a sequence of 6 stills
years_seq <- c(2000, 2004, 2008, 2012, 2016, 2020)
p_sequence <- df |>
  filter(year %in% years_seq) |>
  ggplot(aes(x = gdp, y = life_exp, size = pop, color = continent)) +
  geom_point(alpha = 0.5) +
  scale_x_log10() + scale_size(range = c(1, 8), guide = "none") +
  scale_color_manual(values = c(
    Europe = "#1565C0", Asia = "#E53935",
    Africa = "#2E7D32", Americas = "#E65100")) +
  facet_wrap(~year, ncol = 6) +
  theme_minimal(base_size = 7) +
  theme(legend.position = "bottom", legend.text = element_text(size = 6)) +
  labs(title = "Animation as 6 Stills: the frames gganimate interpolates between",
       x = "GDP/cap (log)", y = "Life Exp.")
ggsave("output/frame_sequence.png", p_sequence, width = 16, height = 4, dpi = 300)

cat("\n── All W06-M06 R outputs saved ──\n")
cat("Figures: gapminder_static_2020, gapminder_keyframes,\n")
cat("  line_reveal_static, animate_decision, frame_sequence\n")
cat("Animation code: commented out (requires gganimate + gifski)\n")
