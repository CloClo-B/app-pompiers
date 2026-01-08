import pytest
import random
from datetime import datetime
from fastapi.testclient import TestClient
from app import models
from app.main import app
from app.routers.points_eau import get_db
from app.token_jwt import getTokenUser
from app.models import RoleEnum

class TestPointsEauRouter:
    """Tests pour le Router Points d'eau (Version stable)"""
    
    # ============= FIXTURE CLIENT =============
    @pytest.fixture
    def client(self, db_session):
        """Client de test avec injection de la session DB"""
        def override_get_db():
            yield db_session
        
        app.dependency_overrides[get_db] = override_get_db
        with TestClient(app) as test_client:
            yield test_client
        app.dependency_overrides.clear()
    
    # ============= FIXTURES DONNÉES =============
    @pytest.fixture
    def db_admin(self, db_session):
        """Crée un admin en base pour bypasser rolesChecker"""
        admin = models.Utilisateur(
            nom="Admin", prenom="Test", email=f"adm{random.randint(1,999)}@test.com",
            telephone="0600000000", mot_de_passe="h", role=RoleEnum.admin
        )
        db_session.add(admin)
        db_session.commit()
        return admin

    @pytest.fixture
    def point_eau_test(self, db_session):
        """Crée un point d'eau valide via SQLAlchemy (nécessite GeoAlchemy2)"""
        from geoalchemy2.elements import WKTElement
        
        point = models.PointEau(
            numero_pei=random.randint(100000, 999999),
            nom="Point test",
            statut="PUBLIC",
            type_nature="BI",
            insee5="56001",
            press_deb=5.5,
            debit_1_bar=60.0,
            vol_eau_mi=120.0,
            accessibilite="C",
            disponibilite="DI",
            carto_ref=1,
            utilisateur="test_user",
            date_crea=datetime.now(),
            geom=WKTElement('POINT(200000 6800000)', srid=2154)
        )
        db_session.add(point)
        db_session.commit()
        db_session.refresh(point)
        return point
    
    @pytest.fixture
    def valid_point_payload(self):
        """Payload pour le POST / (format JSON Pydantic)"""
        return {
            "numero_pei": random.randint(100000, 999999),
            "nom": "Nouveau point",
            "statut": "PUBLIC",
            "type_nature": "BI100",
            "insee5": "56002",
            "press_deb": 6.0,
            "debit_1_bar": 70.0,
            "vol_eau_mi": 150.0,
            "accessibilite": "C",
            "disponibilite": "DI",
            "carto_ref": 2,
            "utilisateur": "admin",
            "latitude": 48.0,
            "longitude": -3.0
        }
    
    # ============= TESTS GET ALL =================
    def test_get_all_points_with_data(self, client, point_eau_test):
        response = client.get("/points-eau/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]['numero_pei'] == point_eau_test.numero_pei
    
    # ============= TESTS CREATE  =================
    def test_create_point_success(self, client, valid_point_payload, db_admin):
        # On simule la connexion d'un admin
        app.dependency_overrides[getTokenUser] = lambda: db_admin
        
        response = client.post("/points-eau/", json=valid_point_payload)
        assert response.status_code == 200
        data = response.json()
        assert data['numero_pei'] == valid_point_payload['numero_pei']
        assert 'latitude' in data
    
    def test_create_point_forbidden_for_anonymous(self, client, valid_point_payload):
        response = client.post("/points-eau/", json=valid_point_payload)
        assert response.status_code in [401, 403, 422]

    # ============= TESTS GET BY ID =================
    def test_get_point_by_numero_success(self, client, point_eau_test):
        response = client.get(f"/points-eau/{point_eau_test.numero_pei}")
        assert response.status_code == 200
        assert response.json()["numero_pei"] == point_eau_test.numero_pei

    def test_get_point_not_found(self, client):
        response = client.get("/points-eau/9999999")
        assert response.status_code == 404

    # ============= TESTS DELETE =================
    def test_delete_point_as_admin(self, client, point_eau_test, db_admin):
        app.dependency_overrides[getTokenUser] = lambda: db_admin
        
        response = client.delete(f"/points-eau/{point_eau_test.numero_pei}")
        assert response.status_code == 200
        assert "supprimé" in response.json()["detail"].lower()