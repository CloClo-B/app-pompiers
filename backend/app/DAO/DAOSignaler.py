"""
DAO pour la gestion des Signalements
"""
import os
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from app.models import Signaler, Utilisateur, PointEau


def get_all_signale(db: Session) -> List[Dict[str, Any]]:
    signalements = db.query(
        Signaler.id,
        Signaler.id_point,
        Signaler.probleme,
        Signaler.photo,
        Signaler.id_utilisateur,
        Signaler.date_creation,
    ).all()
    
    return [
        {
            "id": s.id,
            "id_point": s.id_point,
            "probleme": s.probleme,
            "photo": s.photo,
            "id_utilisateur": s.id_utilisateur,
            "date_creation": s.date_creation,
        }
        for s in signalements
    ]


def get_signale_by_id_point(db: Session, id_point: int) -> List[Dict[str, Any]]:
    signalements = db.query(
        Signaler.id,
        Signaler.id_point,
        Signaler.probleme,
        Signaler.photo,
        Signaler.id_utilisateur,
        Signaler.date_creation,
    ).filter(Signaler.id_point == id_point).all()
    
    return [
        {
            "id": s.id,
            "id_point": s.id_point,
            "probleme": s.probleme,
            "photo": s.photo,
            "date_creation": s.date_creation,
            "id_utilisateur": s.id_utilisateur,

        }
        for s in signalements
    ]



def create_signale(db: Session, signale_data: Dict[str, Any]): 
    # verification infos
    if not db.query(PointEau).filter(PointEau.numero_pei == signale_data["id_point"]).first():
        raise ValueError("id_point est invalide")
    
    if not db.query(Utilisateur).filter(Utilisateur.id_utilisateur == signale_data["id_utilisateur"]).first():
        raise ValueError("id_utilisateur est incorrect")
    
    # creation signalement
    new_signale = Signaler(
        id_point=signale_data["id_point"],
        probleme=signale_data["probleme"],
        photo=signale_data["photo"],
        id_utilisateur=signale_data["id_utilisateur"],
    )
    db.add(new_signale)
    db.commit()
    db.refresh(new_signale)
    return new_signale


def delete_signale_by_id_point(db: Session, id_point: int) -> bool:
    signalements = db.query(Signaler).filter(Signaler.id_point == id_point).all()
    photo = []

    if signalements:
        # supression des lignes + ajout image dans photo
        for signale in signalements:
            photo.append(signale.photo)
            db.delete(signale)
        db.commit()
        
        # supression des images
        for img in photo:
            try:
                # Supprimer l'image
                os.remove(img)
                print("Image supprimé avec succès")
            except OSError as e:
                print(f"Erreur lors de la suppression de l'image : {e}")


        return True
    
    return False


def update_signale(db: Session, id_point: int, signale_data: Dict[str, Any]):
    db_signale = db.query(Signaler).filter(Signaler.id_point == id_point).first()
    if not db_signale:
        return None
    
    for key, value in signale_data.items():
        if key == 'id_point':  # Ne pas modifier l'ID
            continue
        if hasattr(db_signale, key):
            setattr(db_signale, key, value)
    
    db.commit()
    db.refresh(db_signale)
    return db_signale