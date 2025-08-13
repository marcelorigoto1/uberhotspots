# ---------------------------------------------------------------------------------
# Functionality overview:
#
# 1. Loads Uber pickup CSV data and creates a GeoDataFrame with point geometries.
# 2. Loads the Manhattan shapefile for spatial filtering.
# 3. Filters pickups to only those within Manhattan.
# 4. For each weekday and hour:
#    - Filters pickups for that time.
#    - Creates a Folium map centered on Manhattan.
#    - Adds the Manhattan boundary and a heatmap of pickups.
#    - Saves the map as an HTML file in static/hotspots_basemap.
# ---------------------------------------------------------------------------------

import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import HeatMap
import os

weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
hours = list(range(24))

print("Loading CSV")
df = pd.read_csv("uber_data_clean.csv")
geometry = gpd.points_from_xy(df["lon"], df["lat"])
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
print("Data criated.")

print("Loading shapefile")
manhattan = gpd.read_file(r"C:\Users\marce\Documents\GitHub\uberhotspots\shapefiles\manhattan.shp")
print("Shapefile loaded.")

print("Filtering pickups ")
gdf_manhattan = gdf[gdf.within(manhattan.union_all())]
print(f"Total pickups: {len(gdf_manhattan)}")

output_dir = "static/hotspots_basemap"
os.makedirs(output_dir, exist_ok=True)

for weekday in weekdays:
    for hour in hours:
        print(f"Generating map {weekday}, {hour}h...")
        subset = gdf_manhattan[(gdf_manhattan["weekday"] == weekday) & (gdf_manhattan["hour"] == hour)]
        print(f"Total pickups: {len(subset)}")
        m = folium.Map(location=[40.7831, -73.9712], zoom_start=12)
        folium.GeoJson(manhattan).add_to(m)
        heat_data = [[row.geometry.y, row.geometry.x] for idx, row in subset.iterrows()]
        HeatMap(heat_data, radius=12).add_to(m)
        output_path = os.path.join(output_dir, f"hotspot_{weekday}_{hour}.html")
        m.save(output_path)
        print(f"Map salved at {output_path}")
