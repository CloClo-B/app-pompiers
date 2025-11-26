# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import points_eau, auth  

app = FastAPI(
    title="API FEN-Alim",
    description="API pour gérer les points d'eau et les missions des pompiers",
    version="1.0.0"
)

# -----------------------------
# Configuration CORS pour dev
# -----------------------------
origins = ["*"]

# origins = [
#     "http://192.168.1.132:19006",  # Expo dev server sur ton téléphone
#     "http://192.168.1.132:8000",   # FastAPI local (facultatif)
# ]



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # autorise seulement ton téléphone
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Inclusion des routeurs
# -----------------------------
app.include_router(points_eau.router, prefix="/points_eau", tags=["Points d'eau"])
app.include_router(auth.router) 

# Tu pourras ajouter d'autres routeurs comme :
# app.include_router(utilisateurs.router, prefix="/utilisateurs", tags=["Utilisateurs"])
# app.include_router(missions.router, prefix="/missions", tags=["Missions"])
