"""W03-M07: Uncertainty — Error Bars, Confidence & Gradient — Python — UNYT"""
import numpy as np, matplotlib.pyplot as plt, os
from scipy.stats import sem
os.makedirs("output",exist_ok=True); np.random.seed(42)

cats=["GAME","FAMILY","TOOLS","BUSINESS","MEDICAL","SOCIAL"]
means=[4.05,4.18,4.12,4.22,3.95,4.30]; sds=[0.55,0.50,0.48,0.42,0.60,0.38]; ns=[959,1832,843,420,395,259]

# 1. POINTRANGE
ses=[s/np.sqrt(n) for s,n in zip(sds,ns)]
idx=np.argsort(means); sc=[cats[i] for i in idx]; sm=[means[i] for i in idx]; se_s=[ses[i] for i in idx]
fig,ax=plt.subplots(figsize=(7,4.5))
ax.errorbar(sm,range(len(sc)),xerr=[1.96*s for s in se_s],fmt="o",color="#1565C0",markersize=7,capsize=5,linewidth=1.5,capthick=1.5)
for i,(m,s) in enumerate(zip(sm,se_s)): ax.text(m+1.96*s+0.01,i,f"{m:.2f}",va="center",fontsize=7,fontweight="bold")
ax.set_yticks(range(len(sc))); ax.set_yticklabels(sc,fontsize=8)
ax.axvline(x=np.mean(means),color="#888",lw=0.8,ls="--")
ax.set_title("Pointrange: Mean ± 95% CI",fontweight="bold"); ax.set_xlabel("Mean Rating")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/pointrange_py.png",dpi=300); plt.close()

# 2. RIBBON
np.random.seed(33); years=np.arange(2015,2025)
revenue=np.array([120,135,128,142,155,170,145,180,195,220]).astype(float)
se_vals=np.random.uniform(8,18,10)
fig,ax=plt.subplots(figsize=(7,4.5))
ax.plot(years,revenue,"-o",color="#1565C0",lw=2,markersize=5)
ax.fill_between(years,revenue-1.96*se_vals,revenue+1.96*se_vals,alpha=0.12,color="#1565C0",label="95% CI")
ax.fill_between(years,revenue-se_vals,revenue+se_vals,alpha=0.25,color="#1565C0",label="±1 SE")
ax.legend(fontsize=7); ax.set_title("Ribbon: Trend ± CI/SE",fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/ribbon_py.png",dpi=300); plt.close()

# 3. GRADIENT BANDS
np.random.seed(44); y2=np.cumsum(np.random.normal(5,8,10))+200
fig,ax=plt.subplots(figsize=(7,4.5))
ax.plot(years,y2,color="#1565C0",lw=2)
for mult,alpha in [(3.0,0.04),(2.5,0.06),(2.0,0.08),(1.5,0.12),(1.0,0.18),(0.5,0.25)]:
    ax.fill_between(years,y2-mult*8,y2+mult*8,alpha=alpha,color="#1565C0")
ax.set_title("Gradient Bands: Faded Probability",fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/gradient_py.png",dpi=300); plt.close()

# 4. FOREST PLOT
studies=["Study A","Study B","Study C","Study D","Study E","POOLED"]
effects=[0.35,0.50,0.28,0.42,0.38,0.40]; ci_lo=[0.15,0.30,0.05,0.22,0.18,0.32]; ci_hi=[0.55,0.70,0.51,0.62,0.58,0.48]
fig,ax=plt.subplots(figsize=(7,4.5))
for i,(s,e,lo,hi) in enumerate(zip(studies,effects,ci_lo,ci_hi)):
    c="#E53935" if s=="POOLED" else "#1565C0"; sz=10 if s=="POOLED" else 7
    ax.errorbar([e],[i],xerr=[[e-lo],[hi-e]],fmt="o" if s!="POOLED" else "D",color=c,markersize=sz,capsize=4,linewidth=1.5 if s!="POOLED" else 2.5)
    ax.text(hi+0.03,i,f"{e:.2f} [{lo:.2f},{hi:.2f}]",va="center",fontsize=7,color=c)
ax.axvline(x=0,color="#888",lw=1,ls="--"); ax.axhline(y=4.5,color="#888",lw=0.5)
ax.set_yticks(range(len(studies))); ax.set_yticklabels(studies,fontsize=8)
ax.set_title("Forest Plot: Effect Sizes",fontweight="bold"); ax.set_xlabel("Effect (95% CI)")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/forest_py.png",dpi=300); plt.close()
print("All W03-M07 Python plots saved")
