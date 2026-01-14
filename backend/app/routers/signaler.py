# Routes FastAPI pour la gestion des signalement de points d’eau
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
import uuid, os
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Signaler, PointEau, Utilisateur
from ..schemas import SignalerBase, SignalerCreate
from app.DAO.DAOSignaler import (
    create_signale as dao_create_signale,  
    get_all_signale,
    get_signale_by_id_point,
    delete_signale_by_id_point
)
from ..models import Utilisateur
from .dependencies import rolesChecker

# Définition de la route pour les signalements
router = APIRouter(prefix="/signaler", tags=["Signaler"])

# Dépendance pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Récupère l’ensemble des signalements accèes non autorisé pour les utilisateurs public
@router.get("/", response_model=list[SignalerBase])
def list_signaler(db: Session = Depends(get_db),user_check: Utilisateur = Depends(rolesChecker("pompier", "commandement","admin"))):
    """Liste tous les signalements"""
    pointSignale = get_all_signale(db)
    return pointSignale

# Récupère tous les signalements associés à un point d’eau donné accèes non autorisé pour les utilisateurs public
@router.get("/id_p/{id_point}", response_model=list[SignalerBase])
def get_signalements_by_point(id_point: int, db: Session = Depends(get_db), user_check: Utilisateur = Depends(rolesChecker("pompier", "commandement","admin"))):
    """Récupère tous les signalements pour un point d'eau spécifique"""
    signalements = get_signale_by_id_point(db, id_point)
    
    if not signalements:
        raise HTTPException(status_code=404, detail=f"Signalement pour le point : {id_point} non trouvé")
    
    return signalements


# Récupère un signalement unique par son identifiant accèes non autorisé pour les utilisateurs public
@router.get("/id_s/{signalement_id}", response_model=SignalerBase)
def get_user(signalement_id: int, db: Session = Depends(get_db), user_check: Utilisateur = Depends(rolesChecker("pompier", "commandement","admin"))):
    signal = db.query(Signaler).filter(Signaler.id == signalement_id).first()
    if not signal:
        raise HTTPException(status_code=404, detail=f"Le point numéro: {signalement_id} n'a pas été trouvé")
    return signal


# Création d’un nouveau signalement avec une photo
@router.post("/", response_model=SignalerCreate)
def create_signalement(id_point: int = Form(...), probleme: str = Form(...), id_utilisateur: int = Form(...), photo: UploadFile = File(...), db: Session = Depends(get_db)):
   
    # verification des infos
    # Vérification de l’existence du point d’eau
    point = db.query(PointEau).filter(PointEau.numero_pei == id_point).first()
    if not point:
        raise HTTPException(status_code=404, detail=f"Le point numéro : {id_point} n'a pas été trouvé")
    utilisateurExite = db.query(Utilisateur).filter(Utilisateur.id_utilisateur == id_utilisateur).first()
    # Vérification de l’existence de l’utilisateur
    if not utilisateurExite:
        raise HTTPException(status_code=404, detail="L'utilisateur est introuvable")
    

    # création d'un id unique pour la photo
    ext = os.path.splitext(photo.filename)[1] or ".jpg"
    filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join("images/signalerImg", filename)

    # sauvegarder l'image dans le dossier images/signalerImg
    with open(file_path, "wb") as f:
        f.write(photo.file.read())

    # données pour le DAO
    data = {
        "id_point": id_point,
        "probleme": probleme,
        "photo": file_path,
        "id_utilisateur": id_utilisateur,
    }
    # Création du signalement
    try:
        return dao_create_signale(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



# Suppression de tous les signalements associés à un point d’eau  accèes non autorisé pour les utilisateurs public
@router.delete("/suprimmer/{id_point}")
def delete_signalements(id_point: int, db: Session = Depends(get_db), user_check: Utilisateur = Depends(rolesChecker("pompier", "commandement","admin"))):

    success = delete_signale_by_id_point(db, id_point)

    # Vérification du succès de la suppression    
    if not success:
        raise HTTPException(status_code=404, detail="id numéro: {id_point} introuvble")
    
    return {"detail": f"Signalements du point {id_point} supprimés avec succès"}