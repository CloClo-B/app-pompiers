# api/routes/points_eau.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import get_db
import crud
from schemas import PointEauCreate

router = APIRouter()

# -----------------------------
# Route pour récupérer tous les points d'eau
# -----------------------------
@router.get("/", summary="Récupère tous les points d'eau")
def read_points_eau(db: Session = Depends(get_db)):
    points = crud.get_all_points_eau(db)
    return {"count": len(points), "points_eau": points}

# Route pour récupérer un point d'eau par ID
@router.get("/{point_id}", summary="Récupère un point d'eau par son ID")
def read_point_eau(point_id: int, db: Session = Depends(get_db)):
    point = crud.get_point_eau_by_id(db, point_id)
    if not point:
        raise HTTPException(status_code=404, detail="Point d'eau non trouvé")
    return point



# créer un point d'eau
@router.post("/", summary="Création d'un point d'eau")
def creer_point(point: PointEauCreate, db: Session = Depends(get_db)):
    data = point.dict()
    point_id = crud.creer_point_eau(db, data)
    return {"id": point_id, "message": "Point d'eau créé avec succès"}
