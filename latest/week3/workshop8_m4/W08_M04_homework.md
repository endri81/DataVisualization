# Workshop 8 · Module 4 — Homework
## Shiny Fundamentals

**Due**: Before Workshop 8, Module 6
**Format**: R script (app.R) + Python Dash script (app.py) + PDF report (max 6 pages)
**Weight**: Part of Workshop 8 homework (5% of total grade)

### Part A — Minimal Netflix Shiny App (35 points)
Build a Shiny app with: (a) `selectInput` for content type (All/Movie/TV Show), (b) `sliderInput` for year range (2015–2021), (c) a `reactive()` expression that filters the data, (d) `renderPlot()` showing a yearly additions line chart, (e) `renderText()` showing the count of filtered titles. Include a `tabsetPanel` with at least two tabs (Trend + Data Table). The app must run without errors.

### Part B — e-Car Shiny App (30 points)
Build a Shiny app for the e-Car dataset with: (a) `checkboxGroupInput` for credit tiers (1–5), (b) `radioButtons` for metric (Rate/Spread/Cost of Funds), (c) `sliderInput` for year range, (d) a `plotlyOutput` showing the tier-stratified trend for the selected metric, (e) an `actionButton("reset")` that restores all defaults via `observeEvent`. The app must run without errors.

### Part C — Reactivity Diagram (15 points)
Draw a reactivity diagram for your Part A app: (a) list all inputs (type, years), (b) list all reactive expressions (filtered data), (c) list all outputs (plot, text, table), (d) draw arrows showing which inputs feed which reactives and which reactives feed which outputs. Include in PDF.

### Part D — Shiny ↔ Dash Comparison (20 points)
For EACH of the following Shiny elements, write the Dash (Python) equivalent and explain in one sentence how the syntax differs: (a) `selectInput()`, (b) `reactive({...})`, (c) `renderPlot()`, (d) `observeEvent(input$reset, {...})`. Present as a 4-row table.

### Submission Checklist
- [ ] `app_netflix.R` (runs with `shiny::runApp()`)
- [ ] `app_ecar.R` (runs with `shiny::runApp()`)
- [ ] `app_dash_preview.py` (from Part D, optional but recommended)
- [ ] PDF report (max 6 pages) with reactivity diagram and Shiny↔Dash table
