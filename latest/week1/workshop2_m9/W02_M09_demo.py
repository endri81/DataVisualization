"""W02-M09: Tidy Data & Data Wrangling for Viz — Python — UNYT Tirana"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
os.makedirs("output", exist_ok=True); np.random.seed(42)

# 1. PIVOT DEMO
gdp_wide = pd.DataFrame({
    "Country": ["Albania", "Greece", "Italy"],
    "2020": [2.9, -9.0, -9.0], "2021": [7.5, 8.4, 6.7], "2022": [4.8, 5.9, 3.7]
})
gdp_long = gdp_wide.melt(id_vars=["Country"], var_name="Year", value_name="GDP_Growth")
gdp_long["Year"] = gdp_long["Year"].astype(int)

fig, ax = plt.subplots(figsize=(7, 4.5))
pal = {"Albania": "#1565C0", "Greece": "#E53935", "Italy": "#2E7D32"}
for c, col in pal.items():
    sub = gdp_long.query("Country == @c")
    ax.plot(sub["Year"], sub["GDP_Growth"], "o-", color=col, linewidth=2, markersize=6, label=c)
ax.axhline(y=0, color="grey", linewidth=0.8, linestyle="--")
ax.set_title("GDP Growth After melt()", fontsize=11, fontweight="bold")
ax.set_xlabel("Year"); ax.set_ylabel("GDP Growth (%)")
ax.legend(fontsize=8); ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/pivot_demo_py.png", dpi=300); plt.close()

# 2. SIX VERBS → PLOT (method chaining)
apps = pd.read_csv("googleplaystore.csv")
summary = (apps
    .query("Type in ['Free', 'Paid']")
    .dropna(subset=["Rating"])
    .assign(Reviews=lambda d: pd.to_numeric(d["Reviews"], errors="coerce"))
    .groupby("Category")
    .agg(n=("Rating", "count"), m=("Rating", "mean"),
         se=("Rating", lambda x: x.std() / np.sqrt(len(x))))
    .reset_index()
    .nlargest(8, "n")
    .sort_values("m"))

fig, ax = plt.subplots(figsize=(7, 5))
ax.barh(summary["Category"], summary["m"], color="#2E7D32", height=0.5, alpha=0.6,
        xerr=summary["se"], capsize=3, ecolor="#333")
for i, (m, s) in enumerate(zip(summary["m"], summary["se"])):
    ax.text(m + s + 0.01, i, f"{m:.2f}", va="center", fontsize=7, fontweight="bold")
ax.set_title("Mean Rating by Category (±SE)", fontsize=11, fontweight="bold")
ax.set_xlabel("Mean Rating"); ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.tick_params(labelsize=7); plt.tight_layout()
plt.savefig("output/wrangle_to_plot_py.png", dpi=300); plt.close()

# 3. COMPLETE PIPELINE — colour by mean rating
top10 = (apps
    .query("Type in ['Free', 'Paid']").dropna(subset=["Rating"])
    .groupby("Category").agg(n=("Rating","count"), m=("Rating","mean")).reset_index()
    .nlargest(10, "n").sort_values("n"))

fig, ax = plt.subplots(figsize=(8, 5))
sc = ax.barh(top10["Category"], top10["n"], color=plt.cm.plasma((top10["m"] - top10["m"].min()) /
    (top10["m"].max() - top10["m"].min())), height=0.6)
sm = plt.cm.ScalarMappable(cmap="plasma", norm=plt.Normalize(top10["m"].min(), top10["m"].max()))
fig.colorbar(sm, ax=ax, shrink=0.7, label="Mean Rating")
ax.set_title("Top 10: Count Coloured by Mean Rating", fontsize=11, fontweight="bold")
ax.set_xlabel("Number of Apps"); ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.tick_params(labelsize=7); plt.tight_layout()
plt.savefig("output/complete_chain_py.png", dpi=300); plt.close()

print("All W02-M09 Python plots saved")
