import os
import json
import psycopg2
from psycopg2.extras import execute_values

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(BASE_DIR, "HYDRANTS_56.json")

with open(JSON_FILE, "r", encoding="utf-8") as f:
    geojson = json.load(f)

conn = psycopg2.connect(
    dbname="fenalim_db",
    user="fenalim",
    password="fenalim123",
    host="db"
)
cur = conn.cursor()

records = []
for feature in geojson['features']:
    props = feature['properties']
    x, y = feature['geometry']['coordinates']
    
    records.append((
        props.get("NUMERO_PEI"),
        props.get("NOM"),
        props.get("STATUT"),
        props.get("TYPE_NATUR"),
        props.get("INSEE5"),
        props.get("ACCESSIBIL"),
        props.get("DISPO"),
        props.get("CARTO_REF"),
        props.get("PRESS_DEB_"),
        props.get("DEBIT_1_BA"),
        props.get("VOL_EAU_MI"),
        props.get("DATE_CREA"),
        props.get("DATE_MAJ"),
        props.get("UTILISATEU"),
        x,
        y
    ))

sql = """
INSERT INTO points_eau (
    numero_pei, nom, statut, type_nature, insee5, accessibilite,
    disponibilite, carto_ref, press_deb, debit_1_bar, vol_eau_mi,
    date_crea, date_maj, utilisateur, geom
)
VALUES %s
"""

execute_values(
    cur,
    sql,
    [(r[:14] + (f"SRID=2154;POINT({r[14]} {r[15]})",)) for r in records]
)

conn.commit()
cur.close()
conn.close()

print(f"{len(records)} points insérés avec succès !")
