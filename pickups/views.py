from django.shortcuts import render
from django.http import JsonResponse
import geopandas as gpd
import pandas as pd
import folium
from folium.plugins import HeatMap
import os

manhattan_shp = r"C:\Users\marce\Documents\GitHub\uberhotspots\shapefiles\manhattan.shp"
manhattan = gpd.read_file(manhattan_shp)

# Generates and saves a Folium map for the selected weekday and hour.
# If the map already exists, returns its path.
def generate_map(weekday, hour):
    output_dir = "static/hotspots_basemap"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"hotspot_{weekday}_{hour}.html")

    # Verify if the file already exists
    if not os.path.exists(output_path):
        df = pd.read_csv("uber_data_clean.csv")
        geometry = gpd.points_from_xy(df["lon"], df["lat"])
        gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
        manhattan = gpd.read_file(r"C:\Users\marce\Documents\GitHub\uberhotspots\shapefiles\manhattan.shp")
        gdf_manhattan = gdf[gdf.within(manhattan.union_all())]
        subset = gdf_manhattan[(gdf_manhattan["weekday"] == weekday) & (gdf_manhattan["hour"] == hour)]

        m = folium.Map(location=[40.7831, -73.9712], zoom_start=12)
        folium.GeoJson(manhattan).add_to(m)
        heat_data = [[row.geometry.y, row.geometry.x] for idx, row in subset.iterrows()]
        HeatMap(heat_data, radius=12).add_to(m)
        m.save(output_path)

    return f"hotspots_basemap/hotspot_{weekday}_{hour}.html"

# Renders the main Folium map view with controls for weekday and hour.
def hotspot_view(request):
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    hours = list(range(24))
    weekday = request.GET.get("weekday", "Monday")
    hour = int(request.GET.get("hour", 8))
    image_path = f"hotspots_basemap/hotspot_{weekday}_{hour}.html"
    return render(request, "hotspot.html", {
        "image_path": image_path,
        "weekdays": weekdays,
        "hours": hours,
        "selected_weekday": weekday,
        "selected_hour": hour
    })

# Renders the comparison view for two Folium maps side by side.
# Function was created but not implemented due to time constraints, this will be done in the future for practice.
def hotspot_compare_view(request):
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    hours = list(range(24))
    weekday_left = request.GET.get("weekday_left", "Monday")
    hour_left = int(request.GET.get("hour_left", 8))
    weekday_right = request.GET.get("weekday_right", "Tuesday")
    hour_right = int(request.GET.get("hour_right", 8))

    image_path_left = f"hotspots_basemap/hotspot_{weekday_left}_{hour_left}.html"
    image_path_right = f"hotspots_basemap/hotspot_{weekday_right}_{hour_right}.html"

    return render(request, "hotspot_compare.html", {
        "weekdays": weekdays,
        "hours": hours,
        "selected_weekday_left": weekday_left,
        "selected_hour_left": hour_left,
        "selected_weekday_right": weekday_right,
        "selected_hour_right": hour_right,
        "image_path_left": image_path_left,
        "image_path_right": image_path_right,
    })

# Returns Uber pickup points as GeoJSON for the selected weekday and hour.
def hotspot_geojson(request):
    weekday = request.GET.get("weekday", "Monday")
    hour = int(request.GET.get("hour", 8))
    df = pd.read_csv("uber_data_clean.csv")
    filtered = df[(df["weekday"] == weekday) & (df["hour"] == hour)]
    features = []
    for _, row in filtered.iterrows():
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row["lon"], row["lat"]],
            },
            "properties": {},
        })
    geojson = {
        "type": "FeatureCollection",
        "features": features,
    }
    return JsonResponse(geojson)

# Renders the Leaflet map view with controls for weekday and hour.
def hotspot_leaflet_view(request):
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    hours = list(range(24))
    weekday = request.GET.get("weekday", "Monday")
    hour = int(request.GET.get("hour", 8))
    return render(request, "hotspot_leaflet.html", {
        "weekdays": weekdays,
        "hours": hours,
        "selected_weekday": weekday,
        "selected_hour": hour
    })

