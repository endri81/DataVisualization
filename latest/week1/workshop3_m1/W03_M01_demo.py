"""W03-M01: Distributions — Histograms, Density, Ridgeline — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
from scipy.stats import gaussian_kde
os.makedirs("output", exist_ok=True); np.random.seed(42)
ratings=np.concatenate([np.random.normal(4.1,0.5,6000),np.random.normal(3.0,0.8,1500),np.random.uniform(1,5,500)]).clip(1,5)

# 1. BIN WIDTH
fig,axes=plt.subplots(1,4,figsize=(14,3.5))
for ax,b in zip(axes,[5,15,40,100]):
    ax.hist(ratings,bins=b,color="#1565C0",edgecolor="white",linewidth=0.3)
    ax.set_title(f"bins={b}",fontsize=9,fontweight="bold"); ax.tick_params(labelsize=6)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.suptitle("Bin Width Matters",fontsize=11,fontweight="bold"); plt.tight_layout()
plt.savefig("output/bin_width_py.png",dpi=300); plt.close()

# 2. OVERLAY
fig,ax=plt.subplots(figsize=(7,4.5))
ax.hist(ratings,bins=35,density=True,color="#1565C0",edgecolor="white",linewidth=0.3,alpha=0.5)
xs=np.linspace(0.5,5.5,200); kde=gaussian_kde(ratings)
ax.plot(xs,kde(xs),color="#E53935",lw=2,label="KDE")
ax.axvline(x=np.mean(ratings),color="#2E7D32",lw=1.5,ls="--",label=f"Mean: {np.mean(ratings):.2f}")
ax.axvline(x=np.median(ratings),color="#E65100",lw=1.5,ls=":",label=f"Median: {np.median(ratings):.2f}")
ax.legend(fontsize=8); ax.set_title("Histogram + KDE + Central Tendency",fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.tick_params(labelsize=7)
plt.tight_layout(); plt.savefig("output/overlay_py.png",dpi=300); plt.close()

# 3. GROUPED DENSITY
np.random.seed(55)
free=np.random.normal(4.1,0.5,2000).clip(1,5); paid=np.random.normal(4.3,0.4,500).clip(1,5)
fig,ax=plt.subplots(figsize=(7,4.5)); xs=np.linspace(1,5,200)
for data,name,c in [(free,"Free","#1565C0"),(paid,"Paid","#E53935")]:
    kde=gaussian_kde(data); ax.fill_between(xs,kde(xs),alpha=0.15,color=c)
    ax.plot(xs,kde(xs),color=c,lw=2,label=name)
ax.legend(fontsize=9); ax.set_title("Grouped Density: Free vs Paid",fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/grouped_density_py.png",dpi=300); plt.close()

# 4. RIDGELINE (manual offset)
np.random.seed(77); cats=["Everyone","Teen","Mature 17+","Everyone 10+","Unrated"]
colors=["#1565C0","#2E7D32","#E53935","#E65100","#7B1FA2"]
fig,ax=plt.subplots(figsize=(7,5.5)); xs=np.linspace(1,5,200); offset=0
for i,(cat,c) in enumerate(zip(cats,colors)):
    data=np.random.normal(4.0-0.15*i,0.4+0.05*i,800).clip(1,5)
    kde=gaussian_kde(data); y=kde(xs)
    ax.fill_between(xs,offset,y+offset,alpha=0.25,color=c)
    ax.plot(xs,y+offset,color=c,lw=1.5)
    ax.text(0.8,offset+0.1,cat,fontsize=8,fontweight="bold",color=c,va="bottom")
    offset+=max(y)*0.7
ax.set_xlabel("Rating"); ax.set_yticks([]); ax.set_title("Ridgeline Plot",fontweight="bold")
for sp in ["top","right","left"]: ax.spines[sp].set_visible(False)
plt.tight_layout(); plt.savefig("output/ridgeline_py.png",dpi=300); plt.close()

# 5. BANDWIDTH
fig,axes=plt.subplots(1,3,figsize=(12,4)); bws=[0.05,0.3,1.0]
titles=["bw=0.05 (undersmoothed)","bw=0.3 (good)","bw=1.0 (oversmoothed)"]
for ax,bw,t in zip(axes,bws,titles):
    kde=gaussian_kde(ratings,bw_method=bw)
    ax.fill_between(xs,kde(xs),alpha=0.15,color="#1565C0"); ax.plot(xs,kde(xs),color="#1565C0",lw=2)
    ax.set_title(t,fontsize=9,fontweight="bold"); ax.tick_params(labelsize=6)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.suptitle("Bandwidth Controls Smoothness",fontsize=11,fontweight="bold"); plt.tight_layout()
plt.savefig("output/bandwidth_py.png",dpi=300); plt.close()

print("All W03-M01 Python plots saved")
