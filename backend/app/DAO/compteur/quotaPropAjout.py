"""
Vérifie si le nombre de proposition d'ajout de points journaliers n'est pas dépassé pour un utilisateur 
appel de la table PropAjoutQuota qui contient les infos du nombre de propositions d'ajout pour 1 utilisateur en fonction de jour 
- 3 propositions pour les publics
- 10 propositions pour les pompiers et commandements
- admin n'a pas cette fonction car il peut déjà créer des points
"""
from app.models import PropAjoutQuota
from sqlalchemy.orm import Session
from sqlalchemy import func


def verifier_quota_proposition_ajout(db: Session, id_utilisateur: int, role: str):
    # récupère le quota du jour 
    compte = db.query(PropAjoutQuota).filter(PropAjoutQuota.id_utilisateur == id_utilisateur, PropAjoutQuota.date_creation == func.current_date()).first()
    

    # limite selon le rôle
    if compte:
        # public
        if role == "public":
            if compte.nb_proposition >= 3:
                raise ValueError(f"Limite quotidienne de 3 atteinte ")
            else:
                compte.nb_proposition += 1
        # pompier ou commandement
        elif (role == "pompier" or role == "commandement"):
            if compte.nb_proposition >= 10:
                raise ValueError(f"Limite quotidienne de 10 atteinte ")
            else: 
                compte.nb_proposition += 1
    else:
        compte = PropAjoutQuota(id_utilisateur=id_utilisateur,nb_proposition=1)
        db.add(compte)
    db.commit()

