from app.models import BanUtilisateur
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException

def verifier_ban_utilisateur(db: Session, id_utilisateur: int):
    ban = db.query(BanUtilisateur).filter(BanUtilisateur.id_utilisateur == id_utilisateur, BanUtilisateur.date_fin > func.now()).first()
    if ban:
        raise ValueError(f"Vous êtes banni jusqu'au {ban.date_fin}")