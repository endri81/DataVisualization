"""W04-M02: Data Wrangling for Visualization (R focus) — Python equivalent — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
os.makedirs("output",exist_ok=True); np.random.seed(42)

# Full cleaning pipeline (pandas equivalent of the R pipe chain)
apps = pd.read_csv("googleplaystore.csv")
apps_clean = (apps
    .drop_duplicates(subset="App", keep="first")
    .assign(
        Reviews=lambda d: pd.to_numeric(d["Reviews"], errors="coerce"),
        Installs=lambda d: d["Installs"].str.replace(r"[+,]","",regex=True).pipe(pd.to_numeric, errors="coerce"),
        Size_MB=lambda d: d["Size"].str.replace("M","").pipe(pd.to_numeric, errors="coerce"),
        Price=lambda d: d["Price"].str.replace("$","").pipe(pd.to_numeric, errors="coerce"),
        date=lambda d: pd.to_datetime(d["Last Updated"], format="%B %d, %Y", errors="coerce"))
    .query("Rating == Rating and Type in ['Free','Paid']")  # drop NA Rating
    .copy())
print(f"Clean: {apps_clean.shape[0]} rows, {apps_clean.shape[1]} cols")

# 1. PIPE-TO-PLOT: groupby → bar
summary = (apps_clean.groupby("Category")
    .agg(mean_r=("Rating","mean"), n=("Rating","count"))
    .nlargest(8,"n").sort_values("mean_r"))
fig,ax=plt.subplots(figsize=(6,5))
colors=["#BBBBBB"]*8; colors[-1]="#1565C0"
ax.barh(summary.index, summary["mean_r"], color=colors, height=0.5)
for i,(idx,row) in enumerate(summary.iterrows()):
    ax.text(row["mean_r"]+0.005,i,f"{row['mean_r']:.2f}",va="center",fontsize=7,fontweight="bold",
        color="#1565C0" if i==7 else "#888")
ax.set_xlim(3.8,4.4); ax.set_title("df.groupby().agg().nlargest().plot()",fontweight="bold")
for sp in ["top","right","left"]: ax.spines[sp].set_visible(False)
ax.tick_params(left=False,labelsize=7); ax.grid(axis="x",alpha=0.1)
plt.tight_layout(); plt.savefig("output/pipe_to_plot_py.png",dpi=300); plt.close()

# 2. PIVOT (melt) → line chart
df_wide = pd.DataFrame({"region":["Tirana","Durres","Vlore","Elbasan"],
    "Q1":[120,90,65,78],"Q2":[135,95,72,82],"Q3":[128,88,70,75],"Q4":[150,110,80,95]})
df_long = df_wide.melt(id_vars="region", var_name="quarter", value_name="revenue")
fig,ax=plt.subplots(figsize=(6,4))
pal={"Tirana":"#1565C0","Durres":"#E53935","Vlore":"#2E7D32","Elbasan":"#E65100"}
for r,c in pal.items():
    sub=df_long.query("region==@r")
    ax.plot(sub["quarter"],sub["revenue"],"-o",color=c,lw=1.5,markersize=5,label=r)
ax.legend(fontsize=7); ax.set_title("After pd.melt(): Line Chart Ready",fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/pivot_line_py.png",dpi=300); plt.close()

# 3. GROUPBY → POINTRANGE
cats=apps_clean["Category"].value_counts().head(8).index
sub=apps_clean.query("Category in @cats")
stats=(sub.groupby("Category")["Rating"]
    .agg(["mean","std","count"])
    .assign(se=lambda d: d["std"]/np.sqrt(d["count"]),
            ci95=lambda d: 1.96*d["std"]/np.sqrt(d["count"]))
    .sort_values("mean"))
fig,ax=plt.subplots(figsize=(6,4.5))
ax.errorbar(stats["mean"],range(len(stats)),xerr=stats["ci95"],fmt="o",color="#1565C0",
    markersize=6,capsize=4,lw=1.5)
ax.set_yticks(range(len(stats))); ax.set_yticklabels(stats.index,fontsize=7)
ax.set_title("groupby → agg → errorbar (Mean ± 95% CI)",fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/pointrange_py.png",dpi=300); plt.close()

print("All W04-M02 Python plots saved")
