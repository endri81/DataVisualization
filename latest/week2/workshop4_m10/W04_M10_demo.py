"""W04-M10: Lab — Full EDA on Netflix — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
from matplotlib.gridspec import GridSpec
os.makedirs("output",exist_ok=True); np.random.seed(42)

nf=pd.read_csv("netflix.csv")
nf["date_added"]=pd.to_datetime(nf["date_added"].str.strip(),errors="coerce")
nf["year_added"]=nf["date_added"].dt.year
nf["dur_min"]=nf.loc[nf["type"]=="Movie","duration"].str.extract(r"(\d+)").astype(float)
nf["seasons"]=nf.loc[nf["type"]=="TV Show","duration"].str.extract(r"(\d+)").astype(float)
nf["primary_genre"]=nf["listed_in"].str.split(",").str[0].str.strip()
nf["primary_country"]=nf["country"].str.split(",").str[0].str.strip()
print(f"Rows: {len(nf)} | Movies: {(nf['type']=='Movie').sum()} | TV: {(nf['type']=='TV Show').sum()}")
print(f"\nMissing %:\n{(nf.isna().mean()*100).round(1).sort_values(ascending=False)}")

# Dashboard (6 panels)
fig=plt.figure(figsize=(14,9)); gs=GridSpec(2,3,figure=fig,hspace=0.4,wspace=0.35)

ax=fig.add_subplot(gs[0,0]); miss=(nf.isna().mean()*100).sort_values(); miss[miss>0].plot.barh(ax=ax,color="#E53935")
ax.axvline(x=5,color="#888",lw=0.8,ls="--"); ax.set_title("(a) Missing %",fontsize=9,fontweight="bold")

ax=fig.add_subplot(gs[0,1]); yr=nf.query("release_year>=2000").groupby(["release_year","type"]).size().unstack(fill_value=0)
if "Movie" in yr: ax.plot(yr.index,yr["Movie"],"-o",color="#1565C0",lw=1.5,markersize=3,label="Movie")
if "TV Show" in yr: ax.plot(yr.index,yr["TV Show"],"-s",color="#E53935",lw=1.5,markersize=3,label="TV")
ax.legend(fontsize=5); ax.set_title("(b) Releases/Year",fontsize=9,fontweight="bold")

ax=fig.add_subplot(gs[0,2]); genres=nf["listed_in"].str.split(",").explode().str.strip().value_counts().head(10).sort_values()
cl=["#BBBBBB"]*10; cl[-1]="#E53935"; ax.barh(genres.index,genres.values,color=cl,height=0.55)
ax.set_title("(c) Top Genres",fontsize=9,fontweight="bold")
for sp in ["top","right","left"]: ax.spines[sp].set_visible(False)
ax.set_xticks([]); ax.tick_params(left=False,labelsize=5)

ax=fig.add_subplot(gs[1,0]); dur=nf["dur_min"].dropna()
ax.hist(dur,bins=40,color="#1565C0",edgecolor="white",lw=0.3)
ax.axvline(x=dur.mean(),color="#E53935",lw=1.5,ls="--"); ax.set_title("(d) Movie Duration",fontsize=9,fontweight="bold")

ax=fig.add_subplot(gs[1,1]); rats=nf["rating"].value_counts().head(8).sort_values()
ax.barh(rats.index,rats.values,color="#7B1FA2",height=0.55)
ax.set_title("(e) Content Rating",fontsize=9,fontweight="bold")
for sp in ["top","right","left"]: ax.spines[sp].set_visible(False)
ax.set_xticks([]); ax.tick_params(left=False,labelsize=5)

ax=fig.add_subplot(gs[1,2]); ctry=nf["primary_country"].value_counts().head(8).sort_values()
cl2=["#BBBBBB"]*8; cl2[-1]="#1565C0"
ax.hlines(range(len(ctry)),0,ctry.values,color="#BBBBBB",lw=1.5)
ax.scatter(ctry.values,range(len(ctry)),s=40,c=cl2,zorder=5,edgecolors="white",lw=0.5)
ax.set_yticks(range(len(ctry))); ax.set_yticklabels(ctry.index,fontsize=5)
ax.set_title("(f) Top Countries",fontsize=9,fontweight="bold")
for sp in ["top","right","left"]: ax.spines[sp].set_visible(False)
ax.set_xticks([]); ax.tick_params(left=False)

for a in fig.get_axes(): a.tick_params(labelsize=5); a.spines["top"].set_visible(False); a.spines["right"].set_visible(False)
fig.suptitle(f"Netflix EDA: {len(nf):,} Titles",fontsize=13,fontweight="bold")
plt.savefig("output/W04_M10_netflix.pdf",bbox_inches="tight")
plt.savefig("output/W04_M10_netflix.png",dpi=300,bbox_inches="tight"); plt.close()
print("W04-M10 Lab Complete (Python)")
