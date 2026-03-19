"""W04-M08: EDA Case Study — e-Car Loan Pricing — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
from matplotlib.gridspec import GridSpec
from scipy.stats import spearmanr
os.makedirs("output",exist_ok=True); np.random.seed(42)

df=pd.read_csv("ecar.csv"); df.columns=[c.strip().replace("  "," ") for c in df.columns]
df["Car Type"]=df["Car Type"].str.strip()
df["Approve Date"]=pd.to_datetime(df["Approve Date"],format="%m/%d/%Y",errors="coerce")
df["Year"]=df["Approve Date"].dt.year
df["Previous Rate"]=pd.to_numeric(df["Previous Rate"],errors="coerce")
df["Spread"]=df["Rate"]-df["Cost of Funds"]
df["is_new"]=df["Previous Rate"].isna()
print(f"Rows: {len(df)}, Cols: {df.shape[1]}")

# Dashboard (6 panels)
fig=plt.figure(figsize=(14,9)); gs=GridSpec(2,3,figure=fig,hspace=0.4,wspace=0.35)
sub=df.sample(20000,random_state=42)

ax=fig.add_subplot(gs[0,0]); ax.hist(sub["FICO"],bins=50,color="#1565C0",edgecolor="white",lw=0.3)
ax.set_title("(a) FICO",fontsize=9,fontweight="bold")
ax=fig.add_subplot(gs[0,1]); ax.hist(sub["Rate"],bins=50,color="#2E7D32",edgecolor="white",lw=0.3)
ax.set_title("(b) Rate",fontsize=9,fontweight="bold")
ax=fig.add_subplot(gs[0,2]); s2=sub.sample(5000); ax.scatter(s2["FICO"],s2["Rate"],s=2,c="#1565C0",alpha=0.08)
rho,_=spearmanr(s2["FICO"],s2["Rate"]); ax.set_title(f"(c) FICO vs Rate (\u03C1={rho:.2f})",fontsize=9,fontweight="bold")
ax=fig.add_subplot(gs[1,0]); tiers=sorted(sub["Tier"].dropna().unique())
bp=ax.boxplot([sub.query("Tier==@t")["Rate"] for t in tiers],labels=[f"T{int(t)}" for t in tiers],patch_artist=True,widths=0.5)
cols5=["#1565C0","#2E7D32","#E65100","#7B1FA2","#C62828"]
for p,c in zip(bp["boxes"],cols5): p.set_facecolor(c); p.set_alpha(0.3)
ax.set_title("(d) Rate by Tier",fontsize=9,fontweight="bold")
ax=fig.add_subplot(gs[1,1]); yr=sub.groupby("Year")["Spread"].agg(["mean","std","count"])
yr["se"]=yr["std"]/np.sqrt(yr["count"]); yr=yr.loc[2002:2012]
ax.plot(yr.index,yr["mean"],"-o",color="#1565C0",lw=1.5,markersize=4)
ax.fill_between(yr.index,yr["mean"]-1.96*yr["se"],yr["mean"]+1.96*yr["se"],alpha=0.15,color="#1565C0")
ax.set_title("(e) Spread Over Time",fontsize=9,fontweight="bold")
ax=fig.add_subplot(gs[1,2])
for label,q,c in [("New","N","#1565C0"),("Used","U","#E53935")]:
    d=sub.query("`Car Type`==@q")["Rate"]; ax.hist(d,bins=40,alpha=0.4,color=c,label=f"{label} (med={d.median():.1f})")
ax.legend(fontsize=6); ax.set_title("(f) New vs Used",fontsize=9,fontweight="bold")

for a in fig.get_axes(): a.tick_params(labelsize=5); a.spines["top"].set_visible(False); a.spines["right"].set_visible(False)
fig.suptitle(f"e-Car Loan EDA: {len(df):,} applications",fontsize=13,fontweight="bold")
plt.savefig("output/W04_M08_dashboard.pdf",bbox_inches="tight")
plt.savefig("output/W04_M08_dashboard.png",dpi=300,bbox_inches="tight"); plt.close()

rho2,_=spearmanr(df["FICO"],df["Rate"])
print(f"Spearman(FICO,Rate)={rho2:.3f}")
print(f"Previous Rate missing: {df['is_new'].mean()*100:.1f}%")
print("All W04-M08 Python outputs saved")
