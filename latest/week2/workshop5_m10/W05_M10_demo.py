"""W05-M10: Lab — Multivariate EDA on Real Estate — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, seaborn as sns, os
from matplotlib.gridspec import GridSpec
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy.stats import spearmanr
os.makedirs("output", exist_ok=True); np.random.seed(42)

# 1. SIMULATED REAL ESTATE DATA
n = 200
re = pd.DataFrame({
    "price": np.round(np.random.lognormal(np.log(80000), 0.6, n)),
    "area_sqm": np.round(np.random.normal(85, 30, n).clip(25)),
    "bedrooms": np.random.choice([1,2,3,4,5], n, p=[0.1,0.3,0.35,0.2,0.05]),
    "bathrooms": np.random.choice([1,2,3], n, p=[0.3,0.5,0.2]),
    "year_built": np.random.choice(range(1970, 2024), n),
    "floor": np.random.choice(range(13), n),
    "type": np.random.choice(["apartment","house"], n, p=[0.75,0.25]),
    "condition": np.random.choice(["new","renovated","original"], n, p=[0.3,0.4,0.3]),
    "lon": np.random.normal(19.82, 0.025, n),
    "lat": np.random.normal(41.33, 0.015, n),
    "neighbourhood": np.random.choice(["Blloku","Komuna e Parisit","21 Dhjetori",
        "Ish-Blloku","Medreseja","Selvia"], n)})
re["price"] = np.where(re["type"]=="house", re["price"]*1.5, re["price"])
re["price"] = np.where(re["neighbourhood"]=="Blloku", re["price"]*1.3, re["price"])
re["price"] = re["price"] + (re["year_built"]-1990)*200
re["price_sqm"] = np.round(re["price"] / re["area_sqm"])
print(f"Dataset: {len(re)} properties, {re.shape[1]} variables")

# 2. SIX-PANEL DASHBOARD
fig = plt.figure(figsize=(14, 9)); gs = GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.35)

ax = fig.add_subplot(gs[0,0])
ax.hist(re["price"]/1000, bins=30, color="#1565C0", edgecolor="white", lw=0.3)
ax.axvline(x=re["price"].median()/1000, color="#E53935", lw=1.5, ls="--")
ax.set_title("(a) Price Distribution", fontsize=9, fontweight="bold")
ax.set_xlabel("Price (000 EUR)")

ax = fig.add_subplot(gs[0,1])
ax.hist(re["area_sqm"], bins=25, color="#2E7D32", edgecolor="white", lw=0.3)
ax.set_title("(b) Area (sqm)", fontsize=9, fontweight="bold")

ax = fig.add_subplot(gs[0,2])
counts = re["type"].value_counts()
ax.bar(counts.index, counts.values, color=["#1565C0","#E53935"], width=0.5)
ax.set_title("(c) Type Split", fontsize=9, fontweight="bold")

ax = fig.add_subplot(gs[1,0])
for t, c in [("apartment","#1565C0"),("house","#E53935")]:
    mask = re["type"]==t
    ax.scatter(re.loc[mask,"area_sqm"], re.loc[mask,"price"]/1000, s=10, c=c, alpha=0.4, label=t)
    z = np.polyfit(re.loc[mask,"area_sqm"], re.loc[mask,"price"]/1000, 1)
    xs = np.linspace(re["area_sqm"].min(), re["area_sqm"].max(), 50)
    ax.plot(xs, np.polyval(z, xs), c=c, lw=1.5)
ax.legend(fontsize=6); ax.set_title("(d) Area vs Price", fontsize=9, fontweight="bold")
ax.set_xlabel("Area (sqm)"); ax.set_ylabel("Price (000 EUR)")

ax = fig.add_subplot(gs[1,1])
nbhd_order = re.groupby("neighbourhood")["price_sqm"].median().sort_values().index
data_by_nbhd = [re.query("neighbourhood==@nb")["price_sqm"].values for nb in nbhd_order]
bp = ax.boxplot(data_by_nbhd, labels=nbhd_order, vert=False, patch_artist=True, widths=0.5)
for patch in bp["boxes"]: patch.set_facecolor("#BBDEFB")
ax.set_title("(e) EUR/sqm by Neighbourhood", fontsize=9, fontweight="bold")
ax.tick_params(labelsize=6)

ax = fig.add_subplot(gs[1,2])
for cond, c in [("new","#1565C0"),("renovated","#2E7D32"),("original","#E53935")]:
    d = re.query("condition==@cond")["price"]/1000
    parts = ax.violinplot([d], positions=[["new","renovated","original"].index(cond)], showmedians=True)
    parts["bodies"][0].set_facecolor(c); parts["bodies"][0].set_alpha(0.3)
ax.set_xticks([0,1,2]); ax.set_xticklabels(["new","renovated","original"], fontsize=7)
ax.set_title("(f) Price by Condition", fontsize=9, fontweight="bold")

for a in fig.get_axes(): a.tick_params(labelsize=6); a.spines["top"].set_visible(False); a.spines["right"].set_visible(False)
fig.suptitle(f"Real Estate EDA: {len(re)} Properties in Tirana\nMedian: EUR {re['price'].median():,.0f} | {re['area_sqm'].median():.0f} sqm", fontsize=13, fontweight="bold")
plt.savefig("output/re_dashboard.png", dpi=300, bbox_inches="tight")
plt.savefig("output/re_dashboard.pdf", bbox_inches="tight"); plt.close()

# 3. PCA BIPLOT
num_cols = ["price","area_sqm","bedrooms","bathrooms","year_built","floor"]
X = StandardScaler().fit_transform(re[num_cols])
pca = PCA(n_components=2); scores = pca.fit_transform(X)

fig, ax = plt.subplots(figsize=(8, 6))
for t, c in [("apartment","#1565C0"),("house","#E53935")]:
    mask = re["type"]==t
    ax.scatter(scores[mask,0], scores[mask,1], s=15, c=c, alpha=0.4, edgecolors="white", lw=0.3, label=t)
loadings = pca.components_.T * 3
for i, name in enumerate(num_cols):
    ax.annotate("", xy=(loadings[i,0],loadings[i,1]), xytext=(0,0),
        arrowprops=dict(arrowstyle="->", color="#E65100", lw=1.5))
    ax.text(loadings[i,0]*1.15, loadings[i,1]*1.15, name, fontsize=7, fontweight="bold", color="#E65100", ha="center")
ax.axhline(y=0, color="#888", lw=0.5, ls=":"); ax.axvline(x=0, color="#888", lw=0.5, ls=":")
ax.legend(fontsize=8)
ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)")
ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)")
ax.set_title("PCA Biplot: Real Estate Features", fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/re_pca.png", dpi=300); plt.close()

# 4. CORRELATION HEATMAP
corr = re[num_cols].corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
fig, ax = plt.subplots(figsize=(7, 6))
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="RdBu_r",
    vmin=-1, vmax=1, center=0, square=True, linewidths=0.5, ax=ax,
    cbar_kws={"shrink": 0.8, "label": "Pearson r"})
ax.set_title("Correlation Heatmap: Real Estate", fontweight="bold")
plt.tight_layout(); plt.savefig("output/re_corr.png", dpi=300); plt.close()

# 5. CLUSTERED HEATMAP (z-scored subset)
sub = re[num_cols].sample(30, random_state=42)
g = sns.clustermap(sub, method="ward", standard_scale=1, cmap="RdBu_r",
    figsize=(8, 8), linewidths=0.3, cbar_kws={"label": "Z-score"})
g.ax_heatmap.set_title("Clustered Heatmap (30 properties, z-scored)", fontsize=10, fontweight="bold")
plt.savefig("output/re_clustermap.png", dpi=300, bbox_inches="tight"); plt.close()

# 6. PARALLEL COORDINATES
from pandas.plotting import parallel_coordinates
df_norm = re[num_cols + ["type"]].copy()
for c in num_cols:
    df_norm[c] = (df_norm[c] - df_norm[c].min()) / (df_norm[c].max() - df_norm[c].min())
fig, ax = plt.subplots(figsize=(10, 4))
parallel_coordinates(df_norm.sample(100, random_state=42), "type",
    colormap="coolwarm", alpha=0.15, ax=ax)
ax.set_title("Parallel Coordinates: Real Estate by Type", fontweight="bold")
ax.legend(fontsize=7); ax.tick_params(labelsize=7)
plt.tight_layout(); plt.savefig("output/re_parcoord.png", dpi=300); plt.close()

# 7. SPATIAL POINT MAP
fig, ax = plt.subplots(figsize=(7, 7))
sc = ax.scatter(re.lon, re.lat, c=re.price_sqm, s=re.area_sqm/3,
    cmap="plasma", alpha=0.5, edgecolors="white", lw=0.3)
plt.colorbar(sc, ax=ax, shrink=0.7, label="EUR/sqm")
ax.set_title("Tirana: Properties by Price/sqm (colour) and Area (size)", fontweight="bold")
ax.set_xlabel("Longitude"); ax.set_ylabel("Latitude")
ax.set_aspect("equal"); ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/re_spatial.png", dpi=300); plt.close()

# 8. FOLIUM INTERACTIVE
try:
    import folium
    import matplotlib
    cmap_f = plt.cm.plasma
    norm_f = plt.Normalize(re.price_sqm.min(), re.price_sqm.max())

    m = folium.Map(location=[41.33, 19.82], zoom_start=14, tiles="CartoDB positron")
    for _, row in re.iterrows():
        rgba = cmap_f(norm_f(row.price_sqm))
        hex_c = "#{:02x}{:02x}{:02x}".format(int(rgba[0]*255), int(rgba[1]*255), int(rgba[2]*255))
        folium.CircleMarker(
            [row.lat, row.lon],
            radius=max(2, row.area_sqm / 30),
            color=hex_c, fill=True, fill_color=hex_c, fill_opacity=0.6, weight=0.5,
            popup=(f"<b>{row.neighbourhood}</b><br>"
                   f"Type: {row.type}<br>"
                   f"Price: EUR {row.price:,.0f}<br>"
                   f"Area: {row.area_sqm:.0f} sqm<br>"
                   f"EUR/sqm: {row.price_sqm:,.0f}"),
            tooltip=f"EUR {row.price:,.0f}"
        ).add_to(m)
    m.save("output/re_interactive.html")
    print("Interactive map saved")
except ImportError:
    print("folium not installed — skipping")

# 9. KEY STATISTICS
rho, _ = spearmanr(re["area_sqm"], re["price"])
print(f"\nMedian price: EUR {re['price'].median():,.0f}")
print(f"Median area: {re['area_sqm'].median():.0f} sqm")
print(f"Spearman(area, price): {rho:.3f}")
print(f"PCA: PC1={pca.explained_variance_ratio_[0]*100:.1f}%, PC2={pca.explained_variance_ratio_[1]*100:.1f}%")
print("\nAll W05-M10 Lab Python outputs saved")
