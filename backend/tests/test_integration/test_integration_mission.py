import pytest
import uuid
from app import models
from app.schemas import MissionCreate 
from app.routers import missions as mission_router  
from sqlalchemy.exc import IntegrityError

class TestMissionIntegration:

    @pytest.fixture
    def utilisateur(self, db_session):
        user = models.Utilisateur(
            nom="Dupont",
            prenom="Jean",
            email=f"jean.{uuid.uuid4()}@test.com", 
            telephone=f"0602{str(uuid.uuid4().int)[:6]}",
            mot_de_passe="pass",
            role=models.RoleEnum.pompier
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

    @pytest.fixture
    def point_eau(self, db_session):
        unique_pei = int(str(uuid.uuid4().int)[:6]) 
        
        point = models.PointEau(
            numero_pei=unique_pei,
            nom="Point Test",
            statut="PUBLIC",
            type_nature="BI",
            insee5="12345",
            press_deb=3.5,
            debit_1_bar=120,
            vol_eau_mi=10000,
            accessibilite="C",
            disponibilite="DI",
            carto_ref=17394051,
            utilisateur="TEST",
            geom=None
        )
        db_session.add(point)
        db_session.commit()
        db_session.refresh(point)
        return point

    @pytest.fixture
    def mission_base(self, db_session, utilisateur, point_eau):
        payload_dict = {
            "nom_mission": "Mission Base",
            "id_point": point_eau.id,
            "id_utilisateur": utilisateur.id_utilisateur,
            "commentaire": "Mission de test",
            "itineraire": None
        }
        payload = MissionCreate(**payload_dict)
        mission = mission_router.create_mission(payload, db_session)
        return mission

    # ======== CAS NORMAL ========
    def test_creer_mission_normal(self, db_session, utilisateur, point_eau):
        payload_dict = {
            "nom_mission": "Mission Normale",
            "id_point": point_eau.id,
            "id_utilisateur": utilisateur.id_utilisateur,
            "commentaire": "Test normal",
            "itineraire": None
        }
        payload = MissionCreate(**payload_dict) 
        
        mission = mission_router.create_mission(payload, db_session)
        
        assert mission.id_mission is not None
        assert mission.nom_mission == "Mission Normale"
        assert mission.id_point == point_eau.id
        assert mission.id_utilisateur == utilisateur.id_utilisateur

    # ======== CAS LIMITE ========
    def test_mission_commentaire_none(self, db_session, utilisateur, point_eau):
        payload_dict = {
            "nom_mission": "Mission Sans Commentaire",
            "id_point": point_eau.id,
            "id_utilisateur": utilisateur.id_utilisateur,
            "commentaire": None,
            "itineraire": None
        }
        payload = MissionCreate(**payload_dict) 
        
        mission = mission_router.create_mission(payload, db_session)
        
        assert mission.commentaire is None

    # ======== CAS D'ERREUR (Vérifie les contraintes de clé étrangère) ========
    def test_mission_utilisateur_inexistant(self, db_session, point_eau):
        payload_dict = {
            "nom_mission": "Mission Erreur",
            "id_point": point_eau.id,
            "id_utilisateur": 99999,
            "commentaire": "Erreur attendue",
            "itineraire": None
        }
        # CORRECTION 2: Convertir le dict en objet Pydantic
        payload = MissionCreate(**payload_dict) 

        with pytest.raises(IntegrityError):
            mission_router.create_mission(payload, db_session)
            db_session.commit() 

    def test_mission_point_inexistant(self, db_session, utilisateur):
        payload_dict = {
            "nom_mission": "Mission Erreur",
            "id_point": 99999,
            "id_utilisateur": utilisateur.id_utilisateur,
            "commentaire": "Erreur attendue",
            "itineraire": None
        }
        payload = MissionCreate(**payload_dict) 

        with pytest.raises(IntegrityError):
            mission_router.create_mission(payload, db_session)
            db_session.commit() 

    # ======== CAS GET_ALL ========
    def test_get_all_missions(self, db_session, utilisateur, point_eau):
        payload1 = MissionCreate(
            nom_mission="Mission1",
            id_point=point_eau.id,
            id_utilisateur=utilisateur.id_utilisateur,
            commentaire="T1",
            itineraire=None
        )
        mission_router.create_mission(payload1, db_session)

        payload2 = MissionCreate(
            nom_mission="Mission2",
            id_point=point_eau.id,
            id_utilisateur=utilisateur.id_utilisateur,
            commentaire="T2",
            itineraire=None
        )
        mission_router.create_mission(payload2, db_session)
        
        missions = mission_router.list_missions(db_session)
        
        noms = [m.nom_mission for m in missions]
        assert "Mission1" in noms
        assert "Mission2" in noms