from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from passlib.context import CryptContext

from ..database import SessionLocal
from ..models import Utilisateur
from ..schemas import UtilisateurCreate, UtilisateurOut, UtilisateurUpdate

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


# ================= CREATE =================
@router.post("/", response_model=UtilisateurOut)
def create_user(payload: UtilisateurCreate, db: Session = Depends(get_db)):
    if payload.mot_de_passe != payload.confirm_password:
        raise HTTPException(status_code=400, detail="Les mots de passe ne correspondent pas.")
    
    if db.query(Utilisateur).filter(Utilisateur.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email déjà utilisé.")

    new_user = Utilisateur(
        nom=payload.nom,
        prenom=payload.prenom,
        telephone=payload.telephone,
        email=payload.email,
        mot_de_passe=hash_password(payload.mot_de_passe),
        role=payload.role,
        date_creation=datetime.now()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# ================= GET ALL =================
@router.get("/", response_model=list[UtilisateurOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(Utilisateur).all()


# ================ GET BY ID =================
@router.get("/{user_id}", response_model=UtilisateurOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Utilisateur).filter(Utilisateur.id_utilisateur == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"Utilisateur {user_id} non trouvé")
    return user


# ============== UPDATE =================
@router.put("/{user_id}", response_model=UtilisateurOut)
def update_user(user_id: int, payload: UtilisateurUpdate, db: Session = Depends(get_db)):
    user = db.query(Utilisateur).filter(Utilisateur.id_utilisateur == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    for key, value in payload.dict(exclude_unset=True).items():
        if key == "mot_de_passe":
            setattr(user, key, hash_password(value))
        elif hasattr(user, key):
            setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user


# ================ DELETE =================
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Utilisateur).filter(Utilisateur.id_utilisateur == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    db.delete(user)
    db.commit()
    return {"detail": f"Utilisateur {user_id} supprimé avec succès"}
