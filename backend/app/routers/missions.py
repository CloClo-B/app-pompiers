# Router FastAPI pour la gestion des missions
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List


from ..database import SessionLocal
from ..models import Utilisateur
from ..schemas import MissionCreate, MissionUpdate, MissionOut, MissionCreateClient
from app.DAO.DAOMissions import (
    create_mission,
    delete_mission_by_id,
    get_all_mission,
    get_mission_by_id,
    update_mission_by_id
)
from .dependencies import rolesChecker

# Définition de la route pour les missions
router = APIRouter(prefix="/missions", tags=["Missions"])

# Dépendance pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Crée une nouvelle mission uniqument pour les commandent et administrateur
@router.post("/", response_model=MissionCreate)  
def create_mission_route(payload: MissionCreateClient, db: Session = Depends(get_db), user_check: Utilisateur = Depends(rolesChecker("commandement","admin"))):
    # recup l'id utilisateur pour l'envoyer au DAO
    mission_data = payload.model_dump()
    mission_data["id_utilisateur"] = user_check.id_utilisateur
    try:
        nouveau_mission = create_mission(db, mission_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return nouveau_mission



# Récupère toutes les missions interdit aux public
@router.get("/", response_model=List[MissionOut])  
def list_missions(db: Session = Depends(get_db), user_check: Utilisateur = Depends(rolesChecker("pompier", "commandement","admin"))):
    mission = get_all_mission(db)
    return mission


# Récupère une mission selon son ID interdit au public
@router.get("/{mission_id}", response_model=MissionOut) 
def get_mission(mission_id: int, db: Session = Depends(get_db), user_check: Utilisateur = Depends(rolesChecker("pompier", "commandement","admin"))):
    mission = get_mission_by_id(db, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail=f"Mission {mission_id} non trouvée")
    return mission


# Mettre à jour une mission uniqument pour les commandent et administrateur
@router.put("/update/{id_mission}", response_model=MissionOut)
def update_mission(id_mission: int, payload: MissionUpdate, db: Session = Depends(get_db), user_check: Utilisateur = Depends(rolesChecker("commandement","admin"))):
    try:
        mission = update_mission_by_id(db, id_mission, payload.model_dump(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    return mission

# Supprime une mission uniqument pour les commandent et administrateur
@router.delete("/supprimer/{mission_id}", response_model=dict)
def delete_mission(mission_id: int, db: Session = Depends(get_db), user_check: Utilisateur = Depends(rolesChecker("commandement","admin"))):
    success = delete_mission_by_id(db, mission_id)
    
    if not success:
        raise HTTPException(status_code=404, detail=f"Mission {mission_id} non trouvée")

    return {"detail": f"Mission {mission_id} supprimée"}
