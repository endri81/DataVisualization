# ============================================================
# Workshop 8 — Module 4: Shiny Fundamentals
# Integrated R Script — UNYT Tirana
# ============================================================
# This script contains TWO Shiny apps and supporting code.
# Run each app section individually (not the whole script).
library(tidyverse); library(shiny); library(plotly); library(DT)
dir.create("output", showWarnings = FALSE)

# ── DATA LOADING (shared across apps) ────────────────────
nf <- read_csv("netflix.csv") |>
  mutate(date_added = mdy(str_trim(date_added)),
    year_added = year(date_added),
    primary_country = str_trim(str_extract(country, "^[^,]+")),
    duration_num = parse_number(duration))

# ══════════════════════════════════════════════════════════
# APP 1: MINIMAL SHINY — Netflix Explorer
# Demonstrates: selectInput, sliderInput, renderPlot, reactive
# ══════════════════════════════════════════════════════════

app1_ui <- fluidPage(
  titlePanel("Netflix Content Explorer"),
  sidebarLayout(
    sidebarPanel(width = 3,
      # Input 1: Content type dropdown
      selectInput("type", "Content Type:",
        choices = c("All", "Movie", "TV Show"),
        selected = "All"),

      # Input 2: Year range slider
      sliderInput("years", "Year Range:",
        min = 2015, max = 2021,
        value = c(2015, 2021), step = 1, sep = ""),

      # Input 3: Country dropdown
      selectInput("country", "Country:",
        choices = c("All", sort(unique(na.omit(nf$primary_country)))),
        selected = "All"),

      # Summary text
      textOutput("n_titles"),
      hr(),
      # Reset button
      actionButton("reset", "Reset All Filters", icon = icon("refresh"))
    ),
    mainPanel(width = 9,
      # Tab panels for different views
      tabsetPanel(
        tabPanel("Trend", plotOutput("trend_plot", height = "400px")),
        tabPanel("Interactive", plotlyOutput("plotly_chart", height = "400px")),
        tabPanel("Data Table", DTOutput("data_table"))
      )
    )
  )
)

app1_server <- function(input, output, session) {
  # ── REACTIVE: Filtered data ────────────────────────────
  # This recalculates automatically when any input changes
  filtered <- reactive({
    df <- nf |>
      filter(!is.na(year_added),
        year_added >= input$years[1],
        year_added <= input$years[2])

    if (input$type != "All") df <- df |> filter(type == input$type)
    if (input$country != "All") df <- df |> filter(primary_country == input$country)
    df
  })

  # ── OUTPUTS ────────────────────────────────────────────
  # Text: number of titles
  output$n_titles <- renderText({
    paste0("Showing ", format(nrow(filtered()), big.mark = ","), " titles")
  })

  # Static ggplot
  output$trend_plot <- renderPlot({
    filtered() |>
      count(year_added, type) |>
      ggplot(aes(x = year_added, y = n, color = type)) +
      geom_line(linewidth = 1.5) + geom_point(size = 3) +
      scale_color_manual(values = c(Movie = "#1565C0", "TV Show" = "#E53935")) +
      theme_minimal(base_size = 14) +
      theme(panel.grid = element_blank(),
        legend.position = "bottom") +
      labs(title = "Yearly Additions by Type",
           x = "Year", y = "Titles Added", color = NULL)
  })

  # Interactive plotly
  output$plotly_chart <- renderPlotly({
    p <- filtered() |>
      count(year_added, type) |>
      ggplot(aes(x = year_added, y = n, color = type,
        text = paste0("Year: ", year_added, "\nType: ", type, "\nCount: ", n))) +
      geom_line(linewidth = 1) + geom_point(size = 2) +
      scale_color_manual(values = c(Movie = "#1565C0", "TV Show" = "#E53935")) +
      theme_minimal() +
      labs(x = "Year", y = "Titles", color = NULL)
    ggplotly(p, tooltip = "text") |>
      layout(hovermode = "x unified", legend = list(orientation = "h"))
  })

  # Data table
  output$data_table <- renderDT({
    filtered() |>
      select(title, type, year_added, rating, duration, primary_country) |>
      datatable(options = list(pageLength = 15, scrollX = TRUE),
        filter = "top")
  })

  # ── OBSERVE: Reset button ─────────────────────────────
  observeEvent(input$reset, {
    updateSelectInput(session, "type", selected = "All")
    updateSliderInput(session, "years", value = c(2015, 2021))
    updateSelectInput(session, "country", selected = "All")
  })
}

# To run: shinyApp(app1_ui, app1_server)

# ══════════════════════════════════════════════════════════
# APP 2: e-Car LOAN EXPLORER
# Demonstrates: radioButtons, checkboxGroupInput, reactive, plotly
# ══════════════════════════════════════════════════════════

ec <- read_csv("ecar.csv") |>
  mutate(Year = year(mdy(`Approve Date`)),
    Spread = Rate - `Cost of Funds`) |>
  filter(Year >= 2002, Year <= 2012)

app2_ui <- fluidPage(
  titlePanel("e-Car Loan Explorer"),
  sidebarLayout(
    sidebarPanel(width = 3,
      # Credit tier selection
      checkboxGroupInput("tiers", "Credit Tiers:",
        choices = sort(unique(ec$Tier)),
        selected = sort(unique(ec$Tier))),

      # Year range
      sliderInput("ec_years", "Year Range:",
        min = 2002, max = 2012,
        value = c(2002, 2012), step = 1, sep = ""),

      # Metric selection
      radioButtons("metric", "Metric:",
        choices = c("Rate", "Spread", "Cost of Funds"),
        selected = "Rate"),

      textOutput("n_loans"),
      actionButton("ec_reset", "Reset")
    ),
    mainPanel(width = 9,
      tabsetPanel(
        tabPanel("Trend", plotlyOutput("ec_trend", height = "400px")),
        tabPanel("Distribution", plotOutput("ec_dist", height = "400px")),
        tabPanel("Data", DTOutput("ec_table"))
      )
    )
  )
)

app2_server <- function(input, output, session) {
  filtered_ec <- reactive({
    ec |>
      filter(Tier %in% input$tiers,
        Year >= input$ec_years[1],
        Year <= input$ec_years[2])
  })

  output$n_loans <- renderText({
    paste0("Showing ", format(nrow(filtered_ec()), big.mark = ","), " loans")
  })

  output$ec_trend <- renderPlotly({
    metric_col <- switch(input$metric,
      "Rate" = "Rate", "Spread" = "Spread", "Cost of Funds" = "Cost of Funds")
    yearly_ec <- filtered_ec() |>
      group_by(Year, Tier) |>
      summarise(value = mean(.data[[metric_col]], na.rm = TRUE), .groups = "drop")

    p <- ggplot(yearly_ec, aes(x = Year, y = value, color = factor(Tier),
        text = paste0("Tier ", Tier, "\nYear: ", Year,
          "\n", input$metric, ": ", round(value, 2)))) +
      geom_line(linewidth = 1) + geom_point(size = 2) +
      theme_minimal() +
      labs(y = input$metric, color = "Tier")
    ggplotly(p, tooltip = "text") |> layout(hovermode = "x unified")
  })

  output$ec_dist <- renderPlot({
    metric_col <- switch(input$metric,
      "Rate" = "Rate", "Spread" = "Spread", "Cost of Funds" = "Cost of Funds")
    ggplot(filtered_ec(), aes(x = .data[[metric_col]], fill = factor(Tier))) +
      geom_histogram(bins = 40, alpha = 0.6, position = "identity") +
      theme_minimal(base_size = 14) +
      labs(title = paste(input$metric, "Distribution by Tier"),
           x = input$metric, fill = "Tier")
  })

  output$ec_table <- renderDT({
    filtered_ec() |>
      select(Year, Tier, Rate, `Cost of Funds`, Spread, Outcome) |>
      datatable(options = list(pageLength = 20, scrollX = TRUE))
  })

  observeEvent(input$ec_reset, {
    updateCheckboxGroupInput(session, "tiers", selected = sort(unique(ec$Tier)))
    updateSliderInput(session, "ec_years", value = c(2002, 2012))
    updateRadioButtons(session, "metric", selected = "Rate")
  })
}

# To run: shinyApp(app2_ui, app2_server)

# ══════════════════════════════════════════════════════════
# INPUT WIDGET CHEATSHEET (printed)
# ══════════════════════════════════════════════════════════
cat("\n── Shiny Input Widget Cheatsheet ──\n")
widgets <- tibble(
  widget = c("selectInput", "sliderInput", "checkboxGroupInput",
    "radioButtons", "textInput", "actionButton",
    "dateRangeInput", "numericInput", "fileInput"),
  purpose = c("Single dropdown", "Numeric range", "Multiple checkboxes",
    "Single radio", "Free text", "Trigger event",
    "Date range", "Single number", "File upload"),
  shneiderman = c("Filter", "Filter", "Filter",
    "Reconfigure", "Filter", "History (reset)",
    "Filter", "Filter", "Extract (reverse)"))
print(widgets, n = 9)

cat("\n── Shiny Output/Render Pairs ──\n")
renders <- tibble(
  ui_function = c("plotOutput()", "plotlyOutput()", "DTOutput()",
    "textOutput()", "tableOutput()", "downloadButton()"),
  server_function = c("renderPlot()", "renderPlotly()", "renderDT()",
    "renderText()", "renderTable()", "downloadHandler()"),
  content = c("Static ggplot", "Interactive plotly", "Searchable DT table",
    "Text string", "Simple HTML table", "Downloadable file"))
print(renders, n = 6)

cat("\n── All W08-M04 R outputs saved ──\n")
cat("App 1: Netflix Explorer (run with shinyApp(app1_ui, app1_server))\n")
cat("App 2: e-Car Explorer (run with shinyApp(app2_ui, app2_server))\n")
