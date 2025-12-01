from pydantic import BaseModel, EmailStr, constr, Field
from enum import Enum
from typing import Optional, List, Any
from datetime import datetime



# =============== POINT D'EAU ================

class PointEauBase(BaseModel):
    id: int

    numero_pei: Optional[str] = None
    nom: Optional[str] = None
    statut: Optional[str] = None

    type_nature: Optional[str] = None
    insee5: Optional[str] = None

    press_deb: Optional[float] = None
    debit_1_bar: Optional[float] = None
    vol_eau_mi: Optional[float] = None


    accessibilite: Optional[str] = None
    disponibilite: Optional[str] = None

    carto_ref: Optional[int] = None

    utilisateur: Optional[str] = None 
    
    latitude: float 
    longitude: float

    date_crea : Optional[datetime] = None
    date_maj: Optional[datetime] = None

    signale : Optional[bool] = 0
    probleme : Optional[str]


    class Config:
        orm_mode = True

class PointEauCreate(BaseModel):
    numero_pei: Optional[str] = None
    nom: Optional[str] = None
    statut: Optional[str] = None
    
    type_nature: Optional[str] = None
    insee5: Optional[str] = None

    press_deb: Optional[float] = None
    debit_1_bar: Optional[float] = None
    vol_eau_mi: Optional[float] = None


    accessibilite: Optional[str] = None
    disponibilite: Optional[str] = None

    carto_ref: Optional[int] = None

    utilisateur: Optional[str] = None # a remplir par la suite avec la session de la personne
    
    latitude: float
    longitude: float

    date_crea: Optional[datetime] = Field(default_factory=datetime.now)
    date_maj: Optional[datetime] = None

    signale : Optional[bool] = 0
    probleme : Optional[str] = None



# ============ UTILISATEUR ===============

class UtilisateurBase(BaseModel):
    nom: str
    prenom: str
    email : EmailStr
    telephone : Optional[str] = None
    role: Optional[str] = "public"


class UtilisateurCreate(UtilisateurBase):
    mot_de_passe: str = Field(min_length=12)


class UtilisateurUpdate(BaseModel):
    nom: Optional[str]
    prenom: Optional[str]
    email: Optional[EmailStr]
    telephone: Optional[str]
    role: Optional[str]
    mot_de_passe: Optional[str]

class UtilisateurOut(UtilisateurBase):
    id_utilisateur: int

    class Config:
        from_attributes: True


# ============= MISSION ===============


class MissionBase(BaseModel):
    nom_mission : str
    id_point: int
    id_utilisateur: int
    commentaire: Optional[str]
    itineraire: Optional[Any] 

class MissionCreate(MissionBase):
    nom_mission : str
    id_point: int
    id_utilisateur: int
    commentaire: Optional[str] = None
    itineraire: Optional[Any] = None

class MissionUpdate(BaseModel):
    statut: Optional[str]
    commentaire: Optional[str]
    itineraire: Optional[Any]

class MissionOut(BaseModel):
    id_mission: int
    nom_mission : str
    id_point: int
    id_utilisateur: int
    date_creation: datetime
    statut: str
    commentaire: Optional[str]
    itineraire: Optional[Any]

    class Config:
        from_attributes = True 


# =============== HISTORIQUE ==================


class HistoriqueBase(BaseModel):
    id_utilisateur: Optional[int]
    action: str
    cible: Optional[str]
    ip: Optional[str]

class HistoriqueCreate(HistoriqueBase):
    pass

class HistoriqueOut(BaseModel):
    id_log: int
    id_utilisateur: Optional[int]
    action: str
    cible: Optional[str]
    date_action: datetime
    ip: Optional[str]

    class Config:
        from_attributes = True