import pytest
import uuid
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from geoalchemy2.elements import WKTElement 
from app import models
from app.schemas import PointEauCreate
from app.main import app

client = TestClient(app)


@pytest.fixture(scope="function")
def point_eau_initial(db_session: Session):
    """Fixture pour créer un PointEau de base pour les tests GET/DELETE/UPDATE."""
    unique_pei = int(str(uuid.uuid4().int)[:6]) 

    point = models.PointEau(
        numero_pei=unique_pei,
        nom="Point Initial",
        statut="PUBLIC",
        type_nature="PI100",
        insee5="01000",
        press_deb=3.0,
        debit_1_bar=100.0,
        vol_eau_mi=5000.0,
        accessibilite="C",
        disponibilite="DI",
        carto_ref=12345678,
        utilisateur="INIT_TEST",
        geom=WKTElement("POINT (800000 6600000)", srid=2154) 
    )
    db_session.add(point)
    db_session.commit()
    db_session.refresh(point) 

    assert point.id is not None
    yield point
    


class TestPointEauCRUD:

    def test_create_point_eau_success(self):
        payload = PointEauCreate(
            numero_pei=int(str(uuid.uuid4().int)[:6]),
            nom="Nouveau Point",
            statut="PRIVE",
            type_nature="BI",
            insee5="99999",
            press_deb=4.5,
            debit_1_bar=150.0,
            vol_eau_mi=8000.0,
            accessibilite="NC",
            disponibilite="IN",
            carto_ref=98765432,
            utilisateur="CREATION_TEST",
            latitude=47.6583,
            longitude=-2.7562
        )
        response = client.post("/points-eau/", json=payload.model_dump(mode='json'))
        assert response.status_code == 200
        data = response.json()
        assert data['nom'] == "Nouveau Point"
        assert data['statut'] == "PRIVE"
        
        # NETTOYAGE : supprime le point créé
        client.delete(f"/points-eau/{data['numero_pei']}")

    def test_create_point_eau_duplicate_pei(self, db_session: Session):
        pei = int(str(uuid.uuid4().int)[:6])
        payload1 = PointEauCreate(
            numero_pei=pei,
            nom="Point Original",
            statut="PUBLIC",
            type_nature="BI",
            latitude=47.0,
            longitude=-2.0
        )
        
        # Crée le premier point
        response1 = client.post("/points-eau/", json=payload1.model_dump(mode='json'))
        assert response1.status_code == 200
        
        try:
            # Tente de créer un doublon
            payload2 = PointEauCreate(
                numero_pei=pei,  # DUPLICATA
                nom="Point Dupliqué Tentative",
                statut="PUBLIC",
                type_nature="BI",
                latitude=47.1,
                longitude=-2.1
            )
            response2 = client.post("/points-eau/", json=payload2.model_dump(mode='json'))
            
            # Si on arrive ici, l'API retourne une réponse HTTP
            assert response2.status_code == 500
            data = response2.json()
            assert "numero_pei" in data['detail']
            assert "existe déjà" in data['detail']
            
        except ValueError as e:
            # Si l'API lève une exception directement (comportement actuel)
            assert "existe déjà" in str(e)
        
        finally:
            # NETTOYAGE : supprime le point créé
            client.delete(f"/points-eau/{pei}")


    def test_list_points_empty(self, db_session: Session):
        response = client.get("/points-eau/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_list_points_with_data(self, point_eau_initial):
        response = client.get("/points-eau/")
        assert response.status_code == 200
        data = response.json()
        found = any(p['numero_pei'] == point_eau_initial.numero_pei for p in data)
        assert found
        assert len(data) >= 1

    def test_get_point_by_id_success(self, point_eau_initial):
        response = client.get(f"/points-eau/{point_eau_initial.numero_pei}")
        
        assert response.status_code == 200
        data = response.json()
        assert data['numero_pei'] == point_eau_initial.numero_pei
        assert data['nom'] == "Point Initial"

    def test_get_point_by_id_not_found(self):
        response = client.get("/points-eau/99999999")
        assert response.status_code == 404
        assert response.json()['detail'] == 'Not Found'

    def test_delete_point_success(self, point_eau_initial):
        response = client.delete(f"/points-eau/{point_eau_initial.numero_pei}")
        
        assert response.status_code == 200
        assert "supprimé" in response.json()['detail']
        response_get = client.get(f"/points-eau/{point_eau_initial.numero_pei}")
        assert response_get.status_code == 404

    def test_delete_point_not_found(self):
        response = client.delete("/points-eau/99999999")
        assert response.status_code == 404
        assert response.json()['detail'] == 'Not Found'

    @pytest.mark.skip(reason="Route UPDATE non fournie, à implémenter si la route est ajoutée")
    def test_update_point_eau_success(self, point_eau_initial):
        pass