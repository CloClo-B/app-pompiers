import pytest
import uuid
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from geoalchemy2.elements import WKTElement 
from app import models
from app.main import app
from app.token_jwt import getTokenUser 

client = TestClient(app)

class TestPointEauCRUD:

    # ================= FIXTURES DE SÉCURITÉ =================
    
    @pytest.fixture(autouse=True)
    def mock_auth(self):
        """
        Simule un utilisateur admin pour TOUS les tests de cette classe.
        Indispensable pour éviter les erreurs 401.
        """
        user_mock = models.Utilisateur(
            id_utilisateur=1,
            nom="Admin",
            prenom="Test",
            email="admin@test.com",
            telephone="0601020304",
            role=models.RoleEnum.admin
        )
        app.dependency_overrides[getTokenUser] = lambda: user_mock
        yield
        app.dependency_overrides.clear()

    # ================= FIXTURES DE DONNÉES =================

    @pytest.fixture
    def point_eau_initial(self, db_session: Session):
        """Crée un PointEau en base via SQLAlchemy."""
        unique_pei = int(str(uuid.uuid4().int)[:8]) 

        point = models.PointEau(
            numero_pei=unique_pei,
            nom="Point Initial",
            statut="PUBLIC",         
            type_nature="PI100",      
            insee5="01000",
            accessibilite="C",       
            disponibilite="DI",     
            geom=WKTElement("POINT (800000 6600000)", srid=2154) 
        )
        db_session.add(point)
        db_session.commit()
        db_session.refresh(point) 

        yield point
        
        # Nettoyage
        db_session.delete(point)
        db_session.commit()

    # ================= TESTS =================

    def test_create_point_eau_success(self, db_session: Session):
        """Teste la création via l'API (POST)."""
        unique_pei = int(str(uuid.uuid4().int)[:8])
        payload = {
            "numero_pei": unique_pei,
            "nom": "Nouveau Point Test",
            "statut": "PRIVE",      
            "type_nature": "BI",     
            "insee5": "99999",
            "latitude": 47.6583,
            "longitude": -2.7562,
            "accessibilite": "NC",
            "disponibilite": "DI",
            "date_crea": "2024-01-01T12:00:00" 
        }
        
        response = client.post("/points-eau/", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data['numero_pei'] == unique_pei
        assert data['statut'] == "PRIVE"

    def test_create_point_eau_duplicate_pei(self, point_eau_initial):
        """Vérifie le rejet d'un numero_pei déjà existant."""
        payload = {
            "numero_pei": point_eau_initial.numero_pei,
            "nom": "Doublon",
            "statut": "PUBLIC",
            "type_nature": "BI",
            "latitude": 48.0,
            "longitude": -2.0
        }
        
        response = client.post("/points-eau/", json=payload)
        assert response.status_code in [400, 409, 500]

    def test_get_point_by_pei_success(self, point_eau_initial):
        """Récupération par le numéro PEI."""
        response = client.get(f"/points-eau/{point_eau_initial.numero_pei}")
        assert response.status_code == 200
        assert response.json()['numero_pei'] == point_eau_initial.numero_pei

    def test_list_points_eau(self, point_eau_initial):
        """Vérifie la présence du point dans la liste globale."""
        response = client.get("/points-eau/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert any(p['numero_pei'] == point_eau_initial.numero_pei for p in data)

    def test_delete_point_eau_success(self, db_session: Session):
        """Suppression d'un point existant."""
        pei = int(str(uuid.uuid4().int)[:8])
        p = models.PointEau(
            numero_pei=pei, 
            statut="PUBLIC", 
            type_nature="BI", 
            geom=WKTElement("POINT(0 0)", srid=2154)
        )
        db_session.add(p)
        db_session.commit()

        response = client.delete(f"/points-eau/{pei}")
        assert response.status_code == 200
        check = client.get(f"/points-eau/{pei}")
        assert check.status_code == 404