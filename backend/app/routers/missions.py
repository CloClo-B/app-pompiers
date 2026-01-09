from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import SessionLocal
from ..models import Mission
from ..schemas import MissionCreate, MissionUpdate, MissionOut

router = APIRouter(prefix="/missions", tags=["Missions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ================= CREATE =================
@router.post("/", response_model=MissionOut)  
def create_mission(payload: MissionCreate, db: Session = Depends(get_db)):
    new_mission = Mission(
        nom_mission=payload.nom_mission,
        id_point=payload.id_point,
        id_utilisateur=payload.id_utilisateur,
        statut="en_attente",
        commentaire=payload.commentaire,
        itineraire=payload.itineraire
    )
    db.add(new_mission)
    db.commit()
    db.refresh(new_mission)
    return new_mission


# ================= GET ALL =================
@router.get("/", response_model=List[MissionOut])  
def list_missions(db: Session = Depends(get_db)):
    return db.query(Mission).all()


# ================= GET BY ID =================
@router.get("/{mission_id}", response_model=MissionOut) 
def get_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.query(Mission).filter(Mission.id_mission == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail=f"Mission {mission_id} non trouvée")
    return mission


# ================= UPDATE =================
@router.put("/{mission_id}", response_model=MissionOut)
def update_mission(mission_id: int, payload: MissionUpdate, db: Session = Depends(get_db)):
    mission = db.query(Mission).filter(Mission.id_mission == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail=f"Mission {mission_id} non trouvée")

    if payload.nom_mission is not None:
        mission.nom_mission = payload.nom_mission
    if payload.id_point is not None:
        mission.id_point = payload.id_point
    if payload.id_utilisateur is not None:
        mission.id_utilisateur = payload.id_utilisateur
    if payload.statut is not None:
        mission.statut = payload.statut
    if payload.commentaire is not None:
        mission.commentaire = payload.commentaire
    if payload.itineraire is not None:
        mission.itineraire = payload.itineraire

    db.commit()
    db.refresh(mission)
    return mission


# ================= DELETE =================
@router.delete("/{mission_id}", response_model=dict)
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.query(Mission).filter(Mission.id_mission == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail=f"Mission {mission_id} non trouvée")

    db.delete(mission)
    db.commit()
    return {"detail": f"Mission {mission_id} supprimée"}
