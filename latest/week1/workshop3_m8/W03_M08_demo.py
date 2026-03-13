"""W03-M08: Small Multiples & Faceted Displays — Python — UNYT"""
import numpy as np, matplotlib.pyplot as plt, os
from matplotlib.gridspec import GridSpec
os.makedirs("output",exist_ok=True); np.random.seed(42)

# 1. SPAGHETTI → SMALL MULTIPLES
regions=["North","South","East","West","Central","Coastal"]
colors=["#1565C0","#E53935","#2E7D32","#E65100","#7B1FA2","#00695C"]
months=np.arange(1,13); all_data={}
for r in regions: all_data[r]=np.cumsum(np.random.normal(2,6,12))+np.random.uniform(30,80)

fig,(ax1,ax2_h)=plt.subplots(1,2,figsize=(13,4.5),gridspec_kw={"width_ratios":[1,1.8]})
for r,c in zip(regions,colors): ax1.plot(months,all_data[r],color=c,lw=1.2,label=r)
ax1.legend(fontsize=5,ncol=2); ax1.set_title("Spaghetti",fontweight="bold",color="#C62828")
ax1.spines["top"].set_visible(False); ax1.spines["right"].set_visible(False)
ax2_h.axis("off"); ax2_h.set_title("Small Multiples",fontweight="bold",color="#1565C0")
inner=GridSpec(2,3,left=0.55,right=0.98,bottom=0.12,top=0.80,wspace=0.2,hspace=0.4,figure=fig)
ymin=min(min(d) for d in all_data.values())-5; ymax=max(max(d) for d in all_data.values())+5
for i,(r,c) in enumerate(zip(regions,colors)):
    ax=fig.add_subplot(inner[i//3,i%3])
    ax.plot(months,all_data[r],color=c,lw=1.5); ax.fill_between(months,all_data[r],alpha=0.06,color=c)
    ax.set_title(r,fontsize=7,fontweight="bold",color=c); ax.set_ylim(ymin,ymax)
    ax.set_xticks([1,6,12]); ax.set_xticklabels(["J","J","D"],fontsize=4)
    ax.tick_params(labelsize=4); ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.suptitle("Spaghetti → Small Multiples",fontweight="bold")
fig.savefig("output/spag_to_sm_py.png",dpi=300,bbox_inches="tight"); plt.close()

# 2. HETEROGENEOUS DASHBOARD — GridSpec
fig=plt.figure(figsize=(13,8)); gs=GridSpec(2,3,figure=fig,hspace=0.4,wspace=0.35)
cats=["FAMILY","GAME","TOOLS","BUS","MED","SOCIAL"]; vals=[1832,959,843,420,395,259]
idx=np.argsort(vals); sc=[cats[i] for i in idx]; sv=[vals[i] for i in idx]
# (a) bar
ax=fig.add_subplot(gs[0,0]); cl=["#BBBBBB"]*6; cl[-1]="#1565C0"
ax.barh(sc,sv,color=cl,height=0.55); ax.set_title("(a) Category Counts",fontsize=8,fontweight="bold")
for sp in ["top","right","left"]: ax.spines[sp].set_visible(False)
ax.set_xticks([]); ax.tick_params(left=False,labelsize=6)
# (b) histogram
ax=fig.add_subplot(gs[0,1]); ratings=np.random.normal(4.1,0.55,2000).clip(1,5)
ax.hist(ratings,bins=30,color="#1565C0",edgecolor="white",lw=0.3); ax.set_title("(b) Rating Dist.",fontsize=8,fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.tick_params(labelsize=6)
# (c) scatter
ax=fig.add_subplot(gs[0,2]); rev=10**np.random.uniform(1,6,300); rat=(3.5+0.15*np.log10(rev)+np.random.normal(0,0.5,300)).clip(1,5)
ax.scatter(rev,rat,s=5,c="#1565C0",alpha=0.2,edgecolors="none"); ax.set_xscale("log")
ax.set_title("(c) Reviews vs Rating",fontsize=8,fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.tick_params(labelsize=6)
# (d) wide line (spans 2 cols)
ax=fig.add_subplot(gs[1,:2]); years=np.arange(2015,2025); trend=np.array([120,135,128,142,155,170,145,180,195,220])
ax.plot(years,trend,"-o",color="#1565C0",lw=1.5,markersize=4)
ax.fill_between(years,trend-15,trend+15,alpha=0.1,color="#1565C0")
ax.set_title("(d) Revenue Trend ± CI (wide)",fontsize=8,fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.tick_params(labelsize=6)
# (e) pointrange
ax=fig.add_subplot(gs[1,2]); means=[4.05,4.18,4.12,4.22,3.95,4.30]; ses=[0.02,0.01,0.02,0.02,0.03,0.02]
idx2=np.argsort(means); sm=[means[i] for i in idx2]; ss=[ses[i] for i in idx2]; sl=[cats[i] for i in idx2]
ax.errorbar(sm,range(6),xerr=[1.96*s for s in ss],fmt="o",color="#1565C0",markersize=5,capsize=4,lw=1.5)
ax.set_yticks(range(6)); ax.set_yticklabels(sl,fontsize=6); ax.set_title("(e) Mean ± 95% CI",fontsize=8,fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.tick_params(labelsize=6)
fig.suptitle("Heterogeneous Dashboard: 5 Chart Types via GridSpec",fontsize=12,fontweight="bold")
fig.text(0.5,0.01,"Source: Google Play Store | UNYT",ha="center",fontsize=7,fontstyle="italic",color="#888")
fig.savefig("output/dashboard_gridspec_py.pdf",bbox_inches="tight")
fig.savefig("output/dashboard_gridspec_py.png",dpi=300,bbox_inches="tight"); plt.close()

# 3. SUBPLOT_MOSAIC
try:
    fig,axes=plt.subplot_mosaic([["bar","bar","scatter"],["hist","box","scatter"]],figsize=(12,7))
    axes["bar"].barh(sc,sv,color="#1565C0",height=0.5); axes["bar"].set_title("(a) Bar (wide)")
    x2=np.random.uniform(1,6,80); y2=0.5*x2+np.random.normal(0,0.8,80)
    axes["scatter"].scatter(x2,y2,s=10,c="#E53935",alpha=0.5); axes["scatter"].set_title("(b) Scatter (tall)")
    axes["hist"].hist(ratings[:500],bins=20,color="#2E7D32",edgecolor="white",lw=0.3); axes["hist"].set_title("(c) Hist")
    free=np.random.normal(4.1,0.55,200).clip(1,5); paid=np.random.normal(4.25,0.45,50).clip(1,5)
    bp=axes["box"].boxplot([free,paid],labels=["Free","Paid"],patch_artist=True,widths=0.4)
    bp["boxes"][0].set_facecolor("#BBDEFB"); bp["boxes"][1].set_facecolor("#FFCDD2")
    axes["box"].set_title("(d) Box")
    for ax in axes.values(): ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.tick_params(labelsize=6)
    fig.suptitle("subplot_mosaic: Named ASCII Layout",fontweight="bold")
    plt.tight_layout(); plt.savefig("output/mosaic_py.png",dpi=300); plt.close()
except Exception as e: print(f"  subplot_mosaic: {e}")

print("All W03-M08 Python plots saved")
