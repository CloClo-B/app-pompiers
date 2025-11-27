
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Historique
from ..schemas import HistoriqueCreate, HistoriqueBase
from typing import List

router = APIRouter(prefix="/historique", tags=["Historique"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=HistoriqueBase)
def create_entry(payload: HistoriqueCreate, db: Session = Depends(get_db)):
    entry = Historique(
        id_mission=payload.id_mission,
        date_action=payload.date_action,
        action=payload.action,
        utilisateur_id=payload.utilisateur_id
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

@router.get("/", response_model=List[HistoriqueBase])
def list_history(db: Session = Depends(get_db)):
    return db.query(Historique).all()
