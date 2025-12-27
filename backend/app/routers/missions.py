from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List


from ..database import SessionLocal
from ..models import Mission
from ..schemas import MissionCreate, MissionUpdate, MissionOut, MissionBase
from app.DAO.DAOMissions import (
    create_mission,
    delete_mission_by_id,
    get_all_mission,
    get_mission_by_date,
    get_mission_by_id,
    update_mission_by_id
)

router = APIRouter(prefix="/missions", tags=["Missions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ================= CREATE =================
@router.post("/", response_model=MissionCreate)  
def create_mission_route(payload: MissionCreate, db: Session = Depends(get_db)):
    try:
        nouveau_mission = create_mission(db, payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return {
        "nom_mission": nouveau_mission.nom_mission,
        "id_point": nouveau_mission.id_point,
        "id_utilisateur": nouveau_mission.id_utilisateur,
        "commentaire": nouveau_mission.commentaire,
        "itineraire": nouveau_mission.itineraire,
    }


# ================= GET ALL =================
@router.get("/", response_model=List[MissionOut])  
def list_missions(db: Session = Depends(get_db)):
    mission = get_all_mission(db)
    return mission


# ================= GET BY ID =================
@router.get("/{mission_id}", response_model=MissionOut) 
def get_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = get_mission_by_id(db, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail=f"Mission {mission_id} non trouvée")
    return mission


# ================= UPDATE =================
@router.put("/update/{id_mission}", response_model=MissionOut)
def update_mission(id_mission: int, payload: MissionUpdate, db: Session = Depends(get_db)):
    try:
        mission = update_mission_by_id(db, id_mission, payload.model_dump(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    return mission

# ================= DELETE =================
@router.delete("/supprimer/{mission_id}", response_model=dict)
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    success = delete_mission_by_id(db, mission_id)
    
    if not success:
        raise HTTPException(status_code=404, detail=f"Mission {mission_id} non trouvée")

    return {"detail": f"Mission {mission_id} supprimée"}
