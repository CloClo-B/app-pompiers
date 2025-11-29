from pyproj import Transformer
from sqlalchemy.orm import Session
from sqlalchemy import text
from geoalchemy2.elements import WKTElement


# from api import models
# from api.auth_utils import hash_password, verify_password


from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt


from .models import PointEau
from sqlalchemy import func

# Récupérer tous les points d'eau avec latitude et longitude
def get_all_points_eau(db: Session):
    points = db.query(
        PointEau.id,
        PointEau.numero_pei,
        PointEau.nom,
        PointEau.statut,
        PointEau.type_nature,
        PointEau.insee5,
        PointEau.accessibilite,
        PointEau.disponibilite,
        PointEau.carto_ref,
        PointEau.press_deb,
        PointEau.debit_1_bar,
        PointEau.vol_eau_mi,
        PointEau.date_crea,
        PointEau.date_maj,
        PointEau.utilisateur,
        func.ST_Y(PointEau.geom).label("latitude"),
        func.ST_X(PointEau.geom).label("longitude"),
    ).all()
    # Transformer les tuples pour que le response_model fonctionne bien
    return [
        {
            "id": p.id,
            "numero_pei": p.numero_pei,
            "nom": p.nom,
            "statut": p.statut,
            "type_nature": p.type_nature,
            "insee5": p.insee5,
            "accessibilite": p.accessibilite,
            "disponibilite": p.disponibilite,
            "carto_ref": p.carto_ref,
            "press_deb": p.press_deb,
            "debit_1_bar": p.debit_1_bar,
            "vol_eau_mi": p.vol_eau_mi,
            "date_crea": p.date_crea,
            "date_maj": p.date_maj,
            "utilisateur": p.utilisateur,
            "latitude": p.latitude,
            "longitude": p.longitude,
        }
        for p in points
    ]


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


def creer_point_eau(db: Session, payload):
    
     # conversion WGS84 (4326) -> Lambert-93 (2154)
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:2154")
    x, y = transformer.transform(payload.latitude, payload.longitude)
    wkt = WKTElement(f"POINT({x} {y})", srid=2154)
    
    new_point = PointEau(
        numero_pei=payload.numero_pei,
        statut= payload.statut,
        type_nature=payload.type_nature,
        insee5=payload.insee5,
        press_deb=payload.press_deb,
        debit_1_bar=payload.debit_1_bar,
        vol_eau_mi=payload.vol_eau_mi,
        accessibilite=payload.accessibilite,
        disponibilite=payload.disponibilite,
        carto_ref=payload.carto_ref,
        date_crea= datetime.now(),
        geom=wkt

    )
    db.add(new_point)
    db.commit()
    db.refresh(new_point)
    return new_point




# PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT_SECRET = "CHANGE_THIS_SECRET"  
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24h

# def hash_password(password: str) -> str:
#     return PWD_CONTEXT.hash(password[:72])

# def verify_password(plain: str, hashed: str) -> bool:
#     return PWD_CONTEXT.verify(plain, hashed)

# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)

# def get_user_by_email(db: Session, email: str):
#     return db.query(models.Utilisateur).filter(models.Utilisateur.email == email).first()

# def create_user(db: Session, user_data: dict):
#     hashed_password = hash_password(user_data["mot_de_passe"][:72])
#     db_user = models.Utilisateur(
#         nom=user_data["nom"],
#         prenom=user_data["prenom"],
#         telephone=user_data.get("telephone", ""),
#         email=user_data["email"],
#         mot_de_passe=hashed_password,
#         role=user_data.get("role", "public"),
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# def authenticate_user(db: Session, email: str, mot_de_passe: str):
#     user = get_user_by_email(db, email)
#     if not user:
#         return None
#     if not verify_password(mot_de_passe, user.mot_de_passe):
#         return None
#     return user