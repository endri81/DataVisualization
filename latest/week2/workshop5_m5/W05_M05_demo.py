"""W05-M05: Introduction to Spatial Data — Python — UNYT"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
os.makedirs("output", exist_ok=True)

# 1. CREATE SPATIAL DATA FROM SCRATCH
cities = pd.DataFrame({
    "name": ["Tirana", "Durrës", "Vlorë", "Shkodër", "Elbasan", "Korçë"],
    "lon": [19.82, 19.45, 19.49, 19.51, 20.08, 20.78],
    "lat": [41.33, 41.32, 40.47, 42.07, 41.11, 40.62],
    "pop_2023": [420000, 115000, 79000, 77000, 78000, 51000]})

# Convert to GeoDataFrame
try:
    import geopandas as gpd
    from shapely.geometry import Point, Polygon

    # Points from lat/lon columns
    geometry = [Point(lon, lat) for lon, lat in zip(cities.lon, cities.lat)]
    cities_gdf = gpd.GeoDataFrame(cities, geometry=geometry, crs="EPSG:4326")
    print("GeoDataFrame created:")
    print(cities_gdf)
    print(f"CRS: {cities_gdf.crs}")

    # 2. PLOT
    fig, ax = plt.subplots(figsize=(6, 7))
    cities_gdf.plot(ax=ax, markersize=cities_gdf["pop_2023"] / 5000,
        color="#E53935", alpha=0.6, edgecolor="white", lw=0.5)
    for _, row in cities_gdf.iterrows():
        ax.text(row.geometry.x + 0.05, row.geometry.y + 0.05,
            row["name"], fontsize=7, fontweight="bold")
    ax.set_title("Albanian Cities (GeoDataFrame, EPSG:4326)", fontweight="bold")
    ax.set_xlabel("Longitude"); ax.set_ylabel("Latitude")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    plt.tight_layout(); plt.savefig("output/cities_gpd.png", dpi=300); plt.close()

    # 3. CRS TRANSFORMATION
    cities_utm = cities_gdf.to_crs(epsg=32634)
    print(f"\nUTM CRS: {cities_utm.crs}")

    # 4. SIMPLIFIED ALBANIA POLYGON
    alb_coords = [(19.3,39.6),(19.8,39.7),(20.1,39.8),(20.6,40.0),
        (21.0,40.5),(20.7,41.0),(20.5,41.5),(20.3,42.0),
        (20.0,42.1),(19.5,41.8),(19.3,41.5),(19.0,40.5),(19.3,39.6)]
    alb_poly = gpd.GeoDataFrame({"name": ["Albania"]},
        geometry=[Polygon(alb_coords)], crs="EPSG:4326")

    # Overlay
    fig, ax = plt.subplots(figsize=(6, 7))
    alb_poly.plot(ax=ax, facecolor="#E3F2FD", edgecolor="#1565C0", linewidth=1.5)
    cities_gdf.plot(ax=ax, markersize=cities_gdf["pop_2023"] / 5000,
        color="#E53935", alpha=0.6, edgecolor="white", lw=0.5, zorder=5)
    for _, row in cities_gdf.iterrows():
        ax.text(row.geometry.x + 0.05, row.geometry.y + 0.05,
            row["name"], fontsize=7, fontweight="bold")
    ax.set_title("Albania: Points on Polygon", fontweight="bold")
    ax.set_aspect("equal"); ax.axis("off")
    plt.tight_layout(); plt.savefig("output/overlay_gpd.png", dpi=300); plt.close()

    # 5. FILE I/O
    cities_gdf.to_file("output/cities.geojson", driver="GeoJSON")
    cities_gdf.to_file("output/cities.gpkg", driver="GPKG")
    back = gpd.read_file("output/cities.geojson")
    print(f"\nRead back: {len(back)} features")

except ImportError:
    print("geopandas not installed — using matplotlib fallback")
    fig, ax = plt.subplots(figsize=(6, 7))
    # Simple Albania outline
    lons = [19.3,19.8,20.1,20.6,21.0,20.7,20.5,20.3,20.0,19.5,19.3,19.0,19.3]
    lats = [39.6,39.7,39.8,40.0,40.5,41.0,41.5,42.0,42.1,41.8,41.5,40.5,39.6]
    ax.fill(lons, lats, alpha=0.15, color="#1565C0", edgecolor="#1565C0", lw=2)
    ax.scatter(cities.lon, cities.lat, s=cities.pop_2023/5000,
        c="#E53935", alpha=0.6, edgecolors="white", lw=0.5, zorder=5)
    for _, row in cities.iterrows():
        ax.text(row.lon + 0.05, row.lat + 0.05, row["name"], fontsize=7, fontweight="bold")
    ax.set_title("Albania (matplotlib fallback)", fontweight="bold")
    ax.set_aspect("equal")
    plt.tight_layout(); plt.savefig("output/albania_fallback.png", dpi=300); plt.close()

# 6. FOLIUM INTERACTIVE (standalone HTML)
try:
    import folium
    m = folium.Map(location=[41.33, 19.82], zoom_start=7,
        tiles="CartoDB positron")
    for _, row in cities.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=row["pop_2023"] ** 0.5 / 100,
            color="#E53935", fill=True, fill_opacity=0.6,
            popup=f"<b>{row['name']}</b><br>Pop: {row['pop_2023']:,}",
            tooltip=row["name"]
        ).add_to(m)
    m.save("output/albania_cities.html")
    print("Interactive map saved: output/albania_cities.html")
except ImportError:
    print("folium not installed — skipping interactive map")

print("\nAll W05-M05 Python outputs saved")
