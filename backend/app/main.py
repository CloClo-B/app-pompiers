import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .database import Base, engine
from .routers.points_eau import router as points_router
from .routers.utilisateurs import router as users_router
from .routers.missions import router as missions_router
from .routers.historique import router as historique_router
from .routers.signaler import router as signaler_router

# Initialisation
app = FastAPI(title="API FastAPI - FEN-Alim")

# Autorise toutes les requêtes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.getenv("TESTING") != "true":
    Base.metadata.create_all(bind=engine)

# Routes
app.include_router(points_router)
app.include_router(users_router)
app.include_router(missions_router)
app.include_router(historique_router)
app.include_router(signaler_router)

# accéder au image depuis le front pour pouvoir les affihcer 
app.mount("/images", StaticFiles(directory="images"), name="images")



@app.get("/health")
def health():
    """Permet de vérifier que l'API fonctionne."""
    return {"status": "ok"}

