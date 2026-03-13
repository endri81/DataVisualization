"""W02-M03: ggplot2 Deep Dive — Python Script — UNYT Tirana"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
os.makedirs("output", exist_ok=True); np.random.seed(42)

# 1. MULTI-AESTHETIC (bubble chart)
n=80; gdp=np.random.uniform(10,100,n); le=50+0.3*gdp+np.random.normal(0,8,n)
pop=np.random.uniform(1e6,5e8,n); cont=np.random.choice(["Africa","Asia","Europe"],n)
pal={"Africa":"#1565C0","Asia":"#E53935","Europe":"#2E7D32"}
fig,ax=plt.subplots(figsize=(7,5))
for g,c in pal.items():
    m=cont==g; ax.scatter(gdp[m],le[m],s=pop[m]/3e6,c=c,alpha=0.5,edgecolors="white",linewidth=0.5,label=g)
ax.legend(fontsize=7,title="Continent"); ax.set_xlabel("GDP ($K)"); ax.set_ylabel("Life Expectancy")
ax.set_title("Bubble: 4 variables (x, y, color, size)",fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/multi_aes_py.png",dpi=300); plt.close()

# 2. OVERPLOTTING — 4 panels
np.random.seed(55); n2=2000; x=np.random.normal(50,15,n2); y=0.3*x+np.random.normal(0,8,n2)
fig,axes=plt.subplots(1,4,figsize=(14,3.5))
axes[0].scatter(x,y,s=3,c="#1565C0"); axes[0].set_title("Overplotting",fontsize=8,fontweight="bold",color="#C62828")
axes[1].scatter(x,y,s=3,c="#1565C0",alpha=0.05); axes[1].set_title("alpha=0.05",fontsize=8,fontweight="bold")
axes[2].scatter(x+np.random.normal(0,1,n2),y+np.random.normal(0,1,n2),s=3,c="#1565C0",alpha=0.08)
axes[2].set_title("jitter + alpha",fontsize=8,fontweight="bold")
axes[3].hexbin(x,y,gridsize=20,cmap="YlGnBu",mincnt=1); axes[3].set_title("hexbin",fontsize=8,fontweight="bold")
for ax in axes: ax.tick_params(labelsize=5); ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.suptitle("Overplotting Solutions",fontsize=11,fontweight="bold"); plt.tight_layout()
plt.savefig("output/overplotting_py.png",dpi=300); plt.close()

# 3. LOLLIPOP
cats=["Compact","Midsize","SUV","Pickup","Minivan"]; vals=[28,24,18,16,22]
idx=np.argsort(vals); sc=[cats[i] for i in idx]; sv=[vals[i] for i in idx]
fig,ax=plt.subplots(figsize=(6,4))
ax.hlines(y=range(len(sc)),xmin=0,xmax=sv,color="#BBBBBB",linewidth=1.5)
ax.scatter(sv,range(len(sc)),s=60,c="#1565C0",zorder=5,edgecolors="white",linewidth=0.5)
ax.set_yticks(range(len(sc))); ax.set_yticklabels(sc)
ax.set_title("Lollipop Chart",fontweight="bold"); ax.set_xlabel("Mean MPG")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/lollipop_py.png",dpi=300); plt.close()

# 4. DUMBBELL
cats2=["Economy","Midsize","Compact","SUV","Pickup"]; v2008=[26,24,28,18,16]; v2024=[32,30,35,24,22]
idx2=np.argsort(v2024); sc2=[cats2[i] for i in idx2]; s08=[v2008[i] for i in idx2]; s24=[v2024[i] for i in idx2]
fig,ax=plt.subplots(figsize=(7,4))
for i,(c,a,b) in enumerate(zip(sc2,s08,s24)):
    ax.plot([a,b],[i,i],color="#CCCCCC",linewidth=2,solid_capstyle="round")
    ax.scatter([a],[i],s=60,c="#1565C0",zorder=5,edgecolors="white",linewidth=0.5)
    ax.scatter([b],[i],s=60,c="#E53935",zorder=5,edgecolors="white",linewidth=0.5)
ax.set_yticks(range(len(sc2))); ax.set_yticklabels(sc2)
ax.scatter([],[],s=40,c="#1565C0",label="2008"); ax.scatter([],[],s=40,c="#E53935",label="2024")
ax.legend(fontsize=7); ax.set_title("Dumbbell: 2008 vs 2024",fontweight="bold"); ax.set_xlabel("MPG")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/dumbbell_py.png",dpi=300); plt.close()

print("All W02-M03 Python plots saved")
