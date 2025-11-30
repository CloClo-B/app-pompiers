from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import SessionLocal
from ..schemas import HistoriqueBase, HistoriqueCreate
from app.DAO.DAOHistorique import (
    get_all_historique,
    get_historique_by_utilisateur,
    get_derniere_action,
    create_historique
)

router = APIRouter(prefix="/historique", tags=["Historique"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[HistoriqueBase])
def list_history(db: Session = Depends(get_db)):
    return get_all_historique(db)


@router.get("/utilisateur/{id_utilisateur}", response_model=List[HistoriqueBase])
def history_by_user(id_utilisateur: int, db: Session = Depends(get_db)):
    return get_historique_by_utilisateur(db, id_utilisateur)


@router.get("/derniere-actions", response_model=List[HistoriqueBase])
def recent_actions(limit: int = 20, db: Session = Depends(get_db)):
    return get_derniere_action(db, limit)


@router.post("/", response_model=HistoriqueBase)
def create_entry(payload: HistoriqueCreate, db: Session = Depends(get_db)):
    return create_historique(db, payload.dict())
