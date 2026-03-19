"""W04-M07: EDA Case Study — Google Play Store — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
from matplotlib.gridspec import GridSpec
from scipy.stats import spearmanr, probplot
os.makedirs("output",exist_ok=True); np.random.seed(42)

# Phase 1: Clean
apps = (pd.read_csv("googleplaystore.csv")
    .drop_duplicates(subset="App",keep="first")
    .assign(Reviews=lambda d: pd.to_numeric(d["Reviews"],errors="coerce"),
            Installs=lambda d: d["Installs"].str.replace(r"[+,]","",regex=True).pipe(pd.to_numeric,errors="coerce"),
            Price=lambda d: d["Price"].str.replace("$","",regex=False).pipe(pd.to_numeric,errors="coerce"))
    .dropna(subset=["Rating"])
    .query("Type in ['Free','Paid'] and Rating>=1 and Rating<=5")
    .assign(log_reviews=lambda d: np.log10(d["Reviews"].clip(lower=1)),
            log_installs=lambda d: np.log10(d["Installs"].clip(lower=1))))
print(f"Cleaned: {len(apps)} rows")

# Phase 2: Dashboard (6 panels)
fig=plt.figure(figsize=(14,9)); gs=GridSpec(2,3,figure=fig,hspace=0.4,wspace=0.35)

ax=fig.add_subplot(gs[0,0]); ax.hist(apps["Rating"],bins=40,color="#1565C0",edgecolor="white",lw=0.3)
ax.axvline(x=apps["Rating"].mean(),color="#E53935",lw=1.5,ls="--"); ax.set_title("(a) Rating Dist.",fontsize=9,fontweight="bold")

ax=fig.add_subplot(gs[0,1])
for t,c in [("Free","#1565C0"),("Paid","#E53935")]:
    d=apps.query("Type==@t")["Rating"]; parts=ax.violinplot([d],positions=[0 if t=="Free" else 1],showmedians=True)
    parts["bodies"][0].set_facecolor(c); parts["bodies"][0].set_alpha(0.3)
ax.set_xticks([0,1]); ax.set_xticklabels(["Free","Paid"]); ax.set_title("(b) by Type",fontsize=9,fontweight="bold")

ax=fig.add_subplot(gs[0,2]); cats=apps["Category"].value_counts().head(8).sort_values()
cl=["#BBBBBB"]*8; cl[-1]="#1565C0"; ax.barh(cats.index,cats.values,color=cl,height=0.55)
ax.set_title("(c) Top Categories",fontsize=9,fontweight="bold")
for sp in ["top","right","left"]: ax.spines[sp].set_visible(False)
ax.set_xticks([]); ax.tick_params(left=False,labelsize=6)

ax=fig.add_subplot(gs[1,0]); sub=apps.query("Reviews>0").sample(2000,random_state=42)
ax.scatter(sub["log_reviews"],sub["Rating"],s=3,c="#1565C0",alpha=0.15)
z=np.polyfit(sub["log_reviews"],sub["Rating"],1); xs=np.linspace(0,7,100); ax.plot(xs,np.polyval(z,xs),color="#E53935",lw=1.5)
rho,_=spearmanr(sub["log_reviews"],sub["Rating"]); ax.set_title(f"(d) Reviews vs Rating (ρ={rho:.2f})",fontsize=9,fontweight="bold")

ax=fig.add_subplot(gs[1,1]); top8=apps["Category"].value_counts().head(8).index
stats=apps.query("Category in @top8").groupby("Category")["Rating"].agg(["mean","std","count"])
stats["ci"]=1.96*stats["std"]/np.sqrt(stats["count"]); stats=stats.sort_values("mean")
ax.errorbar(stats["mean"],range(len(stats)),xerr=stats["ci"],fmt="o",color="#1565C0",markersize=5,capsize=3)
ax.set_yticks(range(len(stats))); ax.set_yticklabels(stats.index,fontsize=6)
ax.set_title("(e) Mean ± 95% CI",fontsize=9,fontweight="bold")

ax=fig.add_subplot(gs[1,2]); probplot(apps["Rating"].values,dist="norm",plot=ax)
ax.get_lines()[0].set_color("#1565C0"); ax.get_lines()[0].set_markersize(1); ax.get_lines()[0].set_alpha(0.3)
ax.get_lines()[1].set_color("#E53935"); ax.set_title("(f) Q-Q",fontsize=9,fontweight="bold")

for ax in fig.get_axes(): ax.tick_params(labelsize=6); ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.suptitle(f"Google Play Store EDA: {len(apps)} apps",fontsize=13,fontweight="bold")
plt.savefig("output/W04_M07_dashboard.pdf",bbox_inches="tight")
plt.savefig("output/W04_M07_dashboard.png",dpi=300,bbox_inches="tight"); plt.close()

# Phase 3: Key stats
rho2,_=spearmanr(apps["log_reviews"],apps["Rating"])
print(f"Mean={apps['Rating'].mean():.3f}, Median={apps['Rating'].median():.3f}")
print(f"Spearman(logRev,Rating)={rho2:.3f}")
print(f"Free={apps.query('Type==\"Free\"').shape[0]/len(apps)*100:.1f}%")
print("All W04-M07 Python outputs saved")
