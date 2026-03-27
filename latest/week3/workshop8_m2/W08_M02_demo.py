"""W08-M02: plotly in R — Python companion showing equivalent patterns"""
import numpy as np, pandas as pd, os
os.makedirs("output", exist_ok=True)

# This module focuses on R plotly. The Python companion shows
# the EQUIVALENT plotly.py patterns for each R technique,
# enabling students to translate between the two.

try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

nf = pd.read_csv("netflix.csv")
nf["date_added"] = pd.to_datetime(nf["date_added"].str.strip(), errors="coerce")
nf["year_added"] = nf["date_added"].dt.year
nf["primary_country"] = nf["country"].str.split(",").str[0].str.strip()
nf["duration_num"] = pd.to_numeric(nf["duration"].str.extract(r"(\d+)")[0], errors="coerce")
yearly = nf.query("2015<=year_added<=2021").groupby(["year_added","type"]).size().reset_index(name="n")
movies = yearly.query("type=='Movie'"); tv = yearly.query("type=='TV Show'")

if not HAS_PLOTLY:
    print("plotly not installed. Install with: pip install plotly")
    print("Printing R↔Python equivalence table instead.\n")

# ── 1. R↔PYTHON EQUIVALENCE TABLE ───────────────────────
print("=== R plotly ↔ Python plotly Equivalence ===\n")
equivalences = [
    ("ggplotly(p, tooltip='text')", "px.line(df, hover_data=[...])", "Quick conversion"),
    ("plot_ly(df, x=~x, y=~y)", "go.Scatter(x=df.x, y=df.y)", "Native API"),
    ("add_trace(...)", "fig.add_trace(go.Scatter(...))", "Add series"),
    ("layout(hovermode='x unified')", "fig.update_layout(hovermode=...)", "Layout config"),
    ("hovertemplate='Year: %{x}'", "hovertemplate='Year: %{x}'", "IDENTICAL syntax"),
    ("subplot(p1, p2, shareX=T)", "make_subplots(rows=2, shared_xaxes=True)", "Multi-panel"),
    ("saveWidget(p, 'f.html')", "fig.write_html('f.html')", "Save to HTML"),
    ("highlight(on='plotly_selected')", "No direct equivalent (use Dash)", "Linked brushing"),
    ("crosstalk::SharedData$new()", "No equivalent (use Dash callbacks)", "Cross-filtering"),
]
for r_code, py_code, note in equivalences:
    print(f"  R:  {r_code}")
    print(f"  Py: {py_code}")
    print(f"  ({note})\n")

if HAS_PLOTLY:
    # ── 2. px.line (equivalent to ggplotly) ──────────────
    fig1 = px.line(yearly, x="year_added", y="n", color="type",
        color_discrete_map={"Movie": "#1565C0", "TV Show": "#E53935"},
        markers=True,
        title="px.line: Python equivalent of ggplotly()",
        labels={"year_added": "Year", "n": "Titles Added", "type": "Type"})
    fig1.update_layout(hovermode="x unified", template="plotly_white")
    fig1.write_html("output/01_px_line.html")

    # ── 3. go.Scatter (equivalent to plot_ly) ────────────
    fig2 = go.Figure()
    for t, c, w in [("Movie", "#1565C0", 3), ("TV Show", "#E53935", 1.5)]:
        sub = yearly.query("type==@t")
        fig2.add_trace(go.Scatter(
            x=sub.year_added, y=sub.n,
            mode="lines+markers", name=t,
            line=dict(color=c, width=w),
            hovertemplate=f"<b>{t}</b><br>Year: %{{x}}<br>"
                f"Titles: %{{y:,}}<extra></extra>"))
    fig2.update_layout(title="go.Scatter: Python equivalent of plot_ly()",
        xaxis_title="Year", yaxis_title="Titles Added",
        hovermode="x unified", template="plotly_white")
    fig2.write_html("output/02_go_scatter.html")

    # ── 4. Scatter with hover details ────────────────────
    sample = nf.dropna(subset=["year_added","duration_num"]).sample(min(1500,len(nf)), random_state=42)
    fig3 = px.scatter(sample, x="year_added", y="duration_num",
        color="type",
        color_discrete_map={"Movie": "#1565C0", "TV Show": "#E53935"},
        hover_name="title",
        hover_data={"year_added": True, "type": True, "rating": True,
            "duration": True, "primary_country": True, "duration_num": False},
        title="Scatter with hover: full metadata on demand",
        opacity=0.4)
    fig3.update_layout(template="plotly_white", hovermode="closest")
    fig3.write_html("output/03_scatter_details.html")

    # ── 5. Dropdown filter (updatemenus) ─────────────────
    ratings = nf.dropna(subset=["rating"])["rating"].value_counts().head(6).index.tolist()
    ryr = (nf.query("2015<=year_added<=2021 and rating in @ratings")
        .groupby(["year_added","rating"]).size().reset_index(name="n"))
    fig4 = go.Figure()
    for r in ratings:
        sub = ryr.query("rating==@r")
        fig4.add_trace(go.Scatter(x=sub.year_added, y=sub.n,
            mode="lines+markers", name=r,
            hovertemplate=f"<b>{r}</b><br>Year: %{{x}}<br>Count: %{{y}}<extra></extra>"))
    buttons = [dict(label="All", method="restyle",
        args=[{"visible": [True]*len(ratings)}])]
    for i, r in enumerate(ratings):
        vis = [False]*len(ratings); vis[i] = True
        buttons.append(dict(label=r, method="restyle", args=[{"visible": vis}]))
    fig4.update_layout(title="Dropdown Filter: Select Rating",
        updatemenus=[dict(type="dropdown", x=0.1, y=1.15, buttons=buttons)],
        template="plotly_white")
    fig4.write_html("output/04_dropdown.html")

    # ── 6. Subplot with shared x-axis ────────────────────
    fig5 = make_subplots(rows=2, cols=1, shared_xaxes=True,
        subplot_titles=("Line Chart", "Bar Chart"))
    for t, c in [("Movie","#1565C0"),("TV Show","#E53935")]:
        sub = yearly.query("type==@t")
        fig5.add_trace(go.Scatter(x=sub.year_added, y=sub.n,
            mode="lines+markers", name=t, line=dict(color=c)),
            row=1, col=1)
        fig5.add_trace(go.Bar(x=sub.year_added, y=sub.n,
            name=t, marker_color=c, showlegend=False),
            row=2, col=1)
    fig5.update_layout(title="Subplot: shared x-axis (zoom syncs)",
        template="plotly_white", barmode="group")
    fig5.write_html("output/05_subplot.html")

    print("\n5 interactive HTML files saved in output/")

else:
    print("Install plotly to generate interactive HTML files.")
    print("pip install plotly")

print("\nAll W08-M02 Python outputs saved")
