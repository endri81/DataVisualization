"""
============================================================
Workshop 1 — Module 10: Comparative Lab
Python Script — Google Play Store EDA
Data Visualization for Data Scientists — UNYT Tirana
============================================================
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import os

os.makedirs("output", exist_ok=True)
plt.rcParams.update({"figure.dpi": 150, "font.size": 10, "axes.titleweight": "bold"})

# ── 1. LOAD & CLEAN ───────────────────────────────────────
apps = pd.read_csv("googleplaystore.csv")
print(f"Shape: {apps.shape}")

apps_clean = (
    apps
    .query("Type in ['Free', 'Paid']")
    .assign(
        Reviews=lambda d: pd.to_numeric(d["Reviews"], errors="coerce"),
        Last_Updated=lambda d: pd.to_datetime(d["Last Updated"],
                                               format="%B %d, %Y", errors="coerce"),
    )
    .assign(Year=lambda d: d["Last_Updated"].dt.year)
    .copy()
)

# ── 2. BAR CHART: Top 10 categories ──────────────────────
top10 = apps_clean.value_counts("Category").head(10).sort_values()

fig, ax = plt.subplots(figsize=(6, 5))
ax.barh(top10.index, top10.values, color="#2E7D32", height=0.6, edgecolor="none")
for i, v in enumerate(top10.values):
    ax.text(v + 15, i, f"{v:,}", va="center", fontsize=7, fontweight="bold")
for sp in ["top", "right", "left"]:
    ax.spines[sp].set_visible(False)
ax.set_xticks([])
ax.tick_params(left=False, labelsize=8)
ax.set_title("(a) Top 10 App Categories")
plt.tight_layout()
fig.savefig("output/bar_PY.png", dpi=300, bbox_inches="tight")
plt.close()

# ── 3. HISTOGRAM: Rating distribution ────────────────────
ratings = apps_clean["Rating"].dropna()
mean_r = ratings.mean()

fig, ax = plt.subplots(figsize=(6, 4))
ax.hist(ratings, bins=40, color="#2E7D32", edgecolor="white", linewidth=0.3)
ax.axvline(x=mean_r, color="#E53935", linewidth=2, linestyle="--")
ax.text(mean_r + 0.05, ax.get_ylim()[1] * 0.92, f"Mean: {mean_r:.2f}",
        fontsize=8, color="#E53935", fontweight="bold")
ax.set_xlabel("Rating"); ax.set_ylabel("Frequency")
ax.set_title("(b) Rating Distribution")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout()
fig.savefig("output/hist_PY.png", dpi=300, bbox_inches="tight")
plt.close()

# ── 4. SCATTER: Reviews vs Rating ────────────────────────
df_sc = apps_clean.dropna(subset=["Rating"]).query("Reviews > 0")

fig, ax = plt.subplots(figsize=(6, 5))
for t, c in [("Free", "#2E7D32"), ("Paid", "#E53935")]:
    mask = df_sc["Type"] == t
    ax.scatter(df_sc.loc[mask, "Reviews"], df_sc.loc[mask, "Rating"],
               s=8, c=c, alpha=0.3, edgecolors="none", label=t)
ax.set_xscale("log")
ax.set_xlabel("Reviews (log scale)"); ax.set_ylabel("Rating")
ax.set_title("(c) Reviews vs Rating")
ax.legend(fontsize=7, title="Type", title_fontsize=8)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout()
fig.savefig("output/scatter_PY.png", dpi=300, bbox_inches="tight")
plt.close()

# ── 5. BOXPLOT: Rating by Type ───────────────────────────
free_r = apps_clean.loc[apps_clean["Type"] == "Free", "Rating"].dropna()
paid_r = apps_clean.loc[apps_clean["Type"] == "Paid", "Rating"].dropna()

fig, ax = plt.subplots(figsize=(5, 4))
bp = ax.boxplot([free_r, paid_r], labels=["Free", "Paid"],
                patch_artist=True, widths=0.45, notch=True)
bp["boxes"][0].set_facecolor("#C8E6C9"); bp["boxes"][0].set_edgecolor("#2E7D32")
bp["boxes"][1].set_facecolor("#FFCDD2"); bp["boxes"][1].set_edgecolor("#E53935")
for med in bp["medians"]:
    med.set_color("#333"); med.set_linewidth(2)
means = [free_r.mean(), paid_r.mean()]
ax.scatter([1, 2], means, c="#E53935", s=50, zorder=5, marker="D", edgecolors="white")
ax.set_ylabel("Rating"); ax.set_title("(d) Rating by Type")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout()
fig.savefig("output/box_PY.png", dpi=300, bbox_inches="tight")
plt.close()

# ── 6. LINE CHART: Apps per year ─────────────────────────
yearly = (apps_clean
    .query("2010 <= Year <= 2018")
    .groupby(["Year", "Type"])
    .size()
    .reset_index(name="n"))

fig, ax = plt.subplots(figsize=(6, 4))
for t, c in [("Free", "#2E7D32"), ("Paid", "#E53935")]:
    sub = yearly.query("Type == @t")
    ax.plot(sub["Year"], sub["n"], "o-", color=c, linewidth=2, markersize=5)
    ax.text(sub["Year"].iloc[-1] + 0.2, sub["n"].iloc[-1], t,
            fontsize=8, fontweight="bold", color=c, va="center")
ax.set_xlim(2009.5, 2019)
ax.set_xlabel("Year"); ax.set_ylabel("Count")
ax.set_title("(e) Apps Added per Year")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout()
fig.savefig("output/line_PY.png", dpi=300, bbox_inches="tight")
plt.close()

# ── 7. STACKED BAR: Content Rating × Type ────────────────
keep_cr = ["Everyone", "Teen", "Mature 17+", "Everyone 10+"]
ct = pd.crosstab(
    apps_clean.loc[apps_clean["Content Rating"].isin(keep_cr), "Content Rating"],
    apps_clean["Type"])

fig, ax = plt.subplots(figsize=(6, 4))
ct.plot.bar(stacked=True, color=["#2E7D32", "#E53935"], edgecolor="white", ax=ax)
ax.set_title("(f) Content Rating × Type")
ax.set_xlabel(None)
ax.tick_params(axis="x", rotation=30, labelsize=7)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.legend(fontsize=7)
plt.tight_layout()
fig.savefig("output/stacked_PY.png", dpi=300, bbox_inches="tight")
plt.close()

# ── 8. DASHBOARD: 6-panel GridSpec ───────────────────────
fig = plt.figure(figsize=(14, 9))
gs = GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.35)

# Re-create all six panels (abbreviated — reuses logic above)
# (a) Bar
ax = fig.add_subplot(gs[0, 0])
ax.barh(top10.index, top10.values, color="#2E7D32", height=0.6, edgecolor="none")
for i, v in enumerate(top10.values):
    ax.text(v + 15, i, f"{v:,}", va="center", fontsize=6, fontweight="bold")
ax.set_title("(a) Top Categories", fontsize=9); ax.tick_params(labelsize=5)
for sp in ["top","right","left"]: ax.spines[sp].set_visible(False)
ax.set_xticks([]); ax.tick_params(left=False)

# (b) Histogram
ax = fig.add_subplot(gs[0, 1])
ax.hist(ratings, bins=40, color="#2E7D32", edgecolor="white", linewidth=0.3)
ax.axvline(x=mean_r, color="#E53935", linewidth=1.5, linestyle="--")
ax.set_title("(b) Rating Dist.", fontsize=9); ax.tick_params(labelsize=5)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

# (c) Scatter
ax = fig.add_subplot(gs[0, 2])
ax.scatter(df_sc["Reviews"], df_sc["Rating"], s=3, c="#E65100", alpha=0.2, edgecolors="none")
ax.set_xscale("log")
ax.set_title("(c) Reviews vs Rating", fontsize=9); ax.tick_params(labelsize=5)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

# (d) Boxplot
ax = fig.add_subplot(gs[1, 0])
bp = ax.boxplot([free_r, paid_r], labels=["Free","Paid"], patch_artist=True, widths=0.4)
bp["boxes"][0].set_facecolor("#C8E6C9"); bp["boxes"][1].set_facecolor("#FFCDD2")
ax.set_title("(d) Rating by Type", fontsize=9); ax.tick_params(labelsize=5)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

# (e) Line
ax = fig.add_subplot(gs[1, 1])
for t, c in [("Free","#2E7D32"),("Paid","#E53935")]:
    sub = yearly.query("Type==@t")
    ax.plot(sub["Year"], sub["n"], "o-", color=c, lw=1.5, ms=4)
ax.set_title("(e) Apps per Year", fontsize=9); ax.tick_params(labelsize=5)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

# (f) Stacked
ax = fig.add_subplot(gs[1, 2])
ct.plot.bar(stacked=True, color=["#2E7D32","#E53935"], edgecolor="white", ax=ax, legend=False)
ax.set_title("(f) Content × Type", fontsize=9); ax.tick_params(labelsize=5, axis="x", rotation=30)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

fig.suptitle("Google Play Store: EDA Dashboard — Python (matplotlib)", fontsize=13, fontweight="bold")
fig.savefig("output/W01_M10_dashboard_PY.pdf", bbox_inches="tight")
fig.savefig("output/W01_M10_dashboard_PY.png", dpi=300, bbox_inches="tight")
plt.close()

print("\n── Workshop 1 Lab Complete (Python) ──")
