"""
============================================================
Workshop 1 — Module 2: Tufte's Principles
Python Demonstration Script
Data Visualization for Data Scientists — UNYT Tirana
============================================================
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs("output", exist_ok=True)
plt.rcParams["figure.dpi"] = 150


# ── 1. Data-Ink Ratio: Progressive Erasure ──────────────────
cats = ["Compact", "Midsize", "SUV", "Pickup", "Minivan", "Subcompact", "2seater"]
vals = [47, 41, 62, 33, 11, 35, 5]

fig, axes = plt.subplots(1, 4, figsize=(16, 4))

# V1: Default matplotlib (heavy styling)
ax = axes[0]
ax.bar(cats, vals, color="steelblue", edgecolor="black", linewidth=1)
ax.set_facecolor("#EEEEEE")
ax.grid(True, linewidth=0.8, color="white")
ax.set_title("V1: Default", fontsize=9, fontweight="bold")
ax.tick_params(labelsize=6)
ax.set_xticklabels(cats, rotation=50, ha="right")

# V2: Remove background and border
ax = axes[1]
ax.bar(cats, vals, color="steelblue", edgecolor="none")
ax.grid(axis="y", linewidth=0.3, color="#DDDDDD")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.set_title("V2: No Fill/Border", fontsize=9, fontweight="bold")
ax.tick_params(labelsize=6)
ax.set_xticklabels(cats, rotation=50, ha="right")

# V3: Horizontal, no grid
ax = axes[2]
sorted_idx = np.argsort(vals)
s_cats = [cats[i] for i in sorted_idx]
s_vals = [vals[i] for i in sorted_idx]
ax.barh(s_cats, s_vals, color="steelblue", height=0.6, edgecolor="none")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.set_title("V3: Horizontal, No Grid", fontsize=9, fontweight="bold")
ax.tick_params(labelsize=7)

# V4: Tufte style
ax = axes[3]
ax.barh(s_cats, s_vals, color="#1565C0", height=0.5, edgecolor="none")
for i, v in enumerate(s_vals):
    ax.text(v + 0.8, i, str(v), va="center", fontsize=8, color="#333")
for sp in ["top", "right", "left", "bottom"]:
    ax.spines[sp].set_visible(False)
ax.set_xticks([])
ax.tick_params(left=False, labelsize=7)
ax.set_title("V4: Tufte Style", fontsize=9, fontweight="bold")

fig.suptitle("Data-Ink Ratio: Progressive Erasure (Python)",
             fontsize=12, fontweight="bold")
plt.tight_layout()
plt.savefig("output/data_ink_erasure_py.png", dpi=150, bbox_inches="tight")
plt.close()


# ── 2. Chartjunk: Pie vs Clean Bar ─────────────────────────
labels = ["Product A", "Product B", "Product C", "Product D"]
sizes = [35, 30, 20, 15]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# Pie chart (demonstration of what to avoid)
ax1.pie(sizes, labels=labels, autopct="%1.0f%%", shadow=True,
        colors=["#FF6B6B", "#4ECDC4", "#FFE66D", "#DDA0DD"],
        explode=(0.05, 0, 0, 0), textprops={"fontsize": 8})
ax1.set_title("Pie Chart\n(hard to compare slices)", fontsize=9,
              fontweight="bold", color="#C62828")

# Clean bar
idx = np.argsort(sizes)
s_labels = [labels[i] for i in idx]
s_sizes = [sizes[i] for i in idx]
ax2.barh(s_labels, s_sizes, color="#1565C0", height=0.55)
for i, v in enumerate(s_sizes):
    ax2.text(v + 0.5, i, f"{v}%", va="center", fontsize=9)
ax2.set_xlabel("Market Share (%)", fontsize=9)
ax2.set_title("Horizontal Bar\n(easy to compare lengths)", fontsize=9,
              fontweight="bold", color="#1565C0")
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.grid(axis="x", alpha=0.15)
ax2.tick_params(labelsize=8)

fig.suptitle("Chartjunk Removal: Pie → Bar", fontsize=12, fontweight="bold")
plt.tight_layout()
plt.savefig("output/chartjunk_removal_py.png", dpi=150, bbox_inches="tight")
plt.close()


# ── 3. Lie Factor: Truncated vs Full Axis ───────────────────
quarters = ["Q1", "Q2", "Q3", "Q4"]
revenue = [982, 995, 1003, 1010]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# Truncated axis (misleading)
ax1.bar(quarters, revenue, color="#E53935", width=0.5, edgecolor="white")
ax1.set_ylim(975, 1015)
ax1.set_title("Truncated Axis\n\"Revenue soaring!\"",
              fontsize=9, fontweight="bold", color="#C62828")
ax1.set_ylabel("Revenue ($M)", fontsize=8)
ax1.tick_params(labelsize=7)

# Full axis (honest)
ax2.bar(quarters, revenue, color="#1565C0", width=0.5, edgecolor="white")
ax2.set_ylim(0, 1200)
for i, v in enumerate(revenue):
    ax2.text(i, v + 20, f"${v}M", ha="center", fontsize=7)
ax2.set_title("Full Axis\n\"Revenue stable\"",
              fontsize=9, fontweight="bold", color="#1565C0")
ax2.set_ylabel("Revenue ($M)", fontsize=8)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.tick_params(labelsize=7)

fig.suptitle("Lie Factor: Baseline Matters", fontsize=12, fontweight="bold")
plt.tight_layout()
plt.savefig("output/lie_factor_demo_py.png", dpi=150, bbox_inches="tight")
plt.close()


# ── 4. Small Multiples ─────────────────────────────────────
np.random.seed(7)
regions = ["North", "South", "East", "West", "Central", "Coastal"]
months = np.arange(1, 13)

fig, axes = plt.subplots(2, 3, figsize=(10, 5), sharey=True)

for ax, region in zip(axes.flatten(), regions):
    base = np.random.uniform(50, 120)
    trend = np.cumsum(np.random.normal(2, 8, 12)) + base

    ax.plot(months, trend, color="#1565C0", linewidth=1.5)
    ax.fill_between(months, trend, alpha=0.08, color="#1565C0")
    ax.set_title(region, fontsize=9, fontweight="bold")
    ax.set_xticks([1, 6, 12])
    ax.set_xticklabels(["Jan", "Jun", "Dec"], fontsize=6)
    ax.tick_params(labelsize=6)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.15)

fig.suptitle("Small Multiples: Same Scale, Easy Comparison (Python)",
             fontsize=11, fontweight="bold")
plt.tight_layout()
plt.savefig("output/small_multiples_py.png", dpi=150, bbox_inches="tight")
plt.close()


# ── 5. Sparklines ──────────────────────────────────────────
np.random.seed(12)
metrics = ["Revenue", "Users", "Retention", "NPS Score"]

fig, axes = plt.subplots(4, 1, figsize=(5, 4))

for ax, metric in zip(axes, metrics):
    data = np.cumsum(np.random.normal(0.5, 3, 52))
    ax.plot(data, color="#1565C0", linewidth=1.0)
    ax.fill_between(range(len(data)), data, alpha=0.04, color="#1565C0")

    # Mark min (red), max (green), endpoint (blue)
    ax.plot(np.argmin(data), data.min(), "o", color="#E53935", markersize=4)
    ax.plot(np.argmax(data), data.max(), "o", color="#2E7D32", markersize=4)
    ax.plot(len(data) - 1, data[-1], "o", color="#1565C0", markersize=3)

    # Remove ALL non-data elements
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)

    ax.set_ylabel(metric, fontsize=8, rotation=0, labelpad=55, va="center")

fig.suptitle("Sparklines: Word-Sized Graphics (Tufte, 2006)",
             fontsize=10, fontweight="bold")
plt.tight_layout()
plt.savefig("output/sparklines_py.png", dpi=150, bbox_inches="tight")
plt.close()


print("── All M02 plots saved to output/ ──")
