"""
Vérifie si le nombre de signalement journalier n'est pas dépasser pour un utilisateur 
apelle la table SignalementQuota qui contient les info du nombre de signalement pour 1 utilisateur en fonction de jour 
- 3 signalements pour les public
- 10 signalements pour les pompier et commandement
- illimité pour admin
"""

from app.models import SignalementQuota
from sqlalchemy.orm import Session
from sqlalchemy import func


def verifier_quota_signalement(db: Session, id_utilisateur: int, role: str):

    # récupère le quota du jour 
    compte = db.query(SignalementQuota).filter(SignalementQuota.id_utilisateur == id_utilisateur, SignalementQuota.date_creation == func.current_date()).first()
    

    # limite selon le rôle
    if compte:
        # public
        if role == "public":
            if compte.nb_signalements >= 3:
                raise ValueError(f"Limite quotidienne de 3 atteinte ")
            else:
                compte.nb_signalements += 1
        # pompier ou commandement
        elif (role == "pompier" or role == "commandement"):
            if compte.nb_signalements >= 10:
                raise ValueError(f"Limite quotidienne de 10 atteinte ")
            else: 
                compte.nb_signalements += 1
    else:
        compte = SignalementQuota(id_utilisateur=id_utilisateur,nb_signalements=1)
        db.add(compte)
    db.commit()

