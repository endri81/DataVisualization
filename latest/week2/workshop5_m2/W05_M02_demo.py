"""W05-M02: Parallel Coordinates & Radar Charts — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
from sklearn.preprocessing import MinMaxScaler
os.makedirs("output",exist_ok=True); np.random.seed(42); n=500
fico=np.random.normal(700,50,n).clip(500,850); rate=12-0.01*fico+np.random.normal(0,1,n)
amount=np.random.uniform(5000,50000,n); term=np.random.choice([36,48,60,72],n,p=[.15,.25,.35,.25])
cof=np.random.uniform(1,4,n); spread=rate-cof; tier=np.digitize(fico,[0,620,680,720,760,900])
df=pd.DataFrame({"FICO":fico,"Rate":rate,"Amount":amount,"Term":term,"Spread":spread,"Tier":tier})

# 1. PARALLEL COORDINATES
cols=["FICO","Rate","Amount","Term","Spread"]; scaler=MinMaxScaler()
normed=scaler.fit_transform(df[cols])
fig,ax=plt.subplots(figsize=(10,5.5)); cmap=plt.cm.viridis; nm=plt.Normalize(1,5)
for i in range(min(200,n)):
    ax.plot(range(len(cols)),normed[i],color=cmap(nm(tier[i])),alpha=0.12,lw=0.6)
# Highlight Tier 1
t1=tier==1
for i in np.where(t1)[0][:50]: ax.plot(range(len(cols)),normed[i],color="#1565C0",alpha=0.4,lw=1.5)
ax.set_xticks(range(len(cols))); ax.set_xticklabels(cols,fontsize=9,fontweight="bold")
ax.set_title("Parallel Coordinates: Tier 1 Highlighted",fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/parcoord_py.png",dpi=300); plt.close()

# 2. RADAR CHART
categories=["FICO","Rate\n(inv)","Amount","Term","Spread","Approval"]
N=len(categories); angles=[i/N*2*np.pi for i in range(N)]; angles+=angles[:1]
t1_means=[0.9,0.85,0.6,0.7,0.8,0.95]; t5_means=[0.3,0.35,0.5,0.8,0.4,0.55]
fig,ax=plt.subplots(figsize=(6,6),subplot_kw=dict(polar=True))
for vals,c,label in [(t1_means,"#1565C0","Tier 1"),(t5_means,"#E53935","Tier 5")]:
    v=vals+vals[:1]; ax.fill(angles,v,alpha=0.1,color=c); ax.plot(angles,v,"-o",color=c,lw=2,markersize=5,label=label)
ax.set_xticks(angles[:-1]); ax.set_xticklabels(categories,fontsize=8,fontweight="bold")
ax.set_ylim(0,1); ax.legend(fontsize=8,loc="upper right",bbox_to_anchor=(1.3,1.1))
ax.set_title("Radar: Tier 1 vs Tier 5",fontweight="bold",pad=20)
plt.tight_layout(); plt.savefig("output/radar_py.png",dpi=300); plt.close()

# 3. PANDAS BUILT-IN PARALLEL COORDINATES
from pandas.plotting import parallel_coordinates
df_norm=df.copy(); df_norm[cols]=(df_norm[cols]-df_norm[cols].min())/(df_norm[cols].max()-df_norm[cols].min())
df_norm["Tier"]=df_norm["Tier"].astype(str)
fig,ax=plt.subplots(figsize=(10,5))
parallel_coordinates(df_norm.sample(200,random_state=42)[cols+["Tier"]],"Tier",colormap="viridis",alpha=0.15,ax=ax)
ax.set_title("pandas.plotting.parallel_coordinates()",fontweight="bold")
ax.legend(fontsize=6); plt.tight_layout(); plt.savefig("output/parcoord_pandas.png",dpi=300); plt.close()

print("All W05-M02 Python plots saved")
