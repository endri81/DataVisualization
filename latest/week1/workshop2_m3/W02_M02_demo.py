"""
Workshop 2 — Module 2: Wickham's Layered Grammar & ggplot2
Python Demonstration Script — UNYT Tirana
"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
os.makedirs("output", exist_ok=True)
np.random.seed(22)

# 1. MAPPING vs SETTING
x=np.random.uniform(1,6,60); y=0.5*x+np.random.normal(0,0.8,60); grp=np.random.choice(["A","B"],60)
fig,(ax1,ax2)=plt.subplots(1,2,figsize=(10,4))
for g,c in [("A","#1565C0"),("B","#E53935")]:
    mask=grp==g; ax1.scatter(x[mask],y[mask],s=30,c=c,alpha=0.6,edgecolors="white",linewidth=0.3,label=g)
ax1.legend(fontsize=7); ax1.set_title("Mapping: color=group",fontweight="bold")
ax1.spines["top"].set_visible(False); ax1.spines["right"].set_visible(False)
ax2.scatter(x,y,s=30,c="#E53935",alpha=0.6,edgecolors="white",linewidth=0.3)
ax2.set_title("Setting: color='red'",fontweight="bold")
ax2.spines["top"].set_visible(False); ax2.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/mapping_vs_setting_py.png",dpi=300); plt.close()

# 2. POSITION ADJUSTMENTS
cats=["A","B","C"]; free=[50,35,20]; paid=[10,15,8]; xp=np.arange(3); w=0.35
fig,axes=plt.subplots(1,4,figsize=(14,3.5))
axes[0].bar(cats,free,0.5,label="Free",color="#1565C0",edgecolor="white")
axes[0].bar(cats,paid,0.5,bottom=free,label="Paid",color="#E53935",edgecolor="white")
axes[0].set_title('"stack"',fontweight="bold"); axes[0].legend(fontsize=6)
axes[1].bar(xp-w/2,free,w,label="Free",color="#1565C0",edgecolor="white")
axes[1].bar(xp+w/2,paid,w,label="Paid",color="#E53935",edgecolor="white")
axes[1].set_xticks(xp); axes[1].set_xticklabels(cats); axes[1].set_title('"dodge"',fontweight="bold"); axes[1].legend(fontsize=6)
tot=[f+p for f,p in zip(free,paid)]; fp=[f/t*100 for f,t in zip(free,tot)]; pp=[p/t*100 for p,t in zip(paid,tot)]
axes[2].bar(cats,fp,0.5,label="Free",color="#1565C0",edgecolor="white")
axes[2].bar(cats,pp,0.5,bottom=fp,label="Paid",color="#E53935",edgecolor="white")
axes[2].set_title('"fill"',fontweight="bold"); axes[2].legend(fontsize=6)
cj=np.random.choice(["A","B","C"],60); vj=np.random.normal(50,12,60)
xj=np.array([["A","B","C"].index(c) for c in cj])+np.random.uniform(-0.15,0.15,60)
axes[3].scatter(xj,vj,s=12,c="#1565C0",alpha=0.5,edgecolors="none"); axes[3].set_xticks([0,1,2]); axes[3].set_xticklabels(["A","B","C"])
axes[3].set_title('"jitter"',fontweight="bold")
for ax in axes: ax.tick_params(labelsize=6); ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.suptitle("Position Adjustments",fontsize=11,fontweight="bold"); plt.tight_layout()
plt.savefig("output/positions_py.png",dpi=300); plt.close()

# 3. COMPLETE EXAMPLE
n=150; x2=np.random.uniform(1,6,n); y2=0.5*x2+np.random.normal(0,0.8,n)
cls=np.random.choice(["compact","midsize","suv","pickup"],n)
pal={"compact":"#1f77b4","midsize":"#2ca02c","suv":"#d62728","pickup":"#ff7f0e"}
fig,ax=plt.subplots(figsize=(7,5))
for c,col in pal.items():
    mask=cls==c; ax.scatter(x2[mask],y2[mask],s=30,c=col,alpha=0.6,edgecolors="white",linewidth=0.3,label=c)
m,b=np.polyfit(x2,y2,1); xs=np.linspace(1,6,50)
ax.plot(xs,m*xs+b,color="grey",linewidth=1.5,linestyle="--")
ax.fill_between(xs,m*xs+b-0.8,m*xs+b+0.8,alpha=0.08,color="grey")
ax.set_xlabel("Displacement (L)"); ax.set_ylabel("Highway MPG")
ax.set_title("Complete Layered Example",fontweight="bold")
ax.legend(fontsize=7,title="Class"); ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.set_facecolor("#FAFAFA"); ax.grid(alpha=0.15); plt.tight_layout()
plt.savefig("output/complete_py.png",dpi=300); plt.close()

print("All W02-M02 Python plots saved")
