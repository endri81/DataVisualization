"""W02-M10: Lab — Building a Visual Report — Python — UNYT Tirana"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
from matplotlib.gridspec import GridSpec
os.makedirs("output", exist_ok=True); np.random.seed(42)

apps = pd.read_csv("googleplaystore.csv")
apps_clean = (apps.query("Type in ['Free','Paid']")
    .assign(Reviews=lambda d: pd.to_numeric(d["Reviews"], errors="coerce"),
            Last_Updated=lambda d: pd.to_datetime(d["Last Updated"], format="%B %d, %Y", errors="coerce"))
    .assign(Year=lambda d: d["Last_Updated"].dt.year).copy())

# Build 6-panel dashboard
fig = plt.figure(figsize=(14, 9))
gs = GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.35)

# (a) Bar
ax = fig.add_subplot(gs[0, 0])
top8 = apps_clean.value_counts("Category").head(8).sort_values()
colors = ["#BBBBBB"] * 8; colors[-1] = "#1565C0"
ax.barh(top8.index, top8.values, color=colors, height=0.5, edgecolor="none")
for i, v in enumerate(top8.values):
    ax.text(v + 15, i, f"{v:,}", va="center", fontsize=6, fontweight="bold",
            color="#1565C0" if i == 7 else "#888")
ax.set_title("(a) Top Categories", fontsize=9, fontweight="bold")
for sp in ["top","right","left"]: ax.spines[sp].set_visible(False)
ax.set_xticks([]); ax.tick_params(left=False, labelsize=6)

# (b) Histogram
ax = fig.add_subplot(gs[0, 1])
ratings = apps_clean["Rating"].dropna()
ax.hist(ratings, bins=30, color="#1565C0", edgecolor="white", linewidth=0.3)
ax.axvline(x=ratings.mean(), color="#E53935", linewidth=1.5, linestyle="--")
ax.text(ratings.mean() + 0.05, ax.get_ylim()[1] * 0.9, f"Mean: {ratings.mean():.2f}",
        fontsize=7, color="#E53935", fontweight="bold")
ax.set_title("(b) Rating Distribution", fontsize=9, fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.tick_params(labelsize=6)

# (c) Scatter
ax = fig.add_subplot(gs[0, 2])
df_sc = apps_clean.dropna(subset=["Rating"]).query("Reviews > 0")
for t, c in [("Free", "#1565C0"), ("Paid", "#E53935")]:
    m = df_sc["Type"] == t
    ax.scatter(df_sc.loc[m, "Reviews"], df_sc.loc[m, "Rating"], s=5, c=c, alpha=0.2, edgecolors="none", label=t)
ax.set_xscale("log"); ax.legend(fontsize=5, title="Type", title_fontsize=6)
ax.set_title("(c) Reviews vs Rating", fontsize=9, fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.tick_params(labelsize=6)

# (d) Boxplot
ax = fig.add_subplot(gs[1, 0])
free_r = apps_clean.loc[apps_clean["Type"] == "Free", "Rating"].dropna()
paid_r = apps_clean.loc[apps_clean["Type"] == "Paid", "Rating"].dropna()
bp = ax.boxplot([free_r, paid_r], labels=["Free", "Paid"], patch_artist=True, widths=0.4, notch=True)
bp["boxes"][0].set_facecolor("#BBDEFB"); bp["boxes"][1].set_facecolor("#FFCDD2")
ax.scatter([1, 2], [free_r.mean(), paid_r.mean()], c="#E53935", s=40, zorder=5, marker="D", edgecolors="white")
ax.set_title("(d) Rating by Type", fontsize=9, fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.tick_params(labelsize=6)

# (e) Line
ax = fig.add_subplot(gs[1, 1])
yearly = apps_clean.query("2010 <= Year <= 2018").groupby(["Year", "Type"]).size().reset_index(name="n")
for t, c in [("Free", "#1565C0"), ("Paid", "#E53935")]:
    sub = yearly.query("Type == @t")
    ax.plot(sub["Year"], sub["n"], "o-", color=c, linewidth=1.5, markersize=4)
    ax.text(sub["Year"].iloc[-1] + 0.2, sub["n"].iloc[-1], t, fontsize=6, fontweight="bold", color=c, va="center")
ax.set_xlim(2009.5, 2019); ax.set_title("(e) Apps per Year", fontsize=9, fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.tick_params(labelsize=6)

# (f) Stacked bar
ax = fig.add_subplot(gs[1, 2])
keep_cr = ["Everyone", "Teen", "Mature 17+", "Everyone 10+"]
ct = pd.crosstab(apps_clean.loc[apps_clean["Content Rating"].isin(keep_cr), "Content Rating"], apps_clean["Type"])
ct.plot.bar(stacked=True, color=["#1565C0", "#E53935"], edgecolor="white", ax=ax, legend=True)
ax.set_title("(f) Content × Type", fontsize=9, fontweight="bold")
ax.tick_params(axis="x", rotation=30, labelsize=5); ax.legend(fontsize=5)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

fig.suptitle("Google Play Store: Complete Visual Report\nWorkshop 2 Lab — Grammar of Graphics Applied",
             fontsize=13, fontweight="bold")
fig.text(0.5, 0.01, "Source: Kaggle | UNYT Data Visualization Course | Prof.Asoc. Endri Raco",
         ha="center", fontsize=8, fontstyle="italic", color="#888")
fig.savefig("output/W02_M10_report.pdf", bbox_inches="tight")
fig.savefig("output/W02_M10_report.png", dpi=300, bbox_inches="tight")
plt.close()
print("Workshop 2 Lab Complete (Python)")
