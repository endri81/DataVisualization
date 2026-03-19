"""W05-M08: Interactive Maps — Python — UNYT"""
import numpy as np, pandas as pd, os
os.makedirs("output", exist_ok=True); np.random.seed(42)

# Data
cities = pd.DataFrame({
    "name": ["Tirana","Durrës","Vlorë","Shkodër","Elbasan","Korçë","Fier","Berat"],
    "lon": [19.82, 19.45, 19.49, 19.51, 20.08, 20.78, 19.55, 19.95],
    "lat": [41.33, 41.32, 40.47, 42.07, 41.11, 40.62, 40.72, 40.70],
    "pop": [420000, 115000, 79000, 77000, 78000, 51000, 85000, 32000],
    "gdp": [8500, 5200, 4800, 3900, 3800, 3500, 4100, 3200]})

events = pd.DataFrame({
    "lon": np.random.normal(19.82, 0.4, 300),
    "lat": np.random.normal(41.0, 0.3, 300),
    "magnitude": np.random.exponential(1, 300) + 2,
    "depth": np.random.uniform(1, 50, 300)})

try:
    import folium
    from folium.plugins import HeatMap, MarkerCluster

    # 1. BASIC MAP WITH CIRCLE MARKERS
    m1 = folium.Map(location=[41.33, 19.82], zoom_start=7,
        tiles="CartoDB positron")
    for _, row in cities.iterrows():
        folium.CircleMarker(
            location=[row.lat, row.lon],
            radius=row["pop"] ** 0.5 / 80,
            color="#1565C0", fill=True, fill_opacity=0.6, weight=1,
            popup=folium.Popup(
                f"<b>{row['name']}</b><br>"
                f"Population: {row['pop']:,}<br>"
                f"GDP/cap: EUR {row['gdp']:,}", max_width=200),
            tooltip=row["name"]
        ).add_to(m1)
    m1.save("output/m08_basic.html")
    print("1. Basic map saved")

    # 2. MULTIPLE TILE LAYERS
    m2 = folium.Map(location=[41.33, 19.82], zoom_start=7)
    folium.TileLayer("CartoDB positron", name="Light").add_to(m2)
    folium.TileLayer("CartoDB dark_matter", name="Dark").add_to(m2)
    folium.TileLayer("OpenStreetMap", name="OSM").add_to(m2)
    # Add cities
    city_group = folium.FeatureGroup(name="Cities")
    for _, row in cities.iterrows():
        folium.CircleMarker(
            [row.lat, row.lon],
            radius=row["pop"] ** 0.5 / 80,
            color="#E53935", fill=True, fill_opacity=0.5,
            tooltip=row["name"]
        ).add_to(city_group)
    city_group.add_to(m2)
    folium.LayerControl().add_to(m2)
    m2.save("output/m08_tiles.html")
    print("2. Multi-tile map saved")

    # 3. EVENT MARKERS WITH COLOUR BY MAGNITUDE
    import matplotlib.pyplot as plt
    cmap = plt.cm.YlOrRd
    norm = plt.Normalize(events.magnitude.min(), events.magnitude.max())

    m3 = folium.Map(location=[41.0, 19.82], zoom_start=8,
        tiles="CartoDB positron")
    for _, row in events.iterrows():
        rgba = cmap(norm(row.magnitude))
        hex_color = "#{:02x}{:02x}{:02x}".format(
            int(rgba[0]*255), int(rgba[1]*255), int(rgba[2]*255))
        folium.CircleMarker(
            [row.lat, row.lon],
            radius=row.magnitude,
            color=hex_color, fill=True, fill_color=hex_color,
            fill_opacity=0.5, weight=0.5,
            popup=f"Mag: {row.magnitude:.1f}<br>Depth: {row.depth:.0f} km",
            tooltip=f"M{row.magnitude:.1f}"
        ).add_to(m3)
    m3.save("output/m08_events.html")
    print("3. Event markers saved")

    # 4. HEATMAP
    m4 = folium.Map(location=[41.0, 19.82], zoom_start=8,
        tiles="CartoDB dark_matter")
    heat_data = list(zip(events.lat, events.lon, events.magnitude))
    HeatMap(heat_data, radius=15, blur=20, max_zoom=12).add_to(m4)
    m4.save("output/m08_heatmap.html")
    print("4. Heatmap saved")

    # 5. COMBINED: events + heatmap + cities with layer control
    m5 = folium.Map(location=[41.0, 19.82], zoom_start=8,
        tiles="CartoDB positron")

    # Event dots layer
    event_group = folium.FeatureGroup(name="Event Dots")
    for _, row in events.sample(150, random_state=42).iterrows():
        folium.CircleMarker(
            [row.lat, row.lon],
            radius=row.magnitude / 2,
            color="#E53935", fill=True, fill_opacity=0.3, weight=0.3,
            popup=f"Mag: {row.magnitude:.1f}"
        ).add_to(event_group)
    event_group.add_to(m5)

    # Heatmap layer
    heat_group = folium.FeatureGroup(name="Heatmap", show=False)
    HeatMap(heat_data, radius=15, blur=20).add_to(heat_group)
    heat_group.add_to(m5)

    # City layer
    city_group2 = folium.FeatureGroup(name="Cities")
    for _, row in cities.iterrows():
        folium.CircleMarker(
            [row.lat, row.lon],
            radius=row["pop"] ** 0.5 / 80,
            color="#1565C0", fill=True, fill_opacity=0.6, weight=1.5,
            popup=f"<b>{row['name']}</b><br>Pop: {row['pop']:,}",
            tooltip=row["name"]
        ).add_to(city_group2)
    city_group2.add_to(m5)

    folium.LayerControl(collapsed=False).add_to(m5)
    m5.save("output/m08_combined.html")
    print("5. Combined map saved")

    # 6. MARKER CLUSTER (for many points)
    m6 = folium.Map(location=[41.0, 19.82], zoom_start=8,
        tiles="CartoDB positron")
    mc = MarkerCluster(name="Clustered Events")
    for _, row in events.iterrows():
        folium.Marker(
            [row.lat, row.lon],
            popup=f"Mag: {row.magnitude:.1f}",
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(mc)
    mc.add_to(m6)
    folium.LayerControl().add_to(m6)
    m6.save("output/m08_clustered.html")
    print("6. Marker cluster saved")

except ImportError:
    print("folium not installed (pip install folium)")
    print("Skipping all interactive maps")

# 7. PLOTLY EXPRESS (alternative)
try:
    import plotly.express as px
    fig = px.scatter_mapbox(
        events, lat="lat", lon="lon",
        color="magnitude", size="magnitude",
        color_continuous_scale="YlOrRd",
        mapbox_style="carto-positron",
        zoom=7, center={"lat": 41.0, "lon": 19.82},
        hover_data={"magnitude": ":.1f", "depth": ":.0f"},
        title="Seismic Events: Plotly Mapbox")
    fig.write_html("output/m08_plotly.html")
    print("7. Plotly mapbox saved")
except ImportError:
    print("plotly not installed — skipping")

print("\nAll W05-M08 Python outputs saved")
