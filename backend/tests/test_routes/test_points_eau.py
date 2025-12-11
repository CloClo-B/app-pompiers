import pytest
from fastapi.testclient import TestClient
from app import models
from app.routers.points_eau import get_db
import random
from datetime import datetime

class TestPointsEauRouter:
    """Tests pour le Router Points d'eau"""
    
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
    
    # ============= FIXTURE CLEANUP =============
    @pytest.fixture(autouse=True)
    def cleanup(self, db_session):
        """Nettoie la table points_eau entre chaque test"""
        yield
        # ✅ Rollback si la session est en erreur avant de nettoyer
        try:
            db_session.query(models.PointEau).delete()
            db_session.commit()
        except Exception:
            db_session.rollback()
            db_session.query(models.PointEau).delete()
            db_session.commit()
    
    # ============= FIXTURES =============
    @pytest.fixture
    def point_eau_test(self, db_session):
        """Crée un point d'eau valide pour les tests"""
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
        """Payload valide pour créer un point d'eau"""
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
            "longitude": -3.0,
            "date_crea": datetime.now().isoformat()
        }
    
    # ============= TESTS GET ALL =================
    def test_get_all_points_empty(self, client):
        """GET / doit retourner une liste vide si aucun point"""
        response = client.get("/points-eau/")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_all_points_with_data(self, client, point_eau_test):
        """GET / doit retourner tous les points d'eau"""
        response = client.get("/points-eau/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]['numero_pei'] == point_eau_test.numero_pei
        assert data[0]['statut'] == point_eau_test.statut
    
    # ============= TESTS CREATE =================
    def test_create_point_success(self, client, valid_point_payload):
        """POST / doit créer un point d'eau valide"""
        response = client.post("/points-eau/", json=valid_point_payload)
        assert response.status_code == 200
        data = response.json()
        assert data['numero_pei'] == valid_point_payload['numero_pei']
        assert data['statut'] == valid_point_payload['statut']
        assert data['type_nature'] == valid_point_payload['type_nature']
        assert 'id' in data
        assert 'latitude' in data
        assert 'longitude' in data
    
    def test_create_point_missing_required_field(self, client, valid_point_payload):
        """POST / sans champ obligatoire doit échouer"""
        del valid_point_payload['numero_pei']
        response = client.post("/points-eau/", json=valid_point_payload)
        assert response.status_code == 422
    
    # ============= TESTS INTEGRATION =================
    def test_create_and_retrieve_point(self, client, valid_point_payload):
        """Cycle complet : créer puis récupérer"""
        # Créer
        create_response = client.post("/points-eau/", json=valid_point_payload)
        assert create_response.status_code == 200
        
        # Récupérer tous
        get_response = client.get("/points-eau/")
        assert get_response.status_code == 200
        data = get_response.json()
        assert len(data) == 1
        assert data[0]['numero_pei'] == valid_point_payload['numero_pei']


# ==================== EXÉCUTION ====================
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])