import pytest
from fastapi.testclient import TestClient
from app import models
from app.routers.historique import get_db
import random

class TestHistoriqueRouter:
    """Tests pour le Router Historique"""
    
    # ============= FIXTURE CLIENT =============
    @pytest.fixture
    def client(self, db_session):
        """Client de test avec override de la dépendance DB"""
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
    def utilisateur_test(self, db_session):
        """Crée un utilisateur valide pour les tests"""
        unique_number = random.randint(10000, 99999)
        user = models.Utilisateur(
            nom="Dupont",
            prenom="Jean",
            email=f"jean.dupont{unique_number}@test.com",
            telephone=f"06{random.randint(10000000, 99999999)}",
            mot_de_passe="hashed_password",
            role=models.RoleEnum.pompier
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user
    
    @pytest.fixture
    def historiques_test(self, db_session, utilisateur_test):
        """Crée 3 entrées d'historique valides pour un utilisateur"""
        actions = ["Connexion", "Création point d'eau", "Modification mission"]
        logs = []
        for action in actions:
            h = models.Historique(
                id_utilisateur=utilisateur_test.id_utilisateur,
                action=action,
                cible="test",
                ip="127.0.0.1"
            )
            db_session.add(h)
            logs.append(h)
        db_session.commit()
        for h in logs:
            db_session.refresh(h)
        return logs
    
    # ============= TESTS GET ALL =============
    def test_get_all_historique_empty(self, client):
        """GET / doit retourner une liste vide si aucun historique"""
        response = client.get("/historique/")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_all_historique_with_data(self, client, historiques_test):
        """GET / doit retourner tous les historiques"""
        response = client.get("/historique/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        actions = [h['action'] for h in data]
        assert "Connexion" in actions
    
    # ============= TESTS GET BY UTILISATEUR =============
    def test_get_historique_by_utilisateur_success(self, client, utilisateur_test, historiques_test):
        """GET /utilisateur/{id} doit retourner l'historique de l'utilisateur"""
        response = client.get(f"/historique/utilisateur/{utilisateur_test.id_utilisateur}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert all(h['id_utilisateur'] == utilisateur_test.id_utilisateur for h in data)
    
    def test_get_historique_by_utilisateur_not_exist(self, client):
        """GET /utilisateur/{id} avec id inexistant doit retourner []"""
        response = client.get("/historique/utilisateur/99999")
        assert response.status_code == 200
        assert response.json() == []
    
    # ============= TESTS GET DERNIERES ACTIONS =============
    def test_get_dernieres_actions_default_limit(self, client, historiques_test):
        """GET /derniere-actions doit utiliser limit=20 par défaut"""
        response = client.get("/historique/derniere-actions")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
    
    def test_get_dernieres_actions_custom_limit(self, client, historiques_test):
        """GET /derniere-actions?limit=2 doit retourner 2 entrées max"""
        response = client.get("/historique/derniere-actions?limit=2")
        assert response.status_code == 200
        assert len(response.json()) == 2
    
    # ============= TESTS CREATE =============
    def test_create_historique_success(self, client, utilisateur_test):
        """POST / doit créer une entrée d'historique"""
        payload = {
            "id_utilisateur": utilisateur_test.id_utilisateur,
            "action": "Test action",
            "cible": "Test cible",
            "ip": "192.168.1.1"
        }
        response = client.post("/historique/", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data['action'] == "Test action"
        assert data['ip'] == "192.168.1.1"
    
    def test_create_historique_missing_required_field(self, client, utilisateur_test):
        """POST / sans champ obligatoire (action) doit échouer"""
        payload = {
            "id_utilisateur": utilisateur_test.id_utilisateur,
            "cible": "Test"
        }
        response = client.post("/historique/", json=payload)
        assert response.status_code == 422

