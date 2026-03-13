"""W02-M08: labs(), Annotations & Storytelling — Python — UNYT Tirana"""
import numpy as np, matplotlib.pyplot as plt, os
os.makedirs("output", exist_ok=True); np.random.seed(42)

# 1. ANNOTATION TYPES — all four on one chart
np.random.seed(33); months=np.arange(1,13); revenue=np.cumsum(np.random.normal(5,8,12))+200
mean_rev=np.mean(revenue); peak_idx=np.argmax(revenue)

fig,ax=plt.subplots(figsize=(8,5))
ax.plot(months,revenue,"-o",color="#1565C0",linewidth=2,markersize=6)
# Reference line
ax.axhline(y=mean_rev,color="grey",lw=1,ls="--")
ax.text(12.5,mean_rev,f"Mean: ${mean_rev:.0f}K",fontsize=7,color="grey",fontweight="bold",va="center")
# Target band
ax.axhspan(210,230,alpha=0.08,color="#2E7D32")
ax.text(0.5,220,"Target",fontsize=7,color="#2E7D32",fontweight="bold")
# Event marker
ax.axvline(x=6.5,color="#E65100",lw=0.8,ls=":")
ax.text(6.7,min(revenue)-3,"H1 | H2",fontsize=7,color="#E65100")
# Peak callout
ax.annotate(f"Peak: ${revenue[peak_idx]:.0f}K",xy=(months[peak_idx],revenue[peak_idx]),
    xytext=(months[peak_idx]+1.5,revenue[peak_idx]+15),fontsize=9,fontweight="bold",color="#E53935",
    arrowprops=dict(arrowstyle="->",color="#E53935",lw=1.5))
ax.set_xlabel("Month"); ax.set_ylabel("Revenue ($K)")
ax.set_title("Four Annotation Types on One Chart",fontsize=12,fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.tick_params(labelsize=7); ax.grid(alpha=0.1)
plt.tight_layout(); plt.savefig("output/annotations_py.png",dpi=300); plt.close()

# 2. STORYTELLING LAYERS
np.random.seed(77); years=np.arange(2015,2025); rev2=np.array([120,135,128,142,155,170,145,180,195,220])
fig,axes=plt.subplots(2,2,figsize=(10,7))
titles=["1. Show the data","2. + Trend line","3. + Key events","4. + Title = finding"]
for i,ax in enumerate(axes.flatten()):
    ax.plot(years,rev2,"-o",color="#1565C0",linewidth=1.5,markersize=4)
    if i>=1:
        m,b=np.polyfit(years,rev2,1); xs=np.linspace(2015,2024,50)
        ax.plot(xs,m*xs+b,color="grey",linewidth=1,linestyle="--")
    if i>=2:
        ax.axvline(x=2020,color="#E53935",linewidth=1,linestyle=":")
        ax.text(2020.2,150,"COVID",fontsize=7,color="#E53935",fontweight="bold")
    if i>=3:
        ax.set_title("Revenue Recovered to\nRecord $220M in 2024",fontsize=9,fontweight="bold",color="#1565C0")
    else:
        ax.set_title(titles[i],fontsize=9,fontweight="bold")
    ax.tick_params(labelsize=6); ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.suptitle("Storytelling Layers: Progressive Reveal",fontsize=12,fontweight="bold")
plt.tight_layout(); plt.savefig("output/storytelling_py.png",dpi=300); plt.close()

# 3. ANNOTATED BAR — complete example
cats=["SUV","Pickup","Midsize","Compact","Minivan"]; vals=[62,33,41,47,11]
idx=np.argsort(vals); sc=[cats[i] for i in idx]; sv=[vals[i] for i in idx]
fig,ax=plt.subplots(figsize=(6,5))
colors=["#BBBBBB"]*5; colors[-1]="#E53935"
ax.barh(sc,sv,color=colors,height=0.5,edgecolor="none")
for i,v in enumerate(sv):
    ax.text(v+0.8,i,str(v),va="center",fontsize=9,fontweight="bold",color="#E53935" if i==4 else "#888")
ax.axvline(x=np.mean(sv),color="#888",lw=0.8,ls="--")
ax.set_title("SUV Leads with 62 Models",fontsize=12,fontweight="bold")
fig.text(0.15,0.90,"Vehicle count by class, 2024",fontsize=9,color="grey")
fig.text(0.15,0.02,"Source: mpg | UNYT",fontsize=7,fontstyle="italic",color="#AAA")
for sp in ["top","right","left"]: ax.spines[sp].set_visible(False)
ax.set_xticks([]); ax.tick_params(left=False,labelsize=9)
plt.subplots_adjust(top=0.84,bottom=0.08)
plt.savefig("output/annotated_bar_py.pdf",bbox_inches="tight")
plt.savefig("output/annotated_bar_py.png",dpi=300,bbox_inches="tight"); plt.close()

print("All W02-M08 Python plots saved")
