"""W04-M01: Tukey's EDA Philosophy — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
from scipy.stats import probplot
os.makedirs("output",exist_ok=True); np.random.seed(42)

# Simulate Google Play data for sandbox
ratings=np.concatenate([np.random.normal(4.1,0.5,6000),np.random.normal(3.0,0.8,1500),np.random.uniform(1,5,500)]).clip(1,5)
n=len(ratings)

# 1. 4-PLOT
fig,axes=plt.subplots(2,2,figsize=(9,7))
axes[0,0].plot(range(n),ratings,linewidth=0.1,alpha=0.3,color="#1565C0")
axes[0,0].axhline(y=np.mean(ratings),color="#E53935",lw=1,ls="--"); axes[0,0].set_title("(a) Run Sequence",fontweight="bold")
axes[0,1].scatter(ratings[:-1],ratings[1:],s=2,c="#1565C0",alpha=0.1,edgecolors="none")
axes[0,1].set_title("(b) Lag-1 Plot",fontweight="bold")
axes[1,0].hist(ratings,bins=30,color="#1565C0",edgecolor="white",lw=0.3)
axes[1,0].set_title("(c) Histogram",fontweight="bold")
probplot(ratings,dist="norm",plot=axes[1,1]); axes[1,1].get_lines()[0].set_color("#1565C0"); axes[1,1].get_lines()[0].set_markersize(2)
axes[1,1].get_lines()[1].set_color("#E53935"); axes[1,1].set_title("(d) Q-Q Plot",fontweight="bold")
for ax in axes.flatten(): ax.tick_params(labelsize=6); ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.suptitle("Tukey's 4-Plot: Rating Data",fontweight="bold")
plt.tight_layout(); plt.savefig("output/four_plot_py.png",dpi=300); plt.close()

# 2. EDA FIRST LOOK
fig,axes=plt.subplots(1,3,figsize=(10,3.5))
axes[0].hist(ratings,bins=30,color="#2E7D32",edgecolor="white",lw=0.3); axes[0].set_title("Histogram",fontweight="bold")
parts=axes[1].violinplot([ratings],showmeans=True,showmedians=True)
parts["bodies"][0].set_facecolor("#2E7D32"); parts["bodies"][0].set_alpha(0.3); axes[1].set_title("Violin",fontweight="bold")
probplot(ratings,dist="norm",plot=axes[2]); axes[2].get_lines()[0].set_color("#2E7D32"); axes[2].get_lines()[0].set_markersize(2)
axes[2].get_lines()[1].set_color("#E53935"); axes[2].set_title("Q-Q Plot",fontweight="bold")
for ax in axes: ax.tick_params(labelsize=6); ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.suptitle("EDA First Look: hist + violin + Q-Q",fontweight="bold")
plt.tight_layout(); plt.savefig("output/eda_first_look_py.png",dpi=300); plt.close()

# 3. BOXENPLOT (letter-value equivalent)
try:
    import seaborn as sns
    fig,ax=plt.subplots(figsize=(4,5))
    sns.boxenplot(y=ratings,color="#1565C0",ax=ax)
    ax.set_title("sns.boxenplot() = Letter-Value",fontweight="bold")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    plt.tight_layout(); plt.savefig("output/boxenplot_py.png",dpi=300); plt.close()
    print("  boxenplot saved")
except: print("  seaborn boxenplot skipped")

# 4. INSPECT
print(f"\nShape: {n} observations")
print(f"Mean: {np.mean(ratings):.3f}, Median: {np.median(ratings):.3f}")
print(f"SD: {np.std(ratings):.3f}, IQR: {np.percentile(ratings,75)-np.percentile(ratings,25):.3f}")
print(f"Skew: {np.mean(((ratings-np.mean(ratings))/np.std(ratings))**3):.3f}")
print("\nAll W04-M01 Python plots saved")
