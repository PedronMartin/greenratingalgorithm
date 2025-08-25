# Contenuto di 'regola3.py'
import geopandas as gpd
from shapely.geometry import LineString
import pandas as pd

def is_unobstructed(tree, building, all_buildings_gdf):
    """
    Verifica se la linea di vista da un albero a un edificio è bloccata.
    """
    try:
        # Trova il punto più vicino all'edificio per la linea di vista
        building_point = building.geometry.exterior.interpolate(building.geometry.exterior.project(tree.geometry))
        line_of_sight = LineString([tree.geometry, building_point])
    except Exception as e:
        # Gestisce i casi in cui l'operazione fallisce
        return False
    
    # Crea una copia del GeoDataFrame e rimuovi l'edificio corrente
    other_buildings = all_buildings_gdf.loc[all_buildings_gdf.index != building.name]
    return not other_buildings.geometry.intersects(line_of_sight).any()

def run_rule_3(edifici, alberi):
    """
    Calcola il numero di alberi visibili da ogni edificio.
    """
    if edifici.empty or alberi.empty:
        print("Dati insufficienti per il calcolo. Assicurati che i GeoDataFrame non siano vuoti.")
        return edifici.assign(visible_trees_count=0)

    # Filtra e riproietta in un'unica operazione
    edifici_proj = edifici[edifici['building'].notna()].to_crs("EPSG:32632")
    alberi_proj = alberi[alberi['natural'].fillna('') == 'tree'].to_crs("EPSG:32632")
    
    # Inizializza un GeoDataFrame per i risultati basato sugli edifici riproiettati
    risultato_edifici = edifici_proj.copy()
    risultato_edifici['visible_trees_count'] = 0

    print("Avvio del calcolo della linea di vista...")
    
    # Itera su ogni edificio
    for idx, edificio in risultato_edifici.iterrows():
        # Crea un buffer di 300 metri
        view_buffer = edificio.geometry.buffer(300)
        
        # Trova gli alberi che si trovano all'interno del buffer
        nearby_trees = alberi_proj[alberi_proj.geometry.within(view_buffer)]
        
        visible_trees = 0
        
        # Itera sugli alberi vicini e verifica la linea di vista
        for _, albero in nearby_trees.iterrows():
            if is_unobstructed(albero, edificio, edifici_proj):
                visible_trees += 1
                
        # Aggiorna il conteggio per l'edificio corrente
        risultato_edifici.loc[idx, 'visible_trees_count'] = visible_trees

    # Crea un GeoDataFrame finale con l'indice originale
    final_result_df = pd.DataFrame(index=edifici.index)
    final_result_df['visible_trees_count'] = 0
    final_result_df.loc[risultato_edifici.index, 'visible_trees_count'] = risultato_edifici['visible_trees_count']
    
    # Restituisce il risultato come GeoDataFrame
    final_result_gdf = edifici.copy()
    final_result_gdf = final_result_gdf.merge(final_result_df, left_index=True, right_index=True)
    return final_result_gdf

"""edifici = gpd.read_file("./Edifici.geojson")
alberi = gpd.read_file("./Alberi.geojson")
print(run_rule_3(edifici, alberi))"""