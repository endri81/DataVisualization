"""W07-M01: Narrative Structure in Data Communication — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
from matplotlib.dates import DateFormatter
os.makedirs("output", exist_ok=True)

# ── 1. LOAD DATA ────────────────────────────────────────
nf = pd.read_csv("netflix.csv")
nf["date_added"] = pd.to_datetime(nf["date_added"].str.strip(), errors="coerce")
nf["year_added"] = nf["date_added"].dt.year

yearly = (nf.query("2015 <= year_added <= 2021")
    .groupby(["year_added", "type"]).size()
    .reset_index(name="n"))

# ── 2. EXPLORATORY vs EXPLANATORY ────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 5))

# EXPLORATORY: raw EDA chart
for t, c, m in [("Movie", "#1565C0", "o"), ("TV Show", "#E53935", "s")]:
    sub = yearly.query("type == @t")
    ax1.plot(sub.year_added, sub.n, f"-{m}", color=c, lw=1, markersize=5, label=t)
ax1.legend(fontsize=8)
ax1.set_title("EXPLORATORY\n'Netflix Additions by Type (2015–2021)'\n"
    "(descriptive title, legend, no emphasis)", fontsize=10, fontweight="bold", color="#888")
ax1.set_xlabel("Year"); ax1.set_ylabel("Count")
ax1.spines["top"].set_visible(False); ax1.spines["right"].set_visible(False)

# EXPLANATORY: story-focused redesign
movies = yearly.query("type == 'Movie'")
tvshows = yearly.query("type == 'TV Show'")
ax2.plot(tvshows.year_added, tvshows.n, "-o", color="#DDDDDD", lw=0.8, markersize=4)
ax2.plot(movies.year_added, movies.n, "-o", color="#1565C0", lw=2.5, markersize=6)
# Direct labels
ax2.text(2021.15, movies.iloc[-1]["n"], " Movies", fontsize=9, fontweight="bold",
    color="#1565C0", va="center")
ax2.text(2021.15, tvshows.iloc[-1]["n"], " TV Shows", fontsize=9,
    color="#BBBBBB", va="center")
ax2.set_xlim(2014.5, 2022.5)
ax2.set_title("EXPLANATORY\n'Movie additions peaked in 2019 and declined since'\n"
    "(declarative title, direct labels, grey+accent)", fontsize=10, fontweight="bold", color="#1565C0")
ax2.set_ylabel("Titles Added")
ax2.spines["top"].set_visible(False); ax2.spines["right"].set_visible(False)

fig.suptitle("The Fundamental Shift: From Exploration to Explanation",
    fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("output/exp_vs_expl.png", dpi=300); plt.close()

# ── 3. BIG IDEA CHART ───────────────────────────────────
peak = movies.loc[movies.n.idxmax()]
latest = movies.iloc[-1]
decline_pct = round((1 - latest["n"] / peak["n"]) * 100)

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(movies.year_added, movies.n, "-o", color="#1565C0", lw=2.5, markersize=6)
# Peak reference line
ax.axhline(y=peak["n"], ls=":", color="#888", lw=0.5)
# Decline annotation with arrow
ax.annotate(f"{decline_pct}% decline\nsince peak",
    xy=(2020.5, (peak["n"] + latest["n"]) / 2),
    fontsize=11, fontweight="bold", color="#E53935", ha="center",
    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#E53935", alpha=0.9))
ax.annotate("", xy=(2020.5, latest["n"] + 10),
    xytext=(2020.5, peak["n"] - 10),
    arrowprops=dict(arrowstyle="<->", color="#E53935", lw=1.5))
ax.set_title(f"Movie additions declined {decline_pct}% from peak —\n"
    "the content pipeline is contracting",
    fontsize=12, fontweight="bold")
ax.set_ylabel("Movie Titles Added"); ax.set_xlabel("")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig("output/big_idea.png", dpi=300); plt.close()

# ── 4. THREE-SLIDE STORY ARC ────────────────────────────
fig, axes = plt.subplots(3, 1, figsize=(10, 14))

# Slide 1: Context (cumulative catalog growth)
cumulative = (nf.dropna(subset=["date_added"])
    .set_index("date_added").resample("ME").size().cumsum())
axes[0].fill_between(cumulative.index, cumulative.values, alpha=0.2, color="#1565C0")
axes[0].plot(cumulative.index, cumulative.values, color="#1565C0", lw=1.5)
axes[0].set_title("1. CONTEXT: Netflix built 8,800+ titles by 2021",
    fontsize=11, fontweight="bold", color="#2E7D32")
axes[0].set_ylabel("Cumulative Titles")
axes[0].xaxis.set_major_formatter(DateFormatter("%Y"))

# Slide 2: Complication (movie decline)
axes[1].plot(tvshows.year_added, tvshows.n, "-o", color="#DDDDDD", lw=0.8, markersize=4)
axes[1].plot(movies.year_added, movies.n, "-o", color="#1565C0", lw=2.5, markersize=6)
axes[1].text(2021.1, movies.iloc[-1]["n"], " Movies", fontsize=9,
    fontweight="bold", color="#1565C0", va="center")
axes[1].text(2021.1, tvshows.iloc[-1]["n"], " TV Shows", fontsize=8,
    color="#BBBBBB", va="center")
axes[1].set_xlim(2014.5, 2022.5)
axes[1].set_title("2. COMPLICATION: Movie additions peaked and declined",
    fontsize=11, fontweight="bold", color="#E65100")
axes[1].set_ylabel("Titles Added")

# Slide 3: Resolution (genre growth)
genres = nf["listed_in"].str.split(",").explode().str.strip()
g17 = nf.query("year_added == 2017")["listed_in"].str.split(",").explode().str.strip().value_counts()
g21 = nf.query("year_added == 2021")["listed_in"].str.split(",").explode().str.strip().value_counts()
growth = ((g21 - g17) / g17.clip(lower=1) * 100).dropna().sort_values().tail(5)
axes[2].barh(growth.index, growth.values, color="#2E7D32", height=0.5)
for i, (genre, val) in enumerate(growth.items()):
    axes[2].text(val + 2, i, f"+{val:.0f}%", va="center", fontsize=8,
        fontweight="bold", color="#2E7D32")
axes[2].set_title("3. RESOLUTION: International & niche genres are the growth engines",
    fontsize=11, fontweight="bold", color="#7B1FA2")
axes[2].set_xlabel("Growth % (2017 → 2021)")

for ax in axes:
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.suptitle("Three-Slide Story Arc: Context → Complication → Resolution",
    fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("output/story_arc_3slides.png", dpi=300); plt.close()

# ── 5. TITLE COMPARISON ─────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4.5))
for ax, title, subtitle in [
    (ax1, "Descriptive: 'Netflix Additions by Type'",
     "(What the chart shows — not what it means)"),
    (ax2, "Declarative: 'Movies peaked 2019; TV grew steadily'",
     "(The title IS the finding — the chart is the evidence)")]:
    for t, c in [("Movie", "#1565C0"), ("TV Show", "#E53935")]:
        sub = yearly.query("type == @t")
        ax.plot(sub.year_added, sub.n, "-o", color=c, lw=1.2, markersize=4, label=t)
    ax.legend(fontsize=6); ax.set_title(f"{title}\n{subtitle}",
        fontsize=9, fontweight="bold")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.suptitle("Chart Titles: Descriptive vs Declarative", fontweight="bold")
plt.tight_layout()
plt.savefig("output/title_comparison.png", dpi=300); plt.close()

print("\nAll W07-M01 Python outputs saved")
print("Figures: exp_vs_expl, big_idea, story_arc_3slides, title_comparison")
