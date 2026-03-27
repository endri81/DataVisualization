# ============================================================
# Workshop 8 — Module 2: plotly in R
# Integrated R Script — UNYT Tirana
# ============================================================
library(tidyverse); library(plotly); library(htmlwidgets)
dir.create("output", showWarnings = FALSE)

# ── 1. LOAD DATA ────────────────────────────────────────
nf <- read_csv("netflix.csv") |>
  mutate(date_added = mdy(str_trim(date_added)),
    year_added = year(date_added),
    primary_country = str_trim(str_extract(country, "^[^,]+")),
    duration_num = parse_number(duration))

yearly <- nf |>
  filter(!is.na(year_added), year_added >= 2015, year_added <= 2021) |>
  count(year_added, type)
movies <- yearly |> filter(type == "Movie")
tv <- yearly |> filter(type == "TV Show")

# ══════════════════════════════════════════════════════════
# APPROACH 1: ggplotly — convert existing ggplot
# ══════════════════════════════════════════════════════════

# ── 2. BASIC ggplotly ────────────────────────────────────
p_gg <- ggplot(yearly, aes(x = year_added, y = n, color = type,
    text = paste0("<b>", type, "</b><br>",
      "Year: ", year_added, "<br>",
      "Titles: ", format(n, big.mark = ",")))) +
  geom_line(linewidth = 1) + geom_point(size = 2) +
  scale_color_manual(values = c(Movie = "#1565C0", "TV Show" = "#E53935")) +
  theme_minimal() +
  labs(title = "ggplotly: Netflix Additions by Type",
       x = "Year", y = "Titles Added", color = "Type")

p1 <- ggplotly(p_gg, tooltip = "text") |>
  layout(hovermode = "x unified",
    hoverlabel = list(bgcolor = "white", font = list(size = 11)))

saveWidget(p1, "output/01_ggplotly_basic.html", selfcontained = TRUE)

# ── 3. ggplotly WITH ANNOTATIONS ─────────────────────────
peak <- movies |> slice_max(n, n = 1)
decline <- round((1 - movies$n[movies$year_added == 2021] / peak$n) * 100)

p_annotated <- ggplot(yearly, aes(x = year_added, y = n, group = type,
    text = paste0(type, ": ", n, " titles (", year_added, ")"))) +
  geom_line(aes(color = type == "Movie"), linewidth = 1) +
  geom_point(data = movies, color = "#1565C0", size = 3) +
  scale_color_manual(values = c("TRUE" = "#1565C0", "FALSE" = "#DDDDDD"),
    guide = "none") +
  theme_minimal() +
  labs(title = paste0("Movie additions declined ", decline, "% from peak"))

p2 <- ggplotly(p_annotated, tooltip = "text") |>
  layout(
    annotations = list(
      list(x = 2020, y = movies$n[movies$year_added == 2021],
        text = paste0("<b>–", decline, "%</b>"),
        showarrow = TRUE, arrowhead = 2, arrowcolor = "#E53935",
        font = list(color = "#E53935", size = 14),
        ax = -50, ay = -40)),
    hovermode = "x unified")

saveWidget(p2, "output/02_ggplotly_annotated.html", selfcontained = TRUE)

# ══════════════════════════════════════════════════════════
# APPROACH 2: plot_ly — native syntax, full control
# ══════════════════════════════════════════════════════════

# ── 4. NATIVE plot_ly LINE CHART ─────────────────────────
p3 <- plot_ly() |>
  add_trace(data = movies,
    x = ~year_added, y = ~n,
    type = "scatter", mode = "lines+markers",
    name = "Movie",
    line = list(color = "#1565C0", width = 3),
    marker = list(size = 8, color = "#1565C0"),
    hovertemplate = paste0(
      "<b>Movie</b><br>",
      "Year: %{x}<br>",
      "Titles: %{y:,}<extra></extra>")) |>
  add_trace(data = tv,
    x = ~year_added, y = ~n,
    type = "scatter", mode = "lines+markers",
    name = "TV Show",
    line = list(color = "#E53935", width = 1.5, dash = "dot"),
    marker = list(size = 5, color = "#E53935"),
    hovertemplate = paste0(
      "<b>TV Show</b><br>",
      "Year: %{x}<br>",
      "Titles: %{y:,}<extra></extra>")) |>
  layout(
    title = list(text = "plot_ly: Full control over traces and tooltips"),
    xaxis = list(title = "Year"),
    yaxis = list(title = "Titles Added"),
    hovermode = "x unified",
    template = "plotly_white")

saveWidget(p3, "output/03_plotly_native.html", selfcontained = TRUE)

# ── 5. SCATTER WITH HOVER DETAILS ────────────────────────
sample <- nf |>
  filter(!is.na(year_added), !is.na(duration_num)) |>
  sample_n(min(1500, n()))

p4 <- plot_ly(sample,
  x = ~year_added, y = ~duration_num,
  color = ~type,
  colors = c(Movie = "#1565C0", "TV Show" = "#E53935"),
  type = "scatter", mode = "markers",
  marker = list(size = 5, opacity = 0.4),
  text = ~paste0("<b>", title, "</b><br>",
    "Type: ", type, "<br>",
    "Year: ", year_added, "<br>",
    "Duration: ", duration, "<br>",
    "Rating: ", rating, "<br>",
    "Country: ", primary_country),
  hoverinfo = "text") |>
  layout(
    title = "Scatter: hover for full title metadata",
    xaxis = list(title = "Year Added"),
    yaxis = list(title = "Duration (min/seasons)"),
    hovermode = "closest")

saveWidget(p4, "output/04_scatter_details.html", selfcontained = TRUE)

# ── 6. DROPDOWN FILTER (updatemenus) ────────────────────
# Ratings filter
ratings <- nf |> filter(!is.na(rating)) |>
  count(rating, sort = TRUE) |> slice_max(n, n = 6) |> pull(rating)

rating_yearly <- nf |>
  filter(!is.na(year_added), year_added >= 2015, year_added <= 2021,
    rating %in% ratings) |>
  count(year_added, rating)

p5 <- plot_ly()
for (r in ratings) {
  sub <- rating_yearly |> filter(rating == r)
  p5 <- p5 |> add_trace(data = sub,
    x = ~year_added, y = ~n,
    type = "scatter", mode = "lines+markers",
    name = r, visible = TRUE,
    hovertemplate = paste0("<b>", r, "</b><br>Year: %{x}<br>Count: %{y}<extra></extra>"))
}

# Dropdown buttons
buttons <- list(
  list(method = "restyle",
    args = list("visible", as.list(rep(TRUE, length(ratings)))),
    label = "All Ratings"))
for (i in seq_along(ratings)) {
  vis <- rep(FALSE, length(ratings)); vis[i] <- TRUE
  buttons[[i + 1]] <- list(method = "restyle",
    args = list("visible", as.list(vis)),
    label = ratings[i])
}

p5 <- p5 |> layout(
  title = "Dropdown Filter: Select a Rating",
  updatemenus = list(list(type = "dropdown", x = 0.1, y = 1.15,
    buttons = buttons)),
  xaxis = list(title = "Year"), yaxis = list(title = "Titles"))

saveWidget(p5, "output/05_dropdown_filter.html", selfcontained = TRUE)

# ── 7. SUBPLOT: TWO CHARTS, SHARED X-AXIS ───────────────
p_line <- plot_ly(yearly, x = ~year_added, y = ~n, color = ~type,
  colors = c(Movie = "#1565C0", "TV Show" = "#E53935"),
  type = "scatter", mode = "lines+markers") |>
  layout(yaxis = list(title = "Count"))

p_bar <- plot_ly(yearly, x = ~year_added, y = ~n, color = ~type,
  colors = c(Movie = "#1565C0", "TV Show" = "#E53935"),
  type = "bar") |>
  layout(yaxis = list(title = "Count"), barmode = "group")

p6 <- subplot(p_line, p_bar, nrows = 2, shareX = TRUE, titleY = TRUE) |>
  layout(title = "subplot: line + bar with shared x-axis (zoom syncs)")

saveWidget(p6, "output/06_subplot.html", selfcontained = TRUE)

# ── 8. LINKED BRUSHING (crosstalk) ──────────────────────
library(crosstalk)
sd <- SharedData$new(sample |> filter(!is.na(rating)), key = ~show_id)

p_scatter <- plot_ly(sd, x = ~year_added, y = ~duration_num,
  color = ~type, type = "scatter", mode = "markers",
  marker = list(size = 4, opacity = 0.5))

p_hist <- plot_ly(sd, x = ~rating, type = "histogram",
  marker = list(color = "#1565C0"))

p7 <- subplot(p_scatter, p_hist, nrows = 1, widths = c(0.6, 0.4)) |>
  highlight(on = "plotly_selected", off = "plotly_deselect",
    color = "#E53935") |>
  layout(title = "Linked Brushing: select in scatter → highlights in histogram",
    dragmode = "select")

saveWidget(p7, "output/07_linked_brushing.html", selfcontained = TRUE)

cat("\n── All W08-M02 R outputs saved ──\n")
cat("7 interactive HTML files in output/\n")
cat("01: ggplotly basic\n02: ggplotly annotated\n")
cat("03: native plot_ly\n04: scatter with details\n")
cat("05: dropdown filter\n06: subplot shared axes\n")
cat("07: linked brushing (crosstalk)\n")
