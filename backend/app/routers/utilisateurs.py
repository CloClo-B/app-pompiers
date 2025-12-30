from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from passlib.context import CryptContext
from ..database import SessionLocal
from ..models import Utilisateur
from ..schemas import UtilisateurCreate, UtilisateurOut, UtilisateurUpdate, LoginPayload, AuthResponse, LogoutPayload, UserProfileOut, UserProfileUpdate, PasswordChangeRequest
from ..token_jwt import createToken, getTokenUser
from .dependencies import rolesChecker
from ..DAO.DAOUtilisateurs import (update_own_profile, change_password as dao_change_password, verify_user_password)

router = APIRouter(prefix="/utilisateurs", tags=["Utilisateurs"])
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

# ================= GESTION DU COMPTE PERSONNEL =================

@router.get("/me", response_model=UserProfileOut)
def get_my_profile(current_user: Utilisateur = Depends(getTokenUser)):
    return current_user


@router.put("/me", response_model=UserProfileOut)
def update_my_profile(
    payload: UserProfileUpdate,
    current_user: Utilisateur = Depends(getTokenUser),
    db: Session = Depends(get_db)
):
    try:
        # Convertir le payload en dict et retirer les None
        update_data = payload.model_dump(exclude_unset=True)
        
        if not update_data:
            raise HTTPException(status_code=400, detail="Aucune donnée à mettre à jour")
        
        updated_user = update_own_profile(db, current_user.id_utilisateur, update_data)
        
        if not updated_user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        
        return updated_user
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la mise à jour: {str(e)}")


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

# ================= CREATE =================
@router.post("/", response_model=AuthResponse)
def create_user(payload: UtilisateurCreate, db: Session = Depends(get_db)):
    
    if payload.mot_de_passe != payload.confirm_password:
        raise HTTPException(status_code=400, detail="Les mots de passe ne correspondent pas.")
    
    if db.query(Utilisateur).filter(Utilisateur.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Compte déjà éxistant Email déjà utilisé.")
    
    if db.query(Utilisateur).filter(Utilisateur.telephone == payload.telephone).first():
        raise HTTPException(status_code=400, detail="Compte déjà éxistant numéro de téléphone déjà utilisé.")
    
    new_user = Utilisateur(
        nom=payload.nom,
        prenom=payload.prenom,
        telephone=payload.telephone,
        email=payload.email,
        mot_de_passe=hash_password(payload.mot_de_passe),
        role=payload.role,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Génération du token pour l'utilisateur 
    data = {"sub": new_user.id_utilisateur, "role": new_user.role}
    tokenUser = createToken(data)
    return AuthResponse(id_utilisateur=new_user.id_utilisateur, token=tokenUser, role=new_user.role)

# ================= VÉRIFIER SI UTILISATEUR EXISTE =================
@router.post("/login", response_model=AuthResponse)
def verif_login(payload: LoginPayload, db: Session = Depends(get_db)):

    user = db.query(Utilisateur).filter(Utilisateur.email == payload.email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")

    if not verify_password(payload.mot_de_passe, user.mot_de_passe):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")

    user.derniere_connexion = datetime.now()
    db.commit()
    
    # Générer JWT
    data = {"sub": user.id_utilisateur, "role": user.role}
    tokenUser = createToken(data)
    return AuthResponse(id_utilisateur=user.id_utilisateur, token=tokenUser, role=user.role)



# ================= GET ALL =================
@router.get("/", response_model=list[UtilisateurOut])
def list_users(current_user: Utilisateur = Depends(getTokenUser), db: Session = Depends(get_db), user_check: Utilisateur = Depends(rolesChecker("admin"))):
    return db.query(Utilisateur).all()

# ================ GET BY ID =================
@router.get("/{user_id}", response_model=UtilisateurOut)
def get_user(user_id: int, db: Session = Depends(get_db), user_check: Utilisateur = Depends(rolesChecker("admin"))):
    user = db.query(Utilisateur).filter(Utilisateur.id_utilisateur == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"Utilisateur {user_id} non trouvé")
    return user

# ============== UPDATE =================
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

# ================ DELETE =================
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
    
    # Vérification 1 : Un admin ne peut pas se supprimer lui-même
    if user_to_delete.id_utilisateur == current_user.id_utilisateur:
        raise HTTPException(
            status_code=400, 
            detail="Vous ne pouvez pas supprimer votre propre compte. Demandez à un autre administrateur."
        )
    
    # Vérification 2 : Protection du dernier administrateur
    if user_to_delete.role == "admin":
        admin_count = db.query(Utilisateur).filter(
            Utilisateur.role == "admin"
        ).count()
        
        if admin_count <= 1:
            raise HTTPException(
                status_code=400,
                detail="Impossible de supprimer le dernier administrateur du système. Créez d'abord un nouvel administrateur."
            )
    
    # Suppression sécurisée
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

# ================ LOGOUT =================
@router.post("/logout")
def logout(payload: LogoutPayload, db: Session = Depends(get_db)):
    
    # Suppression du token coté client
    user = db.query(Utilisateur).filter(Utilisateur.id_utilisateur == payload.id_utilisateur).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return {"detail": "Déconnexion réussie"}