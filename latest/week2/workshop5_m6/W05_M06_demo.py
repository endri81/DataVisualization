"""W05-M06: Choropleth Maps — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
os.makedirs("output", exist_ok=True); np.random.seed(42)

# 1. SIMULATED DISTRICTS
districts = pd.DataFrame({
    "name": ["Tirana","Durrës","Elbasan","Fier","Korçë","Shkodër",
             "Vlorë","Berat","Dibër","Gjirokastër","Kukës","Lezhë"],
    "population": [420000,115000,78000,85000,51000,77000,
                   79000,32000,36000,28000,26000,38000],
    "gdp_per_cap": [8500,5200,3800,4100,3500,3900,
                    4800,3200,2800,3600,2500,3400],
    "unemployment": [12.5,15.3,18.7,16.2,19.8,17.1,
                     14.3,20.5,22.1,18.9,24.3,17.8],
    "lon": [19.82,19.45,20.08,19.55,20.78,19.51,
            19.49,19.95,20.24,20.14,20.42,19.64],
    "lat": [41.33,41.32,41.11,40.72,40.62,42.07,
            40.47,40.70,41.61,40.08,42.08,41.78]})

# Create rectangular polygons
def make_rect(lon, lat, dx=0.25, dy=0.15):
    return [(lon-dx,lat-dy),(lon+dx,lat-dy),(lon+dx,lat+dy),(lon-dx,lat+dy),(lon-dx,lat-dy)]

# 2. MATPLOTLIB CHOROPLETH (no geopandas dependency)
fig, ax = plt.subplots(figsize=(7, 8))
cmap = plt.cm.plasma; norm = plt.Normalize(districts["population"].min(), districts["population"].max())
patches = []
for _, row in districts.iterrows():
    rect_coords = make_rect(row.lon, row.lat)
    poly = Polygon(rect_coords, closed=True)
    patches.append(poly)
    ax.text(row.lon, row.lat, f"{row['name']}\n{row.population:,}",
        ha="center", va="center", fontsize=5.5, fontweight="bold")
pc = PatchCollection(patches, cmap=cmap, edgecolors="white", linewidths=1.5)
pc.set_array(districts["population"].values)
pc.set_clim(districts["population"].min(), districts["population"].max())
ax.add_collection(pc)
ax.set_xlim(18.8, 21.2); ax.set_ylim(39.7, 42.5); ax.set_aspect("equal")
plt.colorbar(pc, ax=ax, shrink=0.6, label="Population")
ax.set_title("Albania: Population by District\n(Sequential palette — plasma)", fontweight="bold")
ax.axis("off")
plt.tight_layout(); plt.savefig("output/choropleth_pop.png", dpi=300); plt.close()

# 3. DIVERGING PALETTE — unemployment deviation
fig, ax = plt.subplots(figsize=(7, 8))
nat_avg = districts["unemployment"].mean()
deviations = districts["unemployment"] - nat_avg
cmap_div = plt.cm.RdBu_r; norm_div = plt.Normalize(-6, 6)
patches2 = []
for _, row in districts.iterrows():
    patches2.append(Polygon(make_rect(row.lon, row.lat), closed=True))
    dev = row.unemployment - nat_avg
    ax.text(row.lon, row.lat, f"{row['name']}\n{dev:+.1f}pp",
        ha="center", va="center", fontsize=5.5, fontweight="bold")
pc2 = PatchCollection(patches2, cmap=cmap_div, edgecolors="white", linewidths=1.5)
pc2.set_array(deviations.values); pc2.set_clim(-6, 6)
ax.add_collection(pc2)
ax.set_xlim(18.8, 21.2); ax.set_ylim(39.7, 42.5); ax.set_aspect("equal")
plt.colorbar(pc2, ax=ax, shrink=0.6, label="Deviation from national avg (pp)")
ax.set_title(f"Unemployment: Deviation from {nat_avg:.1f}% avg\n(Diverging palette — RdBu, centred at 0)", fontweight="bold")
ax.axis("off")
plt.tight_layout(); plt.savefig("output/choropleth_unemp.png", dpi=300); plt.close()

# 4. GEOPANDAS VERSION (if available)
try:
    import geopandas as gpd
    from shapely.geometry import Polygon as ShapelyPoly

    geometry = [ShapelyPoly(make_rect(row.lon, row.lat)) for _, row in districts.iterrows()]
    gdf = gpd.GeoDataFrame(districts, geometry=geometry, crs="EPSG:4326")

    # Choropleth with classification (requires mapclassify)
    try:
        fig, ax = plt.subplots(figsize=(7, 8))
        gdf.plot(column="gdp_per_cap", cmap="Blues", legend=True,
            edgecolor="white", linewidth=1, ax=ax,
            scheme="NaturalBreaks", k=5,
            legend_kwds={"title": "GDP/cap (Jenks)", "fontsize": 7})
        ax.set_title("GDP per Capita: Natural Breaks (Jenks, k=5)", fontweight="bold")
        ax.axis("off")
        plt.tight_layout(); plt.savefig("output/choropleth_jenks.png", dpi=300); plt.close()
        print("Jenks classification choropleth saved")
    except Exception as e:
        print(f"mapclassify not available: {e}")

    # Equal interval comparison
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    gdf.plot(column="gdp_per_cap", cmap="Blues", legend=True,
        edgecolor="white", linewidth=1, ax=ax1, scheme="EqualInterval", k=5,
        legend_kwds={"title": "Equal Interval"})
    ax1.set_title("Equal Interval (5 classes)", fontweight="bold"); ax1.axis("off")
    gdf.plot(column="gdp_per_cap", cmap="Blues", legend=True,
        edgecolor="white", linewidth=1, ax=ax2, scheme="Quantiles", k=5,
        legend_kwds={"title": "Quantile"})
    ax2.set_title("Quantile (5 classes)", fontweight="bold"); ax2.axis("off")
    fig.suptitle("Classification Comparison: Same Data, Different Breaks", fontweight="bold")
    plt.tight_layout(); plt.savefig("output/classification_compare.png", dpi=300); plt.close()
    print("Classification comparison saved")

except ImportError:
    print("geopandas not installed — matplotlib versions only")

# 5. FOLIUM INTERACTIVE CHOROPLETH
try:
    import folium
    m = folium.Map(location=[41.0, 19.8], zoom_start=7, tiles="CartoDB positron")

    # Without GeoJSON file, add coloured rectangles manually
    cmap_f = plt.cm.YlOrRd; norm_f = plt.Normalize(districts.population.min(), districts.population.max())
    for _, row in districts.iterrows():
        color_rgba = cmap_f(norm_f(row.population))
        color_hex = "#{:02x}{:02x}{:02x}".format(int(color_rgba[0]*255), int(color_rgba[1]*255), int(color_rgba[2]*255))
        bounds = [[row.lat-0.15, row.lon-0.25], [row.lat+0.15, row.lon+0.25]]
        folium.Rectangle(bounds=bounds, color="white", weight=1.5,
            fill=True, fill_color=color_hex, fill_opacity=0.7,
            popup=f"<b>{row['name']}</b><br>Pop: {row.population:,}<br>GDP/cap: €{row.gdp_per_cap:,}",
            tooltip=row["name"]
        ).add_to(m)

    m.save("output/choropleth_interactive.html")
    print("Interactive choropleth saved: output/choropleth_interactive.html")
except ImportError:
    print("folium not installed — skipping interactive")

print("\nAll W05-M06 Python outputs saved")
