# Workshop 8 · Module 9 — Homework
## Deployment & Sharing

**Due**: Before Workshop 8, Module 10 (Lab)
**Format**: Deployment-ready files + PDF report (max 6 pages)
**Weight**: Part of Workshop 8 homework (5% of total grade)

### Part A — Standalone HTML Charts (15 points)
Save THREE interactive plotly charts from your W08 work as standalone HTML files (self-contained). Email them to yourself and verify they open in a browser with full interactivity. In 50 words, note the file sizes and whether they render correctly.

### Part B — Shiny Deployment Package (25 points)
Prepare a deployment-ready Shiny app directory containing: (a) `app.R` with only relative paths, (b) bundled `netflix.csv`, (c) verify it runs with `shiny::runApp()`. If you have a shinyapps.io account, deploy it and provide the URL. If not, provide the directory structure and confirm local testing passes.

### Part C — Dash Deployment Package (25 points)
Prepare a deployment-ready Dash app directory containing: (a) `app.py` with `server = app.server`, (b) `requirements.txt`, (c) `Procfile`, (d) bundled data file. Verify it runs locally with `python app.py`. If you deploy to Render.com, provide the URL.

### Part D — Quarto Dashboard (20 points)
Create a Quarto dashboard (`.qmd` file) with `format: dashboard` that includes: (a) 3 value boxes (KPIs), (b) 2 plotly charts in a row layout. Render it with `quarto render` and submit the HTML output. In 100 words, compare: when would you use Quarto Dashboard vs Shiny/Dash?

### Part E — Deployment Decision Table (15 points)
For each scenario, recommend the best deployment method and justify in one sentence: (a) sharing one chart with your manager by email, (b) course homework submission, (c) a team analytics dashboard for 5 users, (d) a public-facing city data portal, (e) a confidential financial dashboard for the board.

### Submission Checklist
- [ ] 3 standalone HTML files (Part A)
- [ ] Shiny deployment directory: app.R + data (Part B)
- [ ] Dash deployment directory: app.py + requirements.txt + Procfile (Part C)
- [ ] Quarto .qmd + rendered .html (Part D)
- [ ] PDF report (max 6 pages) with deployment table + Quarto comparison
