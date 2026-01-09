from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from geoalchemy2.elements import WKTElement
from ..database import SessionLocal
from ..models import PointEau
from ..schemas import PointEauBase, PointEauCreate
from app.DAO.DAOPointsEau import (
    create_point_eau,
    get_all_points_eau,
    get_point_eau_by_numero_pei,
    delete_point_eau_by_numero_pei
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

# ================= GET BY NUMERO_PEI =================
@router.get("/{numero_pei}", response_model=PointEauBase)
def get_point(numero_pei: int, db: Session = Depends(get_db)):
    point = get_point_eau_by_numero_pei(db, numero_pei)
    
    if not point:
        raise HTTPException(status_code=404, detail="Not Found")
    
    return point

# ================= CREATE =================
@router.post("/", response_model=PointEauBase)
def create_point(payload: PointEauCreate, db: Session = Depends(get_db)):
    try:
        nouveau_point = create_point_eau(db, payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Calculer latitude / longitude depuis geom
    latitude = db.scalar(func.ST_Y(nouveau_point.geom))
    longitude = db.scalar(func.ST_X(nouveau_point.geom))
    
    return {
        "id": nouveau_point.id,
        "numero_pei": nouveau_point.numero_pei,
        "nom": nouveau_point.nom,
        "statut": nouveau_point.statut,
        "type_nature": nouveau_point.type_nature,
        "insee5": nouveau_point.insee5,
        "accessibilite": nouveau_point.accessibilite,
        "disponibilite": nouveau_point.disponibilite,
        "carto_ref": nouveau_point.carto_ref,
        "press_deb": nouveau_point.press_deb,
        "debit_1_bar": nouveau_point.debit_1_bar,
        "vol_eau_mi": nouveau_point.vol_eau_mi,
        "date_crea": nouveau_point.date_crea,
        "date_maj": nouveau_point.date_maj,
        "utilisateur": nouveau_point.utilisateur,
        "latitude": latitude,
        "longitude": longitude,
    }

# ================= DELETE =================
@router.delete("/{numero_pei}")
def delete_point(numero_pei: int, db: Session = Depends(get_db)):
    success = delete_point_eau_by_numero_pei(db, numero_pei)
    
    if not success:
        raise HTTPException(status_code=404, detail="Not Found")
    
    return {"detail": f"Point d'eau {numero_pei} supprimé avec succès"}