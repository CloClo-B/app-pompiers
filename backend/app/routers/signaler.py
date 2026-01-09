from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Signaler
from ..schemas import SignalerBase, SignalerCreate
from app.DAO.DAOSignaler import (
    create_signale as dao_create_signale,  
    get_all_signale,
    get_signale_by_id_point,
    delete_signale_by_id_point
)

router = APIRouter(prefix="/signaler", tags=["Signaler"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ================= GET ALL =================
@router.get("/", response_model=list[SignalerBase])
def list_signaler(db: Session = Depends(get_db)):
    """Liste tous les signalements"""
    pointSignale = get_all_signale(db)
    return pointSignale

# ================= GET BY ID_POINT =================
@router.get("/{id_point}", response_model=list[SignalerBase])
def get_signalements_by_point(id_point: int, db: Session = Depends(get_db)):
    """Récupère tous les signalements pour un point d'eau spécifique"""
    signalements = get_signale_by_id_point(db, id_point)
    
    if not signalements:
        raise HTTPException(status_code=404, detail="Not Found")
    
    return signalements

# ================= CREATE =================
@router.post("/", response_model=SignalerBase)
def create_signalement(payload: SignalerCreate, db: Session = Depends(get_db)):
    """Crée un nouveau signalement"""
    try:
        nouveau_signal = dao_create_signale(db, payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return nouveau_signal

# ================= DELETE =================
@router.delete("/{id_point}")
def delete_signalements(id_point: int, db: Session = Depends(get_db)):
    """Supprime tous les signalements d'un point d'eau"""
    success = delete_signale_by_id_point(db, id_point)
    
    if not success:
        raise HTTPException(status_code=404, detail="Not Found")
    
    return {"detail": f"Signalements du point {id_point} supprimés avec succès"}