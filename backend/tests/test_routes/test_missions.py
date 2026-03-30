import pytest
import random
from fastapi.testclient import TestClient
from geoalchemy2.elements import WKTElement

# Imports absolus
from app import models
from app.main import app
from app.routers.missions import get_db
from app.token_jwt import getTokenUser
from app.models import RoleEnum

class TestMissionsRouter:
    """Tests pour le router Missions """

    # ============= FIXTURE CLIENT =============
    @pytest.fixture
    def client(self, db_session):
        def override_get_db():
            yield db_session
        app.dependency_overrides[get_db] = override_get_db
        with TestClient(app) as test_client:
            yield test_client
        app.dependency_overrides.clear()

    # ============= FIXTURES UTILISATEURS =============
    @pytest.fixture
    def db_admin(self, db_session):
        user = models.Utilisateur(
            nom="Admin", prenom="Test", email=f"adm{random.randint(1,999)}@test.com",
            telephone=f"06{random.randint(10000000, 99999999)}", 
            mot_de_passe="h", role=RoleEnum.admin
        )
        db_session.add(user)
        db_session.commit()
        return user

    @pytest.fixture
    def db_pompier(self, db_session):
        user = models.Utilisateur(
            nom="Pompier", prenom="Jean", email=f"pom{random.randint(1,999)}@test.com",
            telephone=f"06{random.randint(10000000, 99999999)}", 
            mot_de_passe="h", role=RoleEnum.pompier
        )
        db_session.add(user)
        db_session.commit()
        return user

    # ============= FIXTURE POINT EAU =============
    @pytest.fixture
    def point_eau_test(self, db_session, db_admin):
        numero_pei = random.randint(100000, 999999)
        point = models.PointEau(
            numero_pei=numero_pei,
            nom="Borne Test",
            statut="PUBLIC",
            type_nature="BI100",
            insee5="56001",
            accessibilite="C",
            disponibilite="DI",
            carto_ref=1,
            press_deb=5.5,
            debit_1_bar=60.0,
            vol_eau_mi=120.0,
            utilisateur=db_admin.id_utilisateur,
            geom=WKTElement('POINT(200000 6800000)', srid=2154)
        )
        db_session.add(point)
        db_session.commit()
        return point

    # ============= FIXTURE MISSION =============
    @pytest.fixture
    def mission_test(self, db_session, db_pompier, point_eau_test):
        mission = models.Mission(
            nom_mission="Mission test",
            id_point=point_eau_test.numero_pei, 
            id_utilisateur=db_pompier.id_utilisateur,
            statut="EN COURS",
            commentaire="Test initial"
        )
        db_session.add(mission)
        db_session.commit()
        return mission

    # ============= TESTS GET =================
    def test_get_all_missions(self, client, mission_test, db_pompier):
        app.dependency_overrides[getTokenUser] = lambda: db_pompier
        response = client.get("/missions/")
        assert response.status_code == 200
        assert len(response.json()) >= 1
        app.dependency_overrides.clear()

    # ============= TEST CREATE =================
    def test_create_mission_success(self, client, db_admin, db_pompier, point_eau_test):
        app.dependency_overrides[getTokenUser] = lambda: db_admin
        payload = {
            "nom_mission": "Verification Borne",
            "id_point": point_eau_test.numero_pei,
            "id_utilisateur": db_pompier.id_utilisateur,
            "commentaire": "A vérifier d'urgence",
            "itineraire": None
        }
        response = client.post("/missions/", json=payload)
        assert response.status_code == 200
        app.dependency_overrides.clear()

    # ============= TEST UPDATE =================
    def test_update_mission_success(self, client, mission_test, db_admin):
        app.dependency_overrides[getTokenUser] = lambda: db_admin
        
        payload = {
            "nom_mission": "Mission modifiée",
            "id_point": mission_test.id_point,
            "id_utilisateur": mission_test.id_utilisateur,
            "statut": "TERMINER",  
            "commentaire": "Terminé par le test",
            "itineraire": None,
            "date_fin": None
        }
        response = client.put(f"/missions/update/{mission_test.id_mission}", json=payload)
        if response.status_code == 422:
            print(f"\nERREUR VALDIATION : {response.json()}")
            
        assert response.status_code == 200
        assert response.json()['statut'] == "TERMINER"
        app.dependency_overrides.clear()

    # ============= TEST DELETE =================
    def test_delete_mission_success(self, client, mission_test, db_admin):
        app.dependency_overrides[getTokenUser] = lambda: db_admin
        response = client.delete(f"/missions/supprimer/{mission_test.id_mission}")
        assert response.status_code == 200
        app.dependency_overrides.clear()