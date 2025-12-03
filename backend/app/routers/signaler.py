from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models import Signaler
from ..schemas import SignalerBase, SignalerCreate
from app.DAO.DAOSignaler import (
    creer_signale,
    get_all_signale
)
router = APIRouter(prefix="/signaler", tags=["Signaler"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[SignalerBase])
def list_signaler(db: Session = Depends(get_db)):
    pointSignale= get_all_signale(db)
    return pointSignale


@router.post("/", response_model=SignalerBase)
def create_signal(payload: SignalerCreate, db: Session = Depends(get_db)):

    nouveau_signal = creer_signale(db, payload)
    return nouveau_signal

