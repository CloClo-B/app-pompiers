import pytest
from fastapi.testclient import TestClient
from app import models
from app.routers.signaler import get_db
import random
from geoalchemy2.elements import WKTElement
from datetime import datetime

class TestSignalerRouter:
    """Tests pour le Router Signaler"""
    
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
    def signalement_test(self, db_session):
        """Crée point d'eau ET signalement pour les tests GET"""
        numero_pei = random.randint(100000, 999999)
        point = models.PointEau(
            numero_pei=numero_pei,
            nom="Point test",
            statut="PUBLIC",
            type_nature="BI",
            geom=WKTElement('POINT(200000 6800000)', srid=2154)
        )
        db_session.add(point)
        db_session.commit()
        
        signalement = models.Signaler(
            id_point=numero_pei,
            probleme="Fuite d'eau",
            photo=None
        )
        db_session.add(signalement)
        db_session.commit()
        db_session.refresh(signalement)
        return signalement
    
    # ============= TESTS GET ALL =================
    def test_get_all_signalements_empty(self, client):
        """GET / doit retourner une liste vide si aucun signalement"""
        response = client.get("/signaler/")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_all_signalements_with_data(self, client, signalement_test):
        """GET / doit retourner tous les signalements"""
        response = client.get("/signaler/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]['probleme'] == signalement_test.probleme
    
    # ============= TESTS CREATE =================
    def test_create_signalement_success(self, client, db_session):
        """POST / doit créer un signalement valide"""
        numero_pei = random.randint(100000, 999999)
        point = models.PointEau(
            numero_pei=numero_pei,
            nom="Point",
            statut="PUBLIC",
            type_nature="BI",
            geom=WKTElement('POINT(200000 6800000)', srid=2154)
        )
        db_session.add(point)
        db_session.commit()
        
        payload = {
            "id_point": numero_pei,
            "probleme": "Bouche incendie endommagée",
            "photo": None
        }
        
        response = client.post("/signaler/", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data['probleme'] == payload['probleme']
        assert data['id_point'] == payload['id_point']
    
    def test_create_signalement_missing_required_field(self, client, db_session):
        """POST / sans champ obligatoire doit échouer"""
        numero_pei = random.randint(100000, 999999)
        point = models.PointEau(
            numero_pei=numero_pei,
            nom="Point",
            statut="PUBLIC",
            type_nature="BI",
            geom=WKTElement('POINT(200000 6800000)', srid=2154)
        )
        db_session.add(point)
        db_session.commit()
        
        payload = {"id_point": numero_pei} 
        response = client.post("/signaler/", json=payload)
        assert response.status_code == 422
    
    def test_create_signalement_with_photo(self, client, db_session):
        """POST / avec photo doit réussir"""
        numero_pei = random.randint(100000, 999999)
        point = models.PointEau(
            numero_pei=numero_pei,
            nom="Point",
            statut="PUBLIC",
            type_nature="BI",
            geom=WKTElement('POINT(200000 6800000)', srid=2154)
        )
        db_session.add(point)
        db_session.commit()
        
        payload = {
            "id_point": numero_pei,
            "probleme": "Problème",
            "photo": "/uploads/photo123.jpg"
        }
        
        response = client.post("/signaler/", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data['photo'] == "/uploads/photo123.jpg"
    
    # ============= TESTS INTEGRATION =================
    def test_create_and_retrieve_signalement(self, client, db_session):
        """Cycle complet : créer puis récupérer"""
        numero_pei = random.randint(100000, 999999)
        point = models.PointEau(
            numero_pei=numero_pei,
            nom="Point",
            statut="PUBLIC",
            type_nature="BI",
            geom=WKTElement('POINT(200000 6800000)', srid=2154)
        )
        db_session.add(point)
        db_session.commit()
        
        payload = {
            "id_point": numero_pei,
            "probleme": "Test intégration",
            "photo": None
        }
        
        create_response = client.post("/signaler/", json=payload)
        assert create_response.status_code == 200
        get_response = client.get("/signaler/")
        assert get_response.status_code == 200
        data = get_response.json()
        assert len(data) == 1
        assert data[0]['probleme'] == payload['probleme']
