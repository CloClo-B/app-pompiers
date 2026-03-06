import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Récupère l'url de la base, s'il n'est pas définit un url basique est utilisé
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://fenalim:fenalim123@db:5432/fenalim_db"
)

# Etablie la connexion à la base
# echo: affiche les requêtes
# future: active la future api sqlalchemy
engine = create_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    pool_size=20,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
)

# Crée une classe de session
# Pour chaque requête une session sera utilisée
# autocommit: les modifications doivent être validées manuellement
# autoflush: évite les flushs
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

# Classe Mère
Base = declarative_base()


# Fonction pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()