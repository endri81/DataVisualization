"""W03-M10: Lab — Chart Selection Decision Framework — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
from matplotlib.gridspec import GridSpec
from scipy.stats import gaussian_kde
os.makedirs("output",exist_ok=True); np.random.seed(42)

netflix = pd.read_csv("netflix.csv") if os.path.exists("netflix.csv") else None
# Use simulated data for sandbox
n_m,n_t=6131,2676
genres_top=["Drama","Comedy","Action","Documentary","Thriller","Horror","Romance","Sci-Fi"]
genre_counts=[2723,1675,1245,890,756,532,412,320]
countries=["United States","India","United Kingdom","Japan","South Korea","Canada"]
country_counts=[2818,972,419,245,199,181]
durations=np.random.normal(100,25,n_m).clip(40,240)
years=np.arange(2010,2022)
m_per_yr=np.array([150,200,280,350,450,550,680,800,900,950,1000,820])
t_per_yr=np.array([30,50,80,120,180,250,350,450,520,580,600,460])

fig=plt.figure(figsize=(16,10)); gs=GridSpec(2,4,figure=fig,hspace=0.45,wspace=0.35)

# (a) Bar — genres
ax=fig.add_subplot(gs[0,0]); idx=np.argsort(genre_counts)[-6:]
sc=[genres_top[i] for i in idx]; sv=[genre_counts[i] for i in idx]
cl=["#BBBBBB"]*6; cl[-1]="#E53935"
ax.barh(sc,sv,color=cl,height=0.55)
for i,v in enumerate(sv): ax.text(v+15,i,f"{v:,}",va="center",fontsize=5,fontweight="bold",color="#E53935" if i==5 else "#888")
ax.set_title("(a) Top Genres [Bar]",fontsize=8,fontweight="bold")
for sp in ["top","right","left"]: ax.spines[sp].set_visible(False)
ax.set_xticks([]); ax.tick_params(left=False,labelsize=5)

# (b) Histogram — duration
ax=fig.add_subplot(gs[0,1])
ax.hist(durations,bins=35,color="#1565C0",edgecolor="white",lw=0.3)
ax.axvline(x=np.mean(durations),color="#E53935",lw=1.5,ls="--")
ax.set_title("(b) Movie Duration [Hist]",fontsize=8,fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.tick_params(labelsize=5)

# (c) Stacked — rating x type
ax=fig.add_subplot(gs[0,2])
top_r=["TV-MA","TV-14","TV-PG","R","PG-13"]; mc=[1800,1200,500,750,400]; tc=[1407,960,363,49,90]
xp=np.arange(len(top_r))
ax.bar(xp,mc,0.5,label="Movie",color="#1565C0",edgecolor="white")
ax.bar(xp,tc,0.5,bottom=mc,label="TV",color="#E53935",edgecolor="white")
ax.set_xticks(xp); ax.set_xticklabels(top_r,fontsize=5); ax.legend(fontsize=5)
ax.set_title("(c) Rating × Type [Stacked]",fontsize=8,fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.tick_params(labelsize=5)

# (d) Waffle — Movie vs TV
ax=fig.add_subplot(gs[0,3]); pct_m=70; grid=np.zeros((10,10),dtype=int); idx2=0
for i in range(10):
    for j in range(10):
        grid[9-i,j]=0 if idx2<pct_m else 1; idx2+=1
for i in range(10):
    for j in range(10):
        ax.add_patch(plt.Rectangle((j,i),0.9,0.9,facecolor="#1565C0" if grid[i,j]==0 else "#E53935",edgecolor="white",lw=1))
ax.set_xlim(-0.2,10.2); ax.set_ylim(-0.2,10.2); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("(d) Movie 70% | TV 30% [Waffle]",fontsize=8,fontweight="bold")

# (e) Line — releases per year
ax=fig.add_subplot(gs[1,0])
ax.plot(years,m_per_yr,"-o",color="#1565C0",lw=1.5,markersize=3,label="Movie")
ax.plot(years,t_per_yr,"-s",color="#E53935",lw=1.5,markersize=3,label="TV")
ax.legend(fontsize=5); ax.set_title("(e) Releases/Year [Line]",fontsize=8,fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.tick_params(labelsize=5)

# (f) Ridgeline — duration by genre
ax=fig.add_subplot(gs[1,1]); xs=np.linspace(40,200,100); offset=0
for g,c in zip(["Drama","Comedy","Action","Doc"],["#1565C0","#E53935","#2E7D32","#E65100"]):
    d=np.random.normal(100+np.random.uniform(-15,15),20+np.random.uniform(-5,5),400).clip(40,200)
    kde=gaussian_kde(d); y=kde(xs)
    ax.fill_between(xs,offset,y+offset,alpha=0.25,color=c); ax.plot(xs,y+offset,color=c,lw=1)
    ax.text(38,offset+0.001,g,fontsize=5,fontweight="bold",color=c,va="bottom"); offset+=max(y)*0.6
ax.set_yticks([]); ax.spines["left"].set_visible(False); ax.set_title("(f) Duration/Genre [Ridgeline]",fontsize=8,fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.tick_params(labelsize=5)

# (g) Boxplot — seasons
ax=fig.add_subplot(gs[1,2]); seasons=np.random.choice([1,2,3,4,5,6],200,p=[0.55,0.20,0.10,0.07,0.05,0.03])
bp=ax.boxplot([seasons],labels=["TV Shows"],patch_artist=True,widths=0.4,notch=True)
bp["boxes"][0].set_facecolor("#BBDEFB"); bp["boxes"][0].set_edgecolor("#1565C0")
ax.set_title("(g) Seasons [Boxplot]",fontsize=8,fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.tick_params(labelsize=5)

# (h) Lollipop — countries
ax=fig.add_subplot(gs[1,3]); idx3=np.argsort(country_counts); sc3=[countries[i] for i in idx3]; sv3=[country_counts[i] for i in idx3]
cl3=["#BBBBBB"]*6; cl3[-1]="#1565C0"
ax.hlines(range(6),0,sv3,color="#BBBBBB",lw=1.5)
ax.scatter(sv3,range(6),s=40,c=cl3,zorder=5,edgecolors="white",lw=0.5)
for i,v in enumerate(sv3): ax.text(v+15,i,f"{v:,}",va="center",fontsize=5,fontweight="bold")
ax.set_yticks(range(6)); ax.set_yticklabels(sc3,fontsize=5)
ax.set_title("(h) Top Countries [Lollipop]",fontsize=8,fontweight="bold")
for sp in ["top","right","left"]: ax.spines[sp].set_visible(False)
ax.set_xticks([]); ax.tick_params(left=False)

fig.suptitle("Netflix: 8 Chart Types from the Decision Framework\nWorkshop 3 Lab",fontsize=13,fontweight="bold")
fig.text(0.5,0.01,"Source: Netflix (Kaggle) | UNYT Data Visualization Course",ha="center",fontsize=8,fontstyle="italic",color="#888")
fig.savefig("output/W03_M10_netflix.pdf",bbox_inches="tight")
fig.savefig("output/W03_M10_netflix.png",dpi=300,bbox_inches="tight"); plt.close()
print("Workshop 3 Lab Complete (Python)")
