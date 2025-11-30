from app import models 
from sqlalchemy.orm import Session
from passlib.context import CryptContext


# ============ UTILISATEUR ====================
def get_all_utilisateur(db: Session):
    utilisateurs = db.query(models.Utilisateur).all()
    output = []
    for u in utilisateurs :
        data = u.__dict__.copy()
        data.pop("mot_de_passe", None)
        output.append(data)
    return output

def get_utilisateur_by_email(db: Session, email: str):
    return db.query(models.Utilisateur).filter(models.Utilisateur.email == email).first()

pwd_context = CryptContext( schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password :str, hashed :str) -> bool:
    return pwd_context.verify(password, hashed)

def create_utilisateur(db:Session, user_data:dict):
    existe = get_utilisateur_by_email(db, user_data["email"])
    if existe:
        return None
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

def delete_utilisateur_by_id(db:Session, id_utilisateur:int):
    db_user = db.query(models.Utilisateur).filter(models.Utilisateur.id_utilisateur == id_utilisateur).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

def update_utilisateur_by_id(db:Session, id_utilisateur:int, user_data:dict):
    db_user = db.query(models.Utilisateur).filter(models.Utilisateur.id_utilisateur == id_utilisateur).first()
    if not db_user :
        return None
    for key, value in user_data.items():
        if key == "email":
            existe = get_utilisateur_by_email(db, value)
            if existe and existe.id_utilisateur != db_user.id_utilisateur :
                raise ValueError("Email déjà utilisé.")
        elif key == "mot_de_passe" and value:
            hashed_mdp = hash_password(value)
            setattr(db_user, key, hashed_mdp)
        elif key in ("id", "id_utilisateur"):
            continue
        elif hasattr(db_user, key):
            setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user
