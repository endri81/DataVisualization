"""W07-M03: Advanced Annotation in Code — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
os.makedirs("output", exist_ok=True)

# ── 1. LOAD DATA ────────────────────────────────────────
nf = pd.read_csv("netflix.csv")
nf["date_added"] = pd.to_datetime(nf["date_added"].str.strip(), errors="coerce")
nf["year_added"] = nf["date_added"].dt.year
yearly = nf.query("2015 <= year_added <= 2021").groupby(["year_added","type"]).size().reset_index(name="n")
movies = yearly.query("type == 'Movie'")
tvshows = yearly.query("type == 'TV Show'")

# ── 2. adjustText: NON-OVERLAPPING LABELS ────────────────
np.random.seed(42)
x = np.random.uniform(1, 10, 15); y = np.random.uniform(1, 10, 15)
labels = [f"Point {i+1}" for i in range(15)]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
# BAD
ax1.scatter(x, y, s=40, c="#1565C0", edgecolors="white", lw=0.5, zorder=5)
for xi, yi, lab in zip(x, y, labels):
    ax1.text(xi+0.1, yi+0.1, lab, fontsize=6)
ax1.set_title("BAD: Overlapping labels\n(ax.text without adjustment)",
    fontweight="bold", color="#C62828")
# GOOD
ax2.scatter(x, y, s=40, c="#1565C0", edgecolors="white", lw=0.5, zorder=5)
try:
    from adjustText import adjust_text
    texts = [ax2.text(xi, yi, lab, fontsize=6) for xi, yi, lab in zip(x, y, labels)]
    adjust_text(texts, ax=ax2,
        arrowprops=dict(arrowstyle="-", color="#888", lw=0.5),
        force_text=0.5, force_points=0.3)
    ax2.set_title("GOOD: adjustText — auto-repelled\n(pip install adjustText)",
        fontweight="bold", color="#1565C0")
except ImportError:
    for i, (xi, yi, lab) in enumerate(zip(x, y, labels)):
        off = 0.4 * (1 if i%2==0 else -1)
        ax2.annotate(lab, (xi,yi), xytext=(xi+off,yi+off), fontsize=6,
            arrowprops=dict(arrowstyle="-", color="#888", lw=0.3))
    ax2.set_title("FALLBACK: manual offset\n(adjustText not installed)",
        fontweight="bold", color="#E65100")
for ax in [ax1,ax2]: ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.suptitle("Label Overlap: Problem and Solution", fontweight="bold")
plt.tight_layout(); plt.savefig("output/adjusttext_demo.png", dpi=300); plt.close()

# ── 3. CALLOUT BOX WITH CURVED ARROW ────────────────────
peak = movies.loc[movies.n.idxmax()]
latest = movies.iloc[-1]
decline = round((1 - latest["n"] / peak["n"]) * 100)

fig, ax = plt.subplots(figsize=(10, 6))
# Grey context
ax.plot(tvshows.year_added, tvshows.n, "-o", color="#DDDDDD", lw=0.8, markersize=3)
# Story line
ax.plot(movies.year_added, movies.n, "-o", color="#1565C0", lw=2.5, markersize=6)
# Reference line at peak
ax.axhline(y=peak["n"], ls=":", color="#888", lw=0.5)
# Shaded decline region
ax.axvspan(2019.5, 2021.5, alpha=0.03, color="#E53935")
# Callout box with curved arrow
ax.annotate(f"–{decline}% decline\nfrom 2019 peak",
    xy=(2020.5, (peak["n"] + latest["n"]) / 2),
    xytext=(2017.5, latest["n"] * 0.75),
    fontsize=10, fontweight="bold", color="#E53935",
    bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
        edgecolor="#E53935", alpha=0.9, lw=1.5),
    arrowprops=dict(arrowstyle="->",
        connectionstyle="arc3,rad=0.3",
        color="#E53935", lw=1.5))
# Direct labels (no legend)
ax.text(2021.15, movies.iloc[-1]["n"], " Movies", fontsize=9,
    fontweight="bold", color="#1565C0", va="center")
ax.text(2021.15, tvshows.iloc[-1]["n"], " TV Shows", fontsize=8,
    color="#BBBBBB", va="center")
ax.set_xlim(2014.5, 2022.5)
ax.set_title(f"Movie additions declined {decline}% from their 2019 peak",
    fontsize=13, fontweight="bold")
ax.text(0.01, -0.08, "Source: Netflix dataset | UNYT",
    transform=ax.transAxes, fontsize=7, color="#888")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/fully_dressed.png", dpi=300); plt.close()

# ── 4. ANNOTATION LAYERS (progressive build) ────────────
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

for i, (ax, title) in enumerate(zip(axes.flatten(), [
    "Layer 0: Bare chart", "Layer 1: + Reference line",
    "Layer 2: + Direct label", "Layer 3: + Callout box"])):
    ax.plot(movies.year_added, movies.n, "-o", color="#1565C0", lw=1.5, markersize=4)
    ax.set_title(title, fontsize=9, fontweight="bold")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=6)
    if i >= 1:  # reference line
        ax.axhline(y=peak["n"], ls=":", color="#888", lw=0.5)
    if i >= 2:  # direct label
        ax.text(2021.1, latest["n"], " Movies", fontsize=7,
            fontweight="bold", color="#1565C0", va="center")
    if i >= 3:  # callout box
        ax.annotate(f"–{decline}%", xy=(2020, latest["n"]),
            xytext=(2018, latest["n"]*0.8),
            fontsize=9, fontweight="bold", color="#E53935",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                edgecolor="#E53935"),
            arrowprops=dict(arrowstyle="->", color="#E53935", lw=1))
fig.suptitle("Annotation Hierarchy: Build in Layers", fontweight="bold")
plt.tight_layout(); plt.savefig("output/annotation_layers.png", dpi=300); plt.close()

# ── 5. e-Car: FULLY ANNOTATED CRISIS CHART ──────────────
ec = pd.read_csv("ecar.csv"); ec.columns=[c.strip().replace("  "," ") for c in ec.columns]
ec["Year"] = pd.to_datetime(ec["Approve Date"], format="%m/%d/%Y", errors="coerce").dt.year
ec["Spread"] = ec["Rate"] - ec["Cost of Funds"]
yr = ec.query("2002<=Year<=2012").groupby("Year").agg(rate=("Rate","mean"),spread=("Spread","mean")).reset_index()

fig, ax = plt.subplots(figsize=(10, 5))
ax.axvspan(2007.5, 2009.5, alpha=0.04, color="#E53935")  # crisis window
ax.plot(yr.Year, yr.spread, color="#DDDDDD", lw=0.8)  # grey context
ax.plot(yr.Year, yr.rate, "-o", color="#1565C0", lw=2.5, markersize=5)
# Lehman callout
ax.annotate("Lehman collapse\n(Sep 2008)",
    xy=(2008, yr.query("Year==2008").rate.values[0]),
    xytext=(2005, yr.rate.max()*0.85),
    fontsize=9, fontweight="bold", color="#E53935",
    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#E53935", lw=1.2),
    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.2",
        color="#E53935", lw=1.5))
# Direct labels
ax.text(2012.2, yr.iloc[-1].rate, " Rate", fontsize=9, fontweight="bold",
    color="#1565C0", va="center")
ax.text(2012.2, yr.iloc[-1].spread, " Spread", fontsize=8, color="#BBB", va="center")
ax.set_xlim(2001.5, 2013.5)
ax.set_title("Loan rates dropped 2pp after the 2008 financial crisis",
    fontsize=12, fontweight="bold")
ax.text(0.01, -0.08, "Source: e-Car dataset | UNYT",
    transform=ax.transAxes, fontsize=7, color="#888")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/ecar_annotated.png", dpi=300); plt.close()

# ── 6. ARROW STYLES DEMO ────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 5))
styles = [("->", "Standard", 0.85), ("-|>", "Filled", 0.70),
    ("-[", "Bar end", 0.55), ("fancy", "Fancy", 0.40), ("wedge", "Wedge", 0.25)]
for style, label, y in styles:
    try:
        ax.annotate(f"  {label} (arrowstyle='{style}')",
            xy=(0.7, y), xytext=(0.2, y), fontsize=9, va="center",
            arrowprops=dict(arrowstyle=style, color="#1565C0", lw=1.5,
                connectionstyle="arc3,rad=0.1"))
    except:
        ax.annotate(f"  {label} ('{style}') — not supported",
            xy=(0.7, y), xytext=(0.2, y), fontsize=9, va="center",
            arrowprops=dict(arrowstyle="->", color="#888", lw=1))
ax.set_xlim(0, 1); ax.set_ylim(0.1, 0.95)
ax.set_title("Arrow Styles: ax.annotate(arrowprops=dict(arrowstyle=...))",
    fontweight="bold")
ax.axis("off")
plt.tight_layout(); plt.savefig("output/arrow_styles.png", dpi=300); plt.close()

print("\nAll W07-M03 Python outputs saved")
