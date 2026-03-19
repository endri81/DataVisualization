"""W04-M04: Missing Data Visualization — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
os.makedirs("output",exist_ok=True)

apps = pd.read_csv("googleplaystore.csv")

# Step 1: How much?
miss_pct = (apps.isna().mean()*100).sort_values(ascending=False)
print("── Missing % ──\n", miss_pct.round(1))
fig, ax = plt.subplots(figsize=(7,4))
miss_pct[miss_pct>0].sort_values().plot.barh(ax=ax, color="#E53935")
ax.set_xlabel("% Missing"); ax.set_title("Missing % per Column", fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/miss_pct_py.png", dpi=300); plt.close()

# Step 2: Missingness matrix
try:
    import missingno as msno
    fig = msno.matrix(apps, figsize=(10,5), sparkline=False, fontsize=8)
    fig.get_figure().savefig("output/miss_matrix_py.png", dpi=300, bbox_inches="tight"); plt.close("all")
    print("  missingno matrix saved")
except ImportError:
    # Manual matrix
    fig, ax = plt.subplots(figsize=(10,5))
    ax.imshow(apps.isna().values[:200].T, aspect="auto",
        cmap=plt.cm.colors.ListedColormap(["#E3F2FD","#E53935"]), interpolation="nearest")
    ax.set_yticks(range(len(apps.columns))); ax.set_yticklabels(apps.columns, fontsize=6)
    ax.set_title("Missingness Matrix (first 200 rows)", fontweight="bold")
    plt.tight_layout(); plt.savefig("output/miss_matrix_py.png", dpi=300); plt.close()
    print("  manual matrix saved (missingno not installed)")

# Step 3: Nullity correlation heatmap
try:
    fig = msno.heatmap(apps, figsize=(7,5), fontsize=8)
    fig.get_figure().savefig("output/miss_heatmap_py.png", dpi=300, bbox_inches="tight"); plt.close("all")
except: pass

# Step 4: Shadow-augmented histogram
apps["Reviews_num"] = pd.to_numeric(apps["Reviews"], errors="coerce")
apps["Rating_missing"] = apps["Rating"].isna()
fig, ax = plt.subplots(figsize=(7,4))
for label, mask, color in [("Rating present",~apps["Rating_missing"],"#1565C0"),("Rating missing",apps["Rating_missing"],"#E53935")]:
    sub = apps.loc[mask, "Reviews_num"].dropna()
    if len(sub)>0: ax.hist(np.log10(sub+1), bins=30, alpha=0.5, color=color, label=f"{label} (n={len(sub)})")
ax.legend(fontsize=7); ax.set_xlabel("log10(Reviews+1)"); ax.set_title("Reviews: Rating Present vs Missing", fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/shadow_hist_py.png", dpi=300); plt.close()

# Step 5: Imputation effect
rating_obs = apps["Rating"].dropna()
rating_imputed = apps["Rating"].fillna(apps["Rating"].mean())
fig, (ax1,ax2) = plt.subplots(1,2, figsize=(10,4))
ax1.hist(rating_obs, bins=30, color="#1565C0", edgecolor="white", lw=0.3)
ax1.set_title(f"Before (n={len(rating_obs)})", fontweight="bold")
ax2.hist(rating_imputed, bins=30, color="#1565C0", edgecolor="white", lw=0.3)
ax2.axvline(x=rating_obs.mean(), color="#E53935", lw=2, ls="--", label="Mean spike")
ax2.set_title("After Mean Imputation", fontweight="bold", color="#C62828"); ax2.legend(fontsize=7)
for ax in [ax1,ax2]: ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.suptitle("Always Plot Before & After Imputation", fontweight="bold")
plt.tight_layout(); plt.savefig("output/imputation_py.png", dpi=300); plt.close()

print("All W04-M04 Python plots saved")
