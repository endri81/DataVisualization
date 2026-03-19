"""W05-M07: Point Maps & Spatial Patterns — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
from scipy.stats import gaussian_kde
os.makedirs("output", exist_ok=True); np.random.seed(42)

# 1. SIMULATED EVENTS
n = 500
events = pd.DataFrame({
    "lon": np.random.normal(19.82, 0.5, n),
    "lat": np.random.normal(41.00, 0.4, n),
    "magnitude": np.random.exponential(1, n) + 2,
    "depth_km": np.random.uniform(1, 60, n)})

cities = pd.DataFrame({
    "name": ["Tirana","Durrës","Vlorë","Shkodër","Elbasan","Korçë","Fier","Berat"],
    "lon": [19.82,19.45,19.49,19.51,20.08,20.78,19.55,19.95],
    "lat": [41.33,41.32,40.47,42.07,41.11,40.62,40.72,40.70],
    "pop": [420000,115000,79000,77000,78000,51000,85000,32000]})

# 2. DOT MAP
fig, ax = plt.subplots(figsize=(6, 7))
ax.scatter(events.lon, events.lat, s=3, c="#E53935", alpha=0.3, edgecolors="none")
ax.set_title("Dot Map: 500 Seismic Events", fontweight="bold")
ax.set_xlabel("Longitude"); ax.set_ylabel("Latitude")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/dot_map.png", dpi=300); plt.close()

# 3. PROPORTIONAL SYMBOL MAP
fig, ax = plt.subplots(figsize=(6, 7))
ax.scatter(cities.lon, cities.lat, s=cities["pop"]/3000, c="#1565C0",
    alpha=0.5, edgecolors="white", lw=1, zorder=5)
for _, row in cities.iterrows():
    ax.text(row.lon + 0.06, row.lat + 0.06, row["name"],
        fontsize=7, fontweight="bold", color="#333")
ax.set_title("Proportional Symbol: Cities by Population", fontweight="bold")
ax.set_xlabel("Longitude"); ax.set_ylabel("Latitude")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/prop_symbol.png", dpi=300); plt.close()

# 4. OVERPLOTTING SOLUTIONS — 3-panel
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 4.5))

# (a) Low alpha
ax1.scatter(events.lon, events.lat, s=3, c="#E53935", alpha=0.05, edgecolors="none")
ax1.set_title("(a) Low alpha (0.05)", fontsize=9, fontweight="bold")

# (b) Hexbin
hb = ax2.hexbin(events.lon, events.lat, gridsize=20, cmap="YlOrRd", mincnt=1)
plt.colorbar(hb, ax=ax2, shrink=0.7, label="Count")
ax2.set_title("(b) Hexbin", fontsize=9, fontweight="bold")

# (c) 2D KDE contour
xy = np.vstack([events.lon, events.lat])
kde = gaussian_kde(xy)
xg, yg = np.mgrid[18.5:21.0:100j, 39.8:42.2:100j]
z = kde(np.vstack([xg.ravel(), yg.ravel()])).reshape(xg.shape)
ax3.contourf(xg, yg, z, levels=12, cmap="YlOrRd")
ax3.scatter(events.lon, events.lat, s=1, c="white", alpha=0.15)
ax3.set_title("(c) 2D KDE Contour", fontsize=9, fontweight="bold")

for ax in [ax1, ax2, ax3]:
    ax.tick_params(labelsize=6)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
fig.suptitle("Overplotting Solutions: 500 Events", fontsize=12, fontweight="bold")
plt.tight_layout(); plt.savefig("output/overplotting_panel.png", dpi=300); plt.close()

# 5. KDE + PROPORTIONAL SYMBOL COMBO
fig, ax = plt.subplots(figsize=(7, 7))
ax.contourf(xg, yg, z, levels=12, cmap="YlOrRd", alpha=0.6)
ax.scatter(cities.lon, cities.lat, s=cities["pop"]/3000, c="#1565C0",
    alpha=0.7, edgecolors="white", lw=1, zorder=5)
for _, row in cities.iterrows():
    ax.text(row.lon + 0.05, row.lat + 0.05, row["name"],
        fontsize=6, fontweight="bold", color="#333")
ax.set_title("KDE Density + City Proportional Symbols", fontweight="bold")
ax.set_aspect("equal"); ax.set_xlabel("Lon"); ax.set_ylabel("Lat")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/combo_map.png", dpi=300); plt.close()

# 6. SEABORN JOINTPLOT (scatter + marginals)
import seaborn as sns
g = sns.jointplot(data=events, x="lon", y="lat", hue=None,
    kind="kde", fill=True, cmap="YlOrRd", height=6)
g.ax_joint.scatter(events.lon, events.lat, s=1, c="#333", alpha=0.1)
g.fig.suptitle("Jointplot: KDE + Marginal Histograms", fontweight="bold", y=1.02)
plt.savefig("output/jointplot_map.png", dpi=300, bbox_inches="tight"); plt.close()

# 7. FOLIUM INTERACTIVE DOT MAP
try:
    import folium
    from folium.plugins import HeatMap

    # Dot map with popups
    m = folium.Map(location=[41.0, 19.82], zoom_start=8,
        tiles="CartoDB positron")
    for _, row in events.sample(200, random_state=42).iterrows():
        folium.CircleMarker(
            location=[row.lat, row.lon],
            radius=row.magnitude / 2,
            color="#E53935", fill=True, fill_opacity=0.4, weight=0.5,
            popup=f"Mag: {row.magnitude:.1f}<br>Depth: {row.depth_km:.0f} km",
            tooltip=f"M{row.magnitude:.1f}"
        ).add_to(m)
    # Add cities as larger blue markers
    for _, row in cities.iterrows():
        folium.CircleMarker(
            location=[row.lat, row.lon],
            radius=row["pop"] ** 0.5 / 80,
            color="#1565C0", fill=True, fill_opacity=0.6, weight=1.5,
            popup=f"<b>{row['name']}</b><br>Pop: {row['pop']:,}",
            tooltip=row["name"]
        ).add_to(m)
    m.save("output/point_map_interactive.html")
    print("Interactive dot map saved")

    # Heatmap version
    m2 = folium.Map(location=[41.0, 19.82], zoom_start=8,
        tiles="CartoDB dark_matter")
    heat_data = list(zip(events.lat, events.lon, events.magnitude))
    HeatMap(heat_data, radius=15, blur=20, max_zoom=12).add_to(m2)
    m2.save("output/heatmap_interactive.html")
    print("Interactive heatmap saved")

except ImportError:
    print("folium not installed — skipping interactive maps")

print("\nAll W05-M07 Python outputs saved")
