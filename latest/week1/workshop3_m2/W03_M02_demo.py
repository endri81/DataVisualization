"""W03-M02: Boxplots, Violins & Beeswarm — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
from scipy.stats import gaussian_kde
os.makedirs("output", exist_ok=True); np.random.seed(42)

cats=["GAME","FAMILY","TOOLS","BUSINESS","MEDICAL","SOCIAL"]
cats_data={c: np.random.normal(4.0+np.random.uniform(-0.3,0.3),0.4+np.random.uniform(0,0.2),
    np.random.randint(100,500)).clip(1,5) for c in cats}

# 1. BOXPLOT + JITTER
fig,ax=plt.subplots(figsize=(7,5))
data_list=[cats_data[c] for c in cats]
bp=ax.boxplot(data_list,labels=cats,patch_artist=True,widths=0.4,notch=True)
colors=["#1565C0","#2E7D32","#E65100","#7B1FA2","#C62828","#00695C"]
for patch,c in zip(bp["boxes"],colors): patch.set_facecolor(c); patch.set_alpha(0.25); patch.set_edgecolor(c)
for med in bp["medians"]: med.set_color("#333"); med.set_linewidth(2)
for i,d in enumerate(data_list):
    xj=np.random.normal(i+1,0.06,min(80,len(d)))
    ax.scatter(xj,np.random.choice(d,min(80,len(d)),replace=False),s=5,c="#E53935",alpha=0.25,edgecolors="none",zorder=5)
ax.set_title("Boxplot + Jitter: Rating by Category",fontweight="bold"); ax.set_ylabel("Rating")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.tick_params(labelsize=7)
plt.tight_layout(); plt.savefig("output/box_jitter_py.png",dpi=300); plt.close()

# 2. VIOLIN + STRIP
fig,ax=plt.subplots(figsize=(7,5))
parts=ax.violinplot(data_list,positions=range(1,7),showmeans=True,showmedians=True,widths=0.6)
for pc,c in zip(parts["bodies"],colors): pc.set_facecolor(c); pc.set_alpha(0.25); pc.set_edgecolor(c)
for i,d in enumerate(data_list):
    xj=np.random.normal(i+1,0.04,min(60,len(d)))
    ax.scatter(xj,np.random.choice(d,min(60,len(d)),replace=False),s=4,c=colors[i],alpha=0.4,edgecolors="none",zorder=5)
ax.set_xticks(range(1,7)); ax.set_xticklabels(cats,fontsize=7)
ax.set_title("Violin + Strip: Shape + Raw Data",fontweight="bold"); ax.set_ylabel("Rating")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.tick_params(labelsize=7)
plt.tight_layout(); plt.savefig("output/violin_strip_py.png",dpi=300); plt.close()

# 3. RAINCLOUD (manual)
free_r=np.random.normal(4.15,0.55,800).clip(1,5); paid_r=np.random.normal(4.25,0.45,200).clip(1,5)
fig,ax=plt.subplots(figsize=(8,5))
for i,(g,d,c) in enumerate(zip(["Free","Paid"],[free_r,paid_r],["#1565C0","#E53935"])):
    pos=i+1; xs=np.linspace(1,5,100); kde=gaussian_kde(d)
    ax.fill_betweenx(xs,pos,pos+kde(xs)*4,alpha=0.2,color=c)
    ax.plot(pos+kde(xs)*4,xs,color=c,linewidth=1)
    q1,med,q3=np.percentile(d,[25,50,75])
    ax.barh(med,0.15,height=q3-q1,left=pos-0.25,color=c,alpha=0.4,edgecolor=c)
    ax.plot([pos-0.25,pos-0.1],[med,med],color="white",linewidth=2)
    xj=np.random.uniform(pos-0.5,pos-0.3,min(100,len(d)))
    ax.scatter(xj,np.random.choice(d,min(100,len(d)),replace=False),s=4,c=c,alpha=0.3,edgecolors="none")
ax.set_xticks([1,2]); ax.set_xticklabels(["Free","Paid"],fontsize=9)
ax.set_ylabel("Rating"); ax.set_title("Raincloud: Box + Half-Violin + Jitter",fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/raincloud_py.png",dpi=300); plt.close()

print("All W03-M02 Python plots saved")
