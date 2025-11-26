from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, Enum, ForeignKey
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
    numero_pei = Column(String)
    nom = Column(String)
    statut = Column(String)
    type_nature = Column(String)
    insee5 = Column(String)
    accessibilite = Column(String)
    disponibilite = Column(String)
    carto_ref = Column(Integer)
    press_deb = Column(Float)
    debit_1_bar = Column(Float)
    vol_eau_mi = Column(Float)
    geom = Column(Geometry("POINT", srid=2154))  # PostGIS

class Utilisateur(Base):
    __tablename__ = "utilisateurs"
    id_utilisateur = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    telephone = Column(String(20))
    email = Column(String(150), unique=True, nullable=False, index=True)
    mot_de_passe = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.public)
    date_creation = Column(TIMESTAMP)
    derniere_connexion = Column(TIMESTAMP)

class Mission(Base):
    __tablename__ = "missions"
    id_mission = Column(Integer, primary_key=True, index=True)
    id_point = Column(Integer, ForeignKey("points_eau.id"), nullable=False)
    id_pompier = Column(Integer, ForeignKey("utilisateurs.id_utilisateur"), nullable=False)
    date_mission = Column(TIMESTAMP, nullable=False)
    type_mission = Column(String, nullable=False)
    statut = Column(String, nullable=False, default="en cours")
    point_eau = relationship("PointEau", backref="missions")
    pompier = relationship("Utilisateur", backref="missions")

class Historique(Base):
    __tablename__ = "historique"
    id_historique = Column(Integer, primary_key=True, index=True)
    id_mission = Column(Integer, ForeignKey("missions.id_mission"), nullable=False)
    date_action = Column(TIMESTAMP, nullable=False)
    action = Column(String, nullable=False)
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.id_utilisateur"), nullable=False)
    mission = relationship("Mission", backref="historique")
    utilisateur = relationship("Utilisateur", backref="historique")