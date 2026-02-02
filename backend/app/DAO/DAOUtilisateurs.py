"""
DAO pour la gestion des Utilisateurs
"""
import os
import base64
import nacl.secret
from app import models
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import Dict, Any, List


# Configuration du contexte de hashage des mots de passe
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
# hasher le mot de passe
def hash_password(password: str) -> str:
    return pwd_context.hash(password)
# verifier que les mots de passe sont identique
def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


# Charger la clé depuis .env
cle_hex = os.getenv("CLE_CHIFFREMENT")
cle = bytes.fromhex(cle_hex)
box = nacl.secret.SecretBox(cle)
# chiffrer le mail et téléphone
def chiffrerTelEtMail(donnee: str) -> str:
    chiffre = box.encrypt(donnee.encode())
    base64B = base64.b64encode(chiffre)  
    return base64B.decode('utf-8')    

# déchiffrer le mail et téléphone
def dechiffrerTelEtMail(donnee: str) -> str:
    dechiffre = base64.b64decode(donnee)
    dechiffrebase64 = box.decrypt(dechiffre)
    return dechiffrebase64.decode('utf-8')

# Récupère tous les utilisateurs sans le mot de passe
def get_all_utilisateur(db: Session) -> List[Dict[str, Any]]:
    utilisateurs = db.query(models.Utilisateur).all()
    output = []
    for u in utilisateurs:
        data = u.__dict__.copy()
        data.pop("_sa_instance_state", None)
        data.pop("mot_de_passe", None)  # Ne jamais retourner les mots de passe

        # Déchiffrement mail et téléphone
        data["email"] = dechiffrerTelEtMail(u.email)
        data["telephone"] = dechiffrerTelEtMail(u.telephone)
        
        output.append(data)
    return output

# Récupère un utilisateur via son ID
def get_utilisateur_by_id(db: Session, id_utilisateur: int):
    user = db.query(models.Utilisateur).filter(
        models.Utilisateur.id_utilisateur == id_utilisateur
    ).first()
    # Déchiffrement mail et téléphone
    user.email = dechiffrerTelEtMail(user.email)
    user.telephone = dechiffrerTelEtMail(user.telephone)
    
    return user

# Récupère un utilisateur via son mail
def get_utilisateur_by_email(db: Session, email: str):
    utilisateurs = db.query(models.Utilisateur).all()
    for user in utilisateurs:
        if dechiffrerTelEtMail(user.email) == email:
            return user
    return None

# Récupère un utilisateur via son numéro de téléphone
def get_utilisateur_by_numero_telephone(db: Session, telephone: str):
    utilisateurs = db.query(models.Utilisateur).all()
    for user in utilisateurs:
        if dechiffrerTelEtMail(user.telephone) == telephone:
            return user
    return None


# Crée un utilisateur et hash le mot de passe
def create_utilisateur(db: Session, user_data: Dict[str, Any]):
    # Vérifier si l'email et téléphone existe déjà
    user_email = user_data["email"]
    user_telephone = user_data["telephone"]
    utilisateurs = db.query(models.Utilisateur).all()

    for u in utilisateurs:
        if dechiffrerTelEtMail(u.email) == user_email:
            raise ValueError("Compte déjà éxistant Email déjà utilisé.")
        if dechiffrerTelEtMail(u.telephone) == user_telephone:
            raise ValueError("Compte déjà éxistant numéro de téléphone déjà utilisé.")
    
    # Hasher le mot de passe
    hashed_password = hash_password(user_data["mot_de_passe"])
    
    # chiffrer téléphone et email
    chiffre_mail = chiffrerTelEtMail(user_email)
    chiffre_telephone = chiffrerTelEtMail(user_telephone)
    
    db_user = models.Utilisateur(
        nom=user_data["nom"],
        prenom=user_data["prenom"],
        email=chiffre_mail,
        telephone= chiffre_telephone,
        mot_de_passe=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# verifier éxistance d'un utilisateur pour connexion
def verifier_connexion(db: Session, email : str, motDePasse: str):
    user = get_utilisateur_by_email(db, email)
    if not user:
        raise ValueError("Email ou mot de passe incorrect")
    if not verify_password(motDePasse, user.mot_de_passe):
        raise ValueError("Email ou mot de passe incorrect")
    return user


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
            chiffre_email = chiffrerTelEtMail(value)
            setattr(db_user, key, chiffre_email)
        
        elif key == "telephone" and value:
            # Vérifier que le téléphone n'est pas déjà utilisé
            existe = get_utilisateur_by_numero_telephone(db, value)
            if existe and existe.id_utilisateur != db_user.id_utilisateur:
                raise ValueError("Numéro de téléphone déjà utilisé.")
            
            chiffre_telephone = chiffrerTelEtMail(value)  
            setattr(db_user, key, chiffre_telephone)
        
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