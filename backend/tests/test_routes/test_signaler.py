import pytest
import random
import io
from fastapi.testclient import TestClient
from geoalchemy2.elements import WKTElement

# Imports absolus
from app import models
from app.main import app
from app.routers.signaler import get_db
from app.token_jwt import getTokenUser
from app.models import RoleEnum

class TestSignalerRouter:
    """Tests pour le Router Signaler"""
    
    @pytest.fixture
    def client(self, db_session):
        def override_get_db():
            yield db_session
        
        app.dependency_overrides[get_db] = override_get_db
        with TestClient(app) as test_client:
            yield test_client
        app.dependency_overrides.clear()

    @pytest.fixture
    def db_user(self, db_session):
        """Crée un utilisateur pompier pour bypasser les rôles"""
        user = models.Utilisateur(
            nom="Test", prenom="Pompier", email=f"p{random.randint(1,999)}@test.com",
            telephone="0600000000", mot_de_passe="h", role=RoleEnum.pompier
        )
        db_session.add(user)
        db_session.commit()
        return user

    @pytest.fixture
    def signalement_test(self, db_session, db_user):
        """Crée un point d'eau et un signalement lié"""
        numero_pei = random.randint(100000, 999999)
        point = models.PointEau(
            numero_pei=numero_pei, nom="Point test", statut="PUBLIC", type_nature="BI",
            geom=WKTElement('POINT(200000 6800000)', srid=2154)
        )
        db_session.add(point)
        db_session.commit()
        
        signalement = models.Signaler(
            id_point=numero_pei, probleme="Fuite", photo="images/test.jpg", 
            id_utilisateur=db_user.id_utilisateur
        )
        db_session.add(signalement)
        db_session.commit()
        return signalement

    # ================= TESTS GET =================
    def test_get_all_signalements(self, client, signalement_test, db_user):
        app.dependency_overrides[getTokenUser] = lambda: db_user
        
        response = client.get("/signaler/")
        assert response.status_code == 200
        assert len(response.json()) >= 1
        app.dependency_overrides.clear()

    # ================= TESTS CREATE (Multipart Form Data) =================
    def test_create_signalement_success(self, client, db_session, db_user):
        numero_pei = random.randint(100000, 999999)
        point = models.PointEau(
            numero_pei=numero_pei, nom="Point", statut="PUBLIC", type_nature="BI",
            geom=WKTElement('POINT(200000 6800000)', srid=2154)
        )
        db_session.add(point)
        db_session.commit()

        payload = {
            "id_point": str(numero_pei),
            "probleme": "Bouche incendie cassée",
            "id_utilisateur": str(db_user.id_utilisateur)
        }
        

        file_data = {"photo": ("test.jpg", io.BytesIO(b"fake-image-content"), "image/jpeg")}

        response = client.post("/signaler/", data=payload, files=file_data)
        
        assert response.status_code == 200
        assert response.json()["id_point"] == numero_pei

    def test_create_signalement_point_not_found(self, client, db_user):
        payload = {
            "id_point": "9999999",
            "probleme": "Inconnu",
            "id_utilisateur": str(db_user.id_utilisateur)
        }
        file_data = {"photo": ("test.jpg", io.BytesIO(b"img"), "image/jpeg")}
        
        response = client.post("/signaler/", data=payload, files=file_data)
        assert response.status_code == 404
        assert "n'a pas été trouvé" in response.json()["detail"]

    # ================= TESTS DELETE =================
    def test_delete_signalement_as_admin(self, client, signalement_test, db_session):
        admin = models.Utilisateur(
            nom="Admin", 
            prenom="System", 
            role=RoleEnum.admin, 
            email=f"adm{random.randint(1,999)}@test.com", 
            telephone="0611223344", 
            mot_de_passe="h"
        )
        db_session.add(admin)
        db_session.commit()
        
        app.dependency_overrides[getTokenUser] = lambda: admin
        
        response = client.delete(f"/signaler/suprimmer/{signalement_test.id_point}")
        assert response.status_code == 200
        app.dependency_overrides.clear()