"""W07-M02: Exploratory vs Explanatory Visualization — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
from matplotlib.dates import DateFormatter
os.makedirs("output", exist_ok=True)

# ── 1. LOAD DATA ────────────────────────────────────────
nf = pd.read_csv("netflix.csv")
nf["date_added"] = pd.to_datetime(nf["date_added"].str.strip(), errors="coerce")
nf["year_added"] = nf["date_added"].dt.year
yearly = (nf.query("2015 <= year_added <= 2021")
    .groupby(["year_added", "type"]).size().reset_index(name="n"))
movies = yearly.query("type == 'Movie'")
tvshows = yearly.query("type == 'TV Show'")

# ── 2. READER-DRIVEN vs AUTHOR-DRIVEN ───────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 5.5))

# Reader-driven (dashboard)
x = np.arange(2015, 2022); w = 0.3
for t, offset, c in [("Movie", -w/2, "#1565C0"), ("TV Show", w/2, "#E53935")]:
    sub = yearly.query("type == @t")
    ax1.bar(sub.year_added + offset, sub.n, width=w, color=c, alpha=0.7, label=t)
ax1.legend(fontsize=8)
ax1.set_title("READER-DRIVEN (Dashboard)\n'Netflix Additions by Type'\n"
    "Descriptive title, legend, both series equal weight",
    fontsize=10, fontweight="bold", color="#888")
ax1.set_xlabel("Year"); ax1.set_ylabel("Titles")
ax1.grid(axis="y", alpha=0.2)

# Author-driven (story slide)
ax2.plot(tvshows.year_added, tvshows.n, "-o", color="#DDDDDD", lw=0.8, markersize=3)
ax2.plot(movies.year_added, movies.n, "-o", color="#1565C0", lw=2.5, markersize=6)
ax2.text(2021.15, movies.iloc[-1]["n"], " Movies", fontsize=9,
    fontweight="bold", color="#1565C0", va="center")
ax2.text(2021.15, tvshows.iloc[-1]["n"], " TV Shows", fontsize=8,
    color="#BBBBBB", va="center")
# Decline callout
peak_n = movies["n"].max()
latest_n = movies.iloc[-1]["n"]
decline = round((1 - latest_n / peak_n) * 100)
ax2.annotate(f"–{decline}% since\n2019 peak", xy=(2020, (peak_n + latest_n)/2),
    fontsize=10, fontweight="bold", color="#E53935", ha="center",
    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#E53935", alpha=0.9))
ax2.set_xlim(2014.5, 2022.5)
ax2.set_title("AUTHOR-DRIVEN (Story Slide)\n"
    f"'Movie additions declined {decline}% from 2019 peak'\n"
    "Declarative title, grey+accent, direct labels",
    fontsize=10, fontweight="bold", color="#1565C0")
ax2.set_ylabel("Titles Added")

for ax in [ax1, ax2]:
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.suptitle("Same Data: Reader-Driven (Dashboard) vs Author-Driven (Story Slide)",
    fontsize=13, fontweight="bold")
plt.tight_layout(); plt.savefig("output/reader_vs_author.png", dpi=300); plt.close()

# ── 3. MARTINI GLASS: 3 Slides → Dashboard ──────────────
fig, axes = plt.subplots(2, 2, figsize=(14, 9))

# Slide 1: Context
cumul = nf.dropna(subset=["date_added"]).set_index("date_added").resample("ME").size().cumsum()
axes[0,0].fill_between(cumul.index, cumul.values, alpha=0.15, color="#1565C0")
axes[0,0].plot(cumul.index, cumul.values, color="#1565C0", lw=1.2)
axes[0,0].set_title("Slide 1: Netflix built 8,800+ titles",
    fontsize=10, fontweight="bold", color="#2E7D32")
axes[0,0].xaxis.set_major_formatter(DateFormatter("%Y"))

# Slide 2: Complication
axes[0,1].plot(tvshows.year_added, tvshows.n, "-o", color="#DDD", lw=0.8, markersize=3)
axes[0,1].plot(movies.year_added, movies.n, "-o", color="#1565C0", lw=2, markersize=5)
axes[0,1].set_title("Slide 2: But movies declining since 2019",
    fontsize=10, fontweight="bold", color="#E65100")

# Slide 3: Resolution
nf["primary_country"] = nf["country"].str.split(",").str[0].str.strip()
top5 = nf.dropna(subset=["primary_country"])["primary_country"].value_counts().head(5)
axes[1,0].barh(top5.index[::-1], top5.values[::-1], color="#2E7D32", height=0.5)
axes[1,0].set_title("Slide 3: US leads, India rising",
    fontsize=10, fontweight="bold", color="#7B1FA2")

# Dashboard transition
monthly = (nf.dropna(subset=["date_added"]).query("date_added.dt.year >= 2015")
    .set_index("date_added").groupby("type").resample("ME").size()
    .reset_index(name="n"))
for t, c in [("Movie", "#1565C0"), ("TV Show", "#E53935")]:
    sub = monthly.query("type == @t")
    axes[1,1].plot(sub["date_added"], sub["n"], color=c, lw=0.5, label=t)
axes[1,1].legend(fontsize=6)
axes[1,1].set_title("→ DASHBOARD: Explore freely (filter, drill down)",
    fontsize=10, fontweight="bold", color="#888")
axes[1,1].xaxis.set_major_formatter(DateFormatter("%Y"))

for ax in axes.flatten():
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=6)
fig.suptitle("Martini Glass: 3 Guided Slides → Dashboard Exploration",
    fontsize=13, fontweight="bold")
plt.tight_layout(); plt.savefig("output/martini_glass.png", dpi=300); plt.close()

# ── 4. e-Car: DASHBOARD vs STORY ────────────────────────
ec = pd.read_csv("ecar.csv"); ec.columns = [c.strip().replace("  "," ") for c in ec.columns]
ec["Year"] = pd.to_datetime(ec["Approve Date"], format="%m/%d/%Y", errors="coerce").dt.year
ec["Spread"] = ec["Rate"] - ec["Cost of Funds"]
yr_ec = ec.query("2002<=Year<=2012").groupby("Year").agg(
    rate=("Rate","mean"), spread=("Spread","mean")).reset_index()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
# Dashboard
ax1.plot(yr_ec.Year, yr_ec.rate, "-o", color="#1565C0", lw=1.2, label="Rate")
ax1.plot(yr_ec.Year, yr_ec.spread, "-s", color="#E53935", lw=1.2, label="Spread")
ax1.legend(fontsize=7)
ax1.set_title("DASHBOARD: 'Rate and Spread Over Time'\n(descriptive, two equal series)",
    fontsize=9, fontweight="bold", color="#888")
# Story
ax2.plot(yr_ec.Year, yr_ec.spread, color="#DDD", lw=0.8)
ax2.plot(yr_ec.Year, yr_ec.rate, "-o", color="#1565C0", lw=2.5, markersize=5)
ax2.axvline(x=2008, ls="--", color="#E53935", lw=0.8)
ax2.annotate("2008 crisis:\n–2pp rate drop", xy=(2008, yr_ec.rate.min()),
    xytext=(2009.5, yr_ec.rate.max()*0.85),
    fontsize=8, fontweight="bold", color="#E53935",
    arrowprops=dict(arrowstyle="->", color="#E53935", lw=1))
ax2.text(2012.1, yr_ec.iloc[-1].rate, " Rate", fontsize=8,
    fontweight="bold", color="#1565C0", va="center")
ax2.text(2012.1, yr_ec.iloc[-1].spread, " Spread", fontsize=7,
    color="#BBB", va="center")
ax2.set_xlim(2001.5, 2013.5)
ax2.set_title("STORY: 'Loan rates dropped 2pp after the 2008 crisis'\n(declarative, grey+accent, annotated)",
    fontsize=9, fontweight="bold", color="#1565C0")
for ax in [ax1,ax2]:
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.set_ylabel("Percentage Points")
fig.suptitle("e-Car: Same Data, Dashboard vs Story Slide", fontweight="bold")
plt.tight_layout(); plt.savefig("output/ecar_dash_vs_story.png", dpi=300); plt.close()

# ── 5. TRANSFORMATION CHECKLIST ──────────────────────────
print("\n=== Dashboard → Story Slide Checklist ===")
checks = [
    ("Title", "Descriptive → Declarative (the finding)"),
    ("Legend", "Remove → Direct labels at endpoints"),
    ("Colour", "All coloured → Grey + accent"),
    ("Gridlines", "Visible → Minimal or none"),
    ("Annotation", "None → Callouts, arrows, % labels"),
    ("Data density", "Show all → Show only the story"),
    ("Interactivity", "Filters/tooltips → Static"),
    ("Subtitle", "Metric description → Strategic implication"),
]
for element, change in checks:
    print(f"  {element:<15} {change}")

print("\nAll W07-M02 Python outputs saved")
