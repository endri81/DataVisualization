"""W04-M06: Correlation & Association Visualization — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, seaborn as sns, os
from scipy.stats import pearsonr, spearmanr, kendalltau, chi2_contingency
os.makedirs("output",exist_ok=True); np.random.seed(42)

apps = pd.read_csv("googleplaystore.csv")
apps["Reviews"] = pd.to_numeric(apps["Reviews"], errors="coerce")
apps["Installs"] = apps["Installs"].str.replace(r"[+,]","",regex=True).pipe(pd.to_numeric,errors="coerce")
apps["Price"] = apps["Price"].str.replace("$","",regex=False).pipe(pd.to_numeric,errors="coerce")
apps = apps.dropna(subset=["Rating","Reviews"]).query("Reviews > 0")
apps["log_reviews"] = np.log10(apps["Reviews"]+1)
apps["log_installs"] = np.log10(apps["Installs"]+1)

# 1. CORRELATION HEATMAP
num_cols = ["Rating","log_reviews","log_installs","Price"]
corr = apps[num_cols].corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
fig,ax = plt.subplots(figsize=(7,6))
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="RdBu_r", vmin=-1, vmax=1, center=0,
    square=True, linewidths=0.5, cbar_kws={"shrink":0.8,"label":"Pearson r"}, ax=ax)
ax.set_title("Correlation Heatmap (lower triangle)", fontweight="bold")
plt.tight_layout(); plt.savefig("output/corr_heatmap_py.png", dpi=300); plt.close()

# 2. PAIRS PLOT
sub = apps[["Rating","log_reviews","Price","Type"]].dropna().sample(800,random_state=42)
g = sns.pairplot(sub, hue="Type", palette={"Free":"#1565C0","Paid":"#E53935"},
    diag_kind="kde", plot_kws={"s":10,"alpha":0.3}, height=2)
g.fig.suptitle("Pairs Plot: scatter + KDE + hue", fontweight="bold", y=1.02)
plt.savefig("output/pairs_py.png", dpi=300, bbox_inches="tight"); plt.close()

# 3. THREE COEFFICIENTS
r_p, _ = pearsonr(apps["log_reviews"], apps["Rating"])
r_s, _ = spearmanr(apps["log_reviews"], apps["Rating"])
r_k, _ = kendalltau(apps["log_reviews"], apps["Rating"])
print(f"log(Reviews) vs Rating: Pearson={r_p:.3f}, Spearman={r_s:.3f}, Kendall={r_k:.3f}")

# 4. CATEGORICAL: chi-squared + Cramer's V
cats5 = apps.query("Category in ['GAME','FAMILY','TOOLS','BUSINESS','MEDICAL']")
ct = pd.crosstab(cats5["Category"], cats5["Type"])
chi2, p, dof, exp = chi2_contingency(ct)
n_obs = ct.sum().sum(); k = min(ct.shape)-1
cramers_v = np.sqrt(chi2 / (n_obs * k))
print(f"Chi2={chi2:.1f}, p={p:.4f}, Cramer's V={cramers_v:.3f}")

# 5. CATEGORICAL VIZ
ct_pct = ct.div(ct.sum(axis=1), axis=0)
fig,ax = plt.subplots(figsize=(7,4))
ct_pct.plot.barh(stacked=True, ax=ax, color={"Free":"#1565C0","Paid":"#E53935"}, edgecolor="white")
ax.set_xlabel("%"); ax.set_title(f"100% Stacked: Type x Category (Cramer's V = {cramers_v:.2f})", fontweight="bold")
ax.legend(fontsize=7); ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/categorical_py.png", dpi=300); plt.close()

print("All W04-M06 Python plots saved")
