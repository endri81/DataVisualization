# ============================================================
# Workshop 8 — Module 1: Interactivity Theory
# Integrated R Script — UNYT Tirana
# ============================================================
# This module introduces interactive concepts. The demo shows
# the SAME data rendered as static (ggplot2) vs interactive (plotly),
# demonstrating what interactivity adds.
library(tidyverse); library(plotly); dir.create("output", showWarnings = FALSE)

# ── 1. LOAD DATA ────────────────────────────────────────
nf <- read_csv("netflix.csv") |>
  mutate(date_added = mdy(str_trim(date_added)),
    year_added = year(date_added),
    primary_country = str_trim(str_extract(country, "^[^,]+")))

# ── 2. STATIC VERSION (ggplot2 — W07 style) ─────────────
yearly <- nf |>
  filter(!is.na(year_added), year_added >= 2015, year_added <= 2021) |>
  count(year_added, type)

p_static <- ggplot(yearly, aes(x = year_added, y = n, color = type)) +
  geom_line(linewidth = 1.5) + geom_point(size = 3) +
  scale_color_manual(values = c(Movie = "#1565C0", "TV Show" = "#E53935")) +
  theme_minimal() +
  labs(title = "STATIC (ggplot2): Author-driven, no interactivity",
       subtitle = "The reader sees exactly what you designed — nothing more",
       x = "Year", y = "Titles Added", color = "Type")
ggsave("output/static_version.png", p_static, width = 9, height = 5, dpi = 300)

# ── 3. INTERACTIVE VERSION (plotly — W08 style) ─────────
# Approach 1: ggplotly (convert existing ggplot)
p_gg <- ggplot(yearly, aes(x = year_added, y = n, color = type,
  text = paste0("Year: ", year_added, "\nType: ", type,
    "\nTitles: ", n))) +
  geom_line(linewidth = 1) + geom_point(size = 2) +
  scale_color_manual(values = c(Movie = "#1565C0", "TV Show" = "#E53935")) +
  theme_minimal() +
  labs(title = "Interactive (ggplotly): hover for details",
       x = "Year", y = "Titles Added", color = "Type")

p_interactive <- ggplotly(p_gg, tooltip = "text") |>
  layout(hoverlabel = list(bgcolor = "white"))

# Save as standalone HTML
htmlwidgets::saveWidget(p_interactive, "output/interactive_ggplotly.html",
  selfcontained = TRUE)

# Approach 2: plot_ly (native plotly syntax)
p_native <- plot_ly(yearly, x = ~year_added, y = ~n, color = ~type,
  colors = c(Movie = "#1565C0", "TV Show" = "#E53935"),
  type = "scatter", mode = "lines+markers",
  text = ~paste0("Year: ", year_added, "<br>Type: ", type,
    "<br>Titles: ", n),
  hoverinfo = "text") |>
  layout(
    title = list(text = "Native plot_ly: full control over interactivity"),
    xaxis = list(title = "Year"),
    yaxis = list(title = "Titles Added"),
    hovermode = "x unified")

htmlwidgets::saveWidget(p_native, "output/interactive_plotly.html",
  selfcontained = TRUE)

# ── 4. SHNEIDERMAN'S MANTRA IN CODE ─────────────────────
# Demonstrate each step on a scatter plot

# Step 1: OVERVIEW — show all titles
scatter_data <- nf |>
  filter(!is.na(year_added), !is.na(date_added)) |>
  sample_n(min(2000, n())) |>
  mutate(duration_num = parse_number(duration))

p_overview <- plot_ly(scatter_data,
  x = ~year_added, y = ~duration_num,
  color = ~type, colors = c(Movie = "#1565C0", "TV Show" = "#E53935"),
  type = "scatter", mode = "markers",
  marker = list(size = 4, opacity = 0.4),
  text = ~paste0("<b>", title, "</b><br>",
    type, " (", year_added, ")<br>",
    "Duration: ", duration, "<br>",
    "Rating: ", rating),
  hoverinfo = "text") |>
  layout(
    title = "Step 1: OVERVIEW — all titles by year and duration",
    xaxis = list(title = "Year Added", range = c(2008, 2022)),
    yaxis = list(title = "Duration (minutes/seasons)"),
    # Step 2: ZOOM is built-in (scroll wheel)
    # Step 3: FILTER via dropdown
    updatemenus = list(
      list(
        type = "dropdown",
        x = 0.1, y = 1.15,
        buttons = list(
          list(method = "restyle",
            args = list("visible", list(TRUE, TRUE)),
            label = "Both"),
          list(method = "restyle",
            args = list("visible", list(TRUE, FALSE)),
            label = "Movies Only"),
          list(method = "restyle",
            args = list("visible", list(FALSE, TRUE)),
            label = "TV Shows Only")
        )
      )
    ))
    # Step 4: DETAILS ON DEMAND = hover tooltip (already configured)
    # Step 5: RELATE = see M02 (linked brushing)
    # Step 6: HISTORY = plotly has reset axes button built-in
    # Step 7: EXTRACT = plotly modebar has "Download as PNG"

htmlwidgets::saveWidget(p_overview, "output/shneiderman_demo.html",
  selfcontained = TRUE)

# ── 5. STATIC vs INTERACTIVE COMPARISON TABLE ────────────
cat("\n── Static vs Interactive Comparison ──\n")
comparison <- tibble(
  dimension = c("Hover tooltip", "Zoom", "Filter", "Linked brushing",
    "Export PNG", "Reset view", "Audience control"),
  static_ggplot = c("No", "No", "No", "No", "Manual ggsave()", "N/A", "None"),
  interactive_plotly = c("Yes (built-in)", "Yes (scroll/drag)",
    "Yes (dropdown/slider)", "Yes (highlight)", "Yes (modebar)",
    "Yes (reset axes)", "Full"))
print(comparison, n = 7)

# ── 6. WHEN TO USE INTERACTIVITY ─────────────────────────
cat("\n── Decision Framework: Static vs Interactive ──\n")
decisions <- tibble(
  context = c("Board presentation", "PDF report", "Ongoing monitoring",
    "Self-service analytics", "Ad-hoc exploration", "Journal paper",
    "Team data review", "Social media"),
  recommendation = c("Static", "Static", "Interactive", "Interactive",
    "Interactive", "Static", "Interactive", "Static"),
  tool = c("ggplot2/matplotlib", "ggplot2/matplotlib", "Shiny/Dash",
    "Shiny/Dash", "plotly notebook", "ggplot2/matplotlib",
    "plotly/Shiny", "ggplot2/matplotlib"))
print(decisions, n = 8)

cat("\n── All W08-M01 R outputs saved ──\n")
cat("Static: output/static_version.png\n")
cat("Interactive: output/interactive_ggplotly.html, interactive_plotly.html\n")
cat("Shneiderman demo: output/shneiderman_demo.html\n")
