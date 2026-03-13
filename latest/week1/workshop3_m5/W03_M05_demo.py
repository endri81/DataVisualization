"""W03-M05: Proportions — Pie, Donut, Treemap & Waffle — Python — UNYT"""
import numpy as np, matplotlib.pyplot as plt, os
os.makedirs("output",exist_ok=True); np.random.seed(42)
cats=["FAMILY","GAME","TOOLS","PHOTOGRAPHY","PRODUCTIVITY","BUSINESS"]
vals=[1832,959,843,376,374,420]; colors=["#1565C0","#E53935","#2E7D32","#E65100","#7B1FA2","#00695C"]

# 1. PIE vs BAR
fig,(ax1,ax2)=plt.subplots(1,2,figsize=(11,4.5))
ax1.pie(vals,labels=cats,autopct="%1.0f%%",colors=colors,startangle=90,textprops={"fontsize":7})
ax1.set_title("Pie: 6 slices = hard to compare",fontweight="bold",color="#C62828")
idx=np.argsort(vals); sc=[cats[i] for i in idx]; sv=[vals[i] for i in idx]; cc=[colors[i] for i in idx]
ax2.barh(sc,sv,color=cc,height=0.55)
for i,v in enumerate(sv): ax2.text(v+15,i,f"{v:,} ({v/sum(vals)*100:.0f}%)",va="center",fontsize=7,fontweight="bold")
ax2.set_title("Bar + %: always better",fontweight="bold",color="#1565C0")
for sp in ["top","right","left"]: ax2.spines[sp].set_visible(False)
ax2.set_xticks([]); ax2.tick_params(left=False,labelsize=7)
fig.suptitle("Pie vs Bar",fontweight="bold"); plt.tight_layout()
plt.savefig("output/pie_vs_bar_py.png",dpi=300); plt.close()

# 2. DONUT KPI
fig,ax=plt.subplots(figsize=(5,4.5))
ax.pie([73,27],colors=["#1565C0","#EEEEEE"],startangle=90,wedgeprops={"width":0.35,"edgecolor":"white","linewidth":2})
ax.text(0,0.05,"73%",ha="center",va="center",fontsize=28,fontweight="bold",color="#1565C0")
ax.text(0,-0.12,"Free Apps",ha="center",va="center",fontsize=10,color="#555")
ax.set_title("Donut: Single KPI",fontweight="bold"); plt.tight_layout()
plt.savefig("output/donut_py.png",dpi=300); plt.close()

# 3. TREEMAP (squarify)
try:
    import squarify
    fig,ax=plt.subplots(figsize=(8,5))
    squarify.plot(sizes=vals,label=[f"{c}\n{v:,}" for c,v in zip(cats,vals)],color=colors,alpha=0.7,
        edgecolor="white",linewidth=2,text_kwargs={"fontsize":8,"fontweight":"bold","color":"white"},ax=ax)
    ax.axis("off"); ax.set_title("Treemap: Area = Count",fontweight="bold")
    plt.tight_layout(); plt.savefig("output/treemap_py.png",dpi=300); plt.close()
    print("  treemap saved (squarify)")
except ImportError:
    print("  squarify not installed — pip install squarify")

# 4. WAFFLE (manual)
fig,ax=plt.subplots(figsize=(6,5))
total=sum(vals); pcts=[round(v/total*100) for v in vals]; diff=100-sum(pcts); pcts[0]+=diff
grid=np.zeros((10,10),dtype=int); idx2=0; cat_idx=0
for i in range(10):
    for j in range(10):
        grid[9-i,j]=cat_idx; idx2+=1
        if idx2>=sum(pcts[:cat_idx+1]) and cat_idx<len(pcts)-1: cat_idx+=1
for i in range(10):
    for j in range(10):
        ax.add_patch(plt.Rectangle((j,i),0.9,0.9,facecolor=colors[grid[i,j]],edgecolor="white",linewidth=1.5))
ax.set_xlim(-0.2,10.2); ax.set_ylim(-0.2,10.2); ax.set_aspect("equal"); ax.axis("off")
for k,(cat,pct,c) in enumerate(zip(cats,pcts,colors)):
    ax.text(10.8,8.5-k*1.2,f"■ {cat} ({pct}%)",fontsize=8,color=c,fontweight="bold",va="center")
ax.set_title("Waffle: 1 square = 1%",fontweight="bold"); plt.tight_layout()
plt.savefig("output/waffle_py.png",dpi=300); plt.close()

# 5. 100% STACKED BAR
fig,ax=plt.subplots(figsize=(9,2.5)); left=0
for cat,val,color in zip(cats,vals,colors):
    pct=val/sum(vals)*100
    ax.barh(["Apps"],pct,left=left,color=color,height=0.5,edgecolor="white",linewidth=1.5,label=cat)
    if pct>5: ax.text(left+pct/2,0,f"{pct:.0f}%",ha="center",va="center",fontsize=7,fontweight="bold",color="white")
    left+=pct
ax.set_xlim(0,100); ax.legend(fontsize=6,ncol=6,loc="upper center",bbox_to_anchor=(0.5,-0.3))
ax.set_title("100% Stacked Bar: The Better Alternative to Pie",fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/stacked_100_py.png",dpi=300); plt.close()

print("All W03-M05 Python plots saved")
