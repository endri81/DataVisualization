"""W04-M03: Data Wrangling for Visualization (Python) — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
os.makedirs("output",exist_ok=True); np.random.seed(42)

# ── FULL CLEANING PIPELINE (method chaining) ──────────────
apps_clean = (
    pd.read_csv("googleplaystore.csv")
    .drop_duplicates(subset="App", keep="first")
    .assign(
        Reviews=lambda d: pd.to_numeric(d["Reviews"], errors="coerce"),
        Installs=lambda d: d["Installs"].str.replace(r"[+,]","",regex=True).pipe(pd.to_numeric, errors="coerce"),
        Size_MB=lambda d: d["Size"].str.replace("M","").pipe(pd.to_numeric, errors="coerce"),
        Price=lambda d: d["Price"].str.replace("$","",regex=False).pipe(pd.to_numeric, errors="coerce"),
        date=lambda d: pd.to_datetime(d["Last Updated"], format="%B %d, %Y", errors="coerce"))
    .dropna(subset=["Rating"])
    .query("Type in ['Free','Paid']")
    .query("Rating >= 1 and Rating <= 5"))
print(f"Clean: {apps_clean.shape[0]} rows, {apps_clean.shape[1]} cols")

# ── 1. CHAIN-TO-PLOT: groupby → bar ──────────────────────
summary = (apps_clean
    .groupby("Category")
    .agg(mean_r=("Rating","mean"), n=("Rating","count"))
    .nlargest(8, "n")
    .sort_values("mean_r"))

fig, ax = plt.subplots(figsize=(7, 5))
colors = ["#BBBBBB"] * len(summary); colors[-1] = "#2E7D32"
ax.barh(summary.index, summary["mean_r"], color=colors, height=0.5)
for i, (idx, row) in enumerate(summary.iterrows()):
    ax.text(row["mean_r"]+0.005, i, f"{row['mean_r']:.2f}", va="center",
        fontsize=7, fontweight="bold", color="#2E7D32" if i==len(summary)-1 else "#888")
ax.set_xlim(3.8, 4.4)
ax.set_title("Python: chain-to-plot (groupby → agg → nlargest → barh)", fontweight="bold")
for sp in ["top","right","left"]: ax.spines[sp].set_visible(False)
ax.tick_params(left=False, labelsize=7); ax.grid(axis="x", alpha=0.1)
plt.tight_layout(); plt.savefig("output/py_chain_to_plot.png", dpi=300); plt.close()

# ── 2. MELT → LINE CHART ─────────────────────────────────
df_wide = pd.DataFrame({
    "region": ["Tirana","Durres","Vlore","Elbasan"],
    "Q1": [120,90,65,78], "Q2": [135,95,72,82], "Q3": [128,88,70,75], "Q4": [150,110,80,95]})
df_long = pd.melt(df_wide, id_vars="region", var_name="quarter", value_name="revenue")

fig, ax = plt.subplots(figsize=(6, 4))
pal = {"Tirana":"#1565C0","Durres":"#E53935","Vlore":"#2E7D32","Elbasan":"#E65100"}
for r, c in pal.items():
    sub = df_long.query("region==@r")
    ax.plot(sub["quarter"], sub["revenue"], "-o", color=c, lw=1.5, markersize=5, label=r)
ax.legend(fontsize=7); ax.set_title("pd.melt() → line chart", fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/py_melt_line.png", dpi=300); plt.close()

# ── 3. EXPLODE → BAR (Netflix genres) ────────────────────
# Simulated Netflix data
netflix = pd.DataFrame({
    "title": ["Movie A","Movie B","Movie C","Movie D","Movie E"],
    "listed_in": ["Drama, Action","Comedy, Drama","Drama, Thriller","Comedy, Romance","Action, Sci-Fi"]})
genres = (netflix
    .assign(genres=lambda d: d["listed_in"].str.split(", "))
    .explode("genres")
    ["genres"].value_counts())
fig, ax = plt.subplots(figsize=(5, 3))
genres.sort_values().plot.barh(ax=ax, color="#E53935")
ax.set_title(".explode() → genre counts", fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/py_explode_bar.png", dpi=300); plt.close()

# ── 4. GROUPBY + AGG → POINTRANGE ────────────────────────
cats = apps_clean["Category"].value_counts().head(8).index
sub = apps_clean.query("Category in @cats")
stats = (sub.groupby("Category")["Rating"]
    .agg(["mean","std","count"])
    .assign(se=lambda d: d["std"]/np.sqrt(d["count"]),
            ci95=lambda d: 1.96*d["std"]/np.sqrt(d["count"]))
    .sort_values("mean"))
fig, ax = plt.subplots(figsize=(6, 4.5))
ax.errorbar(stats["mean"], range(len(stats)), xerr=stats["ci95"], fmt="o",
    color="#2E7D32", markersize=6, capsize=4, lw=1.5)
ax.set_yticks(range(len(stats))); ax.set_yticklabels(stats.index, fontsize=7)
ax.axvline(x=stats["mean"].mean(), color="#888", lw=0.8, ls="--")
ax.set_title("groupby().agg() → pointrange (Mean ± 95% CI)", fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/py_pointrange.png", dpi=300); plt.close()

# ── 5. ANTI-JOIN PATTERN ─────────────────────────────────
# Find categories in apps but not in a lookup table
lookup = pd.DataFrame({"Category": ["GAME","FAMILY","TOOLS","BUSINESS"]})
missing = apps_clean[~apps_clean["Category"].isin(lookup["Category"])]
print(f"\nAnti-join: {missing['Category'].nunique()} categories not in lookup")

print("\nAll W04-M03 Python plots saved")
