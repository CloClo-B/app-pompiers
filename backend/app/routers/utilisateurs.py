# Routes FastAPI pour la gestion des utilisateurs (authentification, profil, administration)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from ..database import SessionLocal
from ..models import Utilisateur
from ..schemas import UtilisateurCreate, UtilisateurOut, UtilisateurOutMin, UtilisateurUpdate, LoginPayload, AuthResponse, LogoutPayload, UserProfileOut, UserProfileUpdate, PasswordChangeRequest
from ..token_jwt import createToken, getTokenUser
from .dependencies import rolesChecker
from ..DAO.DAOUtilisateurs import (update_own_profile, change_password as dao_change_password, create_utilisateur, verifier_connexion, dechiffrerTelEtMail)

# Définition de la route utilisateurs
router = APIRouter(prefix="/utilisateurs", tags=["Utilisateurs"])


# Dépendance pour récupérer une session base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GESTION DU COMPTE PERSONNEL
# Récupération du profil de l’utilisateur connecté
@router.get("/me", response_model=UserProfileOut)
def get_my_profile(current_user: Utilisateur = Depends(getTokenUser)):
    # Déchiffrage des infos
    email = dechiffrerTelEtMail(current_user.email)
    telephone = dechiffrerTelEtMail(current_user.telephone)

    return {
        "id_utilisateur": current_user.id_utilisateur,
        "nom": current_user.nom,
        "prenom": current_user.prenom,
        "email": email,
        "telephone": telephone,
        "role": current_user.role,
        "date_creation": current_user.date_creation,
        "derniere_connexion": current_user.derniere_connexion
    }

    return current_user

# Mise à jour du profil de l’utilisateur connecté
@router.put("/me", response_model=UserProfileOut)
def update_my_profile(
    payload: UserProfileUpdate,
    current_user: Utilisateur = Depends(getTokenUser),
    db: Session = Depends(get_db)
):
    try:
        # Convertir le payload en dict et retirer les None
        update_data = payload.model_dump(exclude_unset=True)
        
        # Vérification que au moins un champ est présent
        if not update_data:
            raise HTTPException(status_code=400, detail="Aucune donnée à mettre à jour")
        
        # Mise à jour via la couche DAO
        updated_user = update_own_profile(db, current_user.id_utilisateur, update_data)
        
        if not updated_user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        
        # Déchiffrage pour la réponse
        email = dechiffrerTelEtMail(updated_user.email)
        telephone = dechiffrerTelEtMail(updated_user.telephone)

        return {
            "id_utilisateur": updated_user.id_utilisateur,
            "nom": updated_user.nom,
            "prenom": updated_user.prenom,
            "email": email,
            "telephone": telephone,
            "role": updated_user.role,
            "date_creation": updated_user.date_creation,
            "derniere_connexion": updated_user.derniere_connexion
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la mise à jour: {str(e)}")

# Changement du mot de passe de l’utilisateur connecté
@router.post("/me/change-password")
def change_my_password(
    payload: PasswordChangeRequest,
    current_user: Utilisateur = Depends(getTokenUser),
    db: Session = Depends(get_db)
):
    
    try:
        # Valider que les mots de passe correspondent
        payload.validate_passwords()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    try:
        success = dao_change_password(
            db, 
            current_user.id_utilisateur,
            payload.old_password,
            payload.new_password
        )
        
        if not success:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        
        return {
            "detail": "Mot de passe modifié avec succès",
            "success": True
        }
    
    except ValueError as e:
        # Erreur de vérification de l'ancien mot de passe
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du changement de mot de passe: {str(e)}")


# Suppression du compte de l’utilisateur connecté
@router.delete("/me")
def delete_my_account(
    current_user: Utilisateur = Depends(getTokenUser),
    db: Session = Depends(get_db)
):

    try:
        # Vérifier que l'utilisateur n'est pas le dernier admin
        if current_user.role == "admin":
            admin_count = db.query(Utilisateur).filter(Utilisateur.role == "admin").count()
            if admin_count <= 1:
                raise HTTPException(
                    status_code=400, 
                    detail="Impossible de supprimer le dernier administrateur"
                )
        
        db.delete(current_user)
        db.commit()
        
        return {
            "detail": "Compte supprimé avec succès",
            "success": True
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la suppression du compte: {str(e)}"
        )

# Creation d'un utilisateur
# Création d’un nouvel utilisateur et génération du token JWT
@router.post("/", response_model=AuthResponse)
def create_user(payload: UtilisateurCreate, db: Session = Depends(get_db)):
    # Vérification des mots de passe
    if payload.mot_de_passe != payload.confirm_password:
        raise HTTPException(status_code=400, detail="Les mots de passe ne correspondent pas.")
    
    # Donées pour le DAO
    new_user = {
        "nom": payload.nom,
        "prenom": payload.prenom,
        "email": payload.email,
        "telephone": payload.telephone,
        "mot_de_passe": payload.mot_de_passe,
    }
    # Création du compte
    try:
        # Génération du token pour l'utilisateur   
        created_user = create_utilisateur(db, new_user)  
        data = {"sub": created_user.id_utilisateur, "role": created_user.role}
        tokenUser = createToken(data)
        return AuthResponse(token=tokenUser, role=created_user.role)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Connexion
# Vérification des identifiants utilisateur et connexion
@router.post("/login", response_model=AuthResponse)
def verif_login(payload: LoginPayload, db: Session = Depends(get_db)):
    
    # récupération de l'utilisateur
    try:
        user = verifier_connexion(db, payload.email, payload.mot_de_passe)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Mise à jour de la date de dernière connexion
    user.derniere_connexion = datetime.now()
    db.commit()

    # Génération du token pour l'utilisateur   
    data = {"sub": user.id_utilisateur, "role": user.role}
    tokenUser = createToken(data)
    return AuthResponse(token=tokenUser, role=user.role)
    


# ADMINISTRATION
# Récupération de tous les utilisateurs sans mot de passe autorisé pour admin uniquement 
@router.get("/", response_model=list[UtilisateurOut])
def list_users(current_user: Utilisateur = Depends(getTokenUser), db: Session = Depends(get_db), user_check: Utilisateur = Depends(rolesChecker("admin"))):
    return db.query(Utilisateur).all()

# Récupération de tous les utilisateurs sans les info sensible comme email, téléphone et mot de passe autorisé pour admin uniquement 
@router.get("/minimum", response_model=list[UtilisateurOutMin])
def list_users_min(current_user: Utilisateur = Depends(getTokenUser), db: Session = Depends(get_db), user_check: Utilisateur = Depends(rolesChecker("admin"))):
    
    complet = db.query(
        Utilisateur.id_utilisateur,
        Utilisateur.nom,
        Utilisateur.prenom,
        Utilisateur.role
    ).all()
    
    return [
        {
        "id_utilisateur": u.id_utilisateur,
        "nom": u.nom,
        "prenom": u.prenom,
        "role": u.role,
        } 
        for u in complet
    ]


# Récupération d’un utilisateur par ID autorisé pour admin uniquement
@router.get("/{user_id}", response_model=UtilisateurOut)
def get_user(user_id: int, db: Session = Depends(get_db), user_check: Utilisateur = Depends(rolesChecker("admin"))):
    user = db.query(Utilisateur).filter(Utilisateur.id_utilisateur == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"Utilisateur {user_id} non trouvé")
    
    
    # Déchiffrage
    email = dechiffrerTelEtMail(user.email)
    telephone = dechiffrerTelEtMail(user.telephone)
    return {
        "id_utilisateur": user.id_utilisateur,
        "nom": user.nom,
        "prenom": user.prenom,
        "email": email,
        "telephone": telephone,
        "role": user.role,
    }
    


# Mise à jour d’un utilisateur autorisé pour admin uniquement
@router.put("/{user_id}", response_model=UtilisateurOut)
def update_user(user_id: int, payload: UtilisateurUpdate, db: Session = Depends(get_db), user_check: Utilisateur = Depends(rolesChecker("admin"))):
    user = db.query(Utilisateur).filter(Utilisateur.id_utilisateur == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    for key, value in payload.model_dump(exclude_unset=True).items():
        if key == "mot_de_passe":
            setattr(user, key, hash_password(value))
        elif hasattr(user, key):
            setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user

# Suppression d’un utilisateur autorisé pour admin uniquement
@router.delete("/{user_id}")
def delete_user(
    user_id: int, 
    current_user: Utilisateur = Depends(getTokenUser),
    db: Session = Depends(get_db), 
    user_check: Utilisateur = Depends(rolesChecker("admin"))
):
    # Récupérer l'utilisateur à supprimer
    user_to_delete = db.query(Utilisateur).filter(
        Utilisateur.id_utilisateur == user_id
    ).first()
    
    if not user_to_delete:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    # Vérification que l'admin ne peut pas se supprimer lui-même
    if user_to_delete.id_utilisateur == current_user.id_utilisateur:
        raise HTTPException(
            status_code=400, 
            detail="Vous ne pouvez pas supprimer votre propre compte. Demandez à un autre administrateur."
        )
    
    # Vérification que il reste bien un administrateur
    if user_to_delete.role == "admin":
        admin_count = db.query(Utilisateur).filter(
            Utilisateur.role == "admin"
        ).count()
        
        if admin_count <= 1:
            raise HTTPException(
                status_code=400,
                detail="Impossible de supprimer le dernier administrateur du système. Créez d'abord un nouvel administrateur."
            )
    
    # Suppression définitive
    try:
        db.delete(user_to_delete)
        db.commit()
        
        return {
            "detail": f"Utilisateur {user_to_delete.prenom} {user_to_delete.nom} (ID: {user_id}) supprimé avec succès",
            "success": True,
            "deleted_user": {
                "id": user_to_delete.id_utilisateur,
                "nom": user_to_delete.nom,
                "prenom": user_to_delete.prenom,
                "role": user_to_delete.role
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la suppression : {str(e)}"
        )

# DÉCONNEXION
@router.post("/logout")
def logout(payload: LogoutPayload, db: Session = Depends(get_db)):
    
    # Suppression du token coté client
    user = db.query(Utilisateur).filter(Utilisateur.id_utilisateur == payload.id_utilisateur).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return {"detail": "Déconnexion réussie"}