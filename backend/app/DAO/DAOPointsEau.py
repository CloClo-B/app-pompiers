from sqlalchemy.orm import Session
from datetime import datetime
from ..models import PointEau
from pyproj import Transformer
from geoalchemy2.elements import WKTElement
from sqlalchemy import func, text

# from app import models, schemas
# from typing import Dict, Any

# Récupérer tous les points d'eau avec latitude et longitude
def get_all_points_eau(db: Session):
    points = db.query(
        PointEau.id,
        PointEau.numero_pei,
        PointEau.nom,
        PointEau.statut,
        PointEau.type_nature,
        PointEau.insee5,
        PointEau.accessibilite,
        PointEau.disponibilite,
        PointEau.carto_ref,
        PointEau.press_deb,
        PointEau.debit_1_bar,
        PointEau.vol_eau_mi,
        PointEau.date_crea,
        PointEau.date_maj,
        PointEau.utilisateur,
        func.ST_Y(PointEau.geom).label("latitude"),
        func.ST_X(PointEau.geom).label("longitude"),
        PointEau.signale,
        PointEau.probleme,
    ).all()
    # Transformer les tuples pour que le response_model fonctionne bien
    return [
        {
            "id": p.id,
            "numero_pei": p.numero_pei,
            "nom": p.nom,
            "statut": p.statut,
            "type_nature": p.type_nature,
            "insee5": p.insee5,
            "accessibilite": p.accessibilite,
            "disponibilite": p.disponibilite,
            "carto_ref": p.carto_ref,
            "press_deb": p.press_deb,
            "debit_1_bar": p.debit_1_bar,
            "vol_eau_mi": p.vol_eau_mi,
            "date_crea": p.date_crea,
            "date_maj": p.date_maj,
            "utilisateur": p.utilisateur,
            "latitude": p.latitude,
            "longitude": p.longitude,
            "signale" : p.signale,
            "probleme" : p.probleme,

        }
        for p in points
    ]


def creer_point_eau(db: Session, payload):
    
     # conversion WGS84 (4326) -> Lambert-93 (2154)
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:2154")
    x, y = transformer.transform(payload.latitude, payload.longitude)
    wkt = WKTElement(f"POINT({x} {y})", srid=2154)
    
    new_point = PointEau(
        numero_pei=payload.numero_pei,
        statut= payload.statut,
        type_nature=payload.type_nature,
        insee5=payload.insee5,
        press_deb=payload.press_deb,
        debit_1_bar=payload.debit_1_bar,
        vol_eau_mi=payload.vol_eau_mi,
        accessibilite=payload.accessibilite,
        disponibilite=payload.disponibilite,
        carto_ref=payload.carto_ref,
        date_crea= datetime.now(),
        geom=wkt,
        signale=payload.signale,
        probleme=payload.probleme,

    )
    db.add(new_point)
    db.commit()
    db.refresh(new_point)
    return new_point






# Récupérer un point d’eau par son ID
# def get_point_eau_by_id(db: Session, point_id: int):
#     query = """
#         SELECT id, numero_pei, adresse, commune,
#                ST_X(geom) AS longitude, ST_Y(geom) AS latitude
#         FROM points_eau
#         WHERE id = :point_id;
#     """
#     row = db.execute(query, {"point_id": point_id}).fetchone()

#     if row:
#         return {
#             "id": row.id,
#             "numero_pei": row.numero_pei,
#             "adresse": row.adresse,
#             "commune": row.commune,
#             "longitude": row.longitude,
#             "latitude": row.latitude,
#         }
#     return None



# def delete_point_eau_by_id(db: Session, numero_pei:int):
#     query = text("DELETE FROM points_eau WHERE id = idSupp;")
#     result = db.execute(query, {"idSupp" : numero_pei})
#     db.commit()
#     return result.rowcount > 0


# def update_point_eau_by_id(db:Session, id_pei:int, data:Dict[str, Any]):
#     db_pei = db.query(models.PointEau).filter(models.PointEau.numero_pei == id_pei).first()
#     if not db_pei:
#         return None
#     for key, value in data.items():
#         if key in ['id', 'geom', 'date_crea', 'latitude', 'longitude']:
#             continue
#         if hasattr(db_pei, key):
#             setattr(db_pei, key, value)
#     if hasattr(db_pei, "date_maj"):
#         db_pei.date_maj = datetime.now()
#     if 'latitude' in data and 'longitude' in data:
#         latitude = data['latitude']
#         longitude = data['longitude']

#         query = text("""
#                                  UPDATE points_eau
#             SET geom = ST_SetSRID(ST_MakePoint(:longitude, :latitude), 2154)
#             WHERE id = :id_pei;
#         """)
#         db.execute(query, {"longitude" : data['longitude'], "latitude" : data['latitude'], "id_pei" : id_pei})
#         db.commit()
#         db.refresh(db_pei)
#     return db_pei
    