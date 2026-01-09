import pytest
import random
from fastapi.testclient import TestClient
from app import models
from app.main import app
from app.token_jwt import getTokenUser 
from app.routers.historique import get_db
from app.models import RoleEnum

@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def user_public(db_session):
    user = models.Utilisateur(
        nom="Public", prenom="Test", email=f"p{random.randint(1,999)}@t.com",
        telephone="0600000000", mot_de_passe="h", role=RoleEnum.public
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def user_pompier(db_session):
    user = models.Utilisateur(
        nom="Pompier", prenom="Test", email=f"p{random.randint(1,999)}@t.com",
        telephone="0611111111", mot_de_passe="h", role=RoleEnum.pompier
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def user_cmd(db_session):
    user = models.Utilisateur(
        nom="Cmd", prenom="Test", email=f"c{random.randint(1,999)}@t.com",
        telephone="0622222222", mot_de_passe="h", role=RoleEnum.commandement
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def user_admin(db_session):
    user = models.Utilisateur(
        nom="Admin", prenom="Test", email=f"a{random.randint(1,999)}@t.com",
        telephone="0633333333", mot_de_passe="h", role=RoleEnum.admin
    )
    db_session.add(user)
    db_session.commit()
    return user


def test_get_all_historique_as_pompier(client, db_session, user_pompier, user_public):
    db_session.add(models.Historique(id_utilisateur=user_public.id_utilisateur, action="A", cible="T", ip="1"))
    db_session.commit()

    app.dependency_overrides[getTokenUser] = lambda: user_pompier
    
    response = client.get("/historique/")
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_get_all_historique_forbidden_for_public(client, user_public):
    app.dependency_overrides[getTokenUser] = lambda: user_public
    
    response = client.get("/historique/")
    assert response.status_code == 403


def test_get_historique_by_utilisateur(client, db_session, user_cmd, user_public):
    db_session.add(models.Historique(id_utilisateur=user_public.id_utilisateur, action="B", cible="T", ip="2"))
    db_session.commit()

    app.dependency_overrides[getTokenUser] = lambda: user_cmd
    
    response = client.get(f"/historique/utilisateur/{user_public.id_utilisateur}")
    assert response.status_code == 200
    assert response.json()[0]["id_utilisateur"] == user_public.id_utilisateur


def test_get_dernieres_actions_limit(client, db_session, user_cmd, user_public):
    for i in range(3):
        db_session.add(models.Historique(id_utilisateur=user_public.id_utilisateur, action=f"Act{i}", cible="T", ip="0"))
    db_session.commit()

    app.dependency_overrides[getTokenUser] = lambda: user_cmd
    
    response = client.get("/historique/derniere-actions?limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_create_historique_as_admin(client, user_admin, user_public):
    app.dependency_overrides[getTokenUser] = lambda: user_admin
    
    payload = {
        "id_utilisateur": user_public.id_utilisateur,
        "action": "Creation",
        "cible": "PEI",
        "ip": "10.0.0.1"
    }
    response = client.post("/historique/", json=payload)
    assert response.status_code == 200
    assert response.json()["action"] == "Creation"

def test_create_historique_forbidden_for_pompier(client, user_pompier, user_public):
    app.dependency_overrides[getTokenUser] = lambda: user_pompier
    
    payload = {"id_utilisateur": user_public.id_utilisateur, "action": "H", "cible": "B", "ip": "0"}
    response = client.post("/historique/", json=payload)
    
    # Un pompier ne peut pas POST (admin requis)
    assert response.status_code == 403