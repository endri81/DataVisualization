"""W03-M03: Comparisons — Bar, Lollipop, Cleveland Dot — Python — UNYT"""
import numpy as np, matplotlib.pyplot as plt, os
os.makedirs("output",exist_ok=True); np.random.seed(42)
cats=["FAMILY","GAME","TOOLS","PHOTOGRAPHY","PRODUCTIVITY","BUSINESS","MEDICAL","SOCIAL"]
vals=[1832,959,843,376,374,420,395,259]
idx=np.argsort(vals); sc=[cats[i] for i in idx]; sv=[vals[i] for i in idx]

# 1. BAR + LOLLIPOP + CLEVELAND side by side
fig,axes=plt.subplots(1,3,figsize=(14,5))
# Bar
c1=["#BBBBBB"]*8; c1[-1]="#1565C0"
axes[0].barh(sc,sv,color=c1,height=0.55); axes[0].set_title("(a) Bar",fontweight="bold")
for i,v in enumerate(sv): axes[0].text(v+15,i,f"{v:,}",va="center",fontsize=6,fontweight="bold",color="#1565C0" if i==7 else "#888")
# Lollipop
axes[1].hlines(range(8),0,sv,color="#BBBBBB",lw=1.5)
axes[1].scatter(sv,range(8),s=50,c=c1,zorder=5,edgecolors="white",lw=0.5); axes[1].set_title("(b) Lollipop",fontweight="bold")
for i,v in enumerate(sv): axes[1].text(v+15,i,f"{v:,}",va="center",fontsize=6,fontweight="bold",color="#1565C0" if i==7 else "#888")
axes[1].set_yticks(range(8)); axes[1].set_yticklabels(sc,fontsize=7)
# Dot
axes[2].scatter(sv,range(8),s=50,c="#1565C0",zorder=5,edgecolors="white",lw=0.5)
axes[2].axvline(x=np.mean(sv),color="#888",lw=0.8,ls="--"); axes[2].set_title("(c) Cleveland Dot",fontweight="bold")
axes[2].grid(axis="x",alpha=0.1); axes[2].set_yticks(range(8)); axes[2].set_yticklabels(sc,fontsize=7)
for i,v in enumerate(sv): axes[2].text(v+15,i,f"{v:,}",va="center",fontsize=6,fontweight="bold")
for ax in axes:
    for sp in ["top","right","left"]: ax.spines[sp].set_visible(False)
    ax.set_xticks([]); ax.tick_params(left=False,labelsize=7)
fig.suptitle("Three Comparison Charts: Decreasing Ink",fontsize=12,fontweight="bold")
plt.tight_layout(); plt.savefig("output/three_charts_py.png",dpi=300); plt.close()

# 2. DUMBBELL
cats2=["GAME","FAMILY","TOOLS","BUSINESS","MEDICAL"]; v20=[500,800,400,200,150]; v24=[959,1832,843,420,395]
idx2=np.argsort(v24); sc2=[cats2[i] for i in idx2]; s20=[v20[i] for i in idx2]; s24=[v24[i] for i in idx2]
fig,ax=plt.subplots(figsize=(8,4.5))
for i in range(len(sc2)):
    ax.plot([s20[i],s24[i]],[i,i],color="#CCCCCC",lw=2.5,solid_capstyle="round")
    ax.scatter([s20[i]],[i],s=60,c="#1565C0",zorder=5,edgecolors="white",lw=0.5)
    ax.scatter([s24[i]],[i],s=60,c="#E53935",zorder=5,edgecolors="white",lw=0.5)
    ax.text(s24[i]+20,i,f"+{s24[i]-s20[i]:,}",va="center",fontsize=7,fontweight="bold",color="#E53935")
ax.set_yticks(range(len(sc2))); ax.set_yticklabels(sc2,fontsize=8)
ax.scatter([],[],s=40,c="#1565C0",label="2020"); ax.scatter([],[],s=40,c="#E53935",label="2024")
ax.legend(fontsize=7); ax.set_title("Dumbbell: 2020 → 2024",fontweight="bold")
for sp in ["top","right","left"]: ax.spines[sp].set_visible(False)
ax.tick_params(left=False); plt.tight_layout(); plt.savefig("output/dumbbell_py.png",dpi=300); plt.close()

# 3. GROUPED + STACKED + 100%
cats3=["Everyone","Teen","Mature","10+"]; free=[52,11,4,8]; paid=[3,0.8,0.3,0.5]; x=np.arange(4); w=0.35
fig,axes=plt.subplots(1,3,figsize=(13,4))
axes[0].bar(x-w/2,free,w,label="Free",color="#1565C0",edgecolor="white")
axes[0].bar(x+w/2,paid,w,label="Paid",color="#E53935",edgecolor="white")
axes[0].set_xticks(x); axes[0].set_xticklabels(cats3,fontsize=7); axes[0].legend(fontsize=6); axes[0].set_title("Grouped",fontweight="bold")
axes[1].bar(cats3,free,0.5,label="Free",color="#1565C0",edgecolor="white")
axes[1].bar(cats3,paid,0.5,bottom=free,label="Paid",color="#E53935",edgecolor="white")
axes[1].legend(fontsize=6); axes[1].set_title("Stacked",fontweight="bold"); axes[1].tick_params(axis="x",labelsize=7)
tot=[f+p for f,p in zip(free,paid)]; fp=[f/t*100 for f,t in zip(free,tot)]; pp=[p/t*100 for p,t in zip(paid,tot)]
axes[2].bar(cats3,fp,0.5,label="Free",color="#1565C0",edgecolor="white")
axes[2].bar(cats3,pp,0.5,bottom=fp,label="Paid",color="#E53935",edgecolor="white")
axes[2].legend(fontsize=6); axes[2].set_ylabel("%"); axes[2].set_title("100% Stacked",fontweight="bold"); axes[2].tick_params(axis="x",labelsize=7)
for ax in axes: ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.tick_params(labelsize=6)
fig.suptitle("Three Bar Variants",fontsize=11,fontweight="bold"); plt.tight_layout()
plt.savefig("output/bar_variants_py.png",dpi=300); plt.close()
print("All W03-M03 Python plots saved")
