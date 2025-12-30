from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, Enum, ForeignKey, func
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
import enum
from .database import Base

class RoleEnum(str, enum.Enum):
    public = "public"
    pompier = "pompier"
    commandement = "commandement"
    admin = "admin"

class PointEau(Base):
    __tablename__ = "points_eau"
    id = Column(Integer, primary_key=True, index=True)
    numero_pei = Column(String(20), nullable=False, unique=True)
    nom = Column(String(100))
    statut = Column(String(20))
    type_nature = Column(String(20))
    insee5 = Column(String(10))
    accessibilite = Column(String(5))
    disponibilite = Column(String(5))
    carto_ref = Column(Integer)
    press_deb = Column(Float)
    debit_1_bar = Column(Float)
    vol_eau_mi = Column(Float)
    date_crea = Column(TIMESTAMP)
    date_maj = Column(TIMESTAMP)
    utilisateur = Column(String(50))
    geom = Column(Geometry("POINT", srid=2154))


class Utilisateur(Base):
    __tablename__ = "utilisateurs"
    id_utilisateur = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    mot_de_passe = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.public)
    date_creation = Column(TIMESTAMP, server_default=func.now())
    derniere_connexion = Column(TIMESTAMP)


class Mission(Base):
    __tablename__ = "missions"
    id_mission = Column(Integer, primary_key=True, index=True)
    id_point = Column(Integer, ForeignKey("points_eau.id"), nullable=False)
    id_utilisateur = Column(Integer, ForeignKey("utilisateurs.id_utilisateur"), nullable=False)
    date_creation = Column(TIMESTAMP, server_default=func.now())
    statut = Column(String(20), default="en_attente")
    commentaire = Column(String)
    itineraire = Column(String)  # JSONB → String ou JSONType selon SQLAlchemy

class Historique(Base):
    __tablename__ = "historiques"
    id_log = Column(Integer, primary_key=True, index=True)
    id_utilisateur = Column(Integer, ForeignKey("utilisateurs.id_utilisateur"))
    action = Column(String(100), nullable=False)
    cible = Column(String(100))
    date_action = Column(TIMESTAMP, server_default=func.now())
    ip = Column(String(50))

