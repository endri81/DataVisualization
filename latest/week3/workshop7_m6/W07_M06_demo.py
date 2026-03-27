"""W07-M06: Declutter & Redesign — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
os.makedirs("output", exist_ok=True)

nf = pd.read_csv("netflix.csv")
nf["date_added"] = pd.to_datetime(nf["date_added"].str.strip(), errors="coerce")
nf["year_added"] = nf["date_added"].dt.year
yearly = nf.query("2016<=year_added<=2021").groupby(["year_added","type"]).size().reset_index(name="n")
movies = yearly.query("type=='Movie'"); tvshows = yearly.query("type=='TV Show'")
peak_n = movies.n.max(); latest_n = movies.iloc[-1]["n"]
decline = round((1 - latest_n / peak_n) * 100)

# ═══════════════════════════════════════════════════════
# 1. BEFORE: Maximum clutter (deliberately bad)
# ═══════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(9, 6))
x = np.arange(2016, 2022); w = 0.3
bars1 = ax.bar(x-w/2, movies.n.values, w, color="#4472C4", edgecolor="black", lw=0.5, label="Movie")
bars2 = ax.bar(x+w/2, tvshows.n.values, w, color="#ED7D31", edgecolor="black", lw=0.5, label="TV Show")
# Labels on every bar
for b in list(bars1) + list(bars2):
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+10, f"{b.get_height():.0f}",
        ha="center", fontsize=5, rotation=90)
ax.legend(frameon=True, fancybox=True, shadow=True, fontsize=7)
ax.set_facecolor("#F8F8F8"); ax.grid(True, color="#CCC", lw=0.5)
for spine in ax.spines.values(): spine.set_linewidth(2); spine.set_color("black")
ax.set_title("Netflix Additions by Type (2016-2021)", fontsize=12, fontweight="bold")
ax.set_xlabel("Year of Addition"); ax.set_ylabel("Number of Titles Added to Platform")
ax.tick_params(labelsize=8, rotation=45)
plt.tight_layout(); plt.savefig("output/before_cluttered.png", dpi=300); plt.close()

# ═══════════════════════════════════════════════════════
# 2. AFTER: Decluttered (same data)
# ═══════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(tvshows.year_added, tvshows.n, "-o", color="#DDDDDD", lw=0.8, markersize=3)
ax.plot(movies.year_added, movies.n, "-o", color="#1565C0", lw=2.5, markersize=6)
ax.text(2021.15, latest_n, " Movies", fontsize=9, fontweight="bold", color="#1565C0", va="center")
ax.text(2021.15, tvshows.iloc[-1]["n"], " TV Shows", fontsize=8, color="#BBB", va="center")
ax.annotate(f"–{decline}%\nfrom peak", xy=(2019.5, (peak_n+latest_n)/2),
    fontsize=10, fontweight="bold", color="#E53935", ha="center",
    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#E53935", alpha=0.9))
ax.set_xlim(2015.5, 2022.5)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#EEE"); ax.spines["bottom"].set_color("#EEE")
ax.tick_params(colors="#888", labelsize=9)
ax.set_ylabel("Titles Added", color="#888")
ax.set_title(f"Movie additions declined {decline}% from their 2019 peak",
    fontsize=13, fontweight="bold")
plt.tight_layout(); plt.savefig("output/after_clean.png", dpi=300); plt.close()

# ═══════════════════════════════════════════════════════
# 3. SIDE-BY-SIDE
# ═══════════════════════════════════════════════════════
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6))

# Before
x_arr = np.arange(2016, 2022); w = 0.3
ax1.bar(x_arr-w/2, movies.n.values, w, color="#4472C4", edgecolor="black", lw=0.5, label="Movie")
ax1.bar(x_arr+w/2, tvshows.n.values, w, color="#ED7D31", edgecolor="black", lw=0.5, label="TV Show")
ax1.legend(frameon=True, shadow=True, fontsize=7)
ax1.set_facecolor("#F8F8F8"); ax1.grid(True, color="#CCC", lw=0.5)
for s in ax1.spines.values(): s.set_linewidth(2); s.set_color("black")
ax1.set_title("BEFORE: 12 clutter elements", fontsize=11, fontweight="bold", color="#C62828")
ax1.set_xlabel("Year"); ax1.set_ylabel("Titles")

# After
ax2.plot(tvshows.year_added, tvshows.n, "-o", color="#DDD", lw=0.8, markersize=3)
ax2.plot(movies.year_added, movies.n, "-o", color="#1565C0", lw=2.5, markersize=6)
ax2.text(2021.15, latest_n, " Movies", fontsize=9, fontweight="bold", color="#1565C0", va="center")
ax2.text(2021.15, tvshows.iloc[-1]["n"], " TV Shows", fontsize=8, color="#BBB", va="center")
ax2.annotate(f"–{decline}%", xy=(2019.5, (peak_n+latest_n)/2),
    fontsize=11, fontweight="bold", color="#E53935",
    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#E53935"))
ax2.set_xlim(2015.5, 2022.5)
ax2.spines["top"].set_visible(False); ax2.spines["right"].set_visible(False)
ax2.spines["left"].set_color("#EEE"); ax2.spines["bottom"].set_color("#EEE")
ax2.tick_params(colors="#888"); ax2.set_ylabel("Titles Added", color="#888")
ax2.set_title("AFTER: Decluttered", fontsize=11, fontweight="bold", color="#1565C0")

fig.suptitle("Chart Makeover: Same Data, Radically Different Clarity", fontsize=14, fontweight="bold")
plt.tight_layout(); plt.savefig("output/before_after.png", dpi=300); plt.close()

# ═══════════════════════════════════════════════════════
# 4. CLEAN rcParams TEMPLATE
# ═══════════════════════════════════════════════════════
clean_params = {
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#EEEEEE",
    "axes.labelcolor": "#888888",
    "xtick.color": "#888888",
    "ytick.color": "#888888",
    "grid.alpha": 0,
    "font.size": 10,
    "axes.titleweight": "bold",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
}
plt.rcParams.update(clean_params)

# Demo with clean defaults
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(movies.year_added, movies.n, "-o", color="#1565C0", lw=2, markersize=5)
ax.set_title("With rcParams: every plot starts clean")
ax.set_ylabel("Movies Added")
plt.tight_layout(); plt.savefig("output/rcparams_demo.png", dpi=300); plt.close()

# ═══════════════════════════════════════════════════════
# 5. INCREMENTAL DECLUTTER: 4 stages
# ═══════════════════════════════════════════════════════
plt.rcParams.update(plt.rcParamsDefault)  # reset for the "before" stage

fig, axes = plt.subplots(2, 2, figsize=(16, 10))

# Stage 0: original clutter
ax = axes[0,0]
ax.bar(x_arr-w/2, movies.n.values, w, color="#4472C4", edgecolor="black", lw=0.5, label="Movie")
ax.bar(x_arr+w/2, tvshows.n.values, w, color="#ED7D31", edgecolor="black", lw=0.5, label="TV Show")
ax.legend(fontsize=6, frameon=True, shadow=True); ax.grid(True, color="#CCC")
ax.set_facecolor("#F8F8F8"); ax.set_title("Stage 0: Maximum clutter", fontsize=10, fontweight="bold")

# Stage 1: remove borders, background, shadows
ax = axes[0,1]
ax.bar(x_arr-w/2, movies.n.values, w, color="#1565C0", label="Movie")
ax.bar(x_arr+w/2, tvshows.n.values, w, color="#E53935", label="TV Show")
ax.legend(fontsize=6); ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.set_title("Stage 1: Remove borders, background", fontsize=10, fontweight="bold")

# Stage 2: switch to line, remove gridlines
ax = axes[1,0]
ax.plot(movies.year_added, movies.n, "-o", color="#1565C0", lw=1.5, label="Movie")
ax.plot(tvshows.year_added, tvshows.n, "-o", color="#E53935", lw=1.5, label="TV Show")
ax.legend(fontsize=6); ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.set_title("Stage 2: Line chart, remove grid", fontsize=10, fontweight="bold")

# Stage 3: grey+accent, direct labels, callout
ax = axes[1,1]
ax.plot(tvshows.year_added, tvshows.n, "-o", color="#DDD", lw=0.8, markersize=3)
ax.plot(movies.year_added, movies.n, "-o", color="#1565C0", lw=2.5, markersize=6)
ax.text(2021.1, latest_n, " Movies", fontsize=8, fontweight="bold", color="#1565C0", va="center")
ax.text(2021.1, tvshows.iloc[-1]["n"], " TV", fontsize=7, color="#BBB", va="center")
ax.annotate(f"–{decline}%", xy=(2019.5,(peak_n+latest_n)/2),
    fontsize=10, fontweight="bold", color="#E53935",
    bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="#E53935"))
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#EEE"); ax.spines["bottom"].set_color("#EEE")
ax.set_xlim(2015.5, 2022); ax.set_title("Stage 3: Grey+accent, labels, callout", fontsize=10, fontweight="bold")

fig.suptitle("Incremental Declutter: 4 Stages", fontsize=14, fontweight="bold")
plt.tight_layout(); plt.savefig("output/incremental_declutter.png", dpi=300); plt.close()

# ═══════════════════════════════════════════════════════
# 6. 12-STEP CHECKLIST (printed)
# ═══════════════════════════════════════════════════════
print("\n=== 12-Step Declutter Transformation ===")
steps = [
    ("Chart type",   "Grouped bar → Line (continuous data)"),
    ("Title",        "Descriptive → Declarative (= finding)"),
    ("Legend",       "Box with border → Direct labels (no legend)"),
    ("Borders",      "Heavy black → Removed entirely"),
    ("Gridlines",    "Both axes, grey → Removed entirely"),
    ("Data labels",  "On every bar → Only the callout %"),
    ("Background",   "Grey fill → White"),
    ("Axis labels",  "Verbose → Minimal, muted colour"),
    ("Colour",       "Two bright → Grey + one accent"),
    ("Bar edges",    "Black outlines → None (line chart)"),
    ("Source line",  "Long, distracting → Removed"),
    ("Spines",       "All 4, thick → Left+bottom, light #EEE"),
]
for i, (element, change) in enumerate(steps, 1):
    print(f"  {i:2d}. {element:<15} {change}")

print("\nAll W07-M06 Python outputs saved")
