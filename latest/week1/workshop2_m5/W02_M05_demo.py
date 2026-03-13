"""W02-M05: Faceting & Small Multiples — Python — UNYT Tirana"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
from matplotlib.gridspec import GridSpec
os.makedirs("output", exist_ok=True); np.random.seed(42)

# 1. FACET_WRAP equivalent (plt.subplots with loop)
np.random.seed(33)
regions=["North","South","East","West","Central","Coastal"]
months=np.arange(1,13)
fig,axes=plt.subplots(2,3,figsize=(10,5.5),sharey=True)
for ax,r in zip(axes.flatten(),regions):
    d=np.cumsum(np.random.normal(2,6,12))+np.random.uniform(30,80)
    ax.plot(months,d,color="#1565C0",linewidth=1.5)
    ax.fill_between(months,d,alpha=0.06,color="#1565C0")
    ax.set_title(r,fontsize=9,fontweight="bold")
    ax.set_xticks([1,6,12]); ax.set_xticklabels(["Jan","Jun","Dec"],fontsize=6)
    ax.tick_params(labelsize=6); ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.suptitle("facet_wrap equivalent: plt.subplots(2,3, sharey=True)",fontsize=11,fontweight="bold")
plt.tight_layout(); plt.savefig("output/facet_wrap_py.png",dpi=300); plt.close()

# 2. FACET_GRID equivalent
np.random.seed(44)
types=["Free","Paid"]; ratings=["Everyone","Teen","Mature"]
fig,axes=plt.subplots(2,3,figsize=(10,5.5),sharex=True,sharey=True)
for i,t in enumerate(types):
    for j,r in enumerate(ratings):
        ax=axes[i,j]; data=np.random.normal(4.0+0.1*j-0.05*i,0.5,200).clip(1,5)
        ax.hist(data,bins=20,color="#1565C0" if t=="Free" else "#E53935",edgecolor="white",linewidth=0.3,alpha=0.7)
        if i==0: ax.set_title(r,fontsize=9,fontweight="bold")
        if j==0: ax.set_ylabel(t,fontsize=9,fontweight="bold",rotation=0,labelpad=35)
        ax.tick_params(labelsize=6); ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.suptitle("facet_grid equivalent: rows=Type, cols=Content_Rating",fontsize=11,fontweight="bold")
plt.tight_layout(); plt.savefig("output/facet_grid_py.png",dpi=300); plt.close()

# 3. FIXED vs FREE scales
np.random.seed(55)
groups={"A":(50,10),"B":(200,30),"C":(20,5)}
fig,axes_row=plt.subplots(1,2,figsize=(11,4))
# Fixed
axes_row[0].set_title('scales="fixed"',fontweight="bold"); axes_row[0].axis("off")
inner1=GridSpec(1,3,left=0.03,right=0.47,bottom=0.15,top=0.78,wspace=0.15,figure=fig)
for i,(g,(mu,sd)) in enumerate(groups.items()):
    ax=fig.add_subplot(inner1[0,i]); data=np.random.normal(mu,sd,100)
    ax.hist(data,bins=15,color="#1565C0",edgecolor="white",linewidth=0.3); ax.set_ylim(0,35)
    ax.set_title(f"Group {g}",fontsize=7,fontweight="bold"); ax.tick_params(labelsize=5)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
# Free
axes_row[1].set_title('scales="free"',fontweight="bold"); axes_row[1].axis("off")
inner2=GridSpec(1,3,left=0.55,right=0.98,bottom=0.15,top=0.78,wspace=0.15,figure=fig)
np.random.seed(55)
for i,(g,(mu,sd)) in enumerate(groups.items()):
    ax=fig.add_subplot(inner2[0,i]); data=np.random.normal(mu,sd,100)
    ax.hist(data,bins=15,color="#2E7D32",edgecolor="white",linewidth=0.3)
    ax.set_title(f"Group {g}",fontsize=7,fontweight="bold"); ax.tick_params(labelsize=5)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.suptitle("Fixed vs Free Scales",fontsize=11,fontweight="bold")
fig.savefig("output/fixed_vs_free_py.png",dpi=300,bbox_inches="tight"); plt.close()

# 4. FACET + SMOOTH per panel
np.random.seed(77)
groups2=["Compact","Midsize","SUV","Pickup"]
fig,axes=plt.subplots(1,4,figsize=(14,3.5))
for ax,g in zip(axes,groups2):
    x=np.random.uniform(1,6,40); y=0.5*x+np.random.normal(0,0.8,40)
    ax.scatter(x,y,s=12,c="#1565C0",alpha=0.5,edgecolors="none")
    m,b=np.polyfit(x,y,1); xs=np.linspace(1,6,50)
    ax.plot(xs,m*xs+b,color="#E53935",linewidth=1.5)
    ax.fill_between(xs,m*xs+b-0.8,m*xs+b+0.8,alpha=0.08,color="#E53935")
    ax.set_title(g,fontsize=9,fontweight="bold"); ax.tick_params(labelsize=5)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.suptitle("Facet + Smooth: Independent Trend per Panel",fontsize=11,fontweight="bold")
plt.tight_layout(); plt.savefig("output/facet_smooth_py.png",dpi=300); plt.close()

print("All W02-M05 Python plots saved")
