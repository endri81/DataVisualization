"""W02-M04: Scales & Coordinate Systems — Python — UNYT Tirana"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
os.makedirs("output", exist_ok=True); np.random.seed(42)

# 1. LINEAR vs LOG
n=300; x=10**np.random.uniform(1,6,n); y=3.5+0.15*np.log10(x)+np.random.normal(0,0.5,n)
fig,(ax1,ax2)=plt.subplots(1,2,figsize=(10,4))
ax1.scatter(x,y,s=8,c="#1565C0",alpha=0.3,edgecolors="none"); ax1.set_title("Linear",fontweight="bold")
ax2.scatter(x,y,s=8,c="#1565C0",alpha=0.3,edgecolors="none"); ax2.set_xscale("log"); ax2.set_title("Log",fontweight="bold")
for ax in [ax1,ax2]: ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/lin_vs_log_py.png",dpi=300); plt.close()

# 2. AXIS FORMATTING
cats=["Q1","Q2","Q3","Q4"]; vals=[1.2e6,2.5e6,1.8e6,3.2e6]
fig,axes=plt.subplots(1,3,figsize=(12,3.5))
axes[0].bar(cats,vals,color="#1565C0",width=0.5)
axes[0].yaxis.set_major_formatter(FuncFormatter(lambda x,p: f"{x:,.0f}")); axes[0].set_title("Comma",fontweight="bold")
axes[1].bar(cats,vals,color="#2E7D32",width=0.5)
axes[1].yaxis.set_major_formatter(FuncFormatter(lambda x,p: f"${x/1e6:.1f}M")); axes[1].set_title("Dollar",fontweight="bold")
pcts=[0.45,0.28,0.18,0.09]
axes[2].bar(cats,pcts,color="#E53935",width=0.5)
axes[2].yaxis.set_major_formatter(FuncFormatter(lambda x,p: f"{x:.0%}")); axes[2].set_title("Percent",fontweight="bold")
for ax in axes: ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.tick_params(labelsize=7)
fig.suptitle("Axis Label Formatting",fontsize=11,fontweight="bold"); plt.tight_layout()
plt.savefig("output/axis_format_py.png",dpi=300); plt.close()

# 3. ZOOM: set_xlim (safe) vs data filter (dangerous)
np.random.seed(55); xz=np.random.uniform(0,100,200); yz=0.4*xz+np.random.normal(0,12,200)
fig,axes=plt.subplots(1,3,figsize=(12,4))
axes[0].scatter(xz,yz,s=10,c="#1565C0",alpha=0.4); m,b=np.polyfit(xz,yz,1); xs=np.linspace(0,100,50)
axes[0].plot(xs,m*xs+b,color="#1565C0",lw=1.5); axes[0].set_title("Full data",fontweight="bold")
mask=(xz>=25)&(xz<=75); m2,b2=np.polyfit(xz[mask],yz[mask],1); xs2=np.linspace(25,75,50)
axes[1].scatter(xz[mask],yz[mask],s=10,c="#E53935",alpha=0.4)
axes[1].plot(xs2,m2*xs2+b2,color="#E53935",lw=1.5); axes[1].set_title("Filter (slope changes!)",fontweight="bold",color="#C62828")
axes[2].scatter(xz,yz,s=10,c="#2E7D32",alpha=0.4)
axes[2].plot(xs,m*xs+b,color="#2E7D32",lw=1.5); axes[2].set_xlim(25,75)
axes[2].set_title("set_xlim (safe zoom)",fontweight="bold",color="#2E7D32")
for ax in axes: ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False); ax.tick_params(labelsize=7)
fig.suptitle("Zoom: Filter vs Clip",fontsize=11,fontweight="bold"); plt.tight_layout()
plt.savefig("output/zoom_py.png",dpi=300); plt.close()

# 4. DATE AXIS
dates=pd.date_range("2020-01","2025-01",freq="MS")
vals2=np.cumsum(np.random.normal(2,8,len(dates)))+100
fig,ax=plt.subplots(figsize=(7,4))
ax.plot(dates,vals2,color="#1565C0",linewidth=1.5)
ax.xaxis.set_major_locator(mdates.YearLocator()); ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[4,7,10]))
ax.set_title("Date Axis with YearLocator + DateFormatter",fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/date_axis_py.png",dpi=300); plt.close()

print("All W02-M04 Python plots saved")
