from pydantic import BaseModel, EmailStr, constr, Field
from enum import Enum
from typing import Optional, List
from datetime import datetime

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


class RoleEnum(str, Enum):
    public = "public"
    pompier = "pompier"
    commandement = "commandement"
    admin = "admin"

class UserCreate(BaseModel):
    nom: str
    prenom: str
    telephone: Optional[str] = None
    email: EmailStr
    mot_de_passe: constr(min_length=12)
    confirm_password: str
    role: Optional[RoleEnum] = RoleEnum.public

class UserOut(BaseModel):
    id_utilisateur: int
    nom: str
    prenom: str
    email: EmailStr
    role: RoleEnum

    class Config:
        orm_mode = True

class MissionBase(BaseModel):
    id_mission: int
    id_point: int
    id_pompier: int
    date_mission: datetime
    type_mission: str
    statut: str

    class Config:
        orm_mode = True

class MissionCreate(BaseModel):
    id_point: int
    id_pompier: int
    date_mission: datetime
    type_mission: str

class HistoriqueBase(BaseModel):
    id_historique: int
    id_mission: int
    date_action: datetime
    action: str
    utilisateur_id: int

    class Config:
        orm_mode = True

class HistoriqueCreate(BaseModel):
    id_mission: int
    date_action: datetime
    action: str
    utilisateur_id: int
