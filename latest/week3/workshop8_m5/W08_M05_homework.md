# Workshop 8 · Module 5 — Homework
## Dash Fundamentals

**Due**: Before Workshop 8, Module 7
**Format**: Python scripts (Dash apps) + R script (Shiny equivalent) + PDF report (max 6 pages)
**Weight**: Part of Workshop 8 homework (5% of total grade)

### Part A — Netflix Dash App (35 points)
Build a complete Dash app for the Netflix dataset with: (a) `dcc.Dropdown` for content type, (b) `dcc.RangeSlider` for year range, (c) `dcc.Dropdown` for country, (d) a `@callback` that filters data and returns a plotly trend chart + summary text, (e) `dcc.Tabs` with at least two tabs (Trend + Data Table), (f) a Reset button using `prevent_initial_call=True`. The app must run locally without errors.

### Part B — e-Car Dash App (30 points)
Build a Dash app for the e-Car dataset with: (a) `dcc.Checklist` for credit tiers, (b) `dcc.RadioItems` for metric selection (Rate/Spread/CoF), (c) `dcc.RangeSlider` for year range, (d) two tabs: tier-stratified trend + distribution histogram. Use `State` for at least one component (e.g., a "Run Analysis" button that triggers expensive computation).

### Part C — Shiny ↔ Dash Translation (20 points)
Take your Part A Dash app and write the Shiny (R) equivalent. Present a 5-row table comparing: (a) layout syntax, (b) input widget syntax, (c) callback vs reactive, (d) output rendering, (e) reset button handling. In 150 words, evaluate: which framework feels more natural for this task?

### Part D — Deployment (15 points)
Deploy your Netflix Dash app to ONE of: (a) Render.com (free tier), (b) local screenshot + `requirements.txt` + `Procfile` ready for deployment. In 100 words, describe the deployment process and any challenges.

### Submission Checklist
- [ ] `app_netflix.py` (runs locally with `python app_netflix.py`)
- [ ] `app_ecar.py` (runs locally)
- [ ] `app_shiny_equivalent.R` (runs with `shiny::runApp()`)
- [ ] `requirements.txt` + `Procfile` (deployment-ready)
- [ ] PDF report (max 6 pages) with Shiny↔Dash table and deployment notes
