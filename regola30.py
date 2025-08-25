# Contenuto di 'regola30.py' (versione corretta)
import geopandas as gpd
from shapely.ops import unary_union
import pandas as pd

def run_rule_30(edifici, alberi):
    """
    Calcola la percentuale di copertura arborea per l'area di studio e la restituisce.

    Args:
        edifici (gpd.GeoDataFrame): GeoDataFrame degli edifici.
        alberi (gpd.GeoDataFrame): GeoDataFrame degli alberi.

    Returns:
        float: La percentuale di copertura arborea.
    """
    if edifici.empty or alberi.empty:
        print("Dati insufficienti per il calcolo. Assicurati che i GeoDataFrame non siano vuoti.")
        return 0.0

    # Riprogietta i dati a un CRS che usa i metri per calcoli accurati
    edifici_proj = edifici.to_crs("EPSG:32632")
    alberi_proj = alberi.to_crs("EPSG:32632")

    # 1. Calcola l'area totale coperta dagli alberi
    alberi_buffer = alberi_proj.buffer(2)
    trees_total_area = unary_union(alberi_buffer.geometry).area

    # 2. Calcola l'area totale della zona di studio in modo sicuro
    combined_geometries = pd.concat([edifici_proj, alberi_proj], ignore_index=True)
    study_area_geometry = unary_union(combined_geometries.geometry)
    study_area = study_area_geometry.area

    # 3. Calcola e restituisce la percentuale di copertura
    percentage = (trees_total_area / study_area) * 100
    return percentage