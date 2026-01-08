import pytest
from fastapi.testclient import TestClient
from app import models
from app.main import app
from app.token_jwt import getTokenUser, createToken
from app.models import RoleEnum

@pytest.fixture
def user_payload():
    return {
        "nom": "Dupont",
        "prenom": "Jean",
        "email": "jean.dupont@test.com",
        "telephone": "0601020304",
        "mot_de_passe": "Password123!",
        "confirm_password": "Password123!",
        "role": "public"
    }

@pytest.fixture
def admin_payload():
    return {
        "nom": "Admin",
        "prenom": "Super",
        "email": "admin@test.com",
        "telephone": "0611111111",
        "mot_de_passe": "AdminPass123!",
        "confirm_password": "AdminPass123!",
        "role": "admin"
    }


@pytest.fixture
def created_user(client, user_payload):
    res = client.post("/utilisateurs/", json=user_payload)
    assert res.status_code == 200
    return res.json()

@pytest.fixture
def db_admin(db_session):
    """Crée un admin directement en DB pour les tests d'autorisation"""
    admin = models.Utilisateur(
        nom="Admin", prenom="Test", email="adm@test.com",
        telephone="0688888888", mot_de_passe="hash", role=RoleEnum.admin
    )
    db_session.add(admin)
    db_session.commit()
    return admin

@pytest.fixture
def db_user(db_session):
    """Crée un utilisateur simple directement en DB"""
    user = models.Utilisateur(
        nom="User", prenom="Test", email="usr@test.com",
        telephone="0677777777", mot_de_passe="hash", role=RoleEnum.public
    )
    db_session.add(user)
    db_session.commit()
    return user


class TestAuth:
    def test_create_user_success(self, client, user_payload):
        res = client.post("/utilisateurs/", json=user_payload)
        assert res.status_code == 200
        data = res.json()
        assert "id_utilisateur" in data
        assert "token" in data

    def test_login_success(self, client, created_user, user_payload):
        login_payload = {
            "email": user_payload["email"],
            "mot_de_passe": user_payload["mot_de_passe"]
        }
        res = client.post("/utilisateurs/login", json=login_payload)
        assert res.status_code == 200
        assert "token" in res.json()

class TestMyProfile:
    def test_get_my_profile_success(self, client, db_user):
        app.dependency_overrides[getTokenUser] = lambda: db_user
        res = client.get("/utilisateurs/me")
        
        assert res.status_code == 200
        assert res.json()["email"] == db_user.email
        app.dependency_overrides.clear()

    def test_update_my_profile_success(self, client, db_user):
        app.dependency_overrides[getTokenUser] = lambda: db_user
        update_data = {"nom": "NouveauNom"}
        res = client.put("/utilisateurs/me", json=update_data)
        
        assert res.status_code == 200
        assert res.json()["nom"] == "NouveauNom"
        app.dependency_overrides.clear()


class TestAdminActions:
    def test_list_users_as_admin(self, client, db_admin, db_user):
        app.dependency_overrides[getTokenUser] = lambda: db_admin
        res = client.get("/utilisateurs/")
        
        assert res.status_code == 200
        assert len(res.json()) >= 2
        app.dependency_overrides.clear()

    def test_list_users_forbidden_for_user(self, client, db_user):
        app.dependency_overrides[getTokenUser] = lambda: db_user
        res = client.get("/utilisateurs/")
        
        assert res.status_code == 403
        app.dependency_overrides.clear()

    def test_delete_user_as_admin(self, client, db_admin, db_user):
        app.dependency_overrides[getTokenUser] = lambda: db_admin
        res = client.delete(f"/utilisateurs/{db_user.id_utilisateur}")
        
        assert res.status_code == 200
        assert res.json()["success"] is True
        app.dependency_overrides.clear()

    def test_delete_admin_self_forbidden(self, client, db_admin):
        app.dependency_overrides[getTokenUser] = lambda: db_admin
        res = client.delete(f"/utilisateurs/{db_admin.id_utilisateur}")

        assert res.status_code == 400
        app.dependency_overrides.clear()


def test_logout_success(client, db_user):
    res = client.post("/utilisateurs/logout", json={"id_utilisateur": db_user.id_utilisateur})
    assert res.status_code == 200
    assert "réussie" in res.json()["detail"]