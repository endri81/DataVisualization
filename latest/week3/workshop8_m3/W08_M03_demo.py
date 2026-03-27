"""
W08-M03: plotly in Python — Interactive Charts — UNYT
This is the PRIMARY demo script for this module (Python-focused).
"""
import numpy as np, pandas as pd, os
os.makedirs("output", exist_ok=True)

try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False
    print("plotly not installed. pip install plotly")

nf = pd.read_csv("netflix.csv")
nf["date_added"] = pd.to_datetime(nf["date_added"].str.strip(), errors="coerce")
nf["year_added"] = nf["date_added"].dt.year
nf["primary_country"] = nf["country"].str.split(",").str[0].str.strip()
nf["duration_num"] = pd.to_numeric(nf["duration"].str.extract(r"(\d+)")[0], errors="coerce")
yearly = nf.query("2015<=year_added<=2021").groupby(["year_added","type"]).size().reset_index(name="n")
movies = yearly.query("type=='Movie'"); tv = yearly.query("type=='TV Show'")

if HAS_PLOTLY:
    # ══════════════════════════════════════════════════════
    # 1. px.line — ONE-LINER TIME SERIES
    # Equivalent to R: ggplotly(ggplot(...) + geom_line())
    # ══════════════════════════════════════════════════════
    fig1 = px.line(yearly, x="year_added", y="n", color="type",
        color_discrete_map={"Movie": "#1565C0", "TV Show": "#E53935"},
        markers=True,
        title="px.line: Netflix Additions by Type (hover for details)",
        labels={"year_added": "Year", "n": "Titles Added", "type": "Type"})
    fig1.update_layout(hovermode="x unified", template="plotly_white")
    fig1.write_html("output/01_px_line.html")
    print("01: px.line saved")

    # ══════════════════════════════════════════════════════
    # 2. px.scatter — HOVER WITH FULL METADATA
    # Equivalent to R: plot_ly(type="scatter", text=~paste0(...))
    # ══════════════════════════════════════════════════════
    sample = nf.dropna(subset=["year_added","duration_num"]).sample(
        min(2000, len(nf)), random_state=42)
    fig2 = px.scatter(sample, x="year_added", y="duration_num",
        color="type",
        color_discrete_map={"Movie": "#1565C0", "TV Show": "#E53935"},
        hover_name="title",
        hover_data={"year_added": True, "type": True, "rating": True,
            "duration": True, "primary_country": True, "duration_num": False},
        opacity=0.4,
        title="px.scatter: hover for full title metadata")
    fig2.update_layout(hovermode="closest", template="plotly_white")
    fig2.write_html("output/02_px_scatter.html")
    print("02: px.scatter saved")

    # ══════════════════════════════════════════════════════
    # 3. go.Scatter — TRACE-LEVEL CONTROL + HOVERTEMPLATE
    # Equivalent to R: plot_ly() |> add_trace(hovertemplate=...)
    # ══════════════════════════════════════════════════════
    fig3 = go.Figure()
    for t, c, w in [("Movie", "#1565C0", 3), ("TV Show", "#E53935", 1.5)]:
        sub = yearly.query("type==@t")
        fig3.add_trace(go.Scatter(
            x=sub.year_added, y=sub.n,
            mode="lines+markers", name=t,
            line=dict(color=c, width=w),
            marker=dict(size=6 if t=="Movie" else 4),
            hovertemplate=(
                f"<b>{t}</b><br>"
                "Year: %{x}<br>"
                "Titles: %{y:,}"
                "<extra></extra>")))
    # Add annotation (equivalent to R: layout(annotations=list(...)))
    peak_n = movies.n.max(); latest_n = movies.iloc[-1]["n"]
    decline = round((1 - latest_n / peak_n) * 100)
    fig3.add_annotation(
        x=2020, y=(peak_n + latest_n) / 2,
        text=f"<b>–{decline}%</b>",
        showarrow=True, arrowhead=2, arrowcolor="#E53935",
        font=dict(color="#E53935", size=14),
        ax=-60, ay=-40)
    fig3.update_layout(
        title=f"go.Scatter: Movie additions declined {decline}% from peak",
        xaxis_title="Year", yaxis_title="Titles Added",
        hovermode="x unified", template="plotly_white")
    fig3.write_html("output/03_go_annotated.html")
    print("03: go.Scatter annotated saved")

    # ══════════════════════════════════════════════════════
    # 4. DROPDOWN FILTER (updatemenus)
    # Equivalent to R: layout(updatemenus=list(list(type="dropdown")))
    # ══════════════════════════════════════════════════════
    ratings = nf.dropna(subset=["rating"])["rating"].value_counts().head(6).index.tolist()
    ryr = (nf.query("2015<=year_added<=2021 and rating in @ratings")
        .groupby(["year_added", "rating"]).size().reset_index(name="n"))

    fig4 = go.Figure()
    for r in ratings:
        sub = ryr.query("rating==@r")
        fig4.add_trace(go.Scatter(
            x=sub.year_added, y=sub.n,
            mode="lines+markers", name=r,
            hovertemplate=f"<b>{r}</b><br>Year: %{{x}}<br>Count: %{{y}}<extra></extra>"))

    buttons = [dict(label="All Ratings", method="restyle",
        args=[{"visible": [True] * len(ratings)}])]
    for i, r in enumerate(ratings):
        vis = [False] * len(ratings); vis[i] = True
        buttons.append(dict(label=r, method="restyle", args=[{"visible": vis}]))

    fig4.update_layout(
        title="Dropdown Filter: Select a Rating Category",
        updatemenus=[dict(type="dropdown", x=0.1, y=1.15, buttons=buttons)],
        xaxis_title="Year", yaxis_title="Titles",
        template="plotly_white")
    fig4.write_html("output/04_dropdown_filter.html")
    print("04: dropdown filter saved")

    # ══════════════════════════════════════════════════════
    # 5. make_subplots — SHARED X-AXIS
    # Equivalent to R: subplot(p1, p2, shareX=TRUE)
    # ══════════════════════════════════════════════════════
    fig5 = make_subplots(rows=2, cols=1, shared_xaxes=True,
        subplot_titles=("Line Chart", "Bar Chart"))
    for t, c in [("Movie", "#1565C0"), ("TV Show", "#E53935")]:
        sub = yearly.query("type==@t")
        fig5.add_trace(go.Scatter(x=sub.year_added, y=sub.n,
            mode="lines+markers", name=t, line=dict(color=c)),
            row=1, col=1)
        fig5.add_trace(go.Bar(x=sub.year_added, y=sub.n,
            name=t, marker_color=c, showlegend=False),
            row=2, col=1)
    fig5.update_layout(
        title="make_subplots: shared x-axis (zoom syncs between panels)",
        template="plotly_white", barmode="group",
        height=600)
    fig5.write_html("output/05_subplot.html")
    print("05: subplot saved")

    # ══════════════════════════════════════════════════════
    # 6. px ANIMATION — ANIMATED SCATTER
    # Equivalent to R: plot_ly(frame=~year) |> animation_opts()
    # ══════════════════════════════════════════════════════
    genres = nf["listed_in"].str.split(",").explode().str.strip()
    top5 = genres.value_counts().head(5).index.tolist()
    nf_g = nf.assign(listed_in=nf["listed_in"].str.split(",")).explode("listed_in")
    nf_g["genre"] = nf_g["listed_in"].str.strip()
    genre_yr = (nf_g.query("genre in @top5 and 2015<=year_added<=2021")
        .groupby(["year_added", "genre"]).size().reset_index(name="n"))

    fig6 = px.bar(genre_yr, x="genre", y="n", color="genre",
        animation_frame="year_added",
        range_y=[0, genre_yr.n.max() * 1.2],
        title="px Animation: Genre Additions by Year (press Play)",
        labels={"n": "Titles Added", "genre": "Genre", "year_added": "Year"})
    fig6.update_layout(template="plotly_white",
        transition=dict(duration=500))
    fig6.write_html("output/06_animation.html")
    print("06: animation saved")

    # ══════════════════════════════════════════════════════
    # 7. FACETED px — SMALL MULTIPLES
    # Equivalent to R: ggplot + facet_wrap → ggplotly
    # ══════════════════════════════════════════════════════
    top3_countries = (nf.dropna(subset=["primary_country"])
        ["primary_country"].value_counts().head(3).index.tolist())
    country_yr = (nf.query("primary_country in @top3_countries and 2015<=year_added<=2021")
        .groupby(["year_added", "primary_country", "type"]).size().reset_index(name="n"))

    fig7 = px.line(country_yr, x="year_added", y="n", color="type",
        facet_col="primary_country",
        color_discrete_map={"Movie": "#1565C0", "TV Show": "#E53935"},
        markers=True,
        title="px Facet: Small Multiples by Country (interactive!)",
        labels={"year_added": "Year", "n": "Titles"})
    fig7.update_layout(template="plotly_white")
    fig7.write_html("output/07_faceted.html")
    print("07: faceted saved")

    print(f"\n7 interactive HTML files saved in output/")

else:
    print("Install plotly: pip install plotly")

# ══════════════════════════════════════════════════════════
# COMPARISON TABLE: px vs go
# ══════════════════════════════════════════════════════════
print("\n=== px vs go: When to Use Each ===")
comparisons = [
    ("Quick EDA line/scatter/bar", "px ✓", "go ✗ (overkill)"),
    ("Custom hovertemplate", "px ✗ (limited)", "go ✓"),
    ("Dropdown/slider filters", "px ✗", "go ✓ (updatemenus)"),
    ("Animations", "px ✓ (animation_frame)", "go ✓ (frames)"),
    ("Annotations", "px partial", "go ✓ (add_annotation)"),
    ("Small multiples", "px ✓ (facet_col)", "go ✗ (manual)"),
    ("Production dashboard", "px start → go refine", "go ✓"),
]
for scenario, px_rec, go_rec in comparisons:
    print(f"  {scenario:<30} {px_rec:<20} {go_rec}")

print("\nAll W08-M03 Python outputs saved")
