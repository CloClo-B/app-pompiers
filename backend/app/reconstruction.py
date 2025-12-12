import json
import re

input_path = "/app/app/HYDRANTS_56.json"
output_path = "/app/app/HYDRANTS_56_clean.geojson"

# Lecture brute
with open(input_path, "r", encoding="utf-8") as f:
    raw = f.read()

# Séparation des objets JSON collés
parts = re.split(r'(?=\{"type":"Feature")', raw)

features = []
for p in parts:
    p = p.strip()
    if not p:
        continue

    # S'assurer que l'objet se termine bien par '}'
    # Trouver la dernière "}" valide
    last_brace = p.rfind("}")
    if last_brace == -1:
        continue

    obj_str = p[:last_brace+1]

    try:
        obj = json.loads(obj_str)
        features.append(obj)
    except json.JSONDecodeError:
        # On ignore les segments incomplets
        continue

# Construction GeoJSON
geojson = {
    "type": "FeatureCollection",
    "features": features
}

# Sauvegarde
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(geojson, f, ensure_ascii=False, indent=2)

print(f"GeoJSON reconstruit avec {len(features)} features → {output_path}")
