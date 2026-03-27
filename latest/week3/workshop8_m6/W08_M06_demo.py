"""W08-M06: Dashboard Design Principles — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
from matplotlib.gridspec import GridSpec
os.makedirs("output", exist_ok=True)

nf = pd.read_csv("netflix.csv")
nf["date_added"] = pd.to_datetime(nf["date_added"].str.strip(), errors="coerce")
nf["year_added"] = nf["date_added"].dt.year
nf["primary_country"] = nf["country"].str.split(",").str[0].str.strip()

# GLOBAL PALETTE (Rule 4)
PALETTE = {"Movie": "#1565C0", "TV Show": "#E53935"}

yearly = nf.query("2015<=year_added<=2021").groupby(["year_added","type"]).size().reset_index(name="n")

# ══════════════════════════════════════════════════════════
# DASHBOARD MOCKUP (static matplotlib version)
# Demonstrates the layout grid
# ══════════════════════════════════════════════════════════
fig = plt.figure(figsize=(14, 12))
gs = GridSpec(4, 4, figure=fig, hspace=0.40, wspace=0.35,
    height_ratios=[0.8, 2.5, 2.5, 2])

# ── KPI ROW ──────────────────────────────────────────────
kpis = [
    ("Total Titles", f"{len(nf):,}", "+12.3%", "#333"),
    ("Movies", f"{(nf.type=='Movie').sum():,}", "–5.2%", "#1565C0"),
    ("TV Shows", f"{(nf.type=='TV Show').sum():,}", "+18.7%", "#E53935"),
    ("Countries", f"{nf['primary_country'].nunique()}", "+3.1%", "#7B1FA2"),
]
for i, (label, value, delta, color) in enumerate(kpis):
    ax = fig.add_subplot(gs[0, i])
    ax.text(0.5, 0.65, value, ha="center", va="center",
        fontsize=18, fontweight="bold", color=color, transform=ax.transAxes)
    delta_color = "#2E7D32" if delta.startswith("+") else "#C62828"
    ax.text(0.5, 0.30, delta, ha="center", va="center",
        fontsize=10, fontweight="bold", color=delta_color, transform=ax.transAxes)
    ax.text(0.5, 0.05, label, ha="center", va="center",
        fontsize=8, color="#888", transform=ax.transAxes)
    ax.axis("off")
    ax.add_patch(plt.Rectangle((0.02, 0.02), 0.96, 0.96, fill=False,
        edgecolor="#EEEEEE", lw=1, transform=ax.transAxes))

# ── PRIMARY CHART ────────────────────────────────────────
ax = fig.add_subplot(gs[1, :2])
for t, c in PALETTE.items():
    sub = yearly.query("type==@t")
    ax.plot(sub.year_added, sub.n, "-o", color=c, lw=1.5, markersize=4, label=t)
ax.legend(fontsize=7); ax.set_title("Yearly Additions by Type", fontsize=10, fontweight="bold")
ax.set_ylabel("Titles"); ax.grid(axis="y", alpha=0.2)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

# ── SECONDARY CHART ──────────────────────────────────────
ax = fig.add_subplot(gs[1, 2:])
top10 = nf.dropna(subset=["primary_country"])["primary_country"].value_counts().head(10).sort_values()
ax.barh(top10.index, top10.values, color="#1565C0", alpha=0.7, height=0.6)
ax.set_title("Top 10 Countries", fontsize=10, fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

# ── DETAIL ROW ───────────────────────────────────────────
# Detail 1: Type split
ax = fig.add_subplot(gs[2, :2])
type_split = nf["type"].value_counts()
ax.bar(type_split.index, type_split.values/type_split.sum()*100,
    color=[PALETTE.get(t, "#888") for t in type_split.index], width=0.4)
for i, (t, v) in enumerate(zip(type_split.index, type_split.values/type_split.sum()*100)):
    ax.text(i, v+1, f"{v:.0f}%", ha="center", fontsize=9, fontweight="bold")
ax.set_title("Type Split (%)", fontsize=10, fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

# Detail 2: Top ratings
ax = fig.add_subplot(gs[2, 2:])
top_ratings = nf.dropna(subset=["rating"])["rating"].value_counts().head(6).sort_values()
ax.barh(top_ratings.index, top_ratings.values, color="#2E7D32", alpha=0.7, height=0.5)
ax.set_title("Top Ratings", fontsize=10, fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

# Detail 3: Monthly sparkline
ax = fig.add_subplot(gs[3, :])
monthly = (nf.dropna(subset=["date_added"]).query("date_added.dt.year>=2018")
    .set_index("date_added").resample("ME").size())
ax.plot(monthly.index, monthly.values, color="#1565C0", lw=0.8)
ax.fill_between(monthly.index, monthly.values, alpha=0.05, color="#1565C0")
from matplotlib.dates import DateFormatter
ax.xaxis.set_major_formatter(DateFormatter("%Y-%m"))
ax.set_title("Monthly Trend (2018–2021)", fontsize=10, fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

fig.suptitle("Netflix Content Dashboard (Static Mockup)\n"
    "Layout: KPI row → Primary + Secondary → Detail panels",
    fontsize=14, fontweight="bold")
plt.savefig("output/dashboard_mockup.png", dpi=300, bbox_inches="tight"); plt.close()

# ══════════════════════════════════════════════════════════
# DASH KPI CARD TEMPLATE
# ══════════════════════════════════════════════════════════
kpi_template = '''
import dash_bootstrap_components as dbc
from dash import html

def make_kpi(title, value, delta):
    """Reusable KPI card component."""
    color = "success" if delta >= 0 else "danger"
    arrow = "↑" if delta >= 0 else "↓"
    return dbc.Card(dbc.CardBody([
        html.H6(title, className="text-muted mb-1",
            style={"fontSize": "0.8rem"}),
        html.H3(f"{value:,}", className="fw-bold mb-1"),
        html.P(f"{arrow} {abs(delta):.1f}%",
            className=f"text-{color} mb-0",
            style={"fontSize": "0.9rem"}),
    ]), className="text-center shadow-sm")

# Usage in layout:
kpi_row = dbc.Row([
    dbc.Col(make_kpi("Total Titles", 8807, 12.3), width=3),
    dbc.Col(make_kpi("Movies", 6131, -5.2), width=3),
    dbc.Col(make_kpi("TV Shows", 2676, 18.7), width=3),
    dbc.Col(make_kpi("Countries", 78, 3.1), width=3),
], className="mb-3")
'''
with open("output/kpi_template.py", "w") as f:
    f.write(kpi_template)

# ══════════════════════════════════════════════════════════
# FEW'S RULES + ANTI-PATTERNS
# ══════════════════════════════════════════════════════════
print("=== Few's Six Dashboard Design Rules ===")
rules = [
    ("1. One screen", "No scrolling. Everything visible at once."),
    ("2. KPIs at top", "Big numbers first. Charts below for context."),
    ("3. 5–7 charts max", "Cognitive limit. More = overwhelm."),
    ("4. Consistent colour", "Same colour = same meaning across all panels."),
    ("5. Filter sidebar", "Inputs on left or top. Never inline with charts."),
    ("6. Descriptive titles", "Dashboard = reader-driven. State the metric, not the finding."),
]
for name, desc in rules:
    print(f"  {name}: {desc}")

print("\n=== Five Anti-Patterns ===")
antis = [
    ("Chartjunk dashboard", "→ Flat, minimal, data-ink focus"),
    ("Scroll-of-death", "→ Max 5–7 charts; use tabs"),
    ("Colour chaos", "→ Global palette applied everywhere"),
    ("No KPIs", "→ Add KPI row at top"),
    ("Filter everywhere", "→ Sidebar or top filter bar"),
]
for name, fix in antis:
    print(f"  {name} {fix}")

print("\nAll W08-M06 Python outputs saved")
