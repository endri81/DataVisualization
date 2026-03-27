"""W08-M09: Deployment & Sharing — Python — UNYT"""
import os; os.makedirs("output", exist_ok=True)

# ══════════════════════════════════════════════════════════
# 1. STANDALONE HTML: simplest sharing
# ══════════════════════════════════════════════════════════
try:
    import plotly.express as px, pandas as pd
    nf = pd.read_csv("netflix.csv")
    nf["date_added"] = pd.to_datetime(nf["date_added"].str.strip(), errors="coerce")
    nf["year_added"] = nf["date_added"].dt.year
    yearly = nf.query("2015<=year_added<=2021").groupby(["year_added","type"]).size().reset_index(name="n")

    fig = px.line(yearly, x="year_added", y="n", color="type",
        color_discrete_map={"Movie": "#1565C0", "TV Show": "#E53935"},
        markers=True, title="Netflix Additions by Type")
    fig.update_layout(hovermode="x unified", template="plotly_white")

    # Self-contained (~3 MB, works offline)
    fig.write_html("output/chart_selfcontained.html", include_plotlyjs=True)
    # CDN version (~50 KB, needs internet)
    fig.write_html("output/chart_cdn.html", include_plotlyjs="cdn")
    print("Standalone HTML files saved")
except ImportError:
    print("plotly not available")

# ══════════════════════════════════════════════════════════
# 2. RENDER.COM DEPLOYMENT FILES
# ══════════════════════════════════════════════════════════
deploy_dir = "output/dash_deploy/"
os.makedirs(deploy_dir, exist_ok=True)

# requirements.txt
with open(f"{deploy_dir}requirements.txt", "w") as f:
    f.write("dash==2.14.0\ndash-bootstrap-components==1.5.0\n"
        "pandas==2.1.0\nplotly==5.18.0\ngunicorn==21.2.0\n")

# Procfile
with open(f"{deploy_dir}Procfile", "w") as f:
    f.write("web: gunicorn app:server\n")

# Minimal deployable app
app_code = '''from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd, plotly.express as px

nf = pd.read_csv("netflix.csv")  # RELATIVE path
nf["date_added"] = pd.to_datetime(nf["date_added"].str.strip(), errors="coerce")
nf["year_added"] = nf["date_added"].dt.year

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server  # REQUIRED for gunicorn

app.layout = dbc.Container([
    html.H3("Netflix Dashboard"),
    dbc.Row([
        dbc.Col(dcc.Dropdown(id="type-dd",
            options=[{"label":t,"value":t} for t in ["All","Movie","TV Show"]],
            value="All", clearable=False), width=3),
        dbc.Col(dcc.RangeSlider(id="year-sl", min=2015, max=2021, step=1,
            value=[2015,2021],
            marks={y:str(y) for y in range(2015,2022)}), width=6),
    ], className="mb-3"),
    dcc.Graph(id="chart"),
    html.P(id="count"),
], fluid=True)

@app.callback(Output("chart","figure"), Output("count","children"),
    Input("type-dd","value"), Input("year-sl","value"))
def update(content_type, years):
    df = nf.dropna(subset=["year_added"]).query(f"{years[0]}<=year_added<={years[1]}")
    if content_type != "All":
        df = df.query(f"type==\\'{content_type}\\'")
    yr = df.groupby(["year_added","type"]).size().reset_index(name="n")
    fig = px.line(yr, x="year_added", y="n", color="type",
        color_discrete_map={"Movie":"#1565C0","TV Show":"#E53935"},
        markers=True, title="Netflix Additions by Type")
    fig.update_layout(template="plotly_white", hovermode="x unified")
    return fig, f"Showing {len(df):,} titles"

if __name__=="__main__": app.run(debug=True)
'''
with open(f"{deploy_dir}app.py", "w") as f:
    f.write(app_code)

print(f"\nDash deployment directory: {deploy_dir}")
print(f"  app.py + requirements.txt + Procfile")
print(f"  Add netflix.csv, then push to GitHub → connect Render.com")

# ══════════════════════════════════════════════════════════
# 3. QUARTO DASHBOARD TEMPLATE (Python version)
# ══════════════════════════════════════════════════════════
quarto_py = '''---
title: "Netflix Content Dashboard"
format:
  dashboard:
    orientation: rows
    theme: flatly
---

```{python}
#| label: setup
#| include: false
import pandas as pd, plotly.express as px
nf = pd.read_csv("netflix.csv")
nf["date_added"] = pd.to_datetime(nf["date_added"].str.strip(), errors="coerce")
nf["year_added"] = nf["date_added"].dt.year
```

## Row {height=30%}

### Total Titles {.valuebox}
`{python} f"{len(nf):,}"`

### Movies {.valuebox}
`{python} f"{(nf.type=='Movie').sum():,}"`

### TV Shows {.valuebox}
`{python} f"{(nf.type=='TV Show').sum():,}"`

## Row {height=70%}

### Yearly Trend
```{python}
yearly = nf.query("2015<=year_added<=2021").groupby(["year_added","type"]).size().reset_index(name="n")
fig = px.line(yearly, x="year_added", y="n", color="type",
    color_discrete_map={"Movie":"#1565C0","TV Show":"#E53935"},
    markers=True)
fig.update_layout(template="plotly_white", hovermode="x unified")
fig.show()
```

### Top Countries
```{python}
nf["primary_country"] = nf["country"].str.split(",").str[0].str.strip()
top10 = nf.dropna(subset=["primary_country"])["primary_country"].value_counts().head(10)
fig2 = px.bar(x=top10.values, y=top10.index, orientation="h",
    labels={"x":"Titles","y":""})
fig2.update_traces(marker_color="#1565C0", marker_opacity=0.7)
fig2.update_layout(template="plotly_white", yaxis={"autorange":"reversed"})
fig2.show()
```
'''
with open("output/netflix_dashboard_py.qmd", "w") as f:
    f.write(quarto_py)
print("\nQuarto dashboard (Python): output/netflix_dashboard_py.qmd")
print("Render: quarto render output/netflix_dashboard_py.qmd")

# ══════════════════════════════════════════════════════════
# 4. CHECKLISTS
# ══════════════════════════════════════════════════════════
print("\n=== Deployment Checklist ===")
items = [
    ("Relative paths", 'pd.read_csv("data.csv") — never absolute'),
    ("Pin dependencies", "pip freeze > requirements.txt"),
    ("Include data", "Bundle CSV in repo or use DB URL"),
    ("Test locally", "python app.py → http://localhost:8050"),
    ("Expose server", "server = app.server  # required for gunicorn"),
    ("Procfile", 'web: gunicorn app:server'),
    ("No credentials", 'os.environ["DB_URL"] — never hardcode'),
    ("Performance", "Pre-aggregate, cache expensive ops"),
]
for item, detail in items:
    print(f"  ☐ {item}: {detail}")

print("\n=== Sharing Method Decision ===")
methods = [
    ("One chart by email", "→ fig.write_html('chart.html')"),
    ("Shiny app (R)", "→ shinyapps.io (free 25h/mo)"),
    ("Dash app (Python)", "→ Render.com (free tier)"),
    ("Report dashboard", "→ Quarto Dashboard (.qmd → .html)"),
    ("Static site", "→ GitHub Pages (free)"),
    ("Enterprise", "→ Docker + AWS/GCP ($20+/mo)"),
]
for scenario, solution in methods:
    print(f"  {scenario:<25} {solution}")

print("\nAll W08-M09 Python outputs saved")
