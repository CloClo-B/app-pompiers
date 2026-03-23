"""
DAO pour la gestion des Points d'Eau
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import Dict, Any, List
from app.models import PointEau
from pyproj import Transformer
from geoalchemy2.elements import WKTElement
from geoalchemy2.functions import ST_Transform
from sqlalchemy.exc import IntegrityError


# Récupère tous les points d'eau
def get_all_points_eau(db: Session) -> List[Dict[str, Any]]:
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
        func.ST_Y(ST_Transform(PointEau.geom, 4326)).label("latitude"),
        func.ST_X(ST_Transform(PointEau.geom, 4326)).label("longitude"),
    ).all()
    
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

# Récupère tous les points d'eau Light (Optimisation)
def get_all_points_eau_light(db: Session) -> List[Dict[str, Any]]:
    points = db.query(
        PointEau.id,
        PointEau.numero_pei,
        func.ST_Y(ST_Transform(PointEau.geom, 4326)).label("latitude"),
        func.ST_X(ST_Transform(PointEau.geom, 4326)).label("longitude"),
    ).all()
    
    return [
        {
            "id": p.id,
            "numero_pei": p.numero_pei,
            "latitude": p.latitude,
            "longitude": p.longitude,
        }
        for p in points
    ]


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
    
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:2154")
    x, y = transformer.transform(point_data["latitude"], point_data["longitude"])
    wkt = WKTElement(f"POINT({x} {y})", srid=2154)
    
    new_point = PointEau(
        numero_pei=point_data["numero_pei"],
        statut=point_data["statut"],
        type_nature=point_data["type_nature"],
        nom=point_data.get("nom") or None,
        insee5=point_data.get("insee5") or None,
        press_deb=point_data.get("press_deb"),
        debit_1_bar=point_data.get("debit_1_bar"),
        vol_eau_mi=point_data.get("vol_eau_mi"),
        accessibilite=point_data.get("accessibilite"),
        disponibilite=point_data.get("disponibilite"),
        carto_ref=point_data.get("carto_ref"),
        utilisateur=point_data.get("utilisateur"),
        geom=wkt,
    )
    try:
        db.add(new_point)
        db.commit()
        db.refresh(new_point)
    except IntegrityError as e:
        db.rollback()
        raise ValueError(f"Erreur base de données : {str(e)}")
    
    return new_point


def delete_point_eau_by_id(db: Session, point_id: int) -> bool:
    db_point = db.query(PointEau).filter(PointEau.id == point_id).first()
    if db_point:
        db.delete(db_point)
        db.commit()
        return True
    return False

# Met à jour un point d'eau par ID
def update_point_eau_by_id(db: Session, point_id: int, point_data: Dict[str, Any]):
    db_point = db.query(PointEau).filter(PointEau.id == point_id).first()
    
    # verifier que l'id existe bien
    if not db_point:
        raise ValueError("Id point incorrect")

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
        
        # verifier que les coordonnées sont exact
        if(point_data['latitude'] > 90 or point_data['latitude'] < -90):
            raise ValueError("lattitude incorect")
        
        if(point_data['longitude'] > 180 or point_data['longitude'] < -180):
            raise ValueError("longitude incorect")

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

    if not point:
        raise ValueError("Numéro PEI incorrect")


    p, lat, lon = point
    return {
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
        "latitude": lat,
        "longitude": lon,
    }

# Supprime un point d'eau par numéro PEI
def delete_point_eau_by_numero_pei(db: Session, numero_pei: int) -> bool:
    point = db.query(PointEau).filter(PointEau.numero_pei == numero_pei).first()
    if not point:
        return False

    db.delete(point)
    db.commit()
    return True
