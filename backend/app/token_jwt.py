import os
from dotenv import load_dotenv
from pathlib import Path

import jwt
import secrets
from typing import Optional

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta

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



# On crée un token JWT avec les données de l'utilisateur
def createToken(data: dict):
    copyDict = data.copy()
    copyDict["exp"] = timedelta(hours=time_token) + datetime.utcnow()
    encoding = jwt.encode(copyDict, key_use, algorithm=algo_use)

    return encoding

# Vérification du token en le décodant
def validityToken(token: str):
    try:
        #recupération du token via l'entete de Authorization
        copyDict = jwt.decode(token, key_use, algorithms=[algo_use])

        print(f"Le token est encore valide : {copyDict}")
        return copyDict

    except (jwt.PyJWTError, jwt.ExpiredSignatureError) as errorMsg:
        print(f"Le token est invalide: {errorMsg}")
        return None

# Dépendance FastAPI pour protéger les routes
def getTokenUser(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:

    token = credentials.credentials
    copyDict = validityToken(token)

    if copyDict:
        return copyDict
    else:
        raise HTTPException(status_code=401, detail="Le token n'est plus valide")
