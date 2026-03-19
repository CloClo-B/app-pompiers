"""
DAO pour la gestion des proposition d'ajout de point
"""
import os
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from app.models import PropAjoutPoint, Utilisateur
from pyproj import Transformer
from geoalchemy2.elements import WKTElement
from sqlalchemy import func

# Récupère tous les propositions d'ajout

def get_all_prop_ajout(db: Session) -> List[Dict[str, Any]]:
    propAjouts = db.query(
        PropAjoutPoint.id,
        PropAjoutPoint.description,
        PropAjoutPoint.photo,
        PropAjoutPoint.id_utilisateur,
        PropAjoutPoint.date_creation,
        func.ST_Y(PropAjoutPoint.geom).label("latitude"),
        func.ST_X(PropAjoutPoint.geom).label("longitude"),
    ).all()
    
    return [
        {
            "id": ajout.id,
            "description": ajout.description,
            "photo": ajout.photo,
            "id_utilisateur": ajout.id_utilisateur,
            "date_creation": ajout.date_creation,
            "latitude": ajout.latitude,
            "longitude": ajout.longitude,
        }
        for ajout in propAjouts
    ]


def get_all_prop_ajout_min(db: Session) -> List[Dict[str, Any]]:
    propAjouts = db.query(
        PropAjoutPoint.id,
        PropAjoutPoint.description,
        PropAjoutPoint.date_creation,

    ).all()
    
    return [
        {
            "id": ajout.id,
            "description": ajout.description,
            "date_creation": ajout.date_creation,
        }
        for ajout in propAjouts
    ]


# Récupère la proposition  via l'id 
def get_ajout_by_id(db: Session, id: int) -> Any:
    propAjout = db.query(
        PropAjoutPoint.id,
        PropAjoutPoint.description,
        PropAjoutPoint.photo,
        PropAjoutPoint.id_utilisateur,
        PropAjoutPoint.date_creation,
        func.ST_Y(func.ST_Transform(PropAjoutPoint.geom, 4326)).label("latitude"),
        func.ST_X(func.ST_Transform(PropAjoutPoint.geom, 4326)).label("longitude"),
    ).filter(PropAjoutPoint.id == id).first()
    
    return propAjout


# Crée une nouvelle proposition d'ajout
def create_prop_ajout(db: Session, ajout_data: Dict[str, Any]): 
    
    if not db.query(Utilisateur).filter(Utilisateur.id_utilisateur == ajout_data["id_utilisateur"]).first():
        raise ValueError("id_utilisateur est introuvable")
    
    lat = float(ajout_data["latitude"])
    lon = float(ajout_data["longitude"])
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:2154")
    x, y = transformer.transform(lat,lon)
    wkt = WKTElement(f"POINT({x} {y})", srid=2154)

    # creation ajout
    new_ajout = PropAjoutPoint(
        description=ajout_data["description"],
        photo=ajout_data["photo"],
        id_utilisateur=ajout_data["id_utilisateur"],
        geom=wkt,
    )
    db.add(new_ajout)
    db.commit()
    db.refresh(new_ajout)
    return new_ajout


# Supprime une proposition d'ajout et son image associée
def delete_prop_ajout_by_id(db: Session, id: int) -> bool:
    propAjout = db.query(PropAjoutPoint).filter(PropAjoutPoint.id == id).first()
    
    if propAjout:
        # supression de la ligne + trouver chemin image dans photo
        photo = propAjout.photo
        db.delete(propAjout)
        db.commit()

        
        # supression de l'image
        try:
            # Supprimer l'image
            if os.path.exists(photo):
                os.remove(photo)
            print("Image supprimé avec succès")
        except OSError as e:
            print(f"Erreur lors de la suppression de l'image : {e}")


        return True
    
    return False
