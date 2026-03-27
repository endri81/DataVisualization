# Workshop 8 · Module 8 — Homework
## Case Study: e-Car Interactive Dashboard

**Due**: Before Workshop 8, Module 10 (Lab)
**Format**: R script (Shiny app) + Python script (Dash app) + PDF report (max 6 pages)
**Weight**: Part of Workshop 8 homework (5% of total grade)

### Part A — e-Car Shiny Dashboard (40 points)
Build a Shiny app implementing the module's specification: (a) tier checkboxes + year slider + metric radio + reset, (b) 4 KPI cards (loans, avg rate, avg spread, approval %), (c) rate/spread/CoF trend by tier (plotly line), (d) distribution histogram by tier, (e) quarterly CI ribbon, (f) loan data table with sort/search. All temporal charts must include the 2008 crisis annotation. The app must run without errors.

### Part B — e-Car Dash Dashboard (40 points)
Build the equivalent Dash app with the same specification. Use sequential blue palette for tiers. Include crisis annotation shapes on all temporal panels. CI ribbon must use `go.Scatter(fill="tonexty")`. The app must run locally.

### Part C — Netflix vs e-Car Dashboard Comparison (20 points)
In a 7-row table, compare the two dashboards across: primary dimension, colour palette type, key metric, unique input widget, event annotation, unique panel, and cross-filter design. In 150 words, explain: what is the most important design adaptation when moving from a content domain to a financial domain?

### Submission Checklist
- [ ] `app_ecar_shiny.R` (runs with `shiny::runApp()`)
- [ ] `app_ecar_dash.py` (runs locally)
- [ ] PDF report (max 6 pages) with comparison table
