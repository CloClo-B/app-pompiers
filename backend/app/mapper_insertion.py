import os
import json
import psycopg2
from psycopg2.extras import execute_values
import sys
from datetime import datetime

""" Ce fichier permet d'insérer des points à partir d'un fichier JSON.
    Si le jeu de données correspond au format du SDIS56 alors il est préférable d'utiliser
    le fichier insertion.py, s'il y a un doute sur le format ce fichier est a utiliser.
    Avant d'exécuter ce fichier, il est nécessaire d'indiquer le fichier JSON à utiliser à la fin du fichier.
"""


# Configuration du mapping
UNIVERSAL_MAPPING = {
    "numero_pei": ["NUMERO_PEI", "id_sdis", "id", "ID_PEI"],
    "nom": ["NOM", "type_rd", "LIBELLE", "nom_etab"],
    "statut": ["STATUT", "statut", "ETAT"],
    "type_nature": ["TYPE_NATUR", "type_pei", "NATURE"],
    "insee5": ["INSEE5", "insee", "CODE_INSEE"],
    "press_deb": ["PRESS_DEB_", "press_dyn", "PRESSION"],
    "debit_1_bar": ["DEBIT_1_BA", "debit", "DEBIT"],
    "vol_eau_mi": ["VOL_EAU_MI", "volume", "VOLUME"],
    "accessibilite": ["ACCESSIBIL", "accessibilite", "ACCES"],
    "disponibilite": ["DISPO", "disponible", "DISPONIBILITE"],
    "carto_ref": ["CARTO_REF", "ref_terr", "CARTO"],
    "date_crea": ["DATE_CREA", "date_mes", "date_creation"],
    "date_maj": ["DATE_MAJ", "date_maj"]
}

# Convertion des types
def to_int(val): 
    try: return int(float(val)) if val is not None else 0
    except: return 0

def to_float(val):
    try: return float(val) if val is not None else 0.0
    except: return 0.0

def to_upper_str(val):
    if val is None: return None
    return str(val).strip().upper()

TYPE_CONVERTERS = {
    "numero_pei": to_int,
    "carto_ref": to_int,
    "press_deb": to_float,
    "debit_1_bar": to_float,
    "vol_eau_mi": to_float,
    "statut": to_upper_str,
    "type_nature": to_upper_str,
    "accessibilite": to_upper_str,
    "disponibilite": to_upper_str
}

# Définition de valeurs par défauts
DEFAULTS = {
    "nom": "NON RENSEIGNÉ",
    "statut": "PUBLIC",
    "accessibilite": "C",
    "disponibilite": "DI",
    "carto_ref": 0,
    "press_deb": 0.0,
    "debit_1_bar": 0.0,
    "vol_eau_mi": 0.0,
    "date_crea": datetime.now(),
    "utilisateur": 1
}

# Types de points autorisés
ALLOWED_TYPES = ["BI", "BI100", "PENA", "PI100", "PI110", "PI150", "PI65", "PI70", "PI80", "RESERVE EAU INCENDIE"]

def import_hydrants(json_filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, json_filename)
    
    if not os.path.exists(json_path):
        print(f"Erreur : Le fichier {json_filename} est introuvable dans {base_dir}")
        return

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            geojson = json.load(f)
    except Exception as e:
        print(f"Erreur lecture JSON : {e}")
        return

    # Analyse des données non utilisées
    if geojson.get('features'):
        # On récupère toutes les clés du premier point afin de faire le tri
        first_props = geojson['features'][0]['properties'].keys()
        known_synonyms = {syn for sublist in UNIVERSAL_MAPPING.values() for syn in sublist}
        
        ignored_keys = [k for k in first_props if k not in known_synonyms]
        
        print("\n" + "="*60)
        print("RÉSUMÉ DU JEU DE DONNÉES")
        print(f"Fichier : {json_filename}")
        if ignored_keys:
            print(f"Données JSON ignorées (absentes du mapping) :")
            print(f"   > {', '.join(ignored_keys)}")
        else:
            print("Toutes les données du JSON sont mappées correctement.")
        print("="*60 + "\n")

    records = []
    skipped_count = 0

    for feature in geojson['features']:
        props = feature['properties']
        geom = feature['geometry']['coordinates']
        
        row_data = {}
        for db_col, synonyms in UNIVERSAL_MAPPING.items():
            key = next((s for s in synonyms if s in props), None)
            val = props.get(key)
            
            if isinstance(val, str):
                val = val.strip().upper()
            
            # Remplacement de champs vides par une valeur par défaut
            if val == "" or val is None:
                val = DEFAULTS.get(db_col)
                
            row_data[db_col] = val

        raw_t = (props.get("type_pei") or props.get("TYPE_NATUR") or "").upper()
        raw_d = str(props.get("diam_pei") or props.get("diam_cana") or "").replace(".0", "")
        
        # Tentative de construire le type de point
        val_nature = f"{raw_t}{raw_d}".strip()
        
        if val_nature not in ALLOWED_TYPES:
            if raw_t in ALLOWED_TYPES: val_nature = raw_t
            else: val_nature = "PI100"
        
        row_data["type_nature"] = val_nature

        # Numéro PEI obligatoire
        if not row_data["numero_pei"]: continue

        # Ajout de l'utilisateur (ID 1 pour l'administrateur) et des coordonnées
        final_row = list(row_data.values()) + [1, geom[0], geom[1]]
        records.append(tuple(final_row))

    # Insertion
    conn = None
    try:
        conn = psycopg2.connect(dbname="fenalim_db", user="fenalim", password="fenalim123", host="db")
        cur = conn.cursor()
        
        cols = list(UNIVERSAL_MAPPING.keys()) + ["utilisateur"]
        sql = f"""
            INSERT INTO points_eau ({', '.join(cols)}, geom) 
            VALUES %s 
            ON CONFLICT (numero_pei) DO NOTHING
        """
        
        data_to_send = [r[:-2] + (f"SRID=2154;POINT({r[-2]} {r[-1]})",) for r in records]
        
        execute_values(cur, sql, data_to_send)
        
        print(f"Bilan : {len(records)} points validés, {skipped_count} points rejetés.")
        
        if len(records) > 0:
            # Vérification utilisateur avant d'insérer
            confirm = input("\nConfirmer l'insertion définitive ? (OUI/NON) : ")
            if confirm.strip().upper() == "OUI":
                conn.commit()
                print("Données insérées avec succès !")
            else:
                conn.rollback()
                print("Opération annulée par l'utilisateur.")
        else:
            print("Aucun point validé : pas de donnée insérée.")
            
    except Exception as e:
        if conn: conn.rollback()
        print(f"Erreur SQL : {e}")
    finally:
        if conn: conn.close()

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "HYDRANTS_TEST_22.json"
    import_hydrants(target)