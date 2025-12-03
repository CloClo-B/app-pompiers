from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers.points_eau import router as points_router
from .routers.utilisateurs import router as users_router
from .routers.missions import router as missions_router
from .routers.historique import router as historique_router
from .routers.signaler import router as signaler_router

#initialisation
app = FastAPI(title="API FastAPI - FEN-Alim")

#Autorise toutes les requêtes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Crée les tables définies dans models.py si elles n'existent pas
Base.metadata.create_all(bind=engine)

#Routes
app.include_router(points_router)
app.include_router(users_router)
app.include_router(missions_router)
app.include_router(historique_router)
app.include_router(signaler_router)


@app.get("/health")
def health():
    """Permet de vérifier que l'API fonctonne."""
    return {"status": "ok"}
