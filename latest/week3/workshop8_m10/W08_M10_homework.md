# Workshop 8 — Final Homework
## Lab: Build an Interactive Dashboard

**Due**: Before Workshop 9, Module 1
**Format**: Shiny app (R) OR Dash app (Python) + deployed URL/HTML + PDF report (max 8 pages)
**Weight**: 5% of total grade (summative assessment for Workshop 8)

### Dataset Choice
Choose ONE: Netflix, e-Car, Google Play Store, or Real Estate.

### Required Components (100 marks)

**1. Layout — Few's Grid (15 marks)**
Dashboard must follow Few's layout grid: filter bar at top, KPI row below, primary + secondary charts in the middle, detail panels at bottom. All content must fit one screen (no scrolling at 1920×1080). Use `fluidRow/column` (Shiny) or `dbc.Row/Col` (Dash).

**2. KPI Cards (10 marks)**
4 KPI cards showing key metrics with values that auto-update when filters change. Each card: big number + descriptive label. Conditional colour (green/red for positive/negative delta) is worth +2 bonus.

**3. Chart Quality (25 marks)**
Minimum 4 plotly panels using at least 3 different chart types (line, bar, scatter, histogram, pie, etc.). All charts must have: hover tooltips, consistent colour palette (PALETTE defined once, applied everywhere), descriptive titles, and responsive to filter changes.

**4. Filter Inputs (15 marks)**
Minimum 3 filter inputs: dropdown + slider + one other (checkbox, radio, or second dropdown). Plus a Reset button that restores all defaults. ALL panels (KPIs, charts, table) must react to filter changes.

**5. Cross-Filtering (10 marks)**
Clicking on a chart element (e.g., a country bar, a genre slice) must filter other panels. Implement via `event_data()` (Shiny) or `clickData` (Dash).

**6. Deployment (15 marks)**
Deploy to ONE of: (a) shinyapps.io (submit URL), (b) Render.com (submit URL), (c) Quarto HTML (submit .html file). The deployed version must run without errors. If deployment fails, submit the app code + error log + troubleshooting notes for partial credit.

**7. Reflection Essay (10 marks)**
300 words covering: (a) which dataset you chose and why, (b) your wireframe sketch (include photo/scan), (c) Shneiderman 7-step audit table, (d) Few's 6-rule audit, (e) what was the hardest part, (f) what would you improve with more time.

### Bonus (+10 marks)
Implement in BOTH Shiny and Dash (+5). Add a Quarto dashboard version alongside the app (+5).

### Submission Checklist
- [ ] App code: `app.R` (Shiny) OR `app.py` + `requirements.txt` + `Procfile` (Dash)
- [ ] Deployed URL or Quarto HTML file
- [ ] Screenshot of running dashboard
- [ ] PDF report (max 8 pages): wireframe, Shneiderman audit, Few's audit, reflection
