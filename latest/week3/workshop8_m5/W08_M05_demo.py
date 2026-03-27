"""
W08-M05: Dash Fundamentals — PRIMARY Python Script — UNYT
Contains two complete Dash apps: Netflix Explorer + e-Car Explorer.
Run each separately: python app_netflix.py / python app_ecar.py
"""
import os; os.makedirs("output", exist_ok=True)

# ══════════════════════════════════════════════════════════
# APP 1: NETFLIX DASH EXPLORER (complete, runnable)
# ══════════════════════════════════════════════════════════
netflix_app_code = '''
from dash import Dash, html, dcc, Input, Output, dash_table
import pandas as pd, plotly.express as px

# ── Data ─────────────────────────────────────────────────
nf = pd.read_csv("netflix.csv")
nf["date_added"] = pd.to_datetime(nf["date_added"].str.strip(), errors="coerce")
nf["year_added"] = nf["date_added"].dt.year
nf["primary_country"] = nf["country"].str.split(",").str[0].str.strip()

app = Dash(__name__)

# ── Layout ───────────────────────────────────────────────
app.layout = html.Div([
    html.H1("Netflix Content Explorer", style={"textAlign": "center"}),
    html.Hr(),

    html.Div([
        # SIDEBAR: inputs
        html.Div([
            html.H4("Filters"),

            html.Label("Content Type:"),
            dcc.Dropdown(id="type-dd",
                options=[{"label": t, "value": t}
                         for t in ["All", "Movie", "TV Show"]],
                value="All", clearable=False),

            html.Br(),
            html.Label("Year Range:"),
            dcc.RangeSlider(id="year-slider",
                min=2015, max=2021, step=1,
                value=[2015, 2021],
                marks={y: str(y) for y in range(2015, 2022)}),

            html.Br(),
            html.Label("Country:"),
            dcc.Dropdown(id="country-dd",
                options=[{"label": "All", "value": "All"}] +
                    [{"label": c, "value": c}
                     for c in sorted(nf["primary_country"].dropna().unique())],
                value="All", clearable=False),

            html.Br(),
            html.P(id="summary-text", style={"fontWeight": "bold"}),
            html.Button("Reset Filters", id="reset-btn", n_clicks=0,
                style={"marginTop": "10px"}),

        ], style={"width": "22%", "display": "inline-block",
                  "verticalAlign": "top", "padding": "20px"}),

        # MAIN PANEL: outputs
        html.Div([
            dcc.Tabs([
                dcc.Tab(label="Trend", children=[
                    dcc.Graph(id="trend-chart")]),
                dcc.Tab(label="Top Countries", children=[
                    dcc.Graph(id="country-chart")]),
                dcc.Tab(label="Data Table", children=[
                    dash_table.DataTable(id="data-table",
                        columns=[{"name": c, "id": c} for c in
                            ["title", "type", "year_added", "rating",
                             "duration", "primary_country"]],
                        page_size=15, sort_action="native",
                        filter_action="native",
                        style_table={"overflowX": "auto"})]),
            ])
        ], style={"width": "75%", "display": "inline-block"}),
    ]),
])

# ── Callbacks ────────────────────────────────────────────
@app.callback(
    Output("trend-chart", "figure"),
    Output("country-chart", "figure"),
    Output("data-table", "data"),
    Output("summary-text", "children"),
    Input("type-dd", "value"),
    Input("year-slider", "value"),
    Input("country-dd", "value"))
def update_all(content_type, year_range, country):
    df = nf.dropna(subset=["year_added"]).query(
        f"{year_range[0]} <= year_added <= {year_range[1]}")
    if content_type != "All":
        df = df.query(f"type == \\'{content_type}\\'")
    if country != "All":
        df = df.query(f"primary_country == \\'{country}\\'")

    # Trend chart
    yearly = df.groupby(["year_added", "type"]).size().reset_index(name="n")
    fig_trend = px.line(yearly, x="year_added", y="n", color="type",
        color_discrete_map={"Movie": "#1565C0", "TV Show": "#E53935"},
        markers=True, title="Yearly Additions by Type")
    fig_trend.update_layout(template="plotly_white", hovermode="x unified")

    # Country chart
    top10 = df.dropna(subset=["primary_country"]) \\
        ["primary_country"].value_counts().head(10)
    fig_country = px.bar(x=top10.values, y=top10.index,
        orientation="h", title="Top 10 Countries",
        labels={"x": "Titles", "y": "Country"})
    fig_country.update_layout(template="plotly_white", yaxis={"autorange": "reversed"})

    # Table data
    table_data = df[["title","type","year_added","rating",
        "duration","primary_country"]].head(500).to_dict("records")

    summary = f"Showing {len(df):,} titles ({year_range[0]}–{year_range[1]})"
    return fig_trend, fig_country, table_data, summary

# Reset button
@app.callback(
    Output("type-dd", "value"),
    Output("year-slider", "value"),
    Output("country-dd", "value"),
    Input("reset-btn", "n_clicks"),
    prevent_initial_call=True)
def reset_filters(n_clicks):
    return "All", [2015, 2021], "All"

if __name__ == "__main__":
    app.run(debug=True, port=8050)
'''

with open("output/app_netflix.py", "w") as f:
    f.write(netflix_app_code)
print("App 1 saved: output/app_netflix.py")

# ══════════════════════════════════════════════════════════
# APP 2: e-Car DASH EXPLORER (complete, runnable)
# ══════════════════════════════════════════════════════════
ecar_app_code = '''
from dash import Dash, html, dcc, Input, Output, State
import pandas as pd, plotly.express as px

ec = pd.read_csv("ecar.csv")
ec.columns = [c.strip().replace("  ", " ") for c in ec.columns]
ec["Year"] = pd.to_datetime(ec["Approve Date"], format="%m/%d/%Y", errors="coerce").dt.year
ec["Spread"] = ec["Rate"] - ec["Cost of Funds"]
ec = ec.query("2002 <= Year <= 2012")

app = Dash(__name__)

app.layout = html.Div([
    html.H1("e-Car Loan Explorer"),
    html.Div([
        # Sidebar
        html.Div([
            html.Label("Credit Tiers:"),
            dcc.Checklist(id="tier-check",
                options=[{"label": f"Tier {t}", "value": t}
                         for t in sorted(ec.Tier.unique())],
                value=sorted(ec.Tier.unique()),
                inline=True),
            html.Br(),
            html.Label("Metric:"),
            dcc.RadioItems(id="metric-radio",
                options=[{"label": m, "value": m}
                         for m in ["Rate", "Spread", "Cost of Funds"]],
                value="Rate"),
            html.Br(),
            html.Label("Year Range:"),
            dcc.RangeSlider(id="year-slider",
                min=2002, max=2012, step=1,
                value=[2002, 2012],
                marks={y: str(y) for y in range(2002, 2013)}),
            html.Br(),
            html.P(id="loan-count", style={"fontWeight": "bold"}),
        ], style={"width": "25%", "display": "inline-block",
                  "verticalAlign": "top", "padding": "20px"}),

        # Main
        html.Div([
            dcc.Tabs([
                dcc.Tab(label="Trend", children=[dcc.Graph(id="trend")]),
                dcc.Tab(label="Distribution", children=[dcc.Graph(id="dist")]),
            ])
        ], style={"width": "70%", "display": "inline-block"}),
    ]),
])

@app.callback(
    Output("trend", "figure"),
    Output("dist", "figure"),
    Output("loan-count", "children"),
    Input("tier-check", "value"),
    Input("metric-radio", "value"),
    Input("year-slider", "value"))
def update(tiers, metric, years):
    df = ec.query(f"Tier in @tiers and {years[0]} <= Year <= {years[1]}")

    # Trend by tier
    agg = df.groupby(["Year", "Tier"])[metric].mean().reset_index()
    fig_trend = px.line(agg, x="Year", y=metric, color="Tier",
        markers=True, title=f"{metric} by Credit Tier")
    fig_trend.update_layout(template="plotly_white", hovermode="x unified")

    # Distribution
    fig_dist = px.histogram(df, x=metric, color="Tier",
        nbins=40, opacity=0.6, barmode="overlay",
        title=f"{metric} Distribution by Tier")
    fig_dist.update_layout(template="plotly_white")

    count = f"Showing {len(df):,} loans"
    return fig_trend, fig_dist, count

if __name__ == "__main__":
    app.run(debug=True, port=8051)
'''

with open("output/app_ecar.py", "w") as f:
    f.write(ecar_app_code)
print("App 2 saved: output/app_ecar.py")

# ══════════════════════════════════════════════════════════
# CALLBACK PATTERN CHEATSHEET
# ══════════════════════════════════════════════════════════
print("\n=== Dash Callback Patterns ===\n")
patterns = [
    ("Basic", "@callback(Output('chart','figure'), Input('dd','value'))",
     "Single input → single output"),
    ("Multi-output", "@callback([Output('a','fig'), Output('b','children')], Input(...))",
     "One trigger, multiple updates"),
    ("Multi-input", "@callback(Output(...), Input('dd','value'), Input('slider','value'))",
     "Multiple triggers, fires on ANY change"),
    ("State", "@callback(Output(...), Input('btn','n_clicks'), State('text','value'))",
     "Button triggers; text read but doesn't trigger"),
    ("Prevent init", "@callback(..., prevent_initial_call=True)",
     "Don't fire on page load"),
    ("Chained", "Output of callback A = Input of callback B",
     "Sequential processing pipeline"),
]
for name, code, desc in patterns:
    print(f"  {name}:")
    print(f"    {code}")
    print(f"    → {desc}\n")

# ══════════════════════════════════════════════════════════
# SHINY ↔ DASH FINAL COMPARISON
# ══════════════════════════════════════════════════════════
print("=== Shiny ↔ Dash: When to Use Each ===")
print("  Shiny: team primarily uses R, existing ggplot2 code, shinyapps.io deployment")
print("  Dash:  team uses Python, existing pandas/plotly code, cloud deployment (Render/Heroku)")
print("  Both:  reactive web dashboards, server-side filtering, production-quality")
print("  Neither: if you just need an interactive chart → use plotly alone (M02-M03)")

print("\nAll W08-M05 Python outputs saved")
