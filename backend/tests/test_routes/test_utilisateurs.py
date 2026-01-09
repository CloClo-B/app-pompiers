import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from app import models
from app.routers.utilisateurs import get_db
from app.database import SessionLocal
import random

class TestUtilisateurRouter:
    """Tests pour le Router Utilisateur"""
    
    # ============= FIXTURE CLIENT =============
    @pytest.fixture
    def client(self, db_session):
        """Client de test avec override de la dépendance DB"""
        # Import LOCAL pour éviter l'import circulaire
        from app.main import app
        
        def override_get_db():
            try:
                yield db_session
            finally:
                pass
        
        app.dependency_overrides[get_db] = override_get_db
        with TestClient(app) as test_client:
            yield test_client
        app.dependency_overrides.clear()
    
    # ============= FIXTURES =============
    @pytest.fixture
    def user_payload(self):
        """Payload valide pour créer un utilisateur"""
        unique_number = random.randint(10000, 99999)
        return {
            "nom": "Dupont",
            "prenom": "Jean",
            "email": f"jean.dupont{unique_number}@test.com",
            "telephone": f"06{random.randint(10000000, 99999999)}",
            "mot_de_passe": "Password123!",
            "confirm_password": "Password123!",
            "role": "public"
        }
    
    @pytest.fixture
    def created_user(self, client, user_payload):
        """Crée un utilisateur via l'API et retourne ses données"""
        res = client.post("/utilisateurs/", json=user_payload)
        assert res.status_code == 200
        return res.json()
    
    # ============= TESTS CREATE =================
    def test_create_user(self, client, user_payload):
        """POST / doit créer un utilisateur valide"""
        res = client.post("/utilisateurs/", json=user_payload)
        assert res.status_code == 200
        data = res.json()
        assert data["email"] == user_payload["email"]
        assert data["nom"] == user_payload["nom"]
        assert "mot_de_passe" not in data
        assert "id_utilisateur" in data
    
    def test_create_user_password_mismatch(self, client, user_payload):
        """POST / avec mots de passe différents doit échouer"""
        user_payload["confirm_password"] = "WrongPassword!"
        res = client.post("/utilisateurs/", json=user_payload)
        assert res.status_code == 400
        assert "correspondent pas" in res.json()["detail"]
    
    def test_create_user_duplicate_email(self, client, user_payload):
        """POST / avec email déjà existant doit échouer"""
        client.post("/utilisateurs/", json=user_payload)
        res = client.post("/utilisateurs/", json=user_payload)
        assert res.status_code == 400
        assert "déjà utilisé" in res.json()["detail"]
    
    # ============= TESTS GET ALL =================
    def test_list_users_empty(self, client):
        """GET / doit retourner une liste vide si aucun utilisateur"""
        res = client.get("/utilisateurs/")
        assert res.status_code == 200
        assert res.json() == []
    
    def test_list_users_with_data(self, client, created_user):
        """GET / doit retourner tous les utilisateurs"""
        res = client.get("/utilisateurs/")
        assert res.status_code == 200
        data = res.json()
        assert len(data) == 1
        assert data[0]["email"] == created_user["email"]
    
    # ============= TESTS GET BY ID =================
    def test_get_user_by_id(self, client, created_user):
        """GET /{id} doit retourner l'utilisateur correspondant"""
        user_id = created_user["id_utilisateur"]
        res = client.get(f"/utilisateurs/{user_id}")
        assert res.status_code == 200
        data = res.json()
        assert data["id_utilisateur"] == user_id
        assert data["email"] == created_user["email"]
        assert "mot_de_passe" not in data
    
    def test_get_user_not_found(self, client):
        """GET /{id} avec id inexistant doit retourner 404"""
        res = client.get("/utilisateurs/99999")
        assert res.status_code == 404
        assert "non trouvé" in res.json()["detail"]
    
    # ============= TESTS UPDATE =================
    def test_update_user(self, client, created_user):
        """PUT /{id} doit mettre à jour l'utilisateur"""
        user_id = created_user["id_utilisateur"]
        update_payload = {
            "nom": "Durand",
            "telephone": "0611111111"
        }
        res = client.put(f"/utilisateurs/{user_id}", json=update_payload)
        assert res.status_code == 200
        data = res.json()
        assert data["nom"] == "Durand"
        assert data["telephone"] == "0611111111"
        assert data["email"] == created_user["email"] 
    
    def test_update_user_not_found(self, client):
        """PUT /{id} avec id inexistant doit retourner 404"""
        res = client.put("/utilisateurs/99999", json={"nom": "Test"})
        assert res.status_code == 404
        assert "non trouvé" in res.json()["detail"]
    
    # ============= TESTS DELETE =================
    def test_delete_user(self, client, created_user):
        """DELETE /{id} doit supprimer l'utilisateur"""
        user_id = created_user["id_utilisateur"]
        
        res = client.delete(f"/utilisateurs/{user_id}")
        assert res.status_code == 200
        assert "supprimé avec succès" in res.json()["detail"]
        
        res = client.get(f"/utilisateurs/{user_id}")
        assert res.status_code == 404
    
    def test_delete_user_not_found(self, client):
        """DELETE /{id} avec id inexistant doit retourner 404"""
        res = client.delete("/utilisateurs/99999")
        assert res.status_code == 404
        assert "non trouvé" in res.json()["detail"]

