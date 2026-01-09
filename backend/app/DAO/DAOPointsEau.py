from sqlalchemy.orm import Session
from datetime import datetime
from ..models import PointEau
from pyproj import Transformer
from geoalchemy2.elements import WKTElement
from sqlalchemy import func, text

# from app import models, schemas
# from typing import Dict, Any

<<<<<<< HEAD
# Récupérer tous les points d'eau avec latitude et longitude
def get_all_points_eau(db: Session):
=======
# Récupère tous les points d'eau
def get_all_points_eau(db: Session) -> List[Dict[str, Any]]:
>>>>>>> develop
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

        }
        for p in points
    ]

<<<<<<< HEAD

def creer_point_eau(db: Session, payload):
=======
# Récupère un point d'eau par ID
def get_point_eau_by_id(db: Session, point_id: int) -> Dict[str, Any]:
    point = db.query(
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
    ).filter(PointEau.id == point_id).first()
    
    if point:
        return {
            "id": point.id,
            "numero_pei": point.numero_pei,
            "nom": point.nom,
            "statut": point.statut,
            "type_nature": point.type_nature,
            "insee5": point.insee5,
            "accessibilite": point.accessibilite,
            "disponibilite": point.disponibilite,
            "carto_ref": point.carto_ref,
            "press_deb": point.press_deb,
            "debit_1_bar": point.debit_1_bar,
            "vol_eau_mi": point.vol_eau_mi,
            "date_crea": point.date_crea,
            "date_maj": point.date_maj,
            "utilisateur": point.utilisateur,
            "latitude": point.latitude,
            "longitude": point.longitude,
        }
    return None

# Crée un nouveau point d'eau
def create_point_eau(db: Session, point_data: Dict[str, Any]):
    existing = db.query(PointEau).filter(PointEau.numero_pei == point_data["numero_pei"]).first()
    if existing:
        raise ValueError(f"Le numero_pei {point_data['numero_pei']} existe déjà.")
    
    point_data["statut"] = point_data["statut"].upper()
    point_data["type_nature"] = point_data["type_nature"].upper()
>>>>>>> develop
    
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
    )
    db.add(new_point)
    db.commit()
    db.refresh(new_point)
    return new_point



<<<<<<< HEAD


=======
# Met à jour un point d'eau par ID
def update_point_eau_by_id(db: Session, point_id: int, point_data: Dict[str, Any]):
    db_point = db.query(PointEau).filter(PointEau.id == point_id).first()
    if not db_point:
        return None
    
    # Mettre à jour les champs 
    for key, value in point_data.items():
        if key in ['id', 'geom', 'date_crea', 'latitude', 'longitude']:
            continue
        if hasattr(db_point, key):
            setattr(db_point, key, value)
    
    # Mettre à jour la date de modification
    db_point.date_maj = datetime.now()
    
    # Si latitude/longitude sont fournis, recalculer geom
    if 'latitude' in point_data and 'longitude' in point_data:
        transformer = Transformer.from_crs("EPSG:4326", "EPSG:2154")
        x, y = transformer.transform(point_data['latitude'], point_data['longitude'])
        wkt = WKTElement(f"POINT({x} {y})", srid=2154)
        db_point.geom = wkt
    
    db.commit()
    db.refresh(db_point)
    return db_point

# Récupère un point d'eau par numéro PEI
def get_point_eau_by_numero_pei(db: Session, numero_pei: int):
    point = db.query(
        PointEau,
        func.ST_Y(PointEau.geom).label("latitude"),
        func.ST_X(PointEau.geom).label("longitude"),
    ).filter(PointEau.numero_pei == numero_pei).first()
>>>>>>> develop

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

<<<<<<< HEAD
=======
# Supprime un point d'eau par numéro PEI
def delete_point_eau_by_numero_pei(db: Session, numero_pei: int) -> bool:
    point = db.query(PointEau).filter(PointEau.numero_pei == numero_pei).first()
    if not point:
        return False
>>>>>>> develop


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
    