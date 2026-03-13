"""
============================================================
Workshop 1 — Module 7: Critique & Redesign Workshop
Python Demonstration Script
Data Visualization for Data Scientists — UNYT Tirana
============================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import os

os.makedirs("output", exist_ok=True)
plt.rcParams.update({"figure.dpi": 150, "font.size": 11, "axes.titleweight": "bold"})


# ── REDESIGN 1: Pie → Horizontal Bar ─────────────────────
depts = ["HR", "Legal", "R&D", "Support", "Sales", "Marketing", "Engineering"]
pcts = [6, 4, 10, 12, 18, 22, 28]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

# BEFORE: pie
ax1.pie(pcts, labels=depts, autopct="%1.0f%%", shadow=True,
        colors=["#FF6B6B","#4ECDC4","#FFE66D","#A8E6CF","#DDA0DD","#87CEEB","#F0E68C"],
        explode=[0.05]*7, textprops={"fontsize": 7})
ax1.set_title("BEFORE: Pie", fontsize=9, fontweight="bold", color="#C62828")

# AFTER: sorted horizontal bar
idx = np.argsort(pcts)
s_d = [depts[i] for i in idx]
s_p = [pcts[i] for i in idx]
colors = ["#1565C0"] * 7; colors[-1] = "#E53935"
ax2.barh(s_d, s_p, color=colors, height=0.55, edgecolor="none")
for i, v in enumerate(s_p):
    ax2.text(v + 0.3, i, f"{v}%", va="center", fontsize=9,
             fontweight="bold", color="#E53935" if i == 6 else "#333")
ax2.set_title("AFTER: Sorted Bar", fontsize=9, fontweight="bold", color="#1565C0")
for sp in ["top", "right", "left"]:
    ax2.spines[sp].set_visible(False)
ax2.set_xticks([]); ax2.tick_params(left=False, labelsize=8)

fig.suptitle("Redesign 1: Pie → Horizontal Bar", fontsize=12, fontweight="bold")
plt.tight_layout()
plt.savefig("output/redesign1_pie_to_bar_py.png", dpi=300, bbox_inches="tight")
plt.close()


# ── REDESIGN 2: Dual Axis → Indexed Lines ─────────────────
np.random.seed(11)
months = np.arange(1, 13)
revenue = np.cumsum(np.random.normal(5, 8, 12)) + 200
users = np.cumsum(np.random.normal(50, 80, 12)) + 1000

# Index to 100
rev_idx = revenue / revenue[0] * 100
usr_idx = users / users[0] * 100

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.plot(months, rev_idx, color="#1565C0", linewidth=2)
ax.plot(months, usr_idx, color="#E53935", linewidth=2)
ax.axhline(y=100, color="#888", linewidth=0.8, linestyle="--")
ax.text(12.3, rev_idx[-1], "Revenue", fontsize=8, fontweight="bold",
        color="#1565C0", va="center")
ax.text(12.3, usr_idx[-1], "Users", fontsize=8, fontweight="bold",
        color="#E53935", va="center")
ax.set_xlim(1, 14)
ax.set_ylabel("Index (Month 1 = 100)", fontsize=9)
ax.set_xlabel("Month", fontsize=9)
ax.set_title("Redesign 2: Indexed Lines (common scale)", fontsize=10, fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig("output/redesign2_indexed_py.png", dpi=300, bbox_inches="tight")
plt.close()


# ── REDESIGN 3: Spaghetti → Small Multiples ──────────────
np.random.seed(33)
regions = ["North", "South", "East", "West", "Central", "Coastal"]

fig, axes = plt.subplots(2, 3, figsize=(10, 5), sharey=True)
y_all = []
data = {}
for r in regions:
    d = np.cumsum(np.random.normal(2, 6, 12)) + np.random.uniform(30, 80)
    data[r] = d
    y_all.extend(d)

y_min, y_max = min(y_all) - 5, max(y_all) + 5

for ax, (r, d) in zip(axes.flatten(), data.items()):
    ax.plot(months, d, color="#1565C0", linewidth=1.2)
    ax.fill_between(months, d, alpha=0.06, color="#1565C0")
    ax.set_title(r, fontsize=9, fontweight="bold")
    ax.set_ylim(y_min, y_max)
    ax.set_xticks([1, 6, 12])
    ax.set_xticklabels(["Jan", "Jun", "Dec"], fontsize=6)
    ax.tick_params(labelsize=6)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

fig.suptitle("Redesign 3: Small Multiples (shared y-scale)", fontsize=11, fontweight="bold")
plt.tight_layout()
plt.savefig("output/redesign3_facets_py.png", dpi=300, bbox_inches="tight")
plt.close()


# ── REDESIGN 4: Rainbow → Grey + Accent ──────────────────
np.random.seed(55)
n = 120
x = np.random.uniform(10, 100, n)
y = 0.4 * x + np.random.normal(0, 12, n)
cats = np.random.choice(["A","B","C","D","E"], n)

fig, ax = plt.subplots(figsize=(7, 5))
mask_d = cats == "D"

# Background (grey)
ax.scatter(x[~mask_d], y[~mask_d], c="#CCCCCC", s=18, alpha=0.3, edgecolors="none")

# Focal (red accent)
ax.scatter(x[mask_d], y[mask_d], c="#E53935", s=50, alpha=0.85,
           edgecolors="white", linewidth=0.5, zorder=5)

# Regression for D only
m, b = np.polyfit(x[mask_d], y[mask_d], 1)
xs_line = np.linspace(10, 100, 50)
ax.plot(xs_line, m * xs_line + b, color="#E53935", linewidth=1.2,
        linestyle="--", alpha=0.7)

ax.set_title("Redesign 4: Grey + Accent (Category D)", fontsize=10, fontweight="bold")
ax.set_xlabel("Spend ($K)", fontsize=9)
ax.set_ylabel("ROI (%)", fontsize=9)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig("output/redesign4_grey_accent_py.png", dpi=300, bbox_inches="tight")
plt.close()


# ── REDESIGN 5: Truncated → Zero Baseline ─────────────────
years = ["2020", "2021", "2022", "2023", "2024"]
scores = [96.2, 97.1, 97.8, 98.3, 99.0]

fig, ax = plt.subplots(figsize=(6, 4.5))
ax.bar(years, scores, color="#1565C0", width=0.5, edgecolor="none")
ax.set_ylim(0, 110)
for i, v in enumerate(scores):
    ax.text(i, v + 1.5, f"{v}", ha="center", fontsize=9, fontweight="bold", color="#333")
ax.axhline(y=scores[0], color="#888", linewidth=0.8, linestyle="--")
ax.text(4.4, scores[0], f"Baseline: {scores[0]}", fontsize=7, va="center", color="#888")
ax.set_title("Redesign 5: Zero Baseline + Reference Line", fontsize=10, fontweight="bold")
ax.set_ylabel("Score", fontsize=9)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig("output/redesign5_honest_py.png", dpi=300, bbox_inches="tight")
plt.close()


print("── All M07 plots saved to output/ ──")
