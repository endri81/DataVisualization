"""W04-M05: Outlier Detection & Visual Diagnostics — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
from scipy.stats import zscore, probplot, chi2
from scipy.spatial.distance import mahalanobis
os.makedirs("output",exist_ok=True); np.random.seed(42)

apps = pd.read_csv("googleplaystore.csv")
apps["Reviews"] = pd.to_numeric(apps["Reviews"], errors="coerce")
apps = apps.dropna(subset=["Rating","Reviews"]).query("Reviews > 0")
rating = apps["Rating"].values

# 1. IQR DETECTION
q1, q3 = np.percentile(rating, [25,75]); iqr = q3-q1
outlier_iqr = (rating < q1-1.5*iqr) | (rating > q3+1.5*iqr)
print(f"IQR outliers: {outlier_iqr.sum()} of {len(rating)}")

# Z-score comparison
z = zscore(rating); outlier_z = np.abs(z) > 2
print(f"Z-score (|z|>2): {outlier_z.sum()}")

fig,(ax1,ax2) = plt.subplots(1,2,figsize=(10,4))
ax1.scatter(range(len(rating)),rating,s=3,c=np.where(outlier_iqr,"#E53935","#1565C0"),alpha=0.3)
ax1.axhline(y=q1-1.5*iqr,color="#E53935",lw=1,ls="--"); ax1.axhline(y=q3+1.5*iqr,color="#E53935",lw=1,ls="--")
ax1.set_title(f"IQR: {outlier_iqr.sum()} outliers",fontweight="bold"); ax1.set_ylabel("Rating")
ax2.scatter(range(len(z)),z,s=3,c=np.where(outlier_z,"#E53935","#1565C0"),alpha=0.3)
ax2.axhline(y=2,color="#E53935",lw=1,ls="--"); ax2.axhline(y=-2,color="#E53935",lw=1,ls="--")
ax2.set_title(f"Z-Score: {outlier_z.sum()} outliers",fontweight="bold"); ax2.set_ylabel("Z")
for ax in [ax1,ax2]: ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.suptitle("IQR vs Z-Score Detection",fontweight="bold")
plt.tight_layout(); plt.savefig("output/iqr_vs_zscore_py.png",dpi=300); plt.close()

# 2. MAHALANOBIS — 2D detection
X = np.column_stack([np.log10(apps["Reviews"]+1), rating])
X = X[np.isfinite(X).all(axis=1)]
mu = np.mean(X,axis=0); cov = np.cov(X.T); cov_inv = np.linalg.inv(cov)
md = np.array([mahalanobis(xi,mu,cov_inv) for xi in X])
threshold = np.sqrt(chi2.ppf(0.95,df=2)); mask = md > threshold

fig,ax = plt.subplots(figsize=(7,5))
ax.scatter(X[~mask,0],X[~mask,1],s=5,c="#1565C0",alpha=0.2,label=f"Normal ({(~mask).sum()})")
ax.scatter(X[mask,0],X[mask,1],s=30,c="#E53935",edgecolors="white",lw=0.5,zorder=5,label=f"Outlier ({mask.sum()})")
ax.legend(fontsize=7); ax.set_xlabel("log10(Reviews)"); ax.set_ylabel("Rating")
ax.set_title(f"Mahalanobis: {mask.sum()} multivariate outliers",fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/mahalanobis_py.png",dpi=300); plt.close()

# 3. REGRESSION DIAGNOSTICS
import statsmodels.api as sm
Xr = sm.add_constant(np.log10(apps["Reviews"].values+1))
yr = rating
model = sm.OLS(yr,Xr).fit()
infl = model.get_influence()
cooks = infl.cooks_distance[0]

fig,axes = plt.subplots(2,2,figsize=(10,7))
axes[0,0].scatter(model.fittedvalues,model.resid,s=3,alpha=0.2,c="#1565C0")
axes[0,0].axhline(y=0,color="#888",ls="--"); axes[0,0].set_title("(a) Resid vs Fitted",fontweight="bold")
probplot(model.resid,dist="norm",plot=axes[0,1]); axes[0,1].set_title("(b) Q-Q Residuals",fontweight="bold")
std_resid = model.resid/np.std(model.resid)
axes[1,0].scatter(model.fittedvalues,np.sqrt(np.abs(std_resid)),s=3,alpha=0.2,c="#1565C0")
axes[1,0].set_title("(c) Scale-Location",fontweight="bold")
axes[1,1].bar(range(len(cooks)),cooks,width=0.3,color="#1565C0")
axes[1,1].axhline(y=4/len(cooks),color="#E53935",ls="--",label=f"4/n={4/len(cooks):.4f}")
axes[1,1].legend(fontsize=6); axes[1,1].set_title("(d) Cook's Distance",fontweight="bold")
for ax in axes.flatten(): ax.tick_params(labelsize=6); ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.suptitle("Regression Diagnostics: Rating ~ log(Reviews)",fontweight="bold")
plt.tight_layout(); plt.savefig("output/regdiag_py.png",dpi=300); plt.close()

# 4. FIT WITH AND WITHOUT
mask_infl = cooks > 4/len(cooks)
model2 = sm.OLS(yr[~mask_infl], Xr[~mask_infl]).fit()
print(f"\nFull: slope={model.params[1]:.4f}, R²={model.rsquared:.4f}")
print(f"Without {mask_infl.sum()} infl: slope={model2.params[1]:.4f}, R²={model2.rsquared:.4f}")
print("\nAll W04-M05 Python plots saved")
