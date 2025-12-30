from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers.points_eau import router as points_router
from .routers.utilisateurs import router as users_router
from .routers.missions import router as missions_router
from .routers.historique import router as historique_router

app = FastAPI(title="API FastAPI - FEN-Alim")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(points_router)
app.include_router(users_router)
app.include_router(missions_router)
app.include_router(historique_router)


@app.get("/health")
def health():
    return {"status": "ok"}
