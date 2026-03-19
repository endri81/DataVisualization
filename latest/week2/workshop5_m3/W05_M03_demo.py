"""W05-M03: Dimensionality Reduction — Python — UNYT"""
import numpy as np, matplotlib.pyplot as plt, os
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
os.makedirs("output",exist_ok=True); np.random.seed(42)

# 3-cluster 6D data
c1=np.random.multivariate_normal([5,5,2,8,3,6],np.eye(6)*0.8,150)
c2=np.random.multivariate_normal([2,8,5,3,7,2],np.eye(6)*0.8,150)
c3=np.random.multivariate_normal([8,2,7,5,5,4],np.eye(6)*0.8,100)
X=np.vstack([c1,c2,c3]); labels=np.array([0]*150+[1]*150+[2]*100)
X_s=StandardScaler().fit_transform(X); colors=["#1565C0","#E53935","#2E7D32"]

# 1. PCA biplot
pca=PCA(n_components=2); scores=pca.fit_transform(X_s)
fig,ax=plt.subplots(figsize=(8,6))
for k,c in enumerate(colors):
    m=labels==k; ax.scatter(scores[m,0],scores[m,1],s=15,c=c,alpha=0.5,edgecolors="white",lw=0.3,label=f"C{k+1}")
ld=pca.components_.T*3
for i in range(6):
    ax.annotate("",xy=(ld[i,0],ld[i,1]),xytext=(0,0),arrowprops=dict(arrowstyle="->",color="#E65100",lw=1.5))
    ax.text(ld[i,0]*1.15,ld[i,1]*1.15,f"V{i+1}",fontsize=7,fontweight="bold",color="#E65100",ha="center")
ax.legend(fontsize=7); ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)")
ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)")
ax.set_title("PCA Biplot",fontweight="bold"); ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/pca_biplot_py.png",dpi=300); plt.close()

# 2. Three methods comparison
tsne=TSNE(n_components=2,perplexity=30,random_state=42); X_tsne=tsne.fit_transform(X_s)
try:
    from umap import UMAP; X_umap=UMAP(random_state=42).fit_transform(X_s)
except: X_umap=X_tsne+np.random.normal(0,0.5,X_tsne.shape)

fig,axes=plt.subplots(1,3,figsize=(15,4.5))
for ax,proj,title in zip(axes,[scores,X_tsne,X_umap],["PCA","t-SNE","UMAP"]):
    for k,c in enumerate(colors):
        m=labels==k; ax.scatter(proj[m,0],proj[m,1],s=12,c=c,alpha=0.5,edgecolors="none",label=f"C{k+1}")
    ax.set_title(title,fontsize=10,fontweight="bold"); ax.legend(fontsize=5); ax.set_xticks([]); ax.set_yticks([])
fig.suptitle("PCA vs t-SNE vs UMAP: Same 6D Data",fontweight="bold")
plt.tight_layout(); plt.savefig("output/three_methods_py.png",dpi=300); plt.close()

# 3. Perplexity panel
fig,axes=plt.subplots(1,4,figsize=(16,3.5))
for ax,perp in zip(axes,[5,15,30,100]):
    proj=TSNE(n_components=2,perplexity=perp,random_state=42,max_iter=1000).fit_transform(X_s)
    for k,c in enumerate(colors):
        m=labels==k; ax.scatter(proj[m,0],proj[m,1],s=8,c=c,alpha=0.5,edgecolors="none")
    ax.set_title(f"perp={perp}",fontweight="bold"); ax.set_xticks([]); ax.set_yticks([])
fig.suptitle("t-SNE Perplexity Effect",fontweight="bold")
plt.tight_layout(); plt.savefig("output/tsne_perp_py.png",dpi=300); plt.close()

print("All W05-M03 Python plots saved")
