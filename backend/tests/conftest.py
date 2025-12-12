import os
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine, text 
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db
from app.models import Base

# Définir la variable TESTING pour la config des tests
if "TESTING" not in os.environ:
    os.environ["TESTING"] = "true"

# Choix de l'URL selon Docker ou local
if os.path.exists("/.dockerenv"):
    TEST_DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://fenalim_test:fenalim_test123@db_test:5432/fenalim_db_test"
    )
else:
    TEST_DATABASE_URL = "postgresql://fenalim_test:fenalim_test123@localhost:5433/fenalim_db_test"

# Création du moteur SQLAlchemy sync pour les tests
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Crée toutes les tables avant la suite de tests, puis les supprime à la fin."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
        if not session.in_transaction():
            session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()

@pytest.fixture(autouse=True)
def clean_database(db_session):
    db_session.execute(text("SET session_replication_role = 'replica';")) 
    for table in Base.metadata.sorted_tables:
        db_session.execute(text(f"TRUNCATE TABLE {table.name} RESTART IDENTITY CASCADE"))
    db_session.execute(text("SET session_replication_role = 'origin';"))
    
    db_session.commit()

@pytest.fixture()
async def client(db_session):
    """
    Client HTTP pour tester l'API FastAPI.
    Override automatique de get_db pour utiliser la session test.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    # Utilisation d'AsyncClient pour la session asynchrone (FastAPI)
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()