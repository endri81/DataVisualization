"""
============================================================
Workshop 1 — Module 5: Typography, Layout & Composition
Python Demonstration Script
Data Visualization for Data Scientists — UNYT Tirana
============================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import os

os.makedirs("output", exist_ok=True)
np.random.seed(42)

# ── Global font settings (Tufte-friendly) ──────────────────
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 11,
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "figure.dpi": 150,
})


# ── 1. Typographic Hierarchy ──────────────────────────────
products = ["Product F", "Product E", "Product D",
            "Product C", "Product B", "Product A"]
revenue = sorted([450, 380, 520, 290, 610, 340])

fig, ax = plt.subplots(figsize=(7, 5))
ax.barh(products, revenue, color="#1565C0", height=0.5, edgecolor="none")
for i, v in enumerate(revenue):
    ax.text(v + 8, i, f"${v}K", va="center", fontsize=8, fontweight="bold", color="#333")

# Five-level hierarchy
ax.set_title("Product Revenue: Q4 2024", fontsize=16, fontweight="bold", pad=8)
fig.text(0.13, 0.92, "Annual revenue in thousands USD, sorted descending",
         fontsize=11, color="grey", ha="left")
ax.set_xlabel("Revenue ($K)", fontsize=10, labelpad=8)
fig.text(0.13, 0.02, "Source: Internal sales database | Prepared: Jan 2025",
         fontsize=8, fontstyle="italic", color="#888", ha="left")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.tick_params(left=False, labelsize=9)
ax.set_xlim(0, 720)
plt.subplots_adjust(top=0.88, bottom=0.12, left=0.18, right=0.95)
plt.savefig("output/typographic_hierarchy_py.pdf", bbox_inches="tight")
plt.savefig("output/typographic_hierarchy_py.png", dpi=300, bbox_inches="tight")
plt.close()


# ── 2. Direct Labelling vs Legend ─────────────────────────
np.random.seed(7)
months = np.arange(1, 13)
series = {
    "Alpha": np.cumsum(np.random.normal(3, 4, 12)) + 40,
    "Beta":  np.cumsum(np.random.normal(2, 3, 12)) + 30,
    "Gamma": np.cumsum(np.random.normal(1, 5, 12)) + 20,
}
colors = {"Alpha": "#1565C0", "Beta": "#E53935", "Gamma": "#2E7D32"}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))

# Version A: legend
for name, data in series.items():
    ax1.plot(months, data, color=colors[name], linewidth=2, label=name)
ax1.legend(fontsize=8, frameon=True, loc="upper left")
ax1.set_title("Version A: Legend", fontsize=10, fontweight="bold")
ax1.set_xlabel("Month"); ax1.set_ylabel("Revenue ($K)")
ax1.spines["top"].set_visible(False); ax1.spines["right"].set_visible(False)

# Version B: direct labels
for name, data in series.items():
    ax2.plot(months, data, color=colors[name], linewidth=2)
    ax2.text(12.3, data[-1], name, fontsize=8, fontweight="bold",
             color=colors[name], va="center")
ax2.set_xlim(1, 15)
ax2.set_title("Version B: Direct Labels", fontsize=10, fontweight="bold")
ax2.set_xlabel("Month"); ax2.set_ylabel("Revenue ($K)")
ax2.spines["top"].set_visible(False); ax2.spines["right"].set_visible(False)

fig.suptitle("Direct Labelling Eliminates the Legend Shuttle",
             fontsize=12, fontweight="bold")
plt.tight_layout()
plt.savefig("output/direct_vs_legend_py.png", dpi=300, bbox_inches="tight")
plt.close()


# ── 3. Multi-Panel with GridSpec ──────────────────────────
np.random.seed(55)
fig = plt.figure(figsize=(10, 6))
gs = GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.35, height_ratios=[1, 1.3])

# (a) Bar chart
ax_a = fig.add_subplot(gs[0, 0])
cats = ["A", "B", "C", "D"]
vals = [42, 58, 35, 67]
ax_a.barh(cats, vals, color="#1565C0", height=0.5)
ax_a.set_title("(a) Revenue", fontsize=9, fontweight="bold")
ax_a.spines["top"].set_visible(False); ax_a.spines["right"].set_visible(False)
ax_a.tick_params(labelsize=7)

# (b) Scatter
ax_b = fig.add_subplot(gs[0, 1])
ax_b.scatter(np.random.uniform(0, 10, 40), np.random.uniform(0, 10, 40),
             s=20, c="#E53935", alpha=0.6)
ax_b.set_title("(b) Scatter", fontsize=9, fontweight="bold")
ax_b.spines["top"].set_visible(False); ax_b.spines["right"].set_visible(False)
ax_b.tick_params(labelsize=7)

# (c) Histogram
ax_c = fig.add_subplot(gs[0, 2])
ax_c.hist(np.random.normal(50, 15, 500), bins=25, color="#2E7D32",
          edgecolor="white", linewidth=0.3)
ax_c.set_title("(c) Distribution", fontsize=9, fontweight="bold")
ax_c.spines["top"].set_visible(False); ax_c.spines["right"].set_visible(False)
ax_c.tick_params(labelsize=7)

# (d) Full-width time series
ax_d = fig.add_subplot(gs[1, :])
t = np.arange(1, 25)
trend = np.cumsum(np.random.normal(2, 5, 24)) + 100
ax_d.plot(t, trend, color="#1565C0", linewidth=2)
ax_d.fill_between(t, trend, alpha=0.06, color="#1565C0")
ax_d.set_title("(d) 24-Month Trend (full width)", fontsize=9, fontweight="bold")
ax_d.set_xlabel("Month", fontsize=8)
ax_d.spines["top"].set_visible(False); ax_d.spines["right"].set_visible(False)
ax_d.tick_params(labelsize=7)

fig.suptitle("Multi-Panel Report: GridSpec Layout", fontsize=12, fontweight="bold")
plt.savefig("output/multipanel_report_py.pdf", bbox_inches="tight")
plt.savefig("output/multipanel_report_py.png", dpi=300, bbox_inches="tight")
plt.close()


# ── 4. Annotation Patterns ───────────────────────────────
np.random.seed(99)
months24 = np.arange(1, 25)
rev = np.cumsum(np.random.normal(2, 6, 24)) + 100
rev[11] = rev[10] - 25
rev[12:] = rev[12:] + 15

fig, ax = plt.subplots(figsize=(8, 4.5))

# Context band
ax.axvspan(14, 18, color="#E8F5E9", alpha=0.6)
ax.text(16, max(rev) + 5, "Recovery\nperiod", ha="center",
        fontsize=8, fontweight="bold", color="#2E7D32")

# Reference line
mean_rev = np.mean(rev)
ax.axhline(y=mean_rev, color="grey", linewidth=1, linestyle="--")
ax.text(24.5, mean_rev, f"Mean: {mean_rev:.0f}", fontsize=7, va="center", color="grey")

# Data
ax.plot(months24, rev, color="#1565C0", linewidth=2)

# Callout
ax.annotate("Product recall\n(Month 12)",
            xy=(12, rev[11]), xytext=(16, rev[11] - 18),
            fontsize=8, fontweight="bold", color="#C62828",
            arrowprops=dict(arrowstyle="->", color="#C62828", linewidth=1.5),
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFEBEE",
                      edgecolor="#C62828", alpha=0.8))

ax.set_xlabel("Month", fontsize=9)
ax.set_ylabel("Revenue ($K)", fontsize=9)
ax.set_title("Three Annotation Patterns: Callout + Band + Reference",
             fontsize=10, fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig("output/annotation_patterns_py.png", dpi=300, bbox_inches="tight")
plt.close()


print("── All M05 plots saved to output/ ──")
