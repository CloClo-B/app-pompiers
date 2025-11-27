from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from geoalchemy2.elements import WKTElement

from ..database import SessionLocal
from ..models import PointEau
from ..schemas import PointEauBase, PointEauCreate

router = APIRouter(prefix="/points-eau", tags=["Points d'eau"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[PointEauBase])
def list_points(db: Session = Depends(get_db)):
    points = db.query(
        PointEau.id,
        PointEau.numero_pei,
        PointEau.nom,
        PointEau.statut,
        func.ST_Y(PointEau.geom).label("latitude"),
        func.ST_X(PointEau.geom).label("longitude"),
    ).all()
    return points

@router.post("/", response_model=PointEauBase)
def create_point(payload: PointEauCreate, db: Session = Depends(get_db)):
    wkt = WKTElement(f"POINT({payload.longitude} {payload.latitude})", srid=4326)
    new_point = PointEau(
        numero_pei=payload.numero_pei,
        nom=payload.nom,
        statut=payload.statut,
        geom=wkt
    )
    db.add(new_point)
    db.commit()
    db.refresh(new_point)

    return db.query(
        PointEau.id,
        PointEau.numero_pei,
        PointEau.nom,
        PointEau.statut,
        func.ST_Y(PointEau.geom).label("latitude"),
        func.ST_X(PointEau.geom).label("longitude"),
    ).filter(PointEau.id == new_point.id).first()
