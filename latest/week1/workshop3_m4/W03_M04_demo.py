"""W03-M04: Relationships — Scatter, Bubble & Hexbin — Python — UNYT"""
import numpy as np, matplotlib.pyplot as plt, os
from matplotlib.gridspec import GridSpec
from scipy.stats import gaussian_kde
os.makedirs("output",exist_ok=True); np.random.seed(42)

n=3000; rev=10**np.random.uniform(1,6,n); rat=(3.5+0.15*np.log10(rev)+np.random.normal(0,0.5,n)).clip(1,5)

# 1. OVERPLOTTING CASCADE
fig,axes=plt.subplots(1,4,figsize=(14,3.5))
axes[0].scatter(rev,rat,s=3,c="#1565C0"); axes[0].set_title("Raw (overplotted)",fontsize=8,fontweight="bold",color="#C62828")
axes[1].scatter(rev,rat,s=3,c="#1565C0",alpha=0.05); axes[1].set_title("alpha=0.05",fontsize=8,fontweight="bold")
axes[2].hexbin(np.log10(rev),rat,gridsize=25,cmap="YlGnBu",mincnt=1); axes[2].set_title("Hexbin",fontsize=8,fontweight="bold")
xy=np.vstack([np.log10(rev),rat]); kde=gaussian_kde(xy)
xg,yg=np.mgrid[1:6:80j,1:5:80j]; z=kde(np.vstack([xg.ravel(),yg.ravel()])).reshape(xg.shape)
axes[3].contourf(xg,yg,z,levels=12,cmap="YlGnBu"); axes[3].set_title("2D KDE",fontsize=8,fontweight="bold")
for ax in axes: ax.tick_params(labelsize=5); ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.suptitle("Overplotting Solutions",fontsize=11,fontweight="bold"); plt.tight_layout()
plt.savefig("output/overplotting_py.png",dpi=300); plt.close()

# 2. BUBBLE
np.random.seed(66); n2=50; gdp=np.random.uniform(5,80,n2); life=55+0.35*gdp+np.random.normal(0,5,n2)
pop=np.random.uniform(1e6,8e8,n2); cont=np.random.choice(["Africa","Asia","Europe","Americas"],n2)
pal={"Africa":"#1565C0","Asia":"#E53935","Europe":"#2E7D32","Americas":"#E65100"}
fig,ax=plt.subplots(figsize=(8,5.5))
for g,c in pal.items():
    m=cont==g; ax.scatter(gdp[m],life[m],s=pop[m]/2e6,c=c,alpha=0.45,edgecolors="white",lw=0.5,label=g)
ax.legend(fontsize=7,title="Continent",markerscale=0.5); ax.set_xlabel("GDP per Capita ($K)"); ax.set_ylabel("Life Expectancy")
ax.set_title("Bubble Chart: Gapminder Style",fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.grid(alpha=0.1)
plt.tight_layout(); plt.savefig("output/bubble_py.png",dpi=300); plt.close()

# 3. MARGINAL DISTRIBUTIONS
np.random.seed(99); n3=200; x3=np.random.normal(50,12,n3); y3=0.4*x3+np.random.normal(0,8,n3)
fig=plt.figure(figsize=(7,6)); gs=GridSpec(4,4,figure=fig,hspace=0.05,wspace=0.05)
ax_m=fig.add_subplot(gs[1:4,0:3]); ax_t=fig.add_subplot(gs[0,0:3],sharex=ax_m); ax_r=fig.add_subplot(gs[1:4,3],sharey=ax_m)
ax_m.scatter(x3,y3,s=15,c="#1565C0",alpha=0.4,edgecolors="none"); ax_m.set_xlabel("X"); ax_m.set_ylabel("Y")
ax_t.hist(x3,bins=25,color="#1565C0",edgecolor="white",lw=0.3,alpha=0.5); ax_t.set_title("Marginal Histograms",fontweight="bold")
ax_r.hist(y3,bins=25,color="#1565C0",edgecolor="white",lw=0.3,alpha=0.5,orientation="horizontal")
ax_t.tick_params(labelbottom=False); ax_r.tick_params(labelleft=False)
for a in [ax_m,ax_t,ax_r]: a.spines["top"].set_visible(False); a.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/marginal_py.png",dpi=300); plt.close()

# 4. SMOOTHERS
np.random.seed(88); x4=np.random.uniform(0,10,150)
fig,(a1,a2)=plt.subplots(1,2,figsize=(11,4.5))
y_lin=2+0.5*x4+np.random.normal(0,1.5,150); y_nl=3+2*np.sin(x4*0.8)+np.random.normal(0,1,150)
a1.scatter(x4,y_lin,s=12,c="#1565C0",alpha=0.4); m,b=np.polyfit(x4,y_lin,1); xs=np.linspace(0,10,50)
a1.plot(xs,m*xs+b,c="#E53935",lw=2); a1.set_title("Linear: method='lm'",fontweight="bold")
a2.scatter(x4,y_nl,s=12,c="#1565C0",alpha=0.4)
from numpy.polynomial import polynomial as P; coef=P.polyfit(x4,y_nl,6); ys=P.polyval(xs,coef)
a2.plot(xs,ys,c="#2E7D32",lw=2); a2.set_title("Non-linear: method='loess'",fontweight="bold")
for a in [a1,a2]: a.spines["top"].set_visible(False); a.spines["right"].set_visible(False)
fig.suptitle("Choosing the Smoother",fontweight="bold"); plt.tight_layout()
plt.savefig("output/smoothers_py.png",dpi=300); plt.close()
print("All W03-M04 Python plots saved")
