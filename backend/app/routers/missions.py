from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Mission
from ..schemas import MissionCreate, MissionBase
from typing import List

router = APIRouter(prefix="/missions", tags=["Missions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=MissionBase)
def create_mission(payload: MissionCreate, db: Session = Depends(get_db)):
    new_mission = Mission(
        id_point=payload.id_point,
        id_pompier=payload.id_pompier,
        date_mission=payload.date_mission,
        type_mission=payload.type_mission,
        statut="en cours"
    )
    db.add(new_mission)
    db.commit()
    db.refresh(new_mission)
    return new_mission

@router.get("/", response_model=List[MissionBase])
def list_missions(db: Session = Depends(get_db)):
    return db.query(Mission).all()
