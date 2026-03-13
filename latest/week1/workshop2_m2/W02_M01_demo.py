"""
============================================================
Workshop 2 — Module 1: Wilkinson's Grammar of Graphics
Python Demonstration Script
Data Visualization for Data Scientists — UNYT Tirana
============================================================

NOTE: This script demonstrates grammar concepts using both
matplotlib (OO API) and plotnine (ggplot2 port). Install plotnine:
    pip install plotnine
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import os

os.makedirs("output", exist_ok=True)
plt.rcParams.update({"figure.dpi": 150, "font.size": 10, "axes.titleweight": "bold"})


# ── 1. SAME DATA, THREE GEOMETRIES ────────────────────────
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
sales = [23, 45, 31, 58, 40, 52, 35]

fig, axes = plt.subplots(1, 3, figsize=(12, 4))

# geom_col equivalent
axes[0].bar(days, sales, color="#1565C0", width=0.55, edgecolor="none")
axes[0].set_title("geom_col()\n(bars)", fontsize=10, fontweight="bold", color="#1565C0")
axes[0].spines["top"].set_visible(False); axes[0].spines["right"].set_visible(False)

# geom_line equivalent
axes[1].plot(days, sales, "o-", color="#2E7D32", linewidth=2, markersize=6)
axes[1].set_title("geom_line()\n(connected points)", fontsize=10, fontweight="bold", color="#2E7D32")
axes[1].spines["top"].set_visible(False); axes[1].spines["right"].set_visible(False)

# geom_point equivalent
axes[2].scatter(days, sales, s=80, c="#E53935", edgecolors="white", linewidth=0.5, zorder=5)
axes[2].set_title("geom_point()\n(dot plot)", fontsize=10, fontweight="bold", color="#E53935")
axes[2].spines["top"].set_visible(False); axes[2].spines["right"].set_visible(False)

for ax in axes:
    ax.tick_params(labelsize=7)

fig.suptitle("Same Data + Same Mapping, Different Geometry\naes(x=day, y=sales)",
             fontsize=12, fontweight="bold")
plt.tight_layout()
plt.savefig("output/three_geoms_py.png", dpi=300, bbox_inches="tight")
plt.close()


# ── 2. LAYERED CONSTRUCTION — 4 stages ───────────────────
np.random.seed(22)
x = np.random.uniform(1, 6, 80)
y = 0.5 * x + np.random.normal(0, 0.8, 80)

fig, axes = plt.subplots(2, 2, figsize=(10, 7))

# Stage 1: data + axes only
axes[0,0].set_xlim(0, 7); axes[0,0].set_ylim(-1, 5)
axes[0,0].set_xlabel("x"); axes[0,0].set_ylabel("y")
axes[0,0].set_title("1. Data + Axes", fontsize=9)

# Stage 2: + scatter
axes[0,1].scatter(x, y, s=18, c="black", alpha=0.4)
axes[0,1].set_title("2. + scatter()", fontsize=9)

# Stage 3: + regression
axes[1,0].scatter(x, y, s=18, c="black", alpha=0.4)
m, b = np.polyfit(x, y, 1)
xs = np.linspace(1, 6, 50)
axes[1,0].plot(xs, m*xs+b, color="#E53935", linewidth=2)
axes[1,0].fill_between(xs, m*xs+b-0.8, m*xs+b+0.8, alpha=0.1, color="#E53935")
axes[1,0].set_title("3. + regression line + CI", fontsize=9)

# Stage 4: + colour + theme
cats = np.random.choice(["A","B","C"], 80)
palette = {"A":"#1565C0", "B":"#E53935", "C":"#2E7D32"}
for c in ["A","B","C"]:
    mask = cats == c
    axes[1,1].scatter(x[mask], y[mask], s=25, c=palette[c], alpha=0.6,
                      edgecolors="white", linewidth=0.3, label=c)
axes[1,1].plot(xs, m*xs+b, color="grey", linewidth=1.2, linestyle="--")
axes[1,1].legend(fontsize=7, title="Class")
axes[1,1].set_xlabel("Displacement (L)", fontsize=8)
axes[1,1].set_ylabel("Highway MPG", fontsize=8)
axes[1,1].set_title("4. + color + labels + theme", fontsize=9)
axes[1,1].spines["top"].set_visible(False); axes[1,1].spines["right"].set_visible(False)
axes[1,1].set_facecolor("#FAFAFA"); axes[1,1].grid(alpha=0.15)

for ax in axes.flatten():
    ax.tick_params(labelsize=6)

fig.suptitle("Layered Construction: Each Step Adds a Component",
             fontsize=12, fontweight="bold")
plt.tight_layout()
plt.savefig("output/layered_construction_py.png", dpi=300, bbox_inches="tight")
plt.close()


# ── 3. COLOR vs FACET — two aesthetic strategies ──────────
np.random.seed(42)
n = 150
xg = np.random.normal(0, 1, n)
yg = np.random.normal(0, 1, n)
grp = np.repeat(["A", "B", "C"], 50)

fig, (ax1, ax2_holder) = plt.subplots(1, 2, figsize=(11, 4.5))

# Strategy A: colour encodes group
palette_g = {"A": "#1565C0", "B": "#E53935", "C": "#2E7D32"}
for g, c in palette_g.items():
    mask = grp == g
    ax1.scatter(xg[mask], yg[mask], s=18, c=c, alpha=0.5, edgecolors="none", label=g)
ax1.legend(fontsize=7, title="Group")
ax1.set_title("aes(color = group)\nOne panel, colour encodes group",
              fontsize=9, fontweight="bold")
ax1.spines["top"].set_visible(False); ax1.spines["right"].set_visible(False)
ax1.tick_params(labelsize=7)

# Strategy B: facets
ax2_holder.axis("off")
ax2_holder.set_title("facet_wrap(~group)\nThree panels, proximity encodes group",
                     fontsize=9, fontweight="bold")
inner_gs = GridSpec(1, 3, left=0.55, right=0.98, bottom=0.15, top=0.78,
                    wspace=0.3, figure=fig)
for i, g in enumerate(["A", "B", "C"]):
    ax_f = fig.add_subplot(inner_gs[0, i])
    mask = grp == g
    ax_f.scatter(xg[mask], yg[mask], s=12, c="#1565C0", alpha=0.5, edgecolors="none")
    ax_f.set_title(f"Group {g}", fontsize=7, fontweight="bold")
    ax_f.tick_params(labelsize=5)
    ax_f.spines["top"].set_visible(False); ax_f.spines["right"].set_visible(False)

fig.suptitle("Same Data + Same Geom, Different Aesthetic Strategy",
             fontsize=12, fontweight="bold")
fig.savefig("output/color_vs_facet_py.png", dpi=300, bbox_inches="tight")
plt.close()


# ── 4. GROUPED BAR — grammar decomposition ───────────────
quarters = ["Q1", "Q2", "Q3", "Q4"]
products = {"Alpha": [120, 150, 180, 200],
            "Beta":  [90, 110, 130, 160],
            "Gamma": [60, 80, 100, 120]}
colors_p = {"Alpha": "#1565C0", "Beta": "#E53935", "Gamma": "#2E7D32"}

x_pos = np.arange(len(quarters))
width = 0.25

fig, ax = plt.subplots(figsize=(7, 5))
for i, (prod, vals) in enumerate(products.items()):
    ax.bar(x_pos + i * width, vals, width, label=prod, color=colors_p[prod], edgecolor="white")

ax.set_xticks(x_pos + width)
ax.set_xticklabels(quarters, fontsize=9)
ax.set_ylabel("Revenue ($K)", fontsize=9)
ax.set_title("Grouped Bar: Grammar Decomposition\n"
             "data + aes(x,y,fill) + geom_bar(position='dodge') + scale + theme",
             fontsize=10, fontweight="bold")
ax.legend(fontsize=8, title="Product")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.tick_params(labelsize=8)
plt.tight_layout()
plt.savefig("output/grouped_bar_grammar_py.png", dpi=300, bbox_inches="tight")
plt.close()


# ── 5. COORD SWAP: Bar → Pie ─────────────────────────────
segments = ["Enterprise", "SMB", "Consumer"]
shares = [45, 35, 20]
seg_colors = ["#1565C0", "#2E7D32", "#E53935"]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# Cartesian (bar)
ax1.bar(segments, shares, color=seg_colors, width=0.55, edgecolor="none")
ax1.set_ylabel("Share (%)", fontsize=9)
ax1.set_title("coord_cartesian (bar)", fontsize=10, fontweight="bold")
ax1.spines["top"].set_visible(False); ax1.spines["right"].set_visible(False)
ax1.tick_params(labelsize=8)

# Polar (pie)
ax2.pie(shares, labels=segments, colors=seg_colors, autopct="%1.0f%%",
        startangle=90, textprops={"fontsize": 9})
ax2.set_title("coord_polar (pie)", fontsize=10, fontweight="bold")

fig.suptitle("Same Data + Same Geom, Different Coordinate System",
             fontsize=12, fontweight="bold")
plt.tight_layout()
plt.savefig("output/coord_swap_py.png", dpi=300, bbox_inches="tight")
plt.close()


# ── 6. plotnine EXAMPLE (if installed) ────────────────────
try:
    from plotnine import ggplot, aes, geom_point, geom_smooth, labs, theme_minimal, scale_color_brewer

    # Using seaborn's mpg dataset as pandas DataFrame
    import seaborn as sns
    mpg = sns.load_dataset("mpg").dropna()

    p = (
        ggplot(mpg, aes(x="displacement", y="mpg", color="origin"))
        + geom_point(alpha=0.6, size=2)
        + geom_smooth(method="lm", se=True, color="grey")
        + scale_color_brewer(type="qual", palette="Set1")
        + labs(title="plotnine: Grammar of Graphics in Python",
               x="Displacement (cu in)", y="Miles per Gallon",
               color="Origin")
        + theme_minimal()
    )
    p.save("output/plotnine_demo.png", dpi=300, width=7, height=5)
    print("  ✓ plotnine demo saved")

except ImportError:
    print("  ℹ plotnine not installed — skipping plotnine demo")
    print("    Install with: pip install plotnine")


print("\n── All W02-M01 plots saved to output/ ──")
