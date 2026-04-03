# Routes FastAPI pour le signalement d'utilisateur 
from app.schemas import SignalUserBase
from app.DAO.DAOPropAjout import delete_prop_ajout_by_id
from app.DAO.DAOSignaler import delete_signalement_by_id

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Utilisateur, BanUtilisateur
from .dependencies import rolesChecker
from datetime import datetime, timedelta
from app.DAO.DAOUtilisateurs import dechiffrerTelEtMail

# Définition de la route pour les signalements utilisateur 
router = APIRouter(prefix="/signaler_utilisateur", tags=["SignalementUtilisateur"])

# Dépendance pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/")
def signaler_utilisateur(payload:  SignalUserBase,db: Session = Depends(get_db),user_check: Utilisateur = Depends(rolesChecker("pompier", "commandement", "admin"))):
    
    # Vérifier que l'utilisateur existe à partir du mail
    tous_les_utilisateurs = db.query(Utilisateur).all()
    existe = next((u for u in tous_les_utilisateurs if dechiffrerTelEtMail(u.email) == payload.mail_utilisateur),None    )
    if not existe:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    
    # supprimme le signalement
    if(payload.signalement_ou_propoition == "signalement"):
        delete_signalement_by_id(db, payload.id_s_ou_p)

    # supprimme le bannissemet
    if(payload.signalement_ou_propoition == "proposition"):
        delete_prop_ajout_by_id(db, payload.id_s_ou_p)
   
   
   
    # Créer le bannissement
    signalement = BanUtilisateur(
        id_utilisateur=existe.id_utilisateur,
        date_fin=datetime.now() + timedelta(days=3),
        raison=payload.raison
    )
    db.add(signalement)
    db.commit()
    db.refresh(signalement)

    return signalement    
