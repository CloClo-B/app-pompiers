import os
from dotenv import load_dotenv
from pathlib import Path

import jwt
import secrets
from typing import Optional

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Utilisateur

security = HTTPBearer()

# Vérification des variables d'environnement
#key_use = os.getenv("key_use")
#algo_use = os.getenv("algo_use")
#time_token = int(os.getenv("time_token"))

key_use="projet_Sprint3" #Genere la clé secrète à utiliser pour le token
algo_use="HS256" #Algorithme utilisé pour le token
time_token=8 #Temps en heures de validité du token de l'utilisateur

print(f"key_use: {key_use}")
print(f"algo_use: {algo_use}")
print(f"time_token: {time_token}")

# Chemin du repertoire pour trouver le .env
#pathEnv = Path(__file__).resolve().parent.parent.parent  # Remonter 3 niveaux

# Définir les variables à utiliser à partir du fichier .env
#load_dotenv(dotenv_path=pathEnv)


def createToken(data: dict):
    copyDict = data.copy()
    expire = datetime.utcnow() + timedelta(hours=time_token)  # expiration correcte
    copyDict.update({
        "exp": expire,              # PyJWT accepte datetime directement
        "sub": str(data["sub"])     # s'assurer que sub est une string
    })
    token = jwt.encode(copyDict, key_use, algorithm=algo_use)
    return token


def validityToken(token: str):
    
    try:
        copyDict = jwt.decode(token, key_use, algorithms=[algo_use])
        print(f"Le token est encore valide : {copyDict}")
        return copyDict
    except (jwt.PyJWTError, jwt.ExpiredSignatureError) as errorMsg:
        print(f"Le token est invalide: {errorMsg}")
        return None



token_client = OAuth2PasswordBearer(tokenUrl="/utilisateurs/login")

def getTokenUser(token: str = Depends(token_client), db: Session = Depends(lambda: SessionLocal())):

    try:
        decodeToken = jwt.decode(token, key_use, algorithms=[algo_use])
        user_sub = decodeToken.get("sub")
        user_exp = decodeToken.get("exp")
        
        if user_exp is None:
            raise HTTPException(status_code=401, detail="Le token n'est plus valide")


    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Le token est expiré")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Le token n'est plus valide")

    user = db.query(Utilisateur).filter_by(id_utilisateur=int(user_sub)).first()

    if not user:
        raise HTTPException(status_code=401, detail="L'utilisateur est introuvable")

    return user
