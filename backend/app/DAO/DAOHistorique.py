from app import models 
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Dict, Any


# =============== HISTORIQUE =================

def get_all_historique(db):
    query = text("SELECT * FROM historiques ORDER BY date_action DESC")
    result = db.execute(query).fetchall()
    return [dict(row._mapping) for row in result]


def get_historique_by_id(db:Session, id_log:int):
    return db.query(models.Historique).filter(models.Historique.id_log == id_log).first()
    
def get_historique_by_utilisateur(db: Session, id_utilisateur:int):
    return db.query(models.Historique).filter(models.Historique.id_utilisateur == id_utilisateur).order_by(models.Historique.date_action.desc()).all()

def get_derniere_action(db:Session, limit: int = 20):
    return db.query(models.Historique).filter(models.Historique.date_action.desc()).limit(limit).all()

def create_historique(db:Session, historique_data:Dict[str, Any]):
    db_historique = models.Historique(
        id_utilisateur = historique_data.get("id_utilisateur"),
        action=historique_data["action"],
        cible=historique_data.get("cible"),
        ip=historique_data.get("ip")
    )
    db.add(db_historique)
    db.commit()
    db.refresh(db_historique)
    return db_historique