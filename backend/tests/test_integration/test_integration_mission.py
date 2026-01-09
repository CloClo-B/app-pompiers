import pytest
import uuid
from app import models
from app.schemas import MissionCreate 
from app.routers import missions as mission_router  
from sqlalchemy.exc import IntegrityError

class TestMissionIntegration:

    @pytest.fixture
    def utilisateur(self, db_session):
        """Crée un utilisateur de test."""
        user = models.Utilisateur(
            nom="Dupont",
            prenom="Jean",
            email=f"jean.{uuid.uuid4().hex[:6]}@test.com", 
            telephone=f"0602{str(uuid.uuid4().int)[:6]}",
            mot_de_passe="haché_par_defaut",
            role=models.RoleEnum.pompier
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

    @pytest.fixture
    def point_eau(self, db_session):
        """Crée un point d'eau de test (PEI)."""
        unique_pei = int(str(uuid.uuid4().int)[:8]) 
        point = models.PointEau(
            numero_pei=unique_pei,
            nom="Point Test",
            statut="PUBLIC",
            type_nature="BI",
            insee5="12345",
            accessibilite="C", 
            disponibilite="DI"
        )
        db_session.add(point)
        db_session.commit()
        db_session.refresh(point)
        return point
    
    @pytest.fixture
    def mission_base(self, db_session, utilisateur, point_eau):
        payload = MissionCreate(
            nom_mission="Mission Base",
            id_point=point_eau.numero_pei,
            id_utilisateur=utilisateur.id_utilisateur,
            commentaire="Mission de test",
            itineraire=None
        )
        mission = mission_router.create_mission(db_session, payload.model_dump()) 
        return mission

    # ======== TESTS DE CRÉATION ========

    def test_creer_mission_success(self, db_session, utilisateur, point_eau):
        payload = MissionCreate(
            nom_mission="Vérification Annuelle",
            id_point=point_eau.numero_pei,
            id_utilisateur=utilisateur.id_utilisateur,
            commentaire="RAS",
            itineraire=None
        )
        mission = mission_router.create_mission(db_session, payload.model_dump())
        assert mission.id_mission is not None

    def test_mission_point_inexistant_fails(self, db_session, utilisateur):
        """Vérifie que le DAO lève une ValueError si le point n'existe pas."""
        payload = MissionCreate(
            nom_mission="Mission Fantôme",
            id_point=99999999, 
            id_utilisateur=utilisateur.id_utilisateur,
            commentaire=None,
            itineraire=None
        )
        with pytest.raises(ValueError) as excinfo:
            mission_router.create_mission(db_session, payload.model_dump())
        
        assert "L'id du point est invalide" in str(excinfo.value)

    # ======== TESTS DE RÉCUPÉRATION ========

    def test_get_all_missions(self, db_session, utilisateur, point_eau):
        """Vérifie la récupération de la liste des missions."""
        p = MissionCreate(
            nom_mission="Mission Liste",
            id_point=point_eau.numero_pei,
            id_utilisateur=utilisateur.id_utilisateur,
            commentaire=None,
            itineraire=None
        )
        mission_router.create_mission(db_session, p.model_dump())
        missions = mission_router.list_missions(db_session)
        
        assert len(missions) >= 1
        noms = [m["nom_mission"] for m in missions] 
        assert "Mission Liste" in noms