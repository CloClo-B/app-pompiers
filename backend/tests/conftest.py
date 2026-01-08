import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text 
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db
from app.models import Base
from app.token_jwt import getTokenUser  # Import pour le bypass

# 1. Configuration Environnement
os.environ["TESTING"] = "true"

if os.path.exists("/.dockerenv"):
    TEST_DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://fenalim_test:fenalim_test123@db_test:5432/fenalim_db_test"
    )
else:
    TEST_DATABASE_URL = "postgresql://fenalim_test:fenalim_test123@localhost:5433/fenalim_db_test"

# 2. Moteur SQLAlchemy (Sync)
# pool_pre_ping vérifie que la connexion est vivante avant de l'utiliser
engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Initialisation de la structure de la base."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def db_session():
    """Session pour préparer les données dans les fixtures de test."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback() # Libère les verrous (Locks)
        session.close()

@pytest.fixture(autouse=True)
def clean_database():
    """Nettoyage TRUNCATE ultra-robuste avec COMMIT explicite."""
    with engine.connect() as connection:
        trans = connection.begin()
        connection.execute(text("SET session_replication_role = 'replica';"))
        for table in reversed(Base.metadata.sorted_tables):
            connection.execute(text(f"TRUNCATE TABLE {table.name} RESTART IDENTITY CASCADE;"))
        connection.execute(text("SET session_replication_role = 'origin';"))
        trans.commit()

@pytest.fixture()
def client(db_session): 
    """
    Client de test synchrone avec Overrides.
    """
    # A. Override de la base de données pour l'API
    def override_get_db():
        session = TestingSessionLocal() 
        try:
            yield session
        finally:
            session.close() 

    # B. Override de l'authentification (Bypass JWT)
    # Cette fonction sera appelée à chaque fois qu'une route demande Depends(getTokenUser)
    def override_get_token_user():
        # On peut injecter ici un utilisateur par défaut si besoin
        # Pour les tests de rôles, on modifiera cette dépendance dans le test même
        return None 

    app.dependency_overrides[get_db] = override_get_db
    # On ne bypass pas getTokenUser ici globalement pour laisser les tests de rôles fonctionner
    
    with TestClient(app) as tc:
        yield tc

    app.dependency_overrides.clear()