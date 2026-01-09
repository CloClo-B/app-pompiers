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


# Récupère tous les utilisateurs sans le mot de passe
def get_all_utilisateur(db: Session) -> List[Dict[str, Any]]:
    utilisateurs = db.query(models.Utilisateur).all()
    output = []
    for u in utilisateurs:
        data = u.__dict__.copy()
        data.pop("_sa_instance_state", None)
        data.pop("mot_de_passe", None)  # Ne jamais retourner les mots de passe
        output.append(data)
    return output

# Récupère un utilisateur via son ID
def get_utilisateur_by_id(db: Session, id_utilisateur: int):
    return db.query(models.Utilisateur).filter(
        models.Utilisateur.id_utilisateur == id_utilisateur
    ).first()

# Récupère un utilisateur via son email
def get_utilisateur_by_email(db: Session, email: str):
    return db.query(models.Utilisateur).filter(models.Utilisateur.email == email).first()


# Crée un utilisateur et hash le mot de passe
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

# Supprime un utilisateur par ID
def delete_utilisateur_by_id(db: Session, id_utilisateur: int) -> bool:
    db_user = db.query(models.Utilisateur).filter(
        models.Utilisateur.id_utilisateur == id_utilisateur
    ).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

# Met à jour un utilisateur par ID
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

# Met à jour son propre profil
def update_own_profile(db: Session, id_utilisateur: int, user_data: Dict[str, Any]):
    db_user = db.query(models.Utilisateur).filter(
        models.Utilisateur.id_utilisateur == id_utilisateur
    ).first()
    
    if not db_user:
        return None
    
    # Liste des champs modifiables par l'utilisateur lui-même
    allowed_fields = ["nom", "prenom", "email", "telephone"]
    
    for key, value in user_data.items():
        if key not in allowed_fields:
            continue
            
        if key == "email" and value:
            # Vérifier que l'email n'est pas déjà utilisé par un autre utilisateur
            existe = get_utilisateur_by_email(db, value)
            if existe and existe.id_utilisateur != db_user.id_utilisateur:
                raise ValueError("Email déjà utilisé.")
            setattr(db_user, key, value)
        
        elif key == "telephone" and value:
            # Vérifier que le téléphone n'est pas déjà utilisé
            existe = db.query(models.Utilisateur).filter(
                models.Utilisateur.telephone == value,
                models.Utilisateur.id_utilisateur != id_utilisateur
            ).first()
            if existe:
                raise ValueError("Numéro de téléphone déjà utilisé.")
            setattr(db_user, key, value)
        
        elif hasattr(db_user, key) and value is not None:
            setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

# Change le mot de passe après vérification
def change_password(db: Session, id_utilisateur: int, old_password: str, new_password: str) -> bool:
    db_user = db.query(models.Utilisateur).filter(
        models.Utilisateur.id_utilisateur == id_utilisateur
    ).first()
    
    if not db_user:
        return False
    
    # Vérifier l'ancien mot de passe
    if not verify_password(old_password, db_user.mot_de_passe):
        raise ValueError("Ancien mot de passe incorrect")
    
    # Hasher et enregistrer le nouveau mot de passe
    db_user.mot_de_passe = hash_password(new_password)
    db.commit()
    return True

# Vérifie le mot de passe d’un utilisateur
def verify_user_password(db: Session, id_utilisateur: int, password: str) -> bool:
    db_user = db.query(models.Utilisateur).filter(
        models.Utilisateur.id_utilisateur == id_utilisateur
    ).first()
    
    if not db_user:
        return False
    
    return verify_password(password, db_user.mot_de_passe)