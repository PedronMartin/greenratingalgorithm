import geopandas as gpd
import pandas as pd

# Importa le funzioni refattorizzate dai tuoi script
from regola3 import run_rule_3
from regola30 import run_rule_30
from regola300 import run_rule_300

# Definisci i nomi dei file di input e output
buildings_filename = "./Edifici.geojson"
trees_filename = "./Alberi.geojson"
green_areas_filename = "./Areeverdi.geojson"
output_filename = "edifici_conformi_3_30_300.geojson"

def run_full_analysis():
    print("Avvio dell'analisi completa 3-30-300...")
    
    # 1. Carica i dati una sola volta
    try:
        edifici = gpd.read_file(buildings_filename)
        alberi = gpd.read_file(trees_filename)
        aree_verdi = gpd.read_file(green_areas_filename)
    except Exception as e:
        print(f"Errore nel caricamento dei file: {e}")
        return
    
    print(f"\nNumero totale di edifici nel dataset: {len(edifici)}")
    print(f"Numero totale di alberi nel dataset: {len(alberi)}")
    print(f"Numero totale di aree verdi nel dataset: {len(aree_verdi)}")
        
    # 2. Esegui gli algoritmi per ogni regola e ottieni i risultati
    print("\n--- Esecuzione Regola 3 (Linea di Vista) ---")
    risultati_3 = run_rule_3(edifici, alberi)
    num_soddisfatti_3 = (risultati_3['visible_trees_count'] > 0).sum()
    print(f"RISULTATO REGOLA 3: {num_soddisfatti_3} edifici soddisfano la regola (su {len(edifici)}).")
    
    print("\n--- Esecuzione Regola 30 (Copertura Arborea) ---")
    percentage_30 = run_rule_30(edifici, alberi)
    print(f"RISULTATO REGOLA 30: La copertura arborea è del {percentage_30:.2f}%.")
    if percentage_30 > 0.0:
        print("La regola del 30% è soddisfatta a livello di zona.")
    else:
        print("La regola del 30% NON è soddisfatta a livello di zona.")
    
    print("\n--- Esecuzione Regola 300 (Area Verde Vicina) ---")
    risultati_300 = run_rule_300(edifici, aree_verdi)
    num_soddisfatti_300 = (risultati_300['score_300'] == 1).sum()
    print(f"RISULTATO REGOLA 300: {num_soddisfatti_300} edifici soddisfano la regola (su {len(edifici)}).")
    
    # 3. Intersezione dei risultati
    print("\nIntersezione dei risultati...")
    
    # Filtro per la regola 3
    edifici_conformi_3 = risultati_3[risultati_3['visible_trees_count'] > 0]
    
    # Filtro per la regola 300
    edifici_conformi_300 = risultati_300[risultati_300['score_300'] == 1]
    
    # Intersezione dei GeoDataFrame
    edifici_intermedi = edifici_conformi_3.loc[edifici_conformi_3.index.intersection(edifici_conformi_300.index)].copy()
    
    print(f"Edifici che soddisfano sia la Regola 3 che la Regola 300: {len(edifici_intermedi)}")
    
    # Aggiungi il controllo della regola 30
    if percentage_30 > 0.0:
        print("La regola 30 è soddisfatta, procedo con il salvataggio.")
        edifici_finali = edifici_intermedi.copy()
    else:
        print("La regola 30 NON è soddisfatta, il risultato finale è 0.")
        # Crea un GeoDataFrame vuoto in modo corretto
        edifici_finali = gpd.GeoDataFrame(columns=edifici.columns, crs=edifici.crs, geometry='geometry')
    
    # 4. Aggiungi le colonne di debug per l'output finale
    if not edifici_finali.empty:
        edifici_finali['visible_trees_count'] = risultati_3.loc[edifici_finali.index, 'visible_trees_count']
        edifici_finali['score_300'] = risultati_300.loc[edifici_finali.index, 'score_300']
        edifici_finali['coverage_percentage'] = percentage_30

    # 5. Salva il risultato finale
    if not edifici_finali.empty:
        edifici_finali.to_crs(edifici.crs).to_file(output_filename, driver='GeoJSON')
        print(f"\n✅ Analisi completata! Trovati {len(edifici_finali)} edifici che rispettano la regola 3-30-300.")
        print("Risultato salvato in:", output_filename)
    else:
        print("\n❌ Nessun edificio trovato che rispetta tutte e 3 le regole.")

if __name__ == "__main__":
    run_full_analysis()