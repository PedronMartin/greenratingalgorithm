# Contenuto di 'regola300.py'
import geopandas as gpd
import pandas as pd

def run_rule_300(edifici, aree_verdi):
    """
    Calcola la regola dei 300 metri.
    """
    if edifici.empty or aree_verdi.empty:
        print("Dati insufficienti per il calcolo. Assicurati che i GeoDataFrame non siano vuoti.")
        return edifici.assign(score_300=0)

    edifici_proj = edifici.to_crs("EPSG:32632")
    aree_verdi_proj = aree_verdi.to_crs("EPSG:32632")

    edifici_buffer = edifici_proj.copy()
    edifici_buffer['geometry'] = edifici_buffer.geometry.buffer(300)
    edifici_buffer['original_index'] = edifici_buffer.index

    join_result = gpd.sjoin(edifici_buffer, aree_verdi_proj, how="inner", predicate='intersects')

    risultato_finale = edifici.copy()
    risultato_finale['score_300'] = 0
    
    if not join_result.empty:
        soddisfatti_index = join_result['original_index'].unique()
        risultato_finale.loc[soddisfatti_index, 'score_300'] = 1

    return risultato_finale