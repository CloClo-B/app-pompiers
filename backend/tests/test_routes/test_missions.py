import pytest
from fastapi.testclient import TestClient
from app import models
from app.routers.missions import get_db
import random

class TestMissionsRouter:
    """Tests pour le router Missions"""

    # ============= FIXTURE CLIENT =============
    @pytest.fixture
    def client(self, db_session):
        from app.main import app

        def override_get_db():
            yield db_session

        app.dependency_overrides[get_db] = override_get_db
        with TestClient(app) as test_client:
            yield test_client
        app.dependency_overrides.clear()

    # ============= FIXTURE UTILISATEUR =============
    @pytest.fixture
    def utilisateur_test(self, db_session):
        unique_number = random.randint(10000, 99999)
        user = models.Utilisateur(
            nom="Dupont",
            prenom="Jean",
            email=f"jean.dupont{unique_number}@test.com",
            telephone=f"06{random.randint(10000000, 99999999)}",
            mot_de_passe="hashed_password",
            role="pompier"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

    # ============= FIXTURE POINT EAU =============
    @pytest.fixture
    def point_eau_test(self, db_session):
        from geoalchemy2.elements import WKTElement
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
        db_session.refresh(point)
        return point

    # ============= FIXTURE MISSION =============
    @pytest.fixture
    def mission_test(self, db_session, utilisateur_test, point_eau_test):
        mission = models.Mission(
            nom_mission="Mission test",
            id_point=point_eau_test.id,
            id_utilisateur=utilisateur_test.id_utilisateur,
            statut="en_attente",
            commentaire="Test",
            itineraire=None
        )
        db_session.add(mission)
        db_session.commit()
        db_session.refresh(mission)
        return mission

    # ============= TEST GET ALL =================
    def test_get_all_missions_empty(self, client):
        response = client.get("/missions/")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_all_missions_with_data(self, client, mission_test):
        response = client.get("/missions/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]['nom_mission'] == mission_test.nom_mission

    # ============= TEST GET BY ID =================
    def test_get_mission_by_id_success(self, client, mission_test):
        response = client.get(f"/missions/{mission_test.id_mission}")
        assert response.status_code == 200
        data = response.json()
        assert data['id_mission'] == mission_test.id_mission
        assert data['nom_mission'] == mission_test.nom_mission

    def test_get_mission_by_id_not_found(self, client):
        response = client.get("/missions/99999")
        assert response.status_code == 404
        assert "non trouvée" in response.json()['detail']

    # ============= TEST CREATE =================
    def test_create_mission_success(self, client, utilisateur_test, point_eau_test):
        payload = {
            "nom_mission": "Nouvelle mission",
            "id_point": point_eau_test.id,
            "id_utilisateur": utilisateur_test.id_utilisateur,
            "commentaire": "Commentaire test",
            "itineraire": None
        }
        response = client.post("/missions/", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data['nom_mission'] == payload['nom_mission']
        assert data['statut'] == "en_attente"

    def test_create_mission_missing_required_field(self, client, utilisateur_test, point_eau_test):
        payload = {
            "id_point": point_eau_test.id,
            "id_utilisateur": utilisateur_test.id_utilisateur
        }
        response = client.post("/missions/", json=payload)
        assert response.status_code == 422

    # ============= TEST UPDATE =================
    def test_update_mission_success(self, client, mission_test):
        payload = {
            "nom_mission": "Mission modifiée",
            "id_point": mission_test.id_point,
            "id_utilisateur": mission_test.id_utilisateur,
            "commentaire": "Modifié",
            "itineraire": None,
            "statut": "en cours"
        }
        response = client.put(f"/missions/{mission_test.id_mission}", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data['nom_mission'] == "Mission modifiée"
        assert data['commentaire'] == "Modifié"
        assert data['statut'] == "en cours"

    def test_update_mission_not_found(self, client):
        payload = {
            "nom_mission": "Test",
            "id_point": 1,
            "id_utilisateur": 1,
            "commentaire": "Test",
            "itineraire": None,
            "statut": "terminé"
        }
        response = client.put("/missions/99999", json=payload)
        assert response.status_code == 404

    # ============= TEST DELETE =================
    def test_delete_mission_success(self, client, mission_test):
        response = client.delete(f"/missions/{mission_test.id_mission}")
        assert response.status_code == 200
        assert "supprimée" in response.json()['detail']
        get_response = client.get(f"/missions/{mission_test.id_mission}")
        assert get_response.status_code == 404

    def test_delete_mission_not_found(self, client):
        response = client.delete("/missions/99999")
        assert response.status_code == 404

    # ============= TEST FULL CRUD =================
    def test_full_crud_cycle(self, client, utilisateur_test, point_eau_test):
        # CREATE
        payload = {
            "nom_mission": "Mission CRUD",
            "id_point": point_eau_test.id,
            "id_utilisateur": utilisateur_test.id_utilisateur,
            "commentaire": "Initial",
            "itineraire": None
        }
        create_response = client.post("/missions/", json=payload)
        mission_id = create_response.json()['id_mission']

        # READ
        get_response = client.get(f"/missions/{mission_id}")
        assert get_response.status_code == 200

        # UPDATE
        update_payload = {
            "nom_mission": "Mission CRUD Modifiée",
            "id_point": point_eau_test.id,
            "id_utilisateur": utilisateur_test.id_utilisateur,
            "commentaire": "Modifié",
            "itineraire": None,
            "statut": "terminé"
        }
        update_response = client.put(f"/missions/{mission_id}", json=update_payload)
        assert update_response.status_code == 200
        assert update_response.json()['statut'] == "terminé"

        # DELETE
        delete_response = client.delete(f"/missions/{mission_id}")
        assert delete_response.status_code == 200

        get_after_delete = client.get(f"/missions/{mission_id}")
        assert get_after_delete.status_code == 404
