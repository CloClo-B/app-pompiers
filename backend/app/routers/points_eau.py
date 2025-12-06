from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from geoalchemy2.elements import WKTElement

from ..database import SessionLocal
from ..models import PointEau
from ..schemas import PointEauBase, PointEauCreate
from app.DAO.DAOPointsEau import (
    create_point_eau,
    get_all_points_eau
)
router = APIRouter(prefix="/points-eau", tags=["Points d'eau"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ================= GET ALL =================
@router.get("/", response_model=list[PointEauBase])
def list_points(db: Session = Depends(get_db)):
    points = get_all_points_eau(db)
    return points

# ================= CREATE =================
@router.post("/", response_model=PointEauBase)
def create_point(payload: PointEauCreate, db: Session = Depends(get_db)):

    nouveau_point = create_point_eau(db, payload)
    return db.query(
        PointEau.id,
        PointEau.numero_pei,
        PointEau.statut,
        PointEau.type_nature,
        PointEau.insee5,
        PointEau.press_deb,
        PointEau.debit_1_bar,
        PointEau.vol_eau_mi,
        PointEau.accessibilite,
        PointEau.disponibilite,
        PointEau.carto_ref,
        PointEau.utilisateur,
        PointEau.date_crea,
        PointEau.date_maj,
        func.ST_Y(PointEau.geom).label("latitude"),
        func.ST_X(PointEau.geom).label("longitude"),

    ).filter(PointEau.id == nouveau_point.id).first()
