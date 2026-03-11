"""
============================================================
Workshop 1 — Module 6: The Design Process
Python Demonstration Script
Data Visualization for Data Scientists — UNYT Tirana
============================================================
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import os

os.makedirs("output", exist_ok=True)
plt.rcParams.update({"figure.dpi": 150, "font.size": 11,
                     "axes.titleweight": "bold"})


# ── COMPLETE PIPELINE DEMO ─────────────────────────────────

# 1. ACQUIRE
df_raw = pd.DataFrame({
    "quarter": ["Q1", "Q2", "Q3", "Q4"],
    "revenue": [245, 310, 280, 395],
    "region": ["East"] * 4,
})
print("── Step 1: Acquire ──")
print(df_raw)

# 2. PARSE
df_raw["quarter"] = pd.Categorical(
    df_raw["quarter"], categories=["Q1","Q2","Q3","Q4"], ordered=True)
print("\n── Step 2: Parse ──")
print(df_raw.dtypes)

# 3. FILTER (no filtering needed on this small demo)
df_filtered = df_raw.copy()

# 4. MINE
max_row = df_filtered.loc[df_filtered["revenue"].idxmax()]
print(f"\n── Step 4: Mine ──")
print(f"Best quarter: {max_row['quarter']} with ${max_row['revenue']}K")

# 5. REPRESENT
fig, ax = plt.subplots(figsize=(6, 4.5))
colors = ["#1565C0" if q != max_row["quarter"] else "#E53935"
          for q in df_filtered["quarter"]]
ax.bar(df_filtered["quarter"], df_filtered["revenue"],
       color=colors, width=0.5, edgecolor="none")
for i, (q, v) in enumerate(zip(df_filtered["quarter"], df_filtered["revenue"])):
    ax.text(i, v + 8, f"${v}K", ha="center", fontsize=9, fontweight="bold", color="#333")

ax.set_ylim(0, 450)
ax.set_title("Q4 Revenue Highest at $395K", fontsize=14, fontweight="bold")
fig.text(0.13, 0.91, "Quarterly revenue, East region, 2024",
         fontsize=10, color="grey")
fig.text(0.13, 0.02, "Source: Internal sales database",
         fontsize=8, fontstyle="italic", color="#888")
ax.set_ylabel("Revenue ($K)", fontsize=10)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(labelsize=9)
plt.subplots_adjust(top=0.85, bottom=0.1)
plt.savefig("output/pipeline_complete_py.pdf", bbox_inches="tight")
plt.savefig("output/pipeline_complete_py.png", dpi=300, bbox_inches="tight")
plt.close()


# ── ITERATIVE REFINEMENT: 3 STAGES ────────────────────────
cats = ["Tools", "Finance", "Games", "Social", "Photo"]
vals = [42, 58, 35, 67, 51]

fig, axes = plt.subplots(1, 3, figsize=(14, 4))

# Stage 1: Sketch
axes[0].bar(cats, vals, color="#AAAAAA", edgecolor="black")
axes[0].set_title("Stage 1: Sketch\n(defaults)", fontsize=9, fontweight="bold")
axes[0].tick_params(labelsize=7)

# Stage 2: Draft
idx = np.argsort(vals)
axes[1].barh([cats[i] for i in idx], [vals[i] for i in idx],
             color="#64B5F6", height=0.6, edgecolor="none")
axes[1].set_title("Stage 2: Draft\n(sorted, horizontal)", fontsize=9, fontweight="bold")
axes[1].spines["top"].set_visible(False); axes[1].spines["right"].set_visible(False)
axes[1].tick_params(labelsize=7)

# Stage 3: Polished
idx_rev = np.argsort(vals)[::-1]
s_cats = [cats[i] for i in idx]
s_vals = [vals[i] for i in idx]
bar_colors = ["#1565C0"] * 5
bar_colors[-1] = "#E53935"  # max (last after sort ascending)
axes[2].barh(s_cats, s_vals, color=bar_colors, height=0.5, edgecolor="none")
for i, v in enumerate(s_vals):
    axes[2].text(v + 0.8, i, str(v), va="center", fontsize=9,
                 fontweight="bold", color="#E53935" if v == max(vals) else "#333")
axes[2].set_title("Stage 3: Polished\n(accent, labels, minimal)", fontsize=9, fontweight="bold")
for sp in ["top", "right", "left"]:
    axes[2].spines[sp].set_visible(False)
axes[2].set_xticks([])
axes[2].tick_params(left=False, labelsize=8)

fig.suptitle("Iterative Refinement: Sketch → Draft → Polished",
             fontsize=12, fontweight="bold")
plt.tight_layout()
plt.savefig("output/iteration_stages_py.png", dpi=300, bbox_inches="tight")
plt.close()


# ── AUDIENCE ADAPTATION ───────────────────────────────────

# Executive version: 1 chart, grey + accent
fig, ax = plt.subplots(figsize=(7, 5))
idx = np.argsort(vals)
s_cats = [cats[i] for i in idx]
s_vals = [vals[i] for i in idx]
bar_colors = ["#BBBBBB"] * 5
bar_colors[-1] = "#E53935"
ax.barh(s_cats, s_vals, color=bar_colors, height=0.5, edgecolor="none")
for i, v in enumerate(s_vals):
    ax.text(v + 0.8, i, str(v), va="center", fontsize=10,
            fontweight="bold", color="#E53935" if v == max(vals) else "#555")
ax.set_title("Games Lead with 67 Downloads", fontsize=14, fontweight="bold")
fig.text(0.15, 0.91, "Top 5 categories, Google Play Store",
         fontsize=10, color="grey")
fig.text(0.15, 0.02, "Source: Kaggle | Executive Summary",
         fontsize=8, fontstyle="italic", color="#888")
for sp in ["top", "right", "left"]:
    ax.spines[sp].set_visible(False)
ax.set_xticks([])
ax.tick_params(left=False, labelsize=9)
plt.subplots_adjust(top=0.85, bottom=0.08)
plt.savefig("output/exec_version_py.png", dpi=300, bbox_inches="tight")
plt.close()

# Analyst version: 4-panel dashboard
np.random.seed(55)
fig = plt.figure(figsize=(10, 7))
gs = GridSpec(2, 2, figure=fig, hspace=0.4, wspace=0.3)

ax1 = fig.add_subplot(gs[0, 0])
ax1.barh(s_cats, s_vals, color="#1565C0", height=0.5)
ax1.set_title("(a) Category Counts", fontsize=9, fontweight="bold")
ax1.spines["top"].set_visible(False); ax1.spines["right"].set_visible(False)
ax1.tick_params(labelsize=7)

ax2 = fig.add_subplot(gs[0, 1])
ax2.hist(np.random.normal(4.0, 0.5, 500), bins=20, color="#2E7D32",
         edgecolor="white", linewidth=0.3)
ax2.set_title("(b) Rating Distribution", fontsize=9, fontweight="bold")
ax2.spines["top"].set_visible(False); ax2.spines["right"].set_visible(False)
ax2.tick_params(labelsize=7)

ax3 = fig.add_subplot(gs[1, 0])
ax3.scatter(np.random.uniform(0, 10, 50), np.random.uniform(3, 5, 50),
            s=25, c="#E53935", alpha=0.6)
ax3.set_title("(c) Reviews vs Rating", fontsize=9, fontweight="bold")
ax3.spines["top"].set_visible(False); ax3.spines["right"].set_visible(False)
ax3.tick_params(labelsize=7)

ax4 = fig.add_subplot(gs[1, 1])
ax4.plot(np.arange(1, 13), np.cumsum(np.random.normal(5, 8, 12)) + 50,
         color="#1565C0", linewidth=1.5)
ax4.set_title("(d) Monthly Trend", fontsize=9, fontweight="bold")
ax4.spines["top"].set_visible(False); ax4.spines["right"].set_visible(False)
ax4.tick_params(labelsize=7)

fig.suptitle("Analyst Dashboard: Full Detail", fontsize=12, fontweight="bold")
plt.savefig("output/analyst_version_py.png", dpi=300, bbox_inches="tight")
plt.close()


print("── All M06 plots saved to output/ ──")
