# Workshop 8 · Module 9 — Course Notes
## Deployment & Sharing

### 1. The Deployment Problem
Building a dashboard (M04–M08) is only half the challenge. The other half is getting it into the hands of the people who need it. This module covers the complete deployment spectrum: from the simplest method (emailing an HTML file) to production cloud deployment (Docker + AWS).

### 2. Deployment Options

**Local development** (free, private): run `shiny::runApp()` or `python app.py` on your machine. The dashboard is accessible only to you via `http://localhost`. Use for development and testing.

**shinyapps.io** (R, free tier available): Posit's hosted platform for Shiny apps. Free tier: 25 active hours/month, 5 applications. Deploy with `rsconnect::deployApp()`. The platform handles R package installation, server management, and SSL. Requirements: relative file paths, data bundled in the app directory, app.R or ui.R+server.R structure.

**Render.com** (Python, free tier available): connects to a GitHub repository and auto-deploys on push. Requires `requirements.txt` (dependencies), `Procfile` (`web: gunicorn app:server`), and `server = app.server` in the Dash app. Free tier provides 750 hours/month of runtime.

**Quarto Dashboards** (no server, free): Quarto's `format: dashboard` produces a standalone HTML file with plotly interactivity (hover, zoom) but no server-side reactivity. Use for report-style dashboards that are emailed, hosted on GitHub Pages, or embedded in wikis. Client-side filtering is possible via OJS (Observable JavaScript) cells. This is the best option when you need interactive charts but not Shiny/Dash-level reactivity.

**Standalone HTML** (simplest, free): `fig.write_html("chart.html")` (Python) or `htmlwidgets::saveWidget(p, "chart.html", selfcontained=TRUE)` (R). One HTML file containing a single plotly chart with all interactivity. Email as attachment; opens in any browser. Use when you need to share one chart, not a full dashboard.

**Docker + Cloud** ($20+/month): containerise the app with Docker, deploy to AWS (ECS/Fargate), GCP (Cloud Run), or Azure (Container Apps). Provides scalability, authentication, and enterprise security. Use for production dashboards serving many concurrent users.

### 3. shinyapps.io Workflow
1. Install `rsconnect`: `install.packages("rsconnect")`
2. Configure account: `rsconnect::setAccountInfo(name, token, secret)` (one-time, from shinyapps.io account settings)
3. Prepare app directory: `app.R` + data files, all with relative paths
4. Deploy: `rsconnect::deployApp(appDir = "path/to/app/")``
5. App is live at `https://username.shinyapps.io/app-name/`

Common pitfalls: absolute file paths (fails on server), missing packages (use `renv` to capture dependencies), large data files (use `readr::read_csv()` which is faster than base R), and forgetting to include the data file in the app directory.

### 4. Render.com Workflow
1. Create `requirements.txt`: list all pip packages with versions
2. Create `Procfile`: `web: gunicorn app:server`
3. In `app.py`: add `server = app.server` (gunicorn needs this)
4. Push to GitHub
5. On Render.com: "New Web Service" → connect repo → deploy
6. App is live at `https://app-name.onrender.com`

Auto-deploy: every `git push` triggers a new deployment automatically.

### 5. Quarto Dashboards
Quarto (the successor to R Markdown) supports a `dashboard` format that produces interactive HTML without any server:

```yaml
---
title: "My Dashboard"
format: dashboard
---
```

The dashboard uses a row/column grid layout defined by `## Row` and `### Column` headers. Code chunks (R or Python) produce plotly figures that render inline with full hover/zoom interactivity. Value boxes provide KPI-style displays. The output is a single HTML file — no server, no deployment complexity.

Limitation: no server-side reactivity. You cannot filter data based on user input the way Shiny/Dash can. However, Quarto supports OJS (Observable JavaScript) cells that provide client-side filtering — sufficient for many report-style dashboards.

### 6. Standalone HTML: The Simplest Sharing Method
When you don't need a full dashboard — just one interactive chart shared with a colleague — the simplest approach is:

R: `htmlwidgets::saveWidget(p, "chart.html", selfcontained = TRUE)` (~3 MB, works offline)
Python: `fig.write_html("chart.html", include_plotlyjs=True)` (~3 MB, works offline)

For smaller files: `selfcontained = FALSE` (R) or `include_plotlyjs="cdn"` (Python) produces a ~50 KB file that loads plotly.js from CDN (requires internet).

### 7. Deployment Checklist
Every deployment should verify: (1) Relative paths only — no `/home/user/...`. (2) Dependencies pinned — `requirements.txt` or `renv.lock`. (3) Data bundled — CSV files included or database URL configured. (4) Tested locally — `shiny::runApp()` or `python app.py` works. (5) Server exposed — Dash needs `server = app.server`. (6) No credentials in code — use environment variables. (7) Error handling — wrap data loading in try/catch. (8) Performance — pre-aggregate for large datasets.

### 8. Security
Free-tier deployments (shinyapps.io free, Render free) are **public** — anyone with the URL can access the dashboard. Do not deploy confidential or sensitive data on free tiers. For authenticated access: Posit Connect (R), Dash Enterprise (Python), or custom authentication middleware.

### References
- shinyapps.io: https://docs.posit.co/shinyapps.io/
- Render: https://render.com/docs/deploy-a-dash-app
- Quarto Dashboards: https://quarto.org/docs/dashboards/
- GitHub Pages: https://pages.github.com/
