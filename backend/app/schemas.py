from pydantic import BaseModel, EmailStr, Field, ConfigDict,model_validator
from typing import Optional, Any
from datetime import datetime


# =============== POINT D'EAU ================

class PointEauBase(BaseModel):
    id: int
    numero_pei: int
    nom: Optional[str] = None
    statut: str
    type_nature: str
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
    date_crea: Optional[datetime] = None
    date_maj: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class PointEauCreate(BaseModel):
    numero_pei: int
    nom: Optional[str] = None
    statut: str
    type_nature: str
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
    date_crea: datetime = Field(default_factory=datetime.now)
    date_maj: Optional[datetime] = None


# ============ UTILISATEUR ===============

class UtilisateurBase(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    telephone: str 
    role: Optional[str] = "public"

class UtilisateurCreate(UtilisateurBase):
    mot_de_passe: str = Field(min_length=12)
    confirm_password: str = Field(min_length=12)

    @model_validator(mode="after")
    def passwords_match(cls, model):
        if model.mot_de_passe != model.confirm_password:
            raise ValueError("Le mot de passe et sa confirmation ne correspondent pas")
        return model
    
class UtilisateurUpdate(BaseModel):
    nom: Optional[str]
    prenom: Optional[str]
    email: Optional[EmailStr]
    telephone: Optional[str]
    role: Optional[str]
    mot_de_passe: Optional[str]


class UtilisateurOut(UtilisateurBase):
    id_utilisateur: int

    model_config = ConfigDict(from_attributes=True)


# ============= MISSION ===============

class MissionBase(BaseModel):
    nom_mission: str
    id_point: int
    id_utilisateur: int
    commentaire: Optional[str]
    itineraire: Optional[Any]


class MissionCreate(MissionBase):
    commentaire: Optional[str] = None
    itineraire: Optional[Any] = None


class MissionUpdate(BaseModel):
    statut: Optional[str]
    commentaire: Optional[str]
    itineraire: Optional[Any]


class MissionOut(BaseModel):
    id_mission: int
    nom_mission: str
    id_point: int
    id_utilisateur: int
    date_creation: datetime
    statut: str
    commentaire: Optional[str]
    itineraire: Optional[Any]

    model_config = ConfigDict(from_attributes=True)


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

    model_config = ConfigDict(from_attributes=True)


# =============== SIGNALER ==================

class SignalerBase(BaseModel):
    id_point: int
    probleme: str
    photo: Optional[str]


class SignalerCreate(SignalerBase):
    model_config = ConfigDict(from_attributes=True)
