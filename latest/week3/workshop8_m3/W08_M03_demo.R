# ============================================================
# Workshop 8 — Module 3: plotly in Python (R companion)
# Shows the EQUIVALENT R patterns for each Python technique
# ============================================================
library(tidyverse); library(plotly); library(htmlwidgets)
dir.create("output", showWarnings = FALSE)

nf <- read_csv("netflix.csv") |>
  mutate(date_added = mdy(str_trim(date_added)),
    year_added = year(date_added),
    primary_country = str_trim(str_extract(country, "^[^,]+")),
    duration_num = parse_number(duration))
yearly <- nf |> filter(!is.na(year_added), year_added >= 2015, year_added <= 2021) |>
  count(year_added, type)

# ── 1. R EQUIVALENT OF px.line ───────────────────────────
p_gg <- ggplot(yearly, aes(x = year_added, y = n, color = type,
    text = paste0("Year: ", year_added, "\nType: ", type, "\nTitles: ", n))) +
  geom_line(linewidth = 1) + geom_point(size = 2) +
  scale_color_manual(values = c(Movie = "#1565C0", "TV Show" = "#E53935")) +
  theme_minimal() + labs(title = "R equivalent of px.line")
p1 <- ggplotly(p_gg, tooltip = "text") |>
  layout(hovermode = "x unified")
saveWidget(p1, "output/01_r_equivalent_px_line.html", selfcontained = TRUE)

# ── 2. R EQUIVALENT OF go.Scatter ────────────────────────
movies <- yearly |> filter(type == "Movie")
tv <- yearly |> filter(type == "TV Show")
peak <- max(movies$n); decline <- round((1 - movies$n[movies$year_added == 2021] / peak) * 100)

p2 <- plot_ly() |>
  add_trace(data = movies, x = ~year_added, y = ~n,
    type = "scatter", mode = "lines+markers", name = "Movie",
    line = list(color = "#1565C0", width = 3),
    hovertemplate = "<b>Movie</b><br>Year: %{x}<br>Titles: %{y:,}<extra></extra>") |>
  add_trace(data = tv, x = ~year_added, y = ~n,
    type = "scatter", mode = "lines+markers", name = "TV Show",
    line = list(color = "#E53935", width = 1.5),
    hovertemplate = "<b>TV Show</b><br>Year: %{x}<br>Titles: %{y:,}<extra></extra>") |>
  layout(title = paste0("R equivalent of go.Scatter (–", decline, "%)"),
    annotations = list(list(
      x = 2020, y = (peak + movies$n[movies$year_added == 2021]) / 2,
      text = paste0("<b>–", decline, "%</b>"),
      showarrow = TRUE, arrowhead = 2, arrowcolor = "#E53935",
      font = list(color = "#E53935", size = 14), ax = -60, ay = -40)),
    xaxis = list(title = "Year"), yaxis = list(title = "Titles"))
saveWidget(p2, "output/02_r_equivalent_go.html", selfcontained = TRUE)

# ── 3. R EQUIVALENT OF make_subplots ─────────────────────
p_line <- plot_ly(yearly, x = ~year_added, y = ~n, color = ~type,
  colors = c(Movie = "#1565C0", "TV Show" = "#E53935"),
  type = "scatter", mode = "lines+markers")
p_bar <- plot_ly(yearly, x = ~year_added, y = ~n, color = ~type,
  colors = c(Movie = "#1565C0", "TV Show" = "#E53935"),
  type = "bar")
p3 <- subplot(p_line, p_bar, nrows = 2, shareX = TRUE) |>
  layout(title = "R equivalent of make_subplots", barmode = "group")
saveWidget(p3, "output/03_r_equivalent_subplot.html", selfcontained = TRUE)

# ── 4. R EQUIVALENT OF animation_frame ───────────────────
nf_genres <- nf |> separate_rows(listed_in, sep = ", ") |>
  mutate(genre = str_trim(listed_in))
top5 <- nf_genres |> count(genre, sort = TRUE) |> slice_max(n, n = 5) |> pull(genre)
genre_yr <- nf_genres |>
  filter(genre %in% top5, !is.na(year_added), year_added >= 2015, year_added <= 2021) |>
  count(year_added, genre)

p4 <- plot_ly(genre_yr, x = ~genre, y = ~n, color = ~genre,
  type = "bar", frame = ~year_added) |>
  layout(title = "R equivalent of px animation (press Play)",
    yaxis = list(range = c(0, max(genre_yr$n) * 1.2))) |>
  animation_opts(frame = 500, transition = 300)
saveWidget(p4, "output/04_r_equivalent_animation.html", selfcontained = TRUE)

cat("\n── R↔Python Equivalence Table ──\n")
cat("  px.line()          ↔  ggplotly(ggplot() + geom_line())\n")
cat("  px.scatter()       ↔  ggplotly(ggplot() + geom_point())\n")
cat("  go.Scatter()       ↔  plot_ly() |> add_trace()\n")
cat("  go.Bar()           ↔  plot_ly(type='bar')\n")
cat("  make_subplots()    ↔  subplot(p1, p2, shareX=TRUE)\n")
cat("  animation_frame=   ↔  frame=~year in plot_ly()\n")
cat("  fig.write_html()   ↔  saveWidget(p, 'f.html')\n")
cat("  updatemenus=       ↔  layout(updatemenus=list(...))\n")

cat("\n── All W08-M03 R companion outputs saved ──\n")
