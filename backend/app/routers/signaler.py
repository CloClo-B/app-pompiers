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

router = APIRouter(prefix="/signaler", tags=["Signaler"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ================= GET ALL =================
@router.get("/", response_model=list[SignalerBase])
def list_signaler(db: Session = Depends(get_db),user_check: Utilisateur = Depends(rolesChecker("commandement"))):
    """Liste tous les signalements"""
    pointSignale = get_all_signale(db)
    return pointSignale

# ================= GET BY ID_POINT =================
@router.get("/id_p/{id_point}", response_model=list[SignalerBase])
def get_signalements_by_point(id_point: int, db: Session = Depends(get_db), user_check: Utilisateur = Depends(rolesChecker("pompier"))):
    """Récupère tous les signalements pour un point d'eau spécifique"""
    signalements = get_signale_by_id_point(db, id_point)
    
    if not signalements:
        raise HTTPException(status_code=404, detail=f"Signalement pour le point : {id_point} non trouvé")
    
    return signalements


# ================= GET BY ID_SIGNALEMENT =================
@router.get("/id_s/{signalement_id}", response_model=SignalerBase)
def get_user(signalement_id: int, db: Session = Depends(get_db), user_check: Utilisateur = Depends(rolesChecker("pompier"))):
    signal = db.query(Signaler).filter(Signaler.id == signalement_id).first()
    if not signal:
        raise HTTPException(status_code=404, detail=f"Le point numéro: {signalement_id} n'a pas été trouvé")
    return signal


# ================= CREATE =================
@router.post("/", response_model=SignalerCreate)
def create_signalement(id_point: int = Form(...), probleme: str = Form(...), id_utilisateur: int = Form(...), photo: UploadFile = File(...), db: Session = Depends(get_db)):
   
    # verification des info
    point = db.query(PointEau).filter(PointEau.numero_pei == id_point).first()
    if not point:
        raise HTTPException(status_code=404, detail=f"Le point numéro : {id_point} n'a pas été trouvé")
    utilisateurExite = db.query(Utilisateur).filter(Utilisateur.id_utilisateur == id_utilisateur).first()
    if not utilisateurExite:
        raise HTTPException(status_code=404, detail="L'utilisateur est introuvable")
    

    # création d'un id pour l'image
    ext = os.path.splitext(photo.filename)[1] or ".jpg"
    filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join("images/signalerImg", filename)

    # sauvegarder l'image dans le dossier images
    with open(file_path, "wb") as f:
        f.write(photo.file.read())

    # données pour le DAO
    data = {
        "id_point": id_point,
        "probleme": probleme,
        "photo": file_path,
        "id_utilisateur": id_utilisateur,
    }

    try:
        return dao_create_signale(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



# ================= DELETE =================
@router.delete("/suprimmer/{id_point}")
def delete_signalements(id_point: int, db: Session = Depends(get_db), user_check: Utilisateur = Depends(rolesChecker("admin"))):
    """Supprime tous les signalements d'un point d'eau"""
    success = delete_signale_by_id_point(db, id_point)
    
    if not success:
        raise HTTPException(status_code=404, detail="id numéro: {id_point} introuvble")
    
    return {"detail": f"Signalements du point {id_point} supprimés avec succès"}