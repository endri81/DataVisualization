# ============================================================
# Workshop 8 — Module 8: e-Car Interactive Dashboard
# Complete Shiny App — UNYT Tirana
# ============================================================
library(tidyverse); library(shiny); library(plotly); library(DT)

ec <- read_csv("ecar.csv") |>
  mutate(ApproveDate = mdy(`Approve Date`),
    Year = year(ApproveDate), Quarter = quarter(ApproveDate),
    Spread = Rate - `Cost of Funds`,
    Approved = Outcome == 1) |>
  filter(Year >= 2002, Year <= 2012)

TIER_PALETTE <- c("1"="#BBDEFB","2"="#64B5F6","3"="#1E88E5","4"="#1565C0","5"="#0D47A1")

# ══════════════════════════════════════════════════════════
# UI
# ══════════════════════════════════════════════════════════
ui <- fluidPage(
  tags$head(tags$style(HTML("
    .kpi-card{text-align:center;padding:8px;border:1px solid #eee;border-radius:8px;background:white;}
    .kpi-value{font-size:26px;font-weight:bold;}
    .kpi-label{font-size:10px;color:#888;}
  "))),
  titlePanel(div(style="color:#1565C0;font-weight:bold;","e-Car Loan Analytics Dashboard")),

  # Filter bar
  fluidRow(style="background:#f9f9f9;padding:10px;margin-bottom:10px;",
    column(4, checkboxGroupInput("tiers","Credit Tiers:",
      choices=sort(unique(ec$Tier)), selected=sort(unique(ec$Tier)), inline=TRUE)),
    column(3, sliderInput("years","Year Range:",min=2002,max=2012,
      value=c(2002,2012),step=1,sep="")),
    column(3, radioButtons("metric","Metric:",
      choices=c("Rate","Spread","Cost of Funds"),selected="Rate",inline=TRUE)),
    column(2, br(), actionButton("reset","Reset",icon=icon("refresh"),
      class="btn-outline-secondary btn-sm"))
  ),

  # KPI row
  fluidRow(column(3,uiOutput("kpi1")),column(3,uiOutput("kpi2")),
    column(3,uiOutput("kpi3")),column(3,uiOutput("kpi4"))),

  # Primary + Secondary
  fluidRow(
    column(6, plotlyOutput("trend",height="300px")),
    column(6, plotlyOutput("distribution",height="300px"))),

  # Detail row
  fluidRow(
    column(4, plotlyOutput("ci_ribbon",height="260px")),
    column(4, plotlyOutput("approval",height="260px")),
    column(4, DTOutput("loan_table")))
)

# ══════════════════════════════════════════════════════════
# SERVER
# ══════════════════════════════════════════════════════════
server <- function(input, output, session) {

  filtered <- reactive({
    ec |> filter(Tier %in% input$tiers,
      Year >= input$years[1], Year <= input$years[2])
  })

  make_kpi <- function(value, label, color) {
    div(class="kpi-card",
      div(class="kpi-value",style=paste0("color:",color),
        if(is.numeric(value) && value > 100) format(round(value), big.mark=",")
        else if(is.numeric(value)) paste0(round(value, 1), "%") else value),
      div(class="kpi-label", label))
  }

  output$kpi1 <- renderUI(make_kpi(nrow(filtered()), "Filtered Loans", "#333"))
  output$kpi2 <- renderUI(make_kpi(mean(filtered()$Rate), "Avg Rate", "#1565C0"))
  output$kpi3 <- renderUI(make_kpi(mean(filtered()$Spread), "Avg Spread (pp)", "#E53935"))
  output$kpi4 <- renderUI(make_kpi(mean(filtered()$Approved)*100, "Approval %", "#2E7D32"))

  # ── RATE TREND BY TIER ─────────────────────────────────
  output$trend <- renderPlotly({
    metric <- input$metric
    yearly_tier <- filtered() |>
      group_by(Year, Tier) |>
      summarise(value = mean(.data[[metric]], na.rm=TRUE), .groups="drop")
    p <- ggplot(yearly_tier, aes(x=Year, y=value, color=factor(Tier),
        text=paste0("Tier ",Tier,"\nYear: ",Year,"\n",metric,": ",round(value,2)))) +
      geom_line(linewidth=1) + geom_point(size=2) +
      scale_color_manual(values=TIER_PALETTE) +
      geom_vline(xintercept=2008, linetype="dashed", color="#E53935", linewidth=0.4) +
      theme_minimal(base_size=9) +
      theme(panel.grid.minor=element_blank(), legend.position="bottom") +
      labs(title=paste(metric,"Trend by Tier"), y=metric, color="Tier", x=NULL)
    ggplotly(p, tooltip="text") |>
      layout(hovermode="x unified",
        shapes=list(list(type="rect",x0=2007.5,x1=2009.5,y0=0,y1=1,
          yref="paper",fillcolor="#E53935",opacity=0.04,line=list(width=0))))
  })

  # ── SPREAD DISTRIBUTION ────────────────────────────────
  output$distribution <- renderPlotly({
    metric <- input$metric
    p <- ggplot(filtered(), aes(x=.data[[metric]], fill=factor(Tier))) +
      geom_histogram(bins=40, alpha=0.5, position="identity") +
      scale_fill_manual(values=TIER_PALETTE) +
      theme_minimal(base_size=9) +
      labs(title=paste(metric,"Distribution by Tier"), x=metric, fill="Tier")
    ggplotly(p) |> layout(barmode="overlay")
  })

  # ── QUARTERLY CI RIBBON ────────────────────────────────
  output$ci_ribbon <- renderPlotly({
    quarterly <- filtered() |>
      group_by(Year, Quarter) |>
      summarise(mean_rate=mean(Rate), se=sd(Rate)/sqrt(n()),
        n=n(), .groups="drop") |>
      mutate(date=as.Date(paste0(Year,"-",Quarter*3-2,"-01")),
        lower=mean_rate-1.96*se, upper=mean_rate+1.96*se)
    plot_ly(quarterly, x=~date) |>
      add_ribbons(ymin=~lower, ymax=~upper,
        fillcolor="rgba(21,101,192,0.15)",
        line=list(color="transparent"), name="95% CI", showlegend=TRUE) |>
      add_lines(y=~mean_rate, line=list(color="#1565C0", width=1.5),
        name="Mean Rate") |>
      layout(title=list(text="Quarterly Rate ± 95% CI", font=list(size=12)),
        yaxis=list(title="Rate (%)"),
        shapes=list(list(type="line",x0=as.numeric(as.Date("2008-09-15"))*86400000,
          x1=as.numeric(as.Date("2008-09-15"))*86400000,y0=0,y1=1,yref="paper",
          line=list(color="#E53935",dash="dash",width=1))),
        hovermode="x unified")
  })

  # ── APPROVAL RATE BY TIER ──────────────────────────────
  output$approval <- renderPlotly({
    approval_yr <- filtered() |>
      group_by(Year, Tier) |>
      summarise(approval=mean(Approved)*100, .groups="drop")
    p <- ggplot(approval_yr, aes(x=Year, y=approval, color=factor(Tier),
        text=paste0("Tier ",Tier,": ",round(approval,1),"% (",Year,")"))) +
      geom_line(linewidth=0.8) + geom_point(size=1.5) +
      scale_color_manual(values=TIER_PALETTE) +
      geom_vline(xintercept=2008, linetype="dashed", color="#E53935", linewidth=0.3) +
      theme_minimal(base_size=9) +
      labs(title="Approval Rate by Tier", y="Approval %", color="Tier", x=NULL)
    ggplotly(p, tooltip="text") |> layout(hovermode="x unified")
  })

  # ── LOAN TABLE ─────────────────────────────────────────
  output$loan_table <- renderDT({
    filtered() |>
      select(Year, Tier, Rate, `Cost of Funds`, Spread, Outcome) |>
      head(300) |>
      datatable(options=list(pageLength=8, scrollX=TRUE, dom="ftip"),
        filter="top", rownames=FALSE)
  })

  # Reset
  observeEvent(input$reset, {
    updateCheckboxGroupInput(session,"tiers",selected=sort(unique(ec$Tier)))
    updateSliderInput(session,"years",value=c(2002,2012))
    updateRadioButtons(session,"metric",selected="Rate")
  })
}

# shinyApp(ui, server)
cat("\n── e-Car Dashboard Shiny App Defined ──\n")
cat("Run: shinyApp(ui, server)\n")
cat("Panels: 4 KPIs + trend by tier + distribution + CI ribbon + approval + DT\n")
cat("Filters: tier checkboxes + year slider + metric radio + reset\n")
