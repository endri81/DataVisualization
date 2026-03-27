# ============================================================
# Workshop 8 — Module 9: Deployment & Sharing
# Integrated R Script — UNYT Tirana
# ============================================================
library(tidyverse); library(plotly); library(htmlwidgets)
dir.create("output", showWarnings = FALSE)

nf <- read_csv("netflix.csv") |>
  mutate(date_added = mdy(str_trim(date_added)), year_added = year(date_added))
yearly <- nf |> filter(!is.na(year_added), year_added >= 2015, year_added <= 2021) |>
  count(year_added, type)

# ══════════════════════════════════════════════════════════
# 1. STANDALONE HTML: simplest sharing method
# ══════════════════════════════════════════════════════════
p <- ggplot(yearly, aes(x = year_added, y = n, color = type,
    text = paste0(type, ": ", n, " (", year_added, ")"))) +
  geom_line(linewidth = 1.2) + geom_point(size = 2.5) +
  scale_color_manual(values = c(Movie = "#1565C0", "TV Show" = "#E53935")) +
  theme_minimal() +
  labs(title = "Netflix Additions by Type", x = "Year", y = "Titles", color = NULL)

p_interactive <- ggplotly(p, tooltip = "text") |>
  layout(hovermode = "x unified")

# Self-contained: includes plotly.js (~3 MB)
saveWidget(p_interactive, "output/chart_selfcontained.html", selfcontained = TRUE)

# CDN version: tiny file (~50 KB) but needs internet
saveWidget(p_interactive, "output/chart_cdn.html", selfcontained = FALSE)

# ══════════════════════════════════════════════════════════
# 2. SHINYAPPS.IO DEPLOYMENT STRUCTURE
# ══════════════════════════════════════════════════════════
# The deployment directory must contain:
# app.R (or ui.R + server.R)
# data files (netflix.csv)
# No absolute paths!

deploy_dir <- "output/shiny_deploy/"
dir.create(deploy_dir, recursive = TRUE, showWarnings = FALSE)

# Write a minimal deployable app
app_code <- '
library(shiny); library(tidyverse); library(plotly)
nf <- read_csv("netflix.csv")  # RELATIVE path
nf$date_added <- mdy(str_trim(nf$date_added))
nf$year_added <- year(nf$date_added)

ui <- fluidPage(
  titlePanel("Netflix Dashboard"),
  sidebarLayout(
    sidebarPanel(width = 3,
      selectInput("type", "Type:", c("All", "Movie", "TV Show")),
      sliderInput("years", "Years:", 2015, 2021, c(2015, 2021), sep = "")),
    mainPanel(plotlyOutput("chart"), textOutput("count"))))

server <- function(input, output, session) {
  filtered <- reactive({
    df <- nf |> filter(!is.na(year_added),
      year_added >= input$years[1], year_added <= input$years[2])
    if (input$type != "All") df <- filter(df, type == input$type)
    df
  })
  output$chart <- renderPlotly({
    yr <- filtered() |> count(year_added, type)
    p <- ggplot(yr, aes(x = year_added, y = n, color = type,
      text = paste0(type, ": ", n))) +
      geom_line(linewidth = 1) + geom_point(size = 2) +
      scale_color_manual(values = c(Movie = "#1565C0", "TV Show" = "#E53935")) +
      theme_minimal()
    ggplotly(p, tooltip = "text") |> layout(hovermode = "x unified")
  })
  output$count <- renderText(paste0("Showing ", nrow(filtered()), " titles"))
}

shinyApp(ui, server)
'
writeLines(app_code, paste0(deploy_dir, "app.R"))
# Copy data file
file.copy("netflix.csv", paste0(deploy_dir, "netflix.csv"), overwrite = TRUE)

cat("Shiny deployment directory ready: output/shiny_deploy/\n")
cat("Contents: app.R + netflix.csv\n")
cat("Deploy with: rsconnect::deployApp('output/shiny_deploy/')\n\n")

# ══════════════════════════════════════════════════════════
# 3. QUARTO DASHBOARD TEMPLATE
# ══════════════════════════════════════════════════════════
quarto_template <- '---
title: "Netflix Content Dashboard"
format:
  dashboard:
    orientation: rows
    theme: flatly
---

```{r}
#| label: setup
#| include: false
library(tidyverse); library(plotly)
nf <- read_csv("netflix.csv") |>
  mutate(date_added = mdy(str_trim(date_added)),
    year_added = year(date_added))
yearly <- nf |> filter(!is.na(year_added), year_added >= 2015, year_added <= 2021) |>
  count(year_added, type)
```

## Row {height=30%}

### Total Titles
```{r}
#| content: valuebox
list(value = format(nrow(nf), big.mark = ","), icon = "film",
  color = "primary", title = "Total Titles")
```

### Movies
```{r}
#| content: valuebox
list(value = format(sum(nf$type == "Movie", na.rm = TRUE), big.mark = ","),
  icon = "camera-reels", color = "info", title = "Movies")
```

### TV Shows
```{r}
#| content: valuebox
list(value = format(sum(nf$type == "TV Show", na.rm = TRUE), big.mark = ","),
  icon = "tv", color = "danger", title = "TV Shows")
```

## Row {height=70%}

### Yearly Trend
```{r}
p <- ggplot(yearly, aes(x = year_added, y = n, color = type,
    text = paste0(type, ": ", n))) +
  geom_line(linewidth = 1) + geom_point(size = 2) +
  scale_color_manual(values = c(Movie = "#1565C0", "TV Show" = "#E53935")) +
  theme_minimal() + labs(x = "Year", y = "Titles", color = NULL)
ggplotly(p, tooltip = "text") |> layout(hovermode = "x unified")
```

### Top Countries
```{r}
top10 <- nf |> filter(!is.na(country)) |>
  mutate(primary = str_trim(str_extract(country, "^[^,]+"))) |>
  count(primary, sort = TRUE) |> slice_max(n, n = 10)
p2 <- ggplot(top10, aes(x = fct_reorder(primary, n), y = n,
    text = paste0(primary, ": ", n))) +
  geom_col(fill = "#1565C0", alpha = 0.7) + coord_flip() +
  theme_minimal() + labs(x = NULL, y = "Titles")
ggplotly(p2, tooltip = "text")
```
'
writeLines(quarto_template, "output/netflix_dashboard.qmd")
cat("Quarto dashboard template: output/netflix_dashboard.qmd\n")
cat("Render with: quarto render output/netflix_dashboard.qmd\n\n")

# ══════════════════════════════════════════════════════════
# 4. DEPLOYMENT CHECKLIST
# ══════════════════════════════════════════════════════════
cat("── Deployment Checklist ──\n")
checklist <- tibble(
  item = c("Relative paths only", "Pin dependencies", "Include data files",
    "Test locally", "Expose server (Dash)", "Error handling",
    "No credentials in code", "Performance: pre-aggregate"),
  r_command = c('read_csv("data.csv")', 'renv::snapshot()', 'Copy to app dir',
    'shiny::runApp()', 'N/A', 'tryCatch({...})',
    'Sys.getenv("KEY")', 'Pre-compute summaries'),
  python_command = c('pd.read_csv("data.csv")', 'pip freeze > requirements.txt',
    'Bundle in repo', 'python app.py', 'server = app.server',
    'try/except', 'os.environ["KEY"]', 'Cache with @cache'))
print(checklist, n = 8)

# ══════════════════════════════════════════════════════════
# 5. SHARING METHOD COMPARISON
# ══════════════════════════════════════════════════════════
cat("\n── Sharing Method Decision Table ──\n")
sharing <- tibble(
  method = c("Standalone HTML", "shinyapps.io", "Render.com",
    "Quarto Dashboard", "GitHub Pages", "Docker + Cloud"),
  server_needed = c("No", "Yes (hosted)", "Yes (hosted)",
    "No", "No", "Yes (self-managed)"),
  interactivity = c("plotly only", "Full (reactive)", "Full (callbacks)",
    "plotly + OJS", "Static or plotly", "Full"),
  best_for = c("One chart by email", "R Shiny apps", "Python Dash apps",
    "Report dashboards", "Static sites", "Enterprise"))
print(sharing, n = 6)

cat("\n── All W08-M09 R outputs saved ──\n")
