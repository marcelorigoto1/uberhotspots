import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import contextily as ctx
import os
from shapely.geometry import Point

# Carregar dados
df = pd.read_csv("uber_data_clean.csv")

# Converter para GeoDataFrame
geometry = [Point(xy) for xy in zip(df["lon"], df["lat"])]
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

# Pasta de saída
output_dir = "static/hotspots_basemap"
os.makedirs(output_dir, exist_ok=True)

for weekday in gdf["weekday"].unique():
    for hour in range(24):
        subset = gdf[(gdf["weekday"] == weekday) & (gdf["hour"] == hour)]
        if len(subset) < 100:
            continue

        # Reprojetar para Web Mercator
        subset_proj = subset.to_crs(epsg=3857)

        # Criar gráfico com contexto base
        fig, ax = plt.subplots(figsize=(10, 8))
        try:
            sns.kdeplot(
                x=subset_proj.geometry.x,
                y=subset_proj.geometry.y,
                fill=True,
                cmap="Reds",
                bw_adjust=0.1,
                thresh=0.05,
                levels=7,
                ax=ax
            )
            ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron)
            ax.set_axis_off()

            filename = f"{output_dir}/hotspot_{weekday}_{hour}.png"
            plt.savefig(filename, bbox_inches="tight")
            print(f"Gerado: {weekday} {hour}")
        except Exception as e:
            print(f"Erro ao gerar mapa {weekday} {hour}: {e}")
        finally:
            plt.close()
