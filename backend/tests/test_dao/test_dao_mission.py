import pytest
from datetime import date, timedelta
from app.DAO.DAOMissions import (
    get_all_mission,
    get_mission_by_id,
    get_mission_by_date,
    create_mission,
    update_mission_by_id,
    delete_mission_by_id
)
from app import models
from pyproj import Transformer
from geoalchemy2.elements import WKTElement


@pytest.fixture
def utilisateur_test(db_session):
    user = models.Utilisateur(
        nom="Dupont",
        prenom="Jean",
        email="jean.dupont@test.com",
        telephone="0612345678",
        mot_de_passe="hashed_password",
        role="pompier"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def point_test(db_session):
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:2154")
    x, y = transformer.transform(48.8566, 2.3522)
    wkt = WKTElement(f"POINT({x} {y})", srid=2154)
    
    point = models.PointEau(
        numero_pei=12345,
        statut="PUBLIC",
        type_nature="BI",
        geom=wkt
    )
    db_session.add(point)
    db_session.commit()
    db_session.refresh(point)
    return point


@pytest.fixture
def mission_test(db_session, utilisateur_test, point_test):
    mission = models.Mission(
        nom_mission="Mission Test",
        id_point=point_test.numero_pei,
        id_utilisateur=utilisateur_test.id_utilisateur,
        statut="EN COURS"
    )
    db_session.add(mission)
    db_session.commit()
    db_session.refresh(mission)
    return mission


# ============= TESTS UNITAIRES =============
class TestMissionDAOUnitaire:
    """Tests unitaires - Chaque fonction testée individuellement"""
    
    def test_get_all_mission_empty(self, db_session):
        missions = get_all_mission(db_session)
        assert missions == []

    def test_get_all_mission_returns_dict(self, db_session, mission_test):
        missions = get_all_mission(db_session)
        assert isinstance(missions[0], dict)
        assert "_sa_instance_state" not in missions[0]

    def test_get_mission_by_id_exists(self, db_session, mission_test):
        m = get_mission_by_id(db_session, mission_test.id_mission)
        assert m is not None
        assert m.id_mission == mission_test.id_mission
    
    def test_get_mission_by_id_not_exists(self, db_session):
        m = get_mission_by_id(db_session, 99999)
        assert m is None

    def test_get_mission_by_date_today(self, db_session, mission_test):
        today = date.today()
        missions = get_mission_by_date(db_session, today)
        assert len(missions) >= 1

    def test_create_mission_returns_object(self, db_session, utilisateur_test, point_test):
        data = {
            "nom_mission": "Test Create",
            "id_point": point_test.numero_pei,
            "id_utilisateur": utilisateur_test.id_utilisateur
        }
        m = create_mission(db_session, data)
        assert m.id_mission is not None

    def test_update_mission_modifies_fields(self, db_session, mission_test):
        data = {"statut": "TERMINER"}
        updated = update_mission_by_id(db_session, mission_test.id_mission, data)
        assert updated.statut == "TERMINER"

    def test_delete_mission_returns_boolean(self, db_session, mission_test):
        result = delete_mission_by_id(db_session, mission_test.id_mission)
        assert result is True


# ============= TESTS FONCTIONNELS =============
class TestMissionDAOFonctionnel:
    """Tests fonctionnels - Scénarios d'utilisation métier"""
    
    def test_create_mission_complete(self, db_session, utilisateur_test, point_test):
        data = {
            "nom_mission": "Mission Complete",
            "id_point": point_test.numero_pei,
            "id_utilisateur": utilisateur_test.id_utilisateur,
            "commentaire": "Test fonctionnel",
            "itineraire": "A -> B -> C"
        }
        m = create_mission(db_session, data)
        
        assert m.nom_mission == "Mission Complete"
        assert m.commentaire == "Test fonctionnel"
        assert m.statut == "EN COURS"

    def test_update_mission_multiple_fields(self, db_session, mission_test):
        data = {
            "statut": "TERMINER",
            "commentaire": "Mission terminee"
        }
        updated = update_mission_by_id(db_session, mission_test.id_mission, data)
        
        assert updated.statut == "TERMINER"
        assert updated.commentaire == "Mission terminee"

    def test_get_mission_by_date_filters_correctly(self, db_session, mission_test):
        today = date.today()
        yesterday = today - timedelta(days=1)
        
        missions_today = get_mission_by_date(db_session, today)
        missions_yesterday = get_mission_by_date(db_session, yesterday)
        
        assert len(missions_today) >= 1
        assert len(missions_yesterday) == 0


# ============= TESTS INTÉGRATION =============
class TestMissionDAOIntegration:
    """Tests d'intégration - Interaction entre plusieurs fonctions"""
    
    def test_crud_complete_lifecycle(self, db_session, utilisateur_test, point_test):
        data = {
            "nom_mission": "Mission CRUD",
            "id_point": point_test.numero_pei,
            "id_utilisateur": utilisateur_test.id_utilisateur
        }
        created = create_mission(db_session, data)
        
        found = get_mission_by_id(db_session, created.id_mission)
        assert found.nom_mission == "Mission CRUD"
        
        updated = update_mission_by_id(db_session, created.id_mission, {"statut": "TERMINER"})
        assert updated.statut == "TERMINER"
    
        deleted = delete_mission_by_id(db_session, created.id_mission)
        assert deleted is True
        assert get_mission_by_id(db_session, created.id_mission) is None

    def test_mission_with_related_entities(self, db_session, utilisateur_test, point_test):
        data = {
            "nom_mission": "Mission Relation",
            "id_point": point_test.numero_pei,
            "id_utilisateur": utilisateur_test.id_utilisateur
        }
        mission = create_mission(db_session, data)
        
        assert mission.id_point == point_test.numero_pei
        assert mission.id_utilisateur == utilisateur_test.id_utilisateur


# ============= TESTS SÉCURITÉ =============
class TestMissionDAOSecurity:
    """Tests de sécurité - Contraintes et validations"""
    
    def test_create_mission_invalid_point(self, db_session, utilisateur_test):
        data = {
            "nom_mission": "Mission Invalide",
            "id_point": 99999,
            "id_utilisateur": utilisateur_test.id_utilisateur
        }
        
        with pytest.raises(ValueError, match="id du point est invalide"):
            create_mission(db_session, data)

    def test_create_mission_invalid_user(self, db_session, point_test):
        data = {
            "nom_mission": "Mission Invalide",
            "id_point": point_test.numero_pei,
            "id_utilisateur": 99999
        }
        
        with pytest.raises(ValueError, match="Utilisateur incorrect"):
            create_mission(db_session, data)

    def test_update_mission_not_exists(self, db_session):
        with pytest.raises(ValueError, match="Id mission incorrect"):
            update_mission_by_id(db_session, 99999, {"statut": "TERMINER"})

    def test_update_mission_protected_fields(self, db_session, mission_test):
        original_id = mission_test.id_mission
        original_date = mission_test.date_creation
        
        data = {
            "id_mission": 88888,
            "date_creation": "2000-01-01",
            "statut": "TERMINER"
        }
        updated = update_mission_by_id(db_session, mission_test.id_mission, data)
        
        assert updated.id_mission == original_id
        assert updated.date_creation == original_date

    def test_delete_mission_not_exists(self, db_session):
        result = delete_mission_by_id(db_session, 99999)
        assert result is False