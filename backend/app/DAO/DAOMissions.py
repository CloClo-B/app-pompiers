from app import models 
from sqlalchemy.orm import Session
from typing import Dict, Any
from datetime import datetime, date, timedelta




# =============== MISSION ==================

def get_all_mission(db:Session):
    missions = db.query(models.Mission).all()
    out = []
    for m in missions : 
        data=m.__dict__.copy()
        data.pop("_sa_instance_state", None)
        out.append(data)
    return out

def get_mission_by_id(db: Session, id_mission:int):
    return db.query(models.Mission).filter(models.Mission.id_mission == id_mission).first()

def get_mission_by_date(db: Session, laDate : date):
    debutDeLaJournee = datetime(laDate.year, laDate.month, laDate.day)
    finDeLaJournee = debutDeLaJournee + timedelta(days=1)
    missions = db.query(models.Mission).filter(models.Mission.date_creation >= debutDeLaJournee, models.Mission.date_creation < finDeLaJournee).all()
    return missions

def create_mission(db:Session, mission_data:dict):
    if not db.query(models.PointEau).filter(models.PointEau.id == mission_data["id_point"]).first():
        raise ValueError("id_point est invalide")
    if not db.query(models.Utilisateur).filter(models.Utilisateur.id_utilisateur == mission_data["id_utilisateur"]).first():
        raise ValueError("id_utilisateur est incorrect")
    db_mission = models.Mission(
        id_point=mission_data["id_point"],
        id_utilisateur=mission_data["id_utilisateur"],
        statut=mission_data.get("statut", "en attente"),
        commentaire=mission_data.get("commentaire"),
        itineraire=mission_data.get("itineraire")
    )
    db.add(db_mission)
    db.commit()
    db.refresh(db_mission)
    return db_mission

def delete_mission_by_id(db:Session, id_mission: int):
    db_mission = db.query(models.Mission).filter(models.Mission.id_mission == id_mission).first()
    if db_mission : 
        db.delete(db_mission)
        db.commit()
        return True 
    return False


def update_mission_by_id(db:Session, id_mission: int, mission_data : Dict[str, Any]):
    db_mission = db.query(models.Mission).filter(models.Mission.id_mission == id_mission).first()
    if not db_mission : 
        return None
    for key, value in mission_data.items():
        if key in ["id_mission", "date_creation"]:
            continue
        if hasattr(db_mission, key):
            setattr(db_mission, key, value)
    db.commit()
    db.refresh(db_mission)
    return db_mission