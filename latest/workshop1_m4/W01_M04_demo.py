"""
============================================================
Workshop 1 — Module 4: Color Theory & Accessibility
Python Demonstration Script
Data Visualization for Data Scientists — UNYT Tirana
============================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os

os.makedirs("output", exist_ok=True)
plt.rcParams["figure.dpi"] = 150
np.random.seed(42)


# ── 1. Sequential Palette: Heatmap ─────────────────────────
data = np.random.uniform(10, 90, (6, 8))
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
weeks = [f"W{i}" for i in range(1, 9)]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))

# Viridis (recommended)
im1 = ax1.imshow(data, cmap="viridis", aspect="auto")
ax1.set_xticks(range(8)); ax1.set_xticklabels(weeks, fontsize=7)
ax1.set_yticks(range(6)); ax1.set_yticklabels(days, fontsize=7)
plt.colorbar(im1, ax=ax1, shrink=0.8)
ax1.set_title("viridis (perceptually uniform)", fontsize=9, fontweight="bold")

# YlGnBu (ColorBrewer sequential)
im2 = ax2.imshow(data, cmap="YlGnBu", aspect="auto")
ax2.set_xticks(range(8)); ax2.set_xticklabels(weeks, fontsize=7)
ax2.set_yticks(range(6)); ax2.set_yticklabels(days, fontsize=7)
plt.colorbar(im2, ax=ax2, shrink=0.8)
ax2.set_title("YlGnBu (ColorBrewer)", fontsize=9, fontweight="bold")

fig.suptitle("Sequential Palettes for Quantitative Data", fontsize=11, fontweight="bold")
plt.tight_layout()
plt.savefig("output/heatmap_sequential_py.png", dpi=150, bbox_inches="tight")
plt.close()


# ── 2. Diverging Palette ──────────────────────────────────
np.random.seed(44)
x = np.random.uniform(0, 10, 80)
y = np.random.uniform(0, 8, 80)
z = np.random.uniform(-1, 1, 80)

fig, ax = plt.subplots(figsize=(7, 5))
sc = ax.scatter(x, y, c=z, cmap="RdBu_r", s=60, vmin=-1, vmax=1,
                edgecolors="white", linewidth=0.5)
plt.colorbar(sc, ax=ax, label="Deviation from Mean")
ax.set_title("Diverging Palette: RdBu (centred on zero)", fontsize=10, fontweight="bold")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig("output/diverging_rdbu_py.png", dpi=150, bbox_inches="tight")
plt.close()


# ── 3. Rainbow vs Viridis ─────────────────────────────────
np.random.seed(7)
x = np.random.uniform(0, 10, 200)
y = np.random.uniform(0, 10, 200)
z = np.sin(x) * np.cos(y) + np.random.normal(0, 0.3, 200)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

ax1.scatter(x, y, c=z, cmap="rainbow", s=20, edgecolors="none")
ax1.set_title("Rainbow (BAD)\nFalse contours, CVD-hostile",
              fontsize=9, fontweight="bold", color="#C62828")

ax2.scatter(x, y, c=z, cmap="viridis", s=20, edgecolors="none")
ax2.set_title("Viridis (GOOD)\nPerceptually uniform, CVD-safe",
              fontsize=9, fontweight="bold", color="#1565C0")

fig.suptitle("Never Use Rainbow", fontsize=12, fontweight="bold")
plt.tight_layout()
plt.savefig("output/rainbow_vs_viridis_py.png", dpi=150, bbox_inches="tight")
plt.close()


# ── 4. CVD-Safe Alternative: cividis ──────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

ax1.scatter(x, y, c=z, cmap="viridis", s=20, edgecolors="none")
ax1.set_title("viridis", fontsize=9, fontweight="bold")

ax2.scatter(x, y, c=z, cmap="cividis", s=20, edgecolors="none")
ax2.set_title("cividis (optimised for CVD)", fontsize=9, fontweight="bold")

fig.suptitle("CVD-Safe Alternatives", fontsize=11, fontweight="bold")
plt.tight_layout()
plt.savefig("output/cividis_py.png", dpi=150, bbox_inches="tight")
plt.close()


# ── 5. Grey + Accent Strategy ─────────────────────────────
np.random.seed(55)
n = 100
xs = np.random.uniform(10, 100, n)
ys = 0.4 * xs + np.random.normal(0, 12, n)
cats = np.random.choice(["A", "B", "C", "D"], n)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# All coloured (confusing)
palette = {"A": "#1f77b4", "B": "#ff7f0e", "C": "#2ca02c", "D": "#d62728"}
for c in ["A", "B", "C", "D"]:
    mask = cats == c
    ax1.scatter(xs[mask], ys[mask], c=palette[c], s=30, alpha=0.6, label=c)
ax1.legend(fontsize=7, title="Cat")
ax1.set_title("All Coloured (cluttered)", fontsize=9, fontweight="bold", color="#C62828")
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

# Grey + accent
mask_hl = cats == "D"
ax2.scatter(xs[~mask_hl], ys[~mask_hl], c="#BBBBBB", s=20, alpha=0.3, label="Other")
ax2.scatter(xs[mask_hl], ys[mask_hl], c="#E53935", s=50, alpha=0.9,
            edgecolors="white", linewidth=0.5, zorder=5, label="Category D")
ax2.legend(fontsize=7)
ax2.set_title("Grey + Accent (focused)", fontsize=9, fontweight="bold", color="#1565C0")
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)

fig.suptitle("Strategic Colour: Grey + Accent", fontsize=12, fontweight="bold")
plt.tight_layout()
plt.savefig("output/grey_accent_py.png", dpi=150, bbox_inches="tight")
plt.close()


# ── 6. Qualitative Palettes Compared ─────────────────────
cats_list = ["Cat A", "Cat B", "Cat C", "Cat D", "Cat E"]
vals = [34, 45, 28, 52, 38]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# Saturated rainbow (bad)
rainbow = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF"]
ax1.bar(cats_list, vals, color=rainbow, edgecolor="black", linewidth=1)
ax1.set_title("Saturated Rainbow (BAD)", fontsize=9, fontweight="bold", color="#C62828")
ax1.set_facecolor("#F5F5F5")

# Muted Tableau 10 (good)
muted = ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f"]
ax2.bar(cats_list, vals, color=muted, edgecolor="white", linewidth=1)
ax2.set_title("Tableau 10 Muted (GOOD)", fontsize=9, fontweight="bold", color="#1565C0")
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)

fig.suptitle("Qualitative Palettes: Muted > Saturated", fontsize=11, fontweight="bold")
plt.tight_layout()
plt.savefig("output/qualitative_comparison_py.png", dpi=150, bbox_inches="tight")
plt.close()


print("── All M04 plots saved to output/ ──")
