import os

# Config test
if "TESTING" not in os.environ:
    os.environ["TESTING"] = "true"

# URL de la base
if os.path.exists("/.dockerenv"):
    TEST_DATABASE_URL = os.getenv(
        "DATABASE_URL", 
        "postgresql://fenalim_test:fenalim_test123@db_test:5432/fenalim_db_test"
    )
else:
    TEST_DATABASE_URL = "postgresql://fenalim_test:fenalim_test123@localhost:5433/fenalim_db_test"

# Imports (le package est installé via setup.py)
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db
from app.models import Base

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Crée les tables au début et les supprime à la fin."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session():
    """Fournit une session de base de données pour chaque test."""
    session = TestingSessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()


@pytest.fixture()
async def client(db_session):
    """Fournit un client HTTP async pour tester l'API."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as ac:
        yield ac
    
    app.dependency_overrides.clear()