from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from ..database import SessionLocal
from ..models import Mission
from ..schemas import MissionCreate, MissionBase

router = APIRouter(prefix="/missions", tags=["Missions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ================= CREATE =================
@router.post("/", response_model=MissionBase)
def create_mission(payload: MissionCreate, db: Session = Depends(get_db)):
    new_mission = Mission(
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
@router.get("/", response_model=List[MissionBase])
def list_missions(db: Session = Depends(get_db)):
    return db.query(Mission).all()


# ================= GET BY ID =================
@router.get("/{mission_id}", response_model=MissionBase)
def get_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.query(Mission).filter(Mission.id_mission == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail=f"Mission {mission_id} non trouvée")
    return mission


# ================= UPDATE =================
@router.put("/{mission_id}", response_model=MissionBase)
def update_mission(mission_id: int, payload: MissionCreate, db: Session = Depends(get_db)):
    mission = db.query(Mission).filter(Mission.id_mission == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail=f"Mission {mission_id} non trouvée")

    # Mettre à jour les champs modifiables
    mission.id_point = payload.id_point
    mission.id_utilisateur = payload.id_utilisateur
    mission.statut = payload.statut if payload.statut else mission.statut
    mission.commentaire = payload.commentaire
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
