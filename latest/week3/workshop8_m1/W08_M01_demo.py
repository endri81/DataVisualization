"""W08-M01: Interactivity Theory — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
os.makedirs("output", exist_ok=True)

# plotly is the primary interactive tool in Python
try:
    import plotly.express as px
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False
    print("plotly not installed — generating static equivalents")

nf = pd.read_csv("netflix.csv")
nf["date_added"] = pd.to_datetime(nf["date_added"].str.strip(), errors="coerce")
nf["year_added"] = nf["date_added"].dt.year
yearly = nf.query("2015<=year_added<=2021").groupby(["year_added","type"]).size().reset_index(name="n")

# ── 1. STATIC VERSION (matplotlib — W07 style) ──────────
fig, ax = plt.subplots(figsize=(9, 5))
for t, c in [("Movie", "#1565C0"), ("TV Show", "#E53935")]:
    sub = yearly.query("type == @t")
    ax.plot(sub.year_added, sub.n, "-o", color=c, lw=1.5, markersize=5, label=t)
ax.legend(fontsize=8)
ax.set_title("STATIC (matplotlib): Author-driven, no interactivity\n"
    "The reader sees exactly what you designed", fontweight="bold")
ax.set_xlabel("Year"); ax.set_ylabel("Titles Added")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/static_version.png", dpi=300); plt.close()

# ── 2. INTERACTIVE VERSION (plotly) ──────────────────────
if HAS_PLOTLY:
    # plotly.express: one-liner interactive chart
    fig_px = px.line(yearly, x="year_added", y="n", color="type",
        color_discrete_map={"Movie": "#1565C0", "TV Show": "#E53935"},
        markers=True,
        title="Interactive (plotly.express): hover, zoom, pan built-in",
        labels={"year_added": "Year", "n": "Titles Added", "type": "Type"})
    fig_px.update_traces(
        hovertemplate="Year: %{x}<br>Titles: %{y}<br>Type: %{fullData.name}")
    fig_px.write_html("output/interactive_px.html")
    print("Saved: output/interactive_px.html")

    # plotly.graph_objects: full control
    fig_go = go.Figure()
    for t, c in [("Movie", "#1565C0"), ("TV Show", "#E53935")]:
        sub = yearly.query("type == @t")
        fig_go.add_trace(go.Scatter(
            x=sub.year_added, y=sub.n,
            mode="lines+markers", name=t,
            line=dict(color=c, width=2),
            marker=dict(size=6),
            hovertemplate=f"<b>{t}</b><br>Year: %{{x}}<br>"
                f"Titles: %{{y}}<extra></extra>"))
    fig_go.update_layout(
        title="Native plotly.go: full control over interactivity",
        xaxis_title="Year", yaxis_title="Titles Added",
        hovermode="x unified",
        template="plotly_white")
    fig_go.write_html("output/interactive_go.html")
    print("Saved: output/interactive_go.html")

    # ── 3. SHNEIDERMAN'S MANTRA DEMO ────────────────────
    sample = nf.dropna(subset=["year_added"]).sample(min(2000, len(nf)), random_state=42)
    sample["duration_num"] = pd.to_numeric(
        sample["duration"].str.extract(r"(\d+)")[0], errors="coerce")

    fig_mantra = px.scatter(sample, x="year_added", y="duration_num",
        color="type",
        color_discrete_map={"Movie": "#1565C0", "TV Show": "#E53935"},
        hover_name="title",
        hover_data={"year_added": True, "type": True, "rating": True,
            "duration": True, "duration_num": False},
        title="Shneiderman Demo: Overview → Zoom → Hover for Details",
        labels={"year_added": "Year Added", "duration_num": "Duration"},
        opacity=0.4)
    # Add dropdown filter (Step 3: Filter)
    fig_mantra.update_layout(
        updatemenus=[dict(
            type="dropdown", x=0.1, y=1.15,
            buttons=[
                dict(label="Both", method="update",
                    args=[{"visible": [True, True]}]),
                dict(label="Movies Only", method="update",
                    args=[{"visible": [True, False]}]),
                dict(label="TV Shows Only", method="update",
                    args=[{"visible": [False, True]}]),
            ]
        )],
        template="plotly_white")
    fig_mantra.write_html("output/shneiderman_demo.html")
    print("Saved: output/shneiderman_demo.html")

else:
    # Fallback: annotated static showing what interactivity adds
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    for t, c in [("Movie", "#1565C0"), ("TV Show", "#E53935")]:
        sub = yearly.query("type == @t")
        ax1.plot(sub.year_added, sub.n, "-o", color=c, lw=1.5, label=t)
        ax2.plot(sub.year_added, sub.n, "-o", color=c, lw=1.5, label=t)
    ax1.legend(fontsize=7); ax2.legend(fontsize=7)
    ax1.set_title("STATIC\n(no hover, no zoom, no filter)", fontweight="bold", color="#888")
    ax2.set_title("INTERACTIVE (plotly)\n[hover tooltip, zoom, dropdown filter]",
        fontweight="bold", color="#1565C0")
    ax2.annotate("← Hover shows:\nYear, Type, Count", xy=(2019, 1100),
        fontsize=8, color="#E53935",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#E53935"))
    for ax in [ax1, ax2]:
        ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    fig.suptitle("Static vs Interactive: What Plotly Adds", fontweight="bold")
    plt.tight_layout(); plt.savefig("output/static_vs_interactive.png", dpi=300); plt.close()

# ── 4. COMPARISON + DECISION TABLES ─────────────────────
print("\n=== Static vs Interactive ===")
print(f"{'Dimension':<20} {'Static (matplotlib)':<25} {'Interactive (plotly)'}")
for dim, s, i in [
    ("Hover tooltip", "No", "Yes (built-in)"),
    ("Zoom", "No", "Yes (scroll/drag)"),
    ("Filter", "No", "Yes (dropdown/slider)"),
    ("Linked brushing", "No", "Yes (highlight)"),
    ("Export PNG", "Manual savefig()", "Yes (modebar)"),
    ("Reset view", "N/A", "Yes (reset axes)"),
    ("Audience control", "None", "Full")]:
    print(f"  {dim:<20} {s:<25} {i}")

print("\n=== When to Use ===")
for ctx, rec in [
    ("Board presentation", "Static"),
    ("PDF report", "Static"),
    ("Ongoing monitoring", "Interactive"),
    ("Self-service analytics", "Interactive"),
    ("Journal paper", "Static"),
    ("Team data review", "Interactive"),
    ("Social media", "Static")]:
    print(f"  {ctx:<25} → {rec}")

print("\nAll W08-M01 Python outputs saved")
