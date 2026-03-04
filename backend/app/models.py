from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, Enum, ForeignKey, func, DateTime
from geoalchemy2 import Geometry
import enum
from .database import Base

# Modèles SQLAlchemy de l’application contient le model de création de table

# Rôles possibles pour un utilisateur
class RoleEnum(str, enum.Enum):    
    public = "public"
    pompier = "pompier"
    commandement = "commandement"
    admin = "admin"

# Table des utilisateur
class Utilisateur(Base):
    __tablename__ = "utilisateurs"
    id_utilisateur = Column(Integer, primary_key=True, index=True)
    nom = Column(String(40), nullable=False)
    prenom = Column(String(40), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    telephone = Column(String(255), unique=True, nullable=False)
    mot_de_passe = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.admin)
    date_creation = Column(DateTime, server_default=func.now(), nullable=False)
    derniere_connexion = Column(DateTime)


# Table des points d’eau
class PointEau(Base):
    """Représente un point d'eau."""
    __tablename__ = "points_eau"
    id = Column(Integer, primary_key=True, index=True)
    numero_pei = Column(Integer, nullable=False, unique=True)
    nom = Column(String(100), nullable=True)

    # Statut autorisé : PUBLIC ou PRIVE
    statut = Column(        
        Enum('PUBLIC', 'PRIVE', name="type_statut_autorise"),
        nullable=False
    )
    # Type de point d'eau autorisé : BI, BI100, PENA, PI100, PI110, PI150, PI65, PI70, PI80, RESERVE EAU INCENDIE
    type_nature = Column(
        Enum('BI', 'BI100', 'PENA', 'PI100', 'PI110','PI150', 'PI65', 'PI70','PI80','RESERVE EAU INCENDIE', name="type_point_autorise"),
        nullable=False
    )
    insee5 = Column(String(10))
    # type d'accessibilité autorisée : C (accessible), NC (non communiquée), NON (inaccessible)
    accessibilite = Column(
        Enum('C', 'NC', 'NON', name="type_accessibilite_autorise"), nullable=False
    )

    # Type de disponnibilite autorisée : DI (disponible), IN (indisponible)
    disponibilite = Column(
        Enum('DI', 'IN', name="type_disponibilite_autorise"), nullable=False
    )
    carto_ref = Column(Integer, nullable=False)
    press_deb = Column(Float, nullable=False)
    debit_1_bar = Column(Float, nullable=False)
    vol_eau_mi = Column(Float, nullable=False)
    date_crea = Column(TIMESTAMP, server_default=func.now() , nullable=False)
    date_maj = Column(TIMESTAMP, nullable=True)
    utilisateur = Column(Integer, ForeignKey("utilisateurs.id_utilisateur"), nullable=False)
    geom = Column(Geometry("POINT", srid=2154), nullable=False)



# Table des Mission
class Mission(Base):
    __tablename__ = "missions"
    id_mission = Column(Integer, primary_key=True, index=True)
    nom_mission = Column(String(100), nullable=False)
    id_point = Column(Integer, ForeignKey("points_eau.numero_pei"), nullable=False)
    id_utilisateur = Column(Integer, ForeignKey("utilisateurs.id_utilisateur"), nullable=False)
    date_creation = Column(DateTime, server_default=func.now(), nullable=False)
        
    # Statut de mission autorisé : EN COURS ou TERMINER
    statut = Column(
        Enum('EN COURS', 'TERMINER', name="type_mission_autorise"),
        default="EN COURS"
    )
    commentaire = Column(String(100), nullable=True)
    itineraire = Column(String, nullable=True)
    date_fin = Column(DateTime, nullable=True)


# Signalement de problème sur un point d’eau
class Signaler(Base):
    __tablename__ = "signaler"
    id = Column(Integer, primary_key=True, index=True)
    id_point = Column(Integer, ForeignKey("points_eau.numero_pei"), nullable=False)
    probleme = Column(String(100), nullable=False)
    photo = Column(String(255), nullable=False) 
    id_utilisateur = Column(Integer, ForeignKey("utilisateurs.id_utilisateur"), nullable=False)
    date_creation = Column(DateTime, server_default=func.now(), nullable=False)

# Historique des actions utilisateurs 
class Historique(Base):
    __tablename__ = "historiques"
    id_log = Column(Integer, primary_key=True, index=True)
    id_utilisateur = Column(Integer, ForeignKey("utilisateurs.id_utilisateur"), nullable=False)
    action = Column(String(100), nullable=False)
    cible = Column(String(100))
    date_action = Column(DateTime, server_default=func.now())
    ip = Column(String(50))
