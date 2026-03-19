"""W05-M09: Snow's Cholera Map — Saving Lives with Data — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
from scipy.spatial import Voronoi, voronoi_plot_2d
from scipy.stats import gaussian_kde
from scipy.spatial.distance import cdist
os.makedirs("output", exist_ok=True); np.random.seed(1854)

# 1. SIMULATED BROAD STREET DATA
pumps = pd.DataFrame({
    "name": ["Broad Street", "Pump 2", "Pump 3", "Pump 4", "Pump 5"],
    "lon": [-0.13680, -0.1400, -0.1330, -0.1355, -0.1390],
    "lat": [51.5134, 51.5155, 51.5105, 51.5160, 51.5110]})

# Deaths: 80% near Broad Street, 20% scattered
deaths_broad = pd.DataFrame({
    "lon": np.random.normal(-0.13680, 0.0008, 400),
    "lat": np.random.normal(51.5134, 0.0006, 400)})
deaths_other = pd.DataFrame({
    "lon": np.random.normal(-0.1370, 0.0025, 100),
    "lat": np.random.normal(51.5135, 0.0020, 100)})
deaths = pd.concat([deaths_broad, deaths_other], ignore_index=True)

# 2. SNOW'S MAP RECREATION
fig, ax = plt.subplots(figsize=(7, 7))
ax.scatter(deaths.lon, deaths.lat, s=8, c="#333", marker="x", lw=0.5, alpha=0.4, label="Deaths")
ax.scatter(pumps.lon, pumps.lat, s=120, c="#E53935", marker="^", edgecolors="white",
    lw=1.5, zorder=5, label="Pumps")
for _, row in pumps.iterrows():
    ax.text(row.lon + 0.0003, row.lat + 0.0004, row["name"],
        fontsize=7, fontweight="bold", color="#E53935")
ax.legend(fontsize=8, loc="upper left")
ax.set_title("Snow's Cholera Map (Simulated Recreation)\nDeaths cluster around the Broad Street pump",
    fontsize=11, fontweight="bold")
ax.set_xlabel("Longitude"); ax.set_ylabel("Latitude")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.tick_params(labelsize=6)
plt.tight_layout(); plt.savefig("output/snow_map.png", dpi=300); plt.close()

# 3. VORONOI TESSELLATION
pump_coords = pumps[["lon", "lat"]].values
# Add mirror points for bounded Voronoi
mirror = np.vstack([pump_coords,
    pump_coords + [0.02, 0], pump_coords - [0.02, 0],
    pump_coords + [0, 0.02], pump_coords - [0, 0.02]])
vor = Voronoi(mirror)

fig, ax = plt.subplots(figsize=(7, 7))
voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors="#1565C0",
    line_width=1.5, point_size=0)
ax.scatter(deaths.lon, deaths.lat, s=5, c="#333", marker="x", lw=0.4, alpha=0.3)
ax.scatter(pumps.lon, pumps.lat, s=120, c="#E53935", marker="^",
    edgecolors="white", lw=1.5, zorder=5)
for _, row in pumps.iterrows():
    ax.text(row.lon + 0.0003, row.lat + 0.0004, row["name"],
        fontsize=7, fontweight="bold", color="#E53935")
ax.set_xlim(-0.143, -0.131); ax.set_ylim(51.509, 51.518)
ax.set_title("Voronoi Tessellation: Nearest-Pump Assignment\nBroad Street cell contains disproportionate deaths",
    fontsize=10, fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.tick_params(labelsize=6)
plt.tight_layout(); plt.savefig("output/voronoi_map.png", dpi=300); plt.close()

# 4. KDE DENSITY SURFACE
xy = np.vstack([deaths.lon, deaths.lat])
kde = gaussian_kde(xy)
xg, yg = np.mgrid[-0.143:-0.131:100j, 51.509:51.518:100j]
z = kde(np.vstack([xg.ravel(), yg.ravel()])).reshape(xg.shape)

fig, ax = plt.subplots(figsize=(7, 7))
ax.contourf(xg, yg, z, levels=15, cmap="YlOrRd", alpha=0.6)
ax.scatter(deaths.lon, deaths.lat, s=3, c="white", marker="x", lw=0.3, alpha=0.3)
ax.scatter(pumps.lon, pumps.lat, s=120, c="#E53935", marker="^",
    edgecolors="white", lw=1.5, zorder=5)
for _, row in pumps.iterrows():
    ax.text(row.lon + 0.0003, row.lat + 0.0004, row["name"],
        fontsize=7, fontweight="bold", color="#E53935")
ax.set_title("KDE Density Surface: Death Hotspot\nPeak density directly over Broad Street pump",
    fontsize=10, fontweight="bold")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.tick_params(labelsize=6)
plt.tight_layout(); plt.savefig("output/snow_kde.png", dpi=300); plt.close()

# 5. DISTANCE / NEAREST-PUMP ANALYSIS
death_coords = deaths[["lon", "lat"]].values
dists = cdist(death_coords, pump_coords, metric="euclidean")
nearest_idx = np.argmin(dists, axis=1)
deaths["nearest_pump"] = pumps["name"].iloc[nearest_idx].values

# Bar chart of deaths per pump
counts = deaths["nearest_pump"].value_counts().sort_values()
colors = ["#E53935" if n == "Broad Street" else "#BBBBBB" for n in counts.index]

fig, ax = plt.subplots(figsize=(7, 4))
ax.barh(counts.index, counts.values, color=colors, height=0.5)
for i, (name, v) in enumerate(counts.items()):
    ax.text(v + 3, i, str(v), va="center", fontsize=8, fontweight="bold")
ax.set_title("Deaths by Nearest Pump (Voronoi Assignment)\nBroad Street pump's cell: 80% of deaths",
    fontsize=10, fontweight="bold")
ax.set_xlabel("Number of Deaths")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.savefig("output/snow_bar.png", dpi=300); plt.close()

print(f"Deaths per pump:\n{deaths['nearest_pump'].value_counts()}")

# 6. FOLIUM INTERACTIVE RECREATION
try:
    import folium
    from folium.plugins import HeatMap

    m = folium.Map(location=[51.5134, -0.1368], zoom_start=17,
        tiles="CartoDB positron")

    # Deaths
    death_group = folium.FeatureGroup(name="Deaths")
    for _, row in deaths.sample(200, random_state=42).iterrows():
        folium.CircleMarker(
            [row.lat, row.lon], radius=1,
            color="#333", fill=True, fill_opacity=0.3, weight=0
        ).add_to(death_group)
    death_group.add_to(m)

    # Pumps
    pump_group = folium.FeatureGroup(name="Pumps")
    for _, row in pumps.iterrows():
        color = "#E53935" if row["name"] == "Broad Street" else "#1565C0"
        folium.Marker(
            [row.lat, row.lon],
            popup=f"<b>{row['name']}</b>",
            tooltip=row["name"],
            icon=folium.Icon(color="red" if row["name"] == "Broad Street" else "blue",
                icon="tint", prefix="fa")
        ).add_to(pump_group)
    pump_group.add_to(m)

    # Heatmap layer (hidden by default)
    heat_group = folium.FeatureGroup(name="Death Heatmap", show=False)
    heat_data = list(zip(deaths.lat, deaths.lon))
    HeatMap(heat_data, radius=10, blur=15, max_zoom=18).add_to(heat_group)
    heat_group.add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)
    m.save("output/snow_interactive.html")
    print("Interactive Snow map saved")

except ImportError:
    print("folium not installed — skipping interactive")

print("\nAll W05-M09 Python outputs saved")
