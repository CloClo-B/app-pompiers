from pydantic import BaseModel, EmailStr, Field, ConfigDict
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
    latitude: Optional[float] = None  
    longitude: Optional[float] = None  
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
    telephone: Optional[str] = None
    role: Optional[str] = "public"


class UtilisateurCreate(UtilisateurBase):
    mot_de_passe: str = Field(min_length=12)
    confirm_password: str = Field(min_length=12)

    def validate_password(self):
        if self.mot_de_passe != self.confirm_password:
            raise ValueError("Le mot de passe et sa confirmation ne correspondent pas")


class UtilisateurUpdate(BaseModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    email: Optional[EmailStr] = None
    telephone: Optional[str] = None
    role: Optional[str] = None
    mot_de_passe: Optional[str] = None


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
    nom_mission: Optional[str] = None
    id_point: Optional[int] = None
    id_utilisateur: Optional[int] = None
    statut: Optional[str] = None
    commentaire: Optional[str] = None
    itineraire: Optional[Any] = None


class MissionOut(BaseModel):
    id_mission: int
    nom_mission: str
    id_point: int
    id_utilisateur: int
    date_creation: datetime
    statut: str
    commentaire: Optional[str]
    itineraire: Optional[Any]

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


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
    id:int
    id_point: int
    probleme: str
    photo: Optional[str]
    id_utilisateur: int
    date_creation: datetime
    


class SignalerCreate(BaseModel):
    id_point: int
    probleme: str
    photo: Optional[str]
    id_utilisateur: int
    model_config = ConfigDict(from_attributes=True)
