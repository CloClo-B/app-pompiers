"""
DAO pour la gestion des Utilisateurs
"""
from app import models
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import Dict, Any, List, Optional

# Configuration du contexte de hashage des mots de passe
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def get_all_utilisateur(db: Session) -> List[Dict[str, Any]]:
    utilisateurs = db.query(models.Utilisateur).all()
    output = []
    for u in utilisateurs:
        data = u.__dict__.copy()
        data.pop("_sa_instance_state", None)
        data.pop("mot_de_passe", None)  # Ne jamais retourner les mots de passe
        output.append(data)
    return output


def get_utilisateur_by_id(db: Session, id_utilisateur: int):
    return db.query(models.Utilisateur).filter(
        models.Utilisateur.id_utilisateur == id_utilisateur
    ).first()


def get_utilisateur_by_email(db: Session, email: str):
    return db.query(models.Utilisateur).filter(models.Utilisateur.email == email).first()


def create_utilisateur(db: Session, user_data: Dict[str, Any]):
    # Vérifier si l'email existe déjà
    existe = get_utilisateur_by_email(db, user_data["email"])
    if existe:
        return None
    
    # Hasher le mot de passe
    hashed_password = hash_password(user_data["mot_de_passe"])
    
    db_user = models.Utilisateur(
        nom=user_data["nom"],
        prenom=user_data["prenom"],
        email=user_data["email"],
        telephone=user_data.get("telephone", ""),
        mot_de_passe=hashed_password,
        role=user_data.get("role", "public")
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_utilisateur_by_id(db: Session, id_utilisateur: int) -> bool:
    db_user = db.query(models.Utilisateur).filter(
        models.Utilisateur.id_utilisateur == id_utilisateur
    ).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False


def update_utilisateur_by_id(db: Session, id_utilisateur: int, user_data: Dict[str, Any]):
    db_user = db.query(models.Utilisateur).filter(
        models.Utilisateur.id_utilisateur == id_utilisateur
    ).first()
    if not db_user:
        return None
    
    for key, value in user_data.items():
        if key == "email":
            # Vérifier que l'email n'est pas déjà utilisé par un autre utilisateur
            existe = get_utilisateur_by_email(db, value)
            if existe and existe.id_utilisateur != db_user.id_utilisateur:
                raise ValueError("Email déjà utilisé.")
            setattr(db_user, key, value)
        elif key == "mot_de_passe" and value:
            # Hasher le nouveau mot de passe
            hashed_mdp = hash_password(value)
            setattr(db_user, key, hashed_mdp)
        elif key in ("id", "id_utilisateur"):
            # Ne pas modifier l'ID
            continue
        elif hasattr(db_user, key):
            setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user