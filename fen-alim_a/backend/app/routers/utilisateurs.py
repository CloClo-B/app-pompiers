from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Utilisateur
from ..schemas import UserCreate, UserOut
from datetime import datetime
from passlib.context import CryptContext

router = APIRouter(prefix="/utilisateurs", tags=["Utilisateurs"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

@router.post("/", response_model=UserOut)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    if payload.mot_de_passe != payload.confirm_password:
        raise HTTPException(
            status_code=400,
            detail="Les mots de passe ne correspondent pas."
        )

    user_exist = db.query(Utilisateur).filter(Utilisateur.email == payload.email).first()
    if user_exist:
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

@router.get("/", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(Utilisateur).all()
