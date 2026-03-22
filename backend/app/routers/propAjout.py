# Routes FastAPI pour la gestion des proposition d'ajout de points d’eau
from app.DAO.ban.banUtuilisateur import verifier_ban_utilisateur
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
import uuid, os
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import PropAjoutPoint, Utilisateur
from ..schemas import PropAjoutBase, PropAjoutBaseOutMin, PropAjoutCreate, PropAjoutOut

from app.DAO.DAOPropAjout import (
    create_prop_ajout,  
    get_all_prop_ajout,
    get_ajout_by_id,
    delete_prop_ajout_by_id,
    get_all_prop_ajout_min
)

from app.DAO.compteur.quotaPropAjout import verifier_quota_proposition_ajout
from app.DAO.DAOUtilisateurs import (dechiffrerTelEtMail,)
from ..models import Utilisateur
from .dependencies import rolesChecker

# Définition de la route pour les proposition d'ajout
router = APIRouter(prefix="/propositionAjout", tags=["Ajout"])

# Dépendance pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Récupère l’ensemble des proposition d'ajout accèes uniquement pour les admin
@router.get("/", response_model=list[PropAjoutBase])
def list_proposition(db: Session = Depends(get_db),user_check: Utilisateur = Depends(rolesChecker("admin"))):
    """Liste tous les proposition d'ajout"""
    ajout = get_all_prop_ajout(db)
    return ajout

# Récupère l’ensemble des proposition d'ajout avec le minimum d'info pour moins charger le reseau accèes uniquement pour les admin
@router.get("/getmin", response_model=list[PropAjoutBaseOutMin])
def list_proposition_minimum(db: Session = Depends(get_db),user_check: Utilisateur = Depends(rolesChecker("admin"))):
    """Liste tous les proposition d'ajout"""
    ajout = get_all_prop_ajout_min(db)
    return ajout


# Récupère une proposition d'ajoute par son identifiant accèes uniquement pour les admin
@router.get("/id/{ajout_id}", response_model=PropAjoutOut)
def get_proposition_id(ajout_id: int, db: Session = Depends(get_db), user_check: Utilisateur = Depends(rolesChecker("admin"))):
    ajout = db.query(PropAjoutPoint).filter(PropAjoutPoint.id == ajout_id).first()
    
    if not ajout:
        raise HTTPException(status_code=404, detail=f"La proposition d'ajout numéro: {ajout_id} n'a pas été trouvé")
    user = db.query(Utilisateur).filter(Utilisateur.id_utilisateur == ajout.id_utilisateur).first()
    
    ajoutProp = get_ajout_by_id(db, ajout_id)

    if not ajoutProp:
        raise HTTPException(status_code=404, detail=f"Proposition d'ajout pour : {ajout_id} non trouvé")
    

    return {
        "id": ajoutProp.id,
        "description": ajoutProp.description,
        "photo": ajoutProp.photo,
        "mail_utilisateur": dechiffrerTelEtMail(user.email),
        "date_creation": ajoutProp.date_creation,
        "latitude": ajoutProp.latitude,
        "longitude": ajoutProp.longitude,
    }

# Création d'une nouvelle proposition d'ajout avec une photo
@router.post("/", response_model=PropAjoutCreate)
def create_proposition(description: str = Form(...), photo: UploadFile = File(...), latitude: str = Form(...), longitude : str = Form(...), db: Session = Depends(get_db),user_check: Utilisateur = Depends(rolesChecker("public", "pompier", "commandement","admin"))):
   
    # verifier que l'utilisateur n'est pas banni sinon pas le droit de signalement
    try:
        verifier_ban_utilisateur(db, user_check.id_utilisateur)
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
 
    # vérifier le nombre de proposition autorisé avec le calculateur de quota par jour
    # si public limite proposition à 3 par jour
    # si pompier ou commandement limite à 10
    try:
        verifier_quota_proposition_ajout(db, user_check.id_utilisateur, user_check.role)
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))

    # création d'un id unique pour la photo
    ext = os.path.splitext(photo.filename)[1] or ".jpg"
    filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join("images/propAjoutImg", filename)


    # sauvegarder l'image dans le dossier images/propAjoutImg
    with open(file_path, "wb") as f:
        f.write(photo.file.read())

    # données pour le DAO
    data = {
        "description": description,
        "photo": file_path,
        "id_utilisateur": user_check.id_utilisateur,
        "latitude": latitude,
        "longitude": longitude
    }
    # Création de la proposition
    try:
        nouveau_prop = create_prop_ajout(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return{
        "description": nouveau_prop.description,
        "photo": file_path,
        "id_utilisateur": nouveau_prop.id_utilisateur,
        "latitude": data["latitude"],
        "longitude": data["longitude"],
    }



# Suppression une proposition d'ajout  en fonction de l'id accèes uniquement pour les admin
@router.delete("/suprimmer/{id}")
def delete_proposition(id: int, db: Session = Depends(get_db), user_check: Utilisateur = Depends(rolesChecker("admin"))):

    success = delete_prop_ajout_by_id(db, id)

    # Vérification du succès de la suppression    
    if not success:
        raise HTTPException(status_code=404, detail=f"id: {id} introuvble")
    
    return {"detail": f"Proposition d'ajout {id} supprimés avec succès"}