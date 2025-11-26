from pydantic import BaseModel, EmailStr, constr
from enum import Enum 
from typing import Optional
from datetime import datetime

# ----------------- PointEau -----------------
class PointEauBase(BaseModel):
    id: int
    numero_pei: str
    nom: str
    statut: str
    latitude: float
    longitude: float

    class Config:
        orm_mode = True

# ----------------- Utilisateur -----------------
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

# ----------------- Mission -----------------
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

# ----------------- Historique -----------------
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
