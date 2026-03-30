# Router FastAPI pour la gestion des points d’eau avec gestion des coordonnées géographiques
from app.DAO.DAOPropAjout import delete_prop_ajout_by_id
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from geoalchemy2.elements import WKTElement
from ..database import SessionLocal
from ..models import PointEau
from ..schemas import PointEauBase, PointEauCreate, PointEauOut, PointEauOutLight, PointEauUpdate
from app.DAO.DAOPointsEau import (
    create_point_eau,
    get_all_points_eau,
    get_all_points_eau_light,
    get_point_eau_by_numero_pei,
    delete_point_eau_by_numero_pei,
    update_point_eau_by_id
)
from ..models import Utilisateur
from .dependencies import rolesChecker

# Définition de la route pour les signalements
router = APIRouter(prefix="/points-eau", tags=["Points d'eau"])

# Dépendance pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# récuperer tout les points d'eau
@router.get("/", response_model=list[PointEauBase])
def list_points(db: Session = Depends(get_db)):
    points = get_all_points_eau(db)
    return points

# récuperer tout les points d'eau Light (Optimisation)
@router.get("/light", response_model=list[PointEauOutLight])
def list_points_light(db: Session = Depends(get_db)):
    points = get_all_points_eau_light(db)
    return points

# Récupère un point d'eau selon son numéro PEI
@router.get("/{numero_pei}", response_model=PointEauOut)
def get_point(numero_pei: int, db: Session = Depends(get_db)):
    try:
        point = get_point_eau_by_numero_pei(db, numero_pei)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"le numéro: {numero_pei} est incorect")
    
    if not point:
        raise HTTPException(status_code=404, detail=f"le numéro: {numero_pei} est incorect")
    
    return point

# Crée un nouveau point d'eau
@router.post("/", response_model=PointEauOut)
def create_point(payload: PointEauCreate, db: Session = Depends(get_db), user_check: Utilisateur = Depends(rolesChecker("admin"))):
    

    # recup l'id utilisateur pour l'envoyer au DAO
    point_data = payload.model_dump()
    point_data["utilisateur"] = user_check.id_utilisateur
    
    # supprime la proposition de point d'eau si le param supp est a true
    if(point_data["supp"] == True):
        delete_prop_ajout_by_id(db, point_data["id_supp"])


    try:
        nouveau_point = create_point_eau(db, point_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
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
        "date_maj": nouveau_point.date_maj,
        "utilisateur": nouveau_point.utilisateur,
        "latitude": point_data["latitude"],
        "longitude": point_data["longitude"],
    }


# Modifier un point d'eau en fonction de son ID
@router.put("/update/{id_point}", response_model=PointEauUpdate)
def update_point(id_point: int, payload: PointEauUpdate, db: Session = Depends(get_db), user_check: Utilisateur = Depends(rolesChecker("admin"))):
    try:
        point = update_point_eau_by_id(db, id_point, payload.model_dump(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    return point




# Supprime un point d'eau selon son numéro PEI
@router.delete("/{numero_pei}")
def delete_point(numero_pei: int, db: Session = Depends(get_db), user_check: Utilisateur = Depends(rolesChecker("admin"))):
    success = delete_point_eau_by_numero_pei(db, numero_pei)
    
    if not success:
        raise HTTPException(status_code=404, detail=f"Numéro pei: {numero_pei} introuvable")
    
    return {"detail": f"Point d'eau {numero_pei} supprimé avec succès"}