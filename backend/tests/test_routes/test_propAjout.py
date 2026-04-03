import pytest
import random
import io
import os
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from geoalchemy2.elements import WKTElement

# Imports absolus
from app import models
from app.main import app
from app.routers.propAjout import get_db
from app.token_jwt import getTokenUser
from app.models import RoleEnum

class TestPropAjoutRouter:
    """Tests pour le Router Proposition Ajout"""
    
    @pytest.fixture
    def client(self, db_session):
        def override_get_db():
            yield db_session
        
        app.dependency_overrides[get_db] = override_get_db
        with TestClient(app) as test_client:
            yield test_client
        app.dependency_overrides.clear()

    @pytest.fixture
    def db_admin(self, db_session):
        """Crée un admin pour bypasser les rôles"""
        admin = models.Utilisateur(
            nom="Admin", prenom="Test", email=f"adm{random.randint(1,999)}@test.com",
            telephone="0600000000", mot_de_passe="h", role=RoleEnum.admin
        )
        db_session.add(admin)
        db_session.commit()
        return admin

    @pytest.fixture
    def db_public(self, db_session):
        """Crée un utilisateur public"""
        public = models.Utilisateur(
            nom="Public", prenom="User", email=f"pub{random.randint(1,999)}@test.com",
            telephone="0600000001", mot_de_passe="h", role=RoleEnum.public
        )
        db_session.add(public)
        db_session.commit()
        return public

    @pytest.fixture
    def proposition_test(self, db_session, db_public):
        """Crée une proposition de test"""
        os.makedirs('images/propAjoutImg', exist_ok=True)
        
        proposition = models.PropAjoutPoint(
            description="Proposition test",
            photo="images/propAjoutImg/test.jpg",
            id_utilisateur=db_public.id_utilisateur,
            geom=WKTElement('POINT(200000 6800000)', srid=2154)
        )
        db_session.add(proposition)
        db_session.commit()
        db_session.refresh(proposition)
        return proposition

    # TESTS GET ALL 
    def test_get_all_propositions_admin(self, client, proposition_test, db_admin):
        """Admin peut voir toutes les propositions"""
        app.dependency_overrides[getTokenUser] = lambda: db_admin
        
        response = client.get("/propositionAjout/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert any(p['description'] == "Proposition test" for p in data)
        app.dependency_overrides.clear()

    def test_get_all_propositions_forbidden_for_non_admin(self, client, db_public):
        """Non-admin ne peut pas voir les propositions"""
        app.dependency_overrides[getTokenUser] = lambda: db_public
        
        response = client.get("/propositionAjout/")
        assert response.status_code in [401, 403]
        app.dependency_overrides.clear()

    #  TESTS GET MIN
    def test_get_all_propositions_min_admin(self, client, proposition_test, db_admin):
        """Admin peut voir la liste minimale"""
        app.dependency_overrides[getTokenUser] = lambda: db_admin
        
        response = client.get("/propositionAjout/getmin")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert any(p['description'] == "Proposition test" for p in data)
        app.dependency_overrides.clear()

    #  TESTS GET BY ID 
    def test_get_proposition_by_id_admin(self, client, proposition_test, db_admin, db_public):
        """Admin peut voir le détail d'une proposition"""
        app.dependency_overrides[getTokenUser] = lambda: db_admin

        # Mock get_ajout_by_id pour éviter ST_Transform non supporté en test
        mock_ajout = MagicMock()
        mock_ajout.id = proposition_test.id
        mock_ajout.description = "Proposition test"
        mock_ajout.photo = "images/propAjoutImg/test.jpg"
        mock_ajout.id_utilisateur = db_public.id_utilisateur
        mock_ajout.date_creation = proposition_test.date_creation
        mock_ajout.latitude = 48.8566
        mock_ajout.longitude = 2.3522

        with patch("app.routers.propAjout.get_ajout_by_id", return_value=mock_ajout), \
             patch("app.routers.propAjout.dechiffrerTelEtMail", return_value="pub@test.com"):
            response = client.get(f"/propositionAjout/id/{proposition_test.id}")

        assert response.status_code == 200
        data = response.json()
        assert data['description'] == "Proposition test"
        assert 'latitude' in data
        assert 'longitude' in data
        app.dependency_overrides.clear()

    def test_get_proposition_by_id_not_found(self, client, db_admin):
        """Proposition inexistante retourne 404"""
        app.dependency_overrides[getTokenUser] = lambda: db_admin
        
        response = client.get("/propositionAjout/id/99999")
        assert response.status_code == 404
        app.dependency_overrides.clear()


    def test_create_proposition_invalid_user(self, client, db_session):
        """Utilisateur inexistant génère une erreur"""
        temp_user = models.Utilisateur(
            nom="Temp", prenom="User", email="temp@test.com",
            telephone="0600000002", mot_de_passe="h", role=RoleEnum.public
        )
        db_session.add(temp_user)
        db_session.commit()
        db_session.refresh(temp_user)
        
        db_session.delete(temp_user)
        db_session.commit()
        
        payload = {
            "description": "Test invalid user",
            "latitude": "48.8566",
            "longitude": "2.3522"
        }
        file_data = {"photo": ("test.jpg", io.BytesIO(b"fake-image-content"), "image/jpeg")}
        
        fake_user = models.Utilisateur(
            id_utilisateur=99999, nom="Fake", prenom="User",
            email="fake@test.com", telephone="0600000003",
            mot_de_passe="h", role=RoleEnum.public
        )
        app.dependency_overrides[getTokenUser] = lambda: fake_user
        
        response = client.post("/propositionAjout/", data=payload, files=file_data)
        assert response.status_code == 400
        app.dependency_overrides.clear()

    #  TESTS DELETE 
    def test_delete_proposition_admin(self, client, proposition_test, db_admin):
        """Admin peut supprimer une proposition"""
        app.dependency_overrides[getTokenUser] = lambda: db_admin
        
        response = client.delete(f"/propositionAjout/suprimmer/{proposition_test.id}")
        assert response.status_code == 200
        assert "supprimés avec succès" in response.json()["detail"]
        app.dependency_overrides.clear()

    def test_delete_proposition_not_found(self, client, db_admin):
        """Suppression d'une proposition inexistante"""
        app.dependency_overrides[getTokenUser] = lambda: db_admin
        
        response = client.delete("/propositionAjout/suprimmer/99999")
        assert response.status_code == 404
        app.dependency_overrides.clear()

    def test_delete_proposition_forbidden_for_non_admin(self, client, proposition_test, db_public):
        """Non-admin ne peut pas supprimer"""
        app.dependency_overrides[getTokenUser] = lambda: db_public
        
        response = client.delete(f"/propositionAjout/suprimmer/{proposition_test.id}")
        assert response.status_code in [401, 403]
        app.dependency_overrides.clear()

    #  TESTS QUOTA INTEGRATION
    def test_create_proposition_quota_exceeded(self, client, db_public, db_session):
        """Test quota dépassé pour utilisateur public"""
        from app.models import PropAjoutQuota
        quota = PropAjoutQuota(
            id_utilisateur=db_public.id_utilisateur,
            nb_proposition=3
        )
        db_session.add(quota)
        db_session.commit()
        
        payload = {
            "description": "Test quota exceeded",
            "latitude": "48.8566",
            "longitude": "2.3522"
        }
        file_data = {"photo": ("test.jpg", io.BytesIO(b"fake-image-content"), "image/jpeg")}
        
        app.dependency_overrides[getTokenUser] = lambda: db_public
        
        response = client.post("/propositionAjout/", data=payload, files=file_data)
        assert response.status_code == 403
        assert "Limite quotidienne de 3 atteinte" in response.json()["detail"]
        app.dependency_overrides.clear()

    #  TESTS BAN INTEGRATION
    def test_create_proposition_user_banned(self, client, db_public, db_session):
        """Utilisateur banni ne peut pas créer de proposition"""
        from app.models import BanUtilisateur
        from datetime import datetime, timedelta
        
        ban = BanUtilisateur(
            id_utilisateur=db_public.id_utilisateur,
            date_fin=datetime.now() + timedelta(days=7),
            raison="Test ban"
        )
        db_session.add(ban)
        db_session.commit()
        
        payload = {
            "description": "Test banned user",
            "latitude": "48.8566",
            "longitude": "2.3522"
        }
        file_data = {"photo": ("test.jpg", io.BytesIO(b"fake-image-content"), "image/jpeg")}
        
        app.dependency_overrides[getTokenUser] = lambda: db_public
        
        response = client.post("/propositionAjout/", data=payload, files=file_data)
        assert response.status_code == 403
        assert "banni" in response.json()["detail"]
        app.dependency_overrides.clear()