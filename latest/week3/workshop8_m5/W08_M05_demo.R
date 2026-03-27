# ============================================================
# Workshop 8 — Module 5: Dash Fundamentals (R companion)
# Shows Shiny equivalents for every Dash pattern
# ============================================================
library(tidyverse); library(shiny); library(plotly)
dir.create("output", showWarnings = FALSE)

# ── SHINY ↔ DASH PATTERN-BY-PATTERN COMPARISON ──────────
cat("\n── Shiny ↔ Dash: Pattern Comparison ──\n\n")

cat("1. BASIC CALLBACK\n")
cat("   Dash:  @app.callback(Output('chart','figure'), Input('dd','value'))\n")
cat("          def update(val): return px.line(...)\n")
cat("   Shiny: output$chart <- renderPlotly({ ggplotly(ggplot(filtered())) })\n")
cat("          # reactive graph handles the connection implicitly\n\n")

cat("2. MULTI-OUTPUT\n")
cat("   Dash:  @callback([Output('a','fig'), Output('b','children')], Input(...))\n")
cat("          def update(val): return fig, text\n")
cat("   Shiny: output$a <- renderPlotly({...})\n")
cat("          output$b <- renderText({...})\n")
cat("          # Each output has its own render; both read same reactive()\n\n")

cat("3. STATE (read without triggering)\n")
cat("   Dash:  @callback(Output, Input('btn','n_clicks'), State('text','value'))\n")
cat("   Shiny: eventReactive(input$btn, { input$text })  # only fires on btn\n\n")

cat("4. PREVENT_INITIAL_CALL\n")
cat("   Dash:  @callback(..., prevent_initial_call=True)\n")
cat("   Shiny: eventReactive(input$btn, { ... }, ignoreNULL=TRUE)  # default\n\n")

cat("5. RESET BUTTON\n")
cat("   Dash:  @callback(Output('dd','value'), Input('reset','n_clicks'))\n")
cat("          def reset(n): return 'All'\n")
cat("   Shiny: observeEvent(input$reset, {\n")
cat("            updateSelectInput(session, 'type', selected = 'All')\n")
cat("          })\n\n")

cat("6. DEPLOYMENT\n")
cat("   Dash:  Render.com, Heroku, AWS (Procfile + requirements.txt)\n")
cat("   Shiny: shinyapps.io, Shiny Server, Posit Connect\n\n")

# ── EXAMPLE: Shiny equivalent of Dash Netflix app ───────
# (Same app structure as M04 App 1 — included for reference)
nf <- read_csv("netflix.csv") |>
  mutate(date_added = mdy(str_trim(date_added)),
    year_added = year(date_added),
    primary_country = str_trim(str_extract(country, "^[^,]+")))

app_ui <- fluidPage(
  titlePanel("Netflix Explorer (Shiny — equivalent to Dash app)"),
  sidebarLayout(
    sidebarPanel(width = 3,
      selectInput("type", "Content Type:",
        choices = c("All", "Movie", "TV Show")),
      sliderInput("years", "Year Range:",
        min = 2015, max = 2021, value = c(2015, 2021), sep = ""),
      selectInput("country", "Country:",
        choices = c("All", sort(unique(na.omit(nf$primary_country))))),
      textOutput("summary"),
      actionButton("reset", "Reset Filters")),
    mainPanel(width = 9,
      tabsetPanel(
        tabPanel("Trend", plotlyOutput("trend")),
        tabPanel("Countries", plotlyOutput("countries")),
        tabPanel("Data", DT::DTOutput("table"))))))

app_server <- function(input, output, session) {
  filtered <- reactive({
    df <- nf |> filter(!is.na(year_added),
      year_added >= input$years[1], year_added <= input$years[2])
    if (input$type != "All") df <- df |> filter(type == input$type)
    if (input$country != "All") df <- df |> filter(primary_country == input$country)
    df
  })
  output$summary <- renderText(paste0("Showing ", nrow(filtered()), " titles"))
  output$trend <- renderPlotly({
    yr <- filtered() |> count(year_added, type)
    p <- ggplot(yr, aes(x = year_added, y = n, color = type,
        text = paste0(type, ": ", n))) +
      geom_line(linewidth = 1) + geom_point(size = 2) +
      scale_color_manual(values = c(Movie = "#1565C0", "TV Show" = "#E53935")) +
      theme_minimal()
    ggplotly(p, tooltip = "text") |> layout(hovermode = "x unified")
  })
  output$countries <- renderPlotly({
    top10 <- filtered() |> filter(!is.na(primary_country)) |>
      count(primary_country, sort = TRUE) |> slice_max(n, n = 10) |>
      mutate(primary_country = fct_reorder(primary_country, n))
    p <- ggplot(top10, aes(x = primary_country, y = n,
        text = paste0(primary_country, ": ", n))) +
      geom_col(fill = "#1565C0") + coord_flip() + theme_minimal()
    ggplotly(p, tooltip = "text")
  })
  output$table <- DT::renderDT({
    filtered() |> select(title, type, year_added, rating, duration, primary_country) |>
      DT::datatable(options = list(pageLength = 15))
  })
  observeEvent(input$reset, {
    updateSelectInput(session, "type", selected = "All")
    updateSliderInput(session, "years", value = c(2015, 2021))
    updateSelectInput(session, "country", selected = "All")
  })
}
# To run: shinyApp(app_ui, app_server)

cat("── Shiny equivalent app defined (run with shinyApp(app_ui, app_server)) ──\n")
cat("── All W08-M05 R companion outputs saved ──\n")
