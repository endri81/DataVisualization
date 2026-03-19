"""W05-M01: High-Dimensional Data — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, seaborn as sns, os
os.makedirs("output",exist_ok=True); np.random.seed(42); n=2000
fico=np.random.normal(700,50,n).clip(500,850); rate=12-0.01*fico+np.random.normal(0,1,n)
amount=np.random.uniform(5000,50000,n); tier=np.digitize(fico,[0,620,680,720,760,900])
cartype=np.random.choice(["New","Used"],n,p=[0.6,0.4])
ecar=pd.DataFrame({"FICO":fico,"Rate":rate,"Amount":amount,"Tier":tier,"CarType":cartype})

# 1. Multi-encoded scatter
fig,ax=plt.subplots(figsize=(8,6))
for ct,marker in [("New","o"),("Used","s")]:
    m=ecar["CarType"]==ct
    sc=ax.scatter(ecar.loc[m,"FICO"],ecar.loc[m,"Rate"],c=ecar.loc[m,"Tier"],s=ecar.loc[m,"Amount"]/300,
        marker=marker,alpha=0.4,cmap="viridis",label=ct,vmin=1,vmax=5)
plt.colorbar(sc,label="Tier"); ax.legend(title="Car Type",fontsize=7)
ax.set_xlabel("FICO"); ax.set_ylabel("Rate (%)"); ax.set_title("5 Variables, 1 Scatter",fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/multi_scatter_py.png",dpi=300); plt.close()

# 2. Hexbin
fig,ax=plt.subplots(figsize=(7,5))
hb=ax.hexbin(ecar["FICO"],ecar["Rate"],gridsize=30,cmap="viridis",mincnt=1)
plt.colorbar(hb,label="Count"); ax.set_title("Hexbin: Aggregated Scatter",fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/hexbin_py.png",dpi=300); plt.close()

# 3. Jointplot with marginals
g=sns.jointplot(data=ecar,x="FICO",y="Rate",hue="CarType",
    palette={"New":"#1565C0","Used":"#E53935"},kind="scatter",height=6,
    joint_kws={"s":10,"alpha":0.3})
g.fig.suptitle("Jointplot: Scatter + Marginal Histograms",fontweight="bold",y=1.02)
plt.savefig("output/jointplot_py.png",dpi=300,bbox_inches="tight"); plt.close()

# 4. 2D KDE
fig,ax=plt.subplots(figsize=(7,5))
sns.kdeplot(data=ecar,x="FICO",y="Rate",fill=True,cmap="Blues",levels=10,ax=ax)
ax.set_title("2D KDE: Density Contours",fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/kde2d_py.png",dpi=300); plt.close()

print("All W05-M01 Python plots saved")
