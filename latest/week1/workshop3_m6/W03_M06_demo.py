"""W03-M06: Rankings — Slope, Bump & Waterfall — Python — UNYT"""
import numpy as np, matplotlib.pyplot as plt, os
os.makedirs("output",exist_ok=True); np.random.seed(42)

cats=["FAMILY","GAME","TOOLS","PHOTOGRAPHY","PRODUCTIVITY","BUSINESS"]
v2020=[800,500,400,200,180,350]; v2024=[1832,959,843,376,374,420]
colors=["#1565C0","#E53935","#2E7D32","#E65100","#7B1FA2","#00695C"]

# 1. SLOPEGRAPH
fig,ax=plt.subplots(figsize=(7,5.5))
for i,(cat,v0,v1,c) in enumerate(zip(cats,v2020,v2024,colors)):
    lw=2.5 if cat=="FAMILY" else 1.2; alpha=1.0 if cat=="FAMILY" else 0.35
    ax.plot([0,1],[v0,v1],"-o",color=c,linewidth=lw,markersize=6,alpha=alpha)
    ax.text(-0.08,v0,f"{cat} ({v0:,})",ha="right",va="center",fontsize=7,fontweight="bold" if cat=="FAMILY" else "normal",color=c)
    ax.text(1.08,v1,f"{cat} ({v1:,})",ha="left",va="center",fontsize=7,fontweight="bold" if cat=="FAMILY" else "normal",color=c)
ax.set_xticks([0,1]); ax.set_xticklabels(["2020","2024"],fontsize=11,fontweight="bold")
ax.set_xlim(-0.4,1.4); ax.set_title("Slopegraph: FAMILY Surged to #1",fontweight="bold")
for sp in ax.spines.values(): sp.set_visible(False)
ax.set_yticks([]); ax.tick_params(bottom=False)
plt.tight_layout(); plt.savefig("output/slopegraph_py.png",dpi=300); plt.close()

# 2. BUMP CHART
years=[2019,2020,2021,2022,2023,2024]
ranks={"FAMILY":[2,2,1,1,1,1],"GAME":[1,1,2,2,2,2],"TOOLS":[3,3,3,3,3,3],
       "BUSINESS":[5,4,4,5,4,4],"PHOTOGRAPHY":[4,5,5,4,5,5],"PRODUCTIVITY":[6,6,6,6,6,6]}
fig,ax=plt.subplots(figsize=(9,5))
for (cat,rk),c in zip(ranks.items(),colors):
    hl=cat in ["FAMILY","GAME"]
    ax.plot(years,rk,"-o",color=c,linewidth=3 if hl else 1.2,alpha=1.0 if hl else 0.35,markersize=7 if hl else 4)
    ax.text(2024.2,rk[-1],cat,fontsize=7,fontweight="bold" if hl else "normal",color=c,va="center")
ax.invert_yaxis(); ax.set_yticks(range(1,7)); ax.set_yticklabels([f"#{i}" for i in range(1,7)])
ax.set_title("Bump: FAMILY Overtook GAME in 2021",fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.grid(axis="y",alpha=0.1)
ax.set_xlim(2018.5,2025.5); ax.tick_params(labelsize=7)
plt.tight_layout(); plt.savefig("output/bump_py.png",dpi=300); plt.close()

# 3. WATERFALL
items=["Start","Product A","Product B","Product C","Returns","Discounts","End"]
values=[0,450,280,190,-85,-35,0]; running=[800,1250,1530,1720,1635,1600,1600]
fig,ax=plt.subplots(figsize=(9,5))
for i in range(len(items)):
    if items[i] in ["Start","End"]:
        ax.bar(i,running[i],width=0.5,color="#1565C0",edgecolor="white",linewidth=1.5)
        ax.text(i,running[i]+20,f"${running[i]:,}",ha="center",fontsize=8,fontweight="bold",color="#1565C0")
    else:
        bottom=min(running[i-1],running[i]); height=abs(values[i])
        color="#2E7D32" if values[i]>0 else "#E53935"
        ax.bar(i,height,bottom=bottom,width=0.5,color=color,edgecolor="white",linewidth=1.5)
        sign="+" if values[i]>0 else ""
        ax.text(i,running[i]+(20 if values[i]>0 else -30),f"{sign}${values[i]:,}",ha="center",fontsize=7,fontweight="bold",color=color)
    if i<len(items)-1: ax.plot([i+0.25,i+0.75],[running[i],running[i]],color="#888",lw=0.8,ls="--")
ax.set_xticks(range(len(items))); ax.set_xticklabels(items,fontsize=8,rotation=20,ha="right")
ax.set_title("Waterfall: $800 Start → $1,600 End",fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.tick_params(labelsize=7)
plt.tight_layout(); plt.savefig("output/waterfall_py.png",dpi=300); plt.close()
print("All W03-M06 Python plots saved")
