# Router FastAPI pour la gestion de l'historique
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
from ..models import Utilisateur
from .dependencies import rolesChecker

# Définition de la route pour les missions
router = APIRouter(prefix="/historique", tags=["Historique"])
# Dépendance pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Récupère tout l'historique
@router.get("/", response_model=List[HistoriqueBase])
def list_history(db: Session = Depends(get_db), user_check: Utilisateur = Depends(rolesChecker("pompier"))):
    return get_all_historique(db)

# Récupère l'historique d'un utilisateur
@router.get("/utilisateur/{id_utilisateur}", response_model=List[HistoriqueBase])
def history_by_user(id_utilisateur: int, db: Session = Depends(get_db), user_check: Utilisateur = Depends(rolesChecker("commandement"))):
    return get_historique_by_utilisateur(db, id_utilisateur)

# Récupère les dernières actions
@router.get("/derniere-actions", response_model=List[HistoriqueBase])
def recent_actions(limit: int = 20, db: Session = Depends(get_db), user_check: Utilisateur = Depends(rolesChecker("commandement"))):
    return get_derniere_action(db, limit)

# Crée une nouvelle entrée dans l'historique
@router.post("/", response_model=HistoriqueBase)
def create_entry(payload: HistoriqueCreate, db: Session = Depends(get_db), user_check: Utilisateur = Depends(rolesChecker("admin"))):
    return create_historique(db, payload.model_dump())
