from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, Any
from datetime import datetime
# Schémas Pydantic utilisés pour la validation la création et la sortie des données de l’API



# POINT D'EAU 
# Schéma de base pour la lecture d’un point d’eau
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


# Schéma utilisé lors de la création d’un point d’eau
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

# UTILISATEUR
# Schéma de base pour un utilisateur
class UtilisateurBase(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    telephone: Optional[str] = None
    role: Optional[str] = "admin"

# Schéma utilisé lors de la création d’un utilisateur
class UtilisateurCreate(UtilisateurBase):
    mot_de_passe: str = Field(min_length=12)
    confirm_password: str = Field(min_length=12)
    # Vérifie la correspondance des mots de passe
    def validate_password(self):
        if self.mot_de_passe != self.confirm_password:
            raise ValueError("Le mot de passe et sa confirmation ne correspondent pas")

# Schéma pour la mise à jour d’un utilisateur
class UtilisateurUpdate(BaseModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    email: Optional[EmailStr] = None
    telephone: Optional[str] = None
    role: Optional[str] = None
    mot_de_passe: Optional[str] = None

# Schéma de sortie utilisateur (sans le mot de passe)
class UtilisateurOut(BaseModel):
    id_utilisateur: int
    nom: str
    prenom: str
    email: EmailStr
    telephone: Optional[str] = None
    role: Optional[str] = "admin"
    model_config = ConfigDict(from_attributes=True)

# Réponse retournée après authentification
class AuthResponse(BaseModel):
    id_utilisateur: int
    token: str
    role: str
    model_config = ConfigDict(from_attributes=True)

# Payload de déconnexion
class LogoutPayload(BaseModel):
    id_utilisateur: int

# Payload de connexion
class LoginPayload(BaseModel):
    email: EmailStr
    mot_de_passe: str


# MISSION
# Schéma de base pour une mission
class MissionBase(BaseModel):
    nom_mission: str
    id_point: int
    id_utilisateur: int
    commentaire: Optional[str]
    itineraire: Optional[Any]

# Schéma de création d’une mission
class MissionCreate(MissionBase):
    nom_mission: str
    id_point: int
    id_utilisateur: int
    commentaire: Optional[str]
    itineraire: Optional[Any]

# Schéma de mise à jour d’une mission
class MissionUpdate(BaseModel):
    nom_mission: Optional[str] = None
    id_point: Optional[int] = None
    id_utilisateur: Optional[int] = None
    statut: Optional[str] = None
    commentaire: Optional[str] = None
    itineraire: Optional[Any] = None
    date_fin: Optional[datetime]

# Schéma de sortie d’une mission
class MissionOut(BaseModel):
    id_mission: int
    nom_mission: str
    id_point: int
    id_utilisateur: int
    date_creation: datetime
    statut: str
    commentaire: Optional[str]
    itineraire: Optional[Any]
    date_fin: Optional[datetime]

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


# HISTORIQUE
# Schéma de base pour l’historique des actions (pas encore fonctionnel)
class HistoriqueBase(BaseModel):
    id_utilisateur: Optional[int]
    action: str
    cible: Optional[str]
    ip: Optional[str]

# Schéma de création d’une entrée d’historique
class HistoriqueCreate(HistoriqueBase):
    pass

# Schéma de sortie de l’historique
class HistoriqueOut(BaseModel):
    id_log: int
    id_utilisateur: Optional[int]
    action: str
    cible: Optional[str]
    date_action: datetime
    ip: Optional[str]

    model_config = ConfigDict(from_attributes=True)


# SIGNALER
# Schéma de base pour un signalement
class SignalerBase(BaseModel):
    id:int
    id_point: int
    probleme: str
    photo: Optional[str]
    id_utilisateur: int
    date_creation: datetime
    
# Schéma de création d’un signalement
class SignalerCreate(BaseModel):
    id_point: int
    probleme: str
    photo: Optional[str]
    id_utilisateur: int
    model_config = ConfigDict(from_attributes=True)

# Schéma de sortie du profil utilisateur
class UserProfileOut(BaseModel):
    id_utilisateur: int
    nom: str
    prenom: str
    email: EmailStr
    telephone: str
    role: str
    date_creation: datetime
    derniere_connexion: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# Schéma de mise à jour du profil utilisateur
class UserProfileUpdate(BaseModel):
    nom: Optional[str] = Field(None, min_length=2, max_length=40)
    prenom: Optional[str] = Field(None, min_length=2, max_length=40)
    email: Optional[EmailStr] = None
    telephone: Optional[str] = Field(None, pattern=r'^\d{10}$') 

# Schéma de changement de mot de passe
class PasswordChangeRequest(BaseModel):
    old_password: str
    new_password: str = Field(min_length=12)
    confirm_new_password: str = Field(min_length=12)
    # Vérifie la cohérence des mots de passe
    def validate_passwords(self):
        if self.new_password != self.confirm_new_password:
            raise ValueError("Le nouveau mot de passe et sa confirmation sont différents ")
        if self.old_password == self.new_password:
            raise ValueError("Le nouveau mot de passe doit être différent de l'ancien")
