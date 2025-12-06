"""
DAO pour la gestion des Signalements
"""
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from app.models import Signaler


def get_all_signale(db: Session) -> List[Dict[str, Any]]:
    signalements = db.query(
        Signaler.id_point,
        Signaler.probleme,
        Signaler.photo,
    ).all()
    
    return [
        {
            "id_point": s.id_point,
            "probleme": s.probleme,
            "photo": s.photo,
        }
        for s in signalements
    ]


def get_signale_by_id_point(db: Session, id_point: int) -> List[Dict[str, Any]]:
    signalements = db.query(
        Signaler.id_point,
        Signaler.probleme,
        Signaler.photo,
    ).filter(Signaler.id_point == id_point).all()
    
    return [
        {
            "id_point": s.id_point,
            "probleme": s.probleme,
            "photo": s.photo,
        }
        for s in signalements
    ]


def create_signale(db: Session, signale_data: Dict[str, Any]):
    # Validation de la clé étrangère (optionnel, si tu veux être strict)
    from app.models import PointEau
    if not db.query(PointEau).filter(PointEau.id == signale_data["id_point"]).first():
        raise ValueError("id_point est invalide")
    
    new_signale = Signaler(
        id_point=signale_data["id_point"],
        probleme=signale_data["probleme"],
        photo=signale_data.get("photo"),
    )
    db.add(new_signale)
    db.commit()
    db.refresh(new_signale)
    return new_signale


def delete_signale_by_id_point(db: Session, id_point: int) -> bool:
    signalements = db.query(Signaler).filter(Signaler.id_point == id_point).all()
    if signalements:
        for signale in signalements:
            db.delete(signale)
        db.commit()
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