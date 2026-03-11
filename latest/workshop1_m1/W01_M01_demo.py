"""
============================================================
Workshop 1 — Module 1: Why Visualize?
Python Demonstration Script
Data Visualization for Data Scientists — UNYT Tirana
============================================================
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# Global plot style — clean, publication-ready
sns.set_theme(style="whitegrid", font_scale=1.0)
plt.rcParams["figure.dpi"] = 150


# ── 1. Anscombe's Quartet ───────────────────────────────────
# Seaborn ships with the Anscombe dataset built in.

df_ans = sns.load_dataset("anscombe")

# Verify that all four datasets share the same statistics
summary = df_ans.groupby("dataset").agg(
    mean_x=("x", "mean"),
    mean_y=("y", "mean"),
    sd_x=("x", "std"),
    sd_y=("y", "std"),
).round(2)

# Correlation requires a custom aggregation
corr = (
    df_ans.groupby("dataset")
    .apply(lambda g: g["x"].corr(g["y"]), include_groups=False)
    .rename("cor_xy")
    .round(3)
)
summary = summary.join(corr)
print("── Anscombe's Quartet: Summary Statistics ──")
print(summary)
print()

# Faceted scatterplot with regression lines (seaborn lmplot)
g = sns.lmplot(
    data=df_ans,
    x="x",
    y="y",
    col="dataset",
    col_wrap=2,
    ci=None,                       # no confidence band
    height=3,
    aspect=1.1,
    scatter_kws={"s": 40, "color": "#1565C0"},
    line_kws={"color": "#E53935", "linewidth": 1.2},
)
g.figure.suptitle(
    "Anscombe's Quartet: Same Statistics, Different Stories",
    fontsize=13, fontweight="bold", y=1.02,
)
g.set_titles("Dataset {col_name}")
plt.tight_layout()
plt.savefig("output/anscombe_quartet_py.png", dpi=150, bbox_inches="tight")
plt.close()


# ── 2. Datasaurus Dozen ────────────────────────────────────
# Load from the datasauRus repository TSV file.

url = (
    "https://raw.githubusercontent.com/"
    "jumpingrivers/datasauRus/main/inst/"
    "extdata/DatasaurusDozen-long.tsv"
)

try:
    df_dino = pd.read_csv(url, sep="\t")
except Exception:
    # Fallback: create a minimal dummy if network is unavailable
    print("Warning: could not fetch Datasaurus data from network.")
    print("Creating local Anscombe-based placeholder instead.\n")
    df_dino = df_ans.rename(columns={"dataset": "dataset"})

# Verify identical statistics across all 13 datasets
dino_stats = df_dino.groupby("dataset").agg(
    mean_x=("x", "mean"),
    mean_y=("y", "mean"),
    sd_x=("x", "std"),
    sd_y=("y", "std"),
).round(1)
print("── Datasaurus Dozen: Summary Statistics ──")
print(dino_stats.head(13))
print()

# Faceted scatterplot — 13 shapes, one set of statistics
datasets = df_dino["dataset"].unique()
n_datasets = len(datasets)
ncols = min(5, n_datasets)
nrows = int(np.ceil(n_datasets / ncols))

fig, axes = plt.subplots(nrows, ncols, figsize=(12, 2.5 * nrows))
axes_flat = axes.flatten() if n_datasets > 1 else [axes]

for i, ds in enumerate(sorted(datasets)):
    ax = axes_flat[i]
    subset = df_dino[df_dino["dataset"] == ds]
    ax.scatter(subset["x"], subset["y"], s=5, alpha=0.5, c="#2E7D32")
    ax.set_title(ds, fontsize=7, fontweight="bold")
    ax.set_xticks([])
    ax.set_yticks([])

# Hide unused subplots
for j in range(i + 1, len(axes_flat)):
    axes_flat[j].set_visible(False)

fig.suptitle(
    "The Datasaurus Dozen — Same Stats, Different Graphs",
    fontsize=12, fontweight="bold",
)
plt.tight_layout()
plt.savefig("output/datasaurus_dozen_py.png", dpi=150, bbox_inches="tight")
plt.close()


# ── 3. First Plot: mpg Dataset ─────────────────────────────
# Seaborn's built-in mpg dataset (auto fuel economy data).

mpg = sns.load_dataset("mpg").dropna()

fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(
    data=mpg,
    x="displacement",
    y="mpg",
    hue="origin",
    alpha=0.7,
    s=50,
    palette="Set1",
    ax=ax,
)
ax.set_title("Engine Displacement vs Fuel Economy", fontweight="bold")
ax.set_xlabel("Engine Displacement (cubic inches)")
ax.set_ylabel("Miles per Gallon")
plt.tight_layout()
plt.savefig("output/mpg_scatter_py.png", dpi=150)
plt.close()


# ── 4. Data-Ink Ratio: Before & After ──────────────────────
# Demonstrate the contrast between a cluttered chart and a
# clean redesign of the same data.

# Count vehicle origins
origin_counts = mpg["origin"].value_counts().sort_values()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# "Before" — heavy gridlines, unnecessary fills, vertical bars
ax1.bar(
    origin_counts.index,
    origin_counts.values,
    color="skyblue",
    edgecolor="black",
    linewidth=1.5,
)
ax1.set_facecolor("#F0F0F0")
ax1.grid(True, which="both", linewidth=0.8, color="grey")
ax1.set_title("Before: Cluttered Design", fontweight="bold")
ax1.set_ylabel("Count")

# "After" — clean horizontal bars with direct labels
ax2.barh(
    origin_counts.index,
    origin_counts.values,
    color="#1565C0",
    height=0.6,
)
for i, (val, name) in enumerate(zip(origin_counts.values, origin_counts.index)):
    ax2.text(val + 3, i, str(val), va="center", fontsize=10)
ax2.set_title("After: Clean Design", fontweight="bold")
ax2.set_xlabel("Count")
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.grid(axis="x", alpha=0.3)

fig.suptitle(
    "Data-Ink Ratio: Removing Chartjunk",
    fontsize=13, fontweight="bold",
)
plt.tight_layout()
plt.savefig("output/data_ink_comparison_py.png", dpi=150)
plt.close()

print("── All plots saved to output/ directory ──")
