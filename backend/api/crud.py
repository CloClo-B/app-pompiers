from sqlalchemy.orm import Session
from sqlalchemy import text
from api import models
from api.auth_utils import hash_password, verify_password

# Récupérer tous les points d'eau avec latitude et longitude
# api/crud.py
from sqlalchemy import text

def get_all_points_eau(db):
    query = text("""
        SELECT 
            id,
            numero_pei,
            nom,
            statut,
            type_nature,
            insee5,
            accessibilite,
            disponibilite,
            carto_ref,
            press_deb,
            debit_1_bar,
            vol_eau_mi,
            date_crea,
            date_maj,
            utilisateur,
            ST_X(geom) AS longitude,
            ST_Y(geom) AS latitude
        FROM points_eau
    """)
    result = db.execute(query).fetchall()
    return [dict(row._mapping) for row in result]


# Récupérer un point d’eau par son ID
def get_point_eau_by_id(db: Session, point_id: int):
    query = """
        SELECT id, numero_pei, adresse, commune,
               ST_X(geom) AS longitude, ST_Y(geom) AS latitude
        FROM points_eau
        WHERE id = :point_id;
    """
    row = db.execute(query, {"point_id": point_id}).fetchone()

    if row:
        return {
            "id": row.id,
            "numero_pei": row.numero_pei,
            "adresse": row.adresse,
            "commune": row.commune,
            "longitude": row.longitude,
            "latitude": row.latitude,
        }
    return None

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_SECRET = "CHANGE_THIS_SECRET"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24h

def hash_password(password: str) -> str:
    return PWD_CONTEXT.hash(password[:72])

def verify_password(plain: str, hashed: str) -> bool:
    return PWD_CONTEXT.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)

def get_user_by_email(db: Session, email: str):
    return db.query(models.Utilisateur).filter(models.Utilisateur.email == email).first()

def create_user(db: Session, user_data: dict):
    hashed_password = hash_password(user_data["mot_de_passe"][:72])
    db_user = models.Utilisateur(
        nom=user_data["nom"],
        prenom=user_data["prenom"],
        telephone=user_data.get("telephone", ""),
        email=user_data["email"],
        mot_de_passe=hashed_password,
        role=user_data.get("role", "public"),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, mot_de_passe: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(mot_de_passe, user.mot_de_passe):
        return None
    return user