"""W05-M04: Heatmaps & Clustered Displays — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, seaborn as sns, os
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.stats import zscore
os.makedirs("output", exist_ok=True); np.random.seed(42)

# 1. SIMULATED MATRIX (3 clusters x 10 features)
g1 = np.random.normal(2, 0.5, (8, 10)); g1[:, :4] += 3
g2 = np.random.normal(2, 0.5, (9, 10)); g2[:, 4:7] += 3
g3 = np.random.normal(2, 0.5, (8, 10)); g3[:, 7:] += 3
data = np.vstack([g1, g2, g3])
samples = [f"S{i+1}" for i in range(25)]
features = [f"F{i+1}" for i in range(10)]
cluster_labels = ["A"]*8 + ["B"]*9 + ["C"]*8
df = pd.DataFrame(data, index=samples, columns=features)

# 2. BASIC HEATMAP (no clustering)
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(df, cmap="YlOrRd", linewidths=0.5, ax=ax)
ax.set_title("Basic Heatmap (no clustering)", fontweight="bold")
plt.tight_layout(); plt.savefig("output/basic_heatmap.png", dpi=300); plt.close()

# 3. CLUSTERED HEATMAP (sns.clustermap)
# Row colour sidebar
palette = {"A": "#1565C0", "B": "#E53935", "C": "#2E7D32"}
row_colors = pd.Series(cluster_labels, index=samples).map(palette)

g = sns.clustermap(df,
    method="ward", metric="euclidean",
    cmap="RdBu_r", center=0,
    figsize=(8, 10), linewidths=0.3,
    row_colors=row_colors,
    cbar_kws={"label": "Value"},
    dendrogram_ratio=(0.15, 0.15))
g.ax_heatmap.set_title("Clustered Heatmap (Ward)", fontsize=11, fontweight="bold", pad=10)
plt.savefig("output/clustered_heatmap.png", dpi=300, bbox_inches="tight"); plt.close()

# 4. Z-SCORED HEATMAP
g2 = sns.clustermap(df,
    method="ward", metric="euclidean",
    standard_scale=0,  # z-score rows
    cmap="RdBu_r", center=0,
    figsize=(8, 10), linewidths=0.3,
    row_colors=row_colors,
    cbar_kws={"label": "Z-score"})
g2.ax_heatmap.set_title("Z-Scored Heatmap (row-normalised)", fontsize=11, fontweight="bold", pad=10)
plt.savefig("output/zscore_heatmap.png", dpi=300, bbox_inches="tight"); plt.close()

# 5. CORRELATION HEATMAP (e-Car)
ecar = pd.read_csv("ecar.csv")
ecar.columns = [c.strip().replace("  ", " ") for c in ecar.columns]
ecar["Spread"] = ecar["Rate"] - ecar["Cost of Funds"]
num_cols = ["FICO", "Rate", "Amount", "Term", "Cost of Funds", "Spread"]
corr = ecar[num_cols].corr()

# Lower triangle mask
mask = np.triu(np.ones_like(corr, dtype=bool))
fig, ax = plt.subplots(figsize=(7, 6))
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="RdBu_r",
    vmin=-1, vmax=1, center=0, square=True, linewidths=0.5, ax=ax,
    cbar_kws={"shrink": 0.8, "label": "Pearson r"})
ax.set_title("e-Car: Correlation Heatmap (lower triangle)", fontweight="bold")
plt.tight_layout(); plt.savefig("output/corr_heatmap.png", dpi=300); plt.close()

# 6. MANUAL CLUSTERED HEATMAP with dendrograms (scipy)
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import pdist

fig = plt.figure(figsize=(10, 8))
ax_dendro_top = fig.add_axes([0.15, 0.78, 0.7, 0.15])
ax_dendro_left = fig.add_axes([0.0, 0.1, 0.12, 0.65])
ax_heat = fig.add_axes([0.15, 0.1, 0.7, 0.65])
ax_cbar = fig.add_axes([0.88, 0.1, 0.03, 0.65])

Z_row = linkage(pdist(data, "euclidean"), "ward")
dn_row = dendrogram(Z_row, ax=ax_dendro_left, orientation="left", no_labels=True,
    color_threshold=0, above_threshold_color="#888")
row_order = dn_row["leaves"]

Z_col = linkage(pdist(data.T, "euclidean"), "ward")
dn_col = dendrogram(Z_col, ax=ax_dendro_top, no_labels=True,
    color_threshold=0, above_threshold_color="#888")
col_order = dn_col["leaves"]

data_ordered = data[row_order][:, col_order]
im = ax_heat.imshow(data_ordered, cmap="RdBu_r", aspect="auto", vmin=0, vmax=6)
ax_heat.set_xticks(range(10)); ax_heat.set_xticklabels([features[i] for i in col_order], fontsize=6, rotation=45)
ax_heat.set_yticks(range(25)); ax_heat.set_yticklabels([samples[i] for i in row_order], fontsize=5)
plt.colorbar(im, cax=ax_cbar, label="Value")
for ax in [ax_dendro_top, ax_dendro_left]:
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_visible(False)
fig.suptitle("Manual Clustered Heatmap with Dendrograms", fontsize=12, fontweight="bold", y=0.97)
fig.savefig("output/manual_clustered.png", dpi=300, bbox_inches="tight"); plt.close()

print("All W05-M04 Python outputs saved")
