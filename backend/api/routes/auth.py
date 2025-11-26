from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, schemas
from api.database import get_db
from api.auth_utils import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/inscription", response_model=schemas.UserOut)
def inscription(payload: schemas.UserCreate, db: Session = Depends(get_db)):
   
    if payload.mot_de_passe != payload.confirm_password:
        raise HTTPException(status_code=400, detail="Les mots de passe ne correspondent pas")
    
    if crud.get_user_by_email(db, payload.email):
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    
    user_data = payload.dict(exclude={"confirm_password"})
    user = crud.create_user(db, user_data)
    return user



# a enlever plus tard

# @router.post("/connexion", response_model=schemas.Token)
# def login(form_data: dict, db: Session = Depends(get_db)):
#     # attendre: { "email": "...", "mot_de_passe": "..." }
#     email = form_data.get("email")
#     mot_de_passe = form_data.get("mot_de_passe")
#     if not email or not mot_de_passe:
#         raise HTTPException(status_code=400, detail="Email et mot de passe requis")
#     user = crud.authenticate_user(db, email, mot_de_passe)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Identifiants invalides")
    
#     token = create_access_token({"sub": str(user.id_utilisateur), "email": user.email, "role": user.role})
#     return {"access_token": token, "token_type": "bearer"}
