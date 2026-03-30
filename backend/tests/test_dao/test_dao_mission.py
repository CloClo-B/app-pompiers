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
    """Crée un utilisateur de test"""
    user = db_session.query(models.Utilisateur).filter_by(id_utilisateur=1).first()
    return user


@pytest.fixture
def point_test(db_session):
    """Crée un point d'eau de test"""
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:2154")
    x, y = transformer.transform(48.8566, 2.3522)
    wkt = WKTElement(f"POINT({x} {y})", srid=2154)
    
    point = models.PointEau(
        numero_pei=12345,
        statut="PUBLIC",
        type_nature="BI",
        geom=wkt,
        accessibilite="C",
        disponibilite="DI",
        carto_ref=1,
        press_deb=0.0,
        debit_1_bar=0.0,
        vol_eau_mi=0.0,
        utilisateur=1
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
        statut="EN COURS",
        commentaire="Mission de test"
    )
    db_session.add(mission)
    db_session.commit()
    db_session.refresh(mission)
    return mission


class TestGetAllMission:
    """Tests pour la récupération de toutes les missions"""
    
    def test_get_all_mission_empty(self, db_session):
        missions = get_all_mission(db_session)
        assert missions == []
        assert isinstance(missions, list)

    def test_get_all_mission_with_data(self, db_session, mission_test):
        missions = get_all_mission(db_session)
        assert len(missions) == 1
        assert missions[0]["id_mission"] == mission_test.id_mission
        assert "_sa_instance_state" not in missions[0]

    def test_get_all_mission_multiple(self, db_session, utilisateur_test, point_test):
        for i in range(3):
            mission = models.Mission(
                nom_mission=f"Mission {i}",
                id_point=point_test.numero_pei,
                id_utilisateur=utilisateur_test.id_utilisateur,
                statut="EN COURS"
            )
            db_session.add(mission)
            db_session.commit()
            db_session.refresh(mission)
        
        missions = get_all_mission(db_session)
        assert len(missions) == 3
        assert all(isinstance(m, dict) for m in missions)


class TestGetMissionById:
    """Tests pour la récupération par ID"""
    
    def test_get_mission_by_id_exists(self, db_session, mission_test):
        m = get_mission_by_id(db_session, mission_test.id_mission)
        assert m is not None
        assert m["id_mission"] == mission_test.id_mission
        assert m["nom_mission"] == "Mission Test"
    
    def test_get_mission_by_id_not_exists(self, db_session):
        with pytest.raises(ValueError, match="Mission introuv"):
            get_mission_by_id(db_session, 99999)


class TestGetMissionByDate:
    """Tests pour la récupération par date"""
    
    def test_get_mission_by_date_today(self, db_session, mission_test):
        today = date.today()
        missions = get_mission_by_date(db_session, today)
        assert len(missions) >= 1
        assert any(m.id_mission == mission_test.id_mission for m in missions)

    def test_get_mission_by_date_no_missions(self, db_session):
        future_date = date.today() + timedelta(days=365)
        missions = get_mission_by_date(db_session, future_date)
        assert missions == []

    def test_get_mission_by_date_multiple(self, db_session, utilisateur_test, point_test):
        for i in range(3):
            mission = models.Mission(
                nom_mission=f"Mission {i}",
                id_point=point_test.numero_pei,
                id_utilisateur=utilisateur_test.id_utilisateur,
                statut="EN COURS"
            )
            db_session.add(mission)
            db_session.commit()
        
        today = date.today()
        missions = get_mission_by_date(db_session, today)
        assert len(missions) >= 3

    def test_get_mission_by_date_past(self, db_session):
        past_date = date.today() - timedelta(days=30)
        missions = get_mission_by_date(db_session, past_date)
        assert missions == []

    def test_get_mission_by_date_boundary(self, db_session, mission_test):
        """Test les limites de début et fin de journée"""
        today = date.today()
        missions = get_mission_by_date(db_session, today)
        assert any(m.id_mission == mission_test.id_mission for m in missions)
        
        yesterday = today - timedelta(days=1)
        missions_yesterday = get_mission_by_date(db_session, yesterday)
        assert not any(m.id_mission == mission_test.id_mission for m in missions_yesterday)


class TestCreateMission:
    """Tests pour la création de missions"""
    
    def test_create_mission_complet(self, db_session, utilisateur_test, point_test):
        data = {
            "nom_mission": "Nouvelle Mission",
            "id_point": point_test.numero_pei,
            "id_utilisateur": utilisateur_test.id_utilisateur,
            "commentaire": "Test complet",
            "itineraire": "Route A -> Route B"
        }
        m = create_mission(db_session, data)
        
        assert m is not None
        assert m.id_mission is not None
        assert m.nom_mission == "Nouvelle Mission"
        assert m.statut == "EN COURS"
        assert m.commentaire == "Test complet"
        assert m.itineraire == "Route A -> Route B"

    def test_create_mission_minimal(self, db_session, utilisateur_test, point_test):
        data = {
            "nom_mission": "Mission Min",
            "id_point": point_test.numero_pei,
            "id_utilisateur": utilisateur_test.id_utilisateur
        }
        m = create_mission(db_session, data)
        
        assert m is not None
        assert m.statut == "EN COURS"
        assert m.commentaire is None
        assert m.itineraire is None

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

    def test_create_mission_with_optional_fields(self, db_session, utilisateur_test, point_test):
        data = {
            "nom_mission": "Mission Complete",
            "id_point": point_test.numero_pei,
            "id_utilisateur": utilisateur_test.id_utilisateur,
            "commentaire": "Commentaire detaille",
            "itineraire": "A -> B -> C"
        }
        
        m = create_mission(db_session, data)
        assert m.commentaire == "Commentaire detaille"
        assert m.itineraire == "A -> B -> C"

    def test_create_mission_with_empty_strings(self, db_session, utilisateur_test, point_test):
        data = {
            "nom_mission": "Mission",
            "id_point": point_test.numero_pei,
            "id_utilisateur": utilisateur_test.id_utilisateur,
            "commentaire": "",
            "itineraire": ""
        }
        
        m = create_mission(db_session, data)
        assert m is not None


class TestDeleteMission:
    """Tests pour la suppression de missions"""
    
    def test_delete_mission_exists(self, db_session, mission_test):
        mission_id = mission_test.id_mission
        result = delete_mission_by_id(db_session, mission_id)
        
        assert result is True
        
        with pytest.raises(ValueError, match="Mission introuv"):
            get_mission_by_id(db_session, mission_id)

    def test_delete_mission_not_exists(self, db_session):
        result = delete_mission_by_id(db_session, 99999)
        assert result is False

    def test_delete_mission_twice(self, db_session, mission_test):
        mission_id = mission_test.id_mission
        
        result1 = delete_mission_by_id(db_session, mission_id)
        assert result1 is True
        
        result2 = delete_mission_by_id(db_session, mission_id)
        assert result2 is False


class TestUpdateMission:
    """Tests pour la mise à jour de missions"""
    
    def test_update_mission_statut(self, db_session, mission_test):
        data = {"statut": "TERMINER"}
        updated = update_mission_by_id(db_session, mission_test.id_mission, data)
        
        assert updated is not None
        assert updated.statut == "TERMINER"
        assert updated.nom_mission == mission_test.nom_mission

    def test_update_mission_statut_terminee(self, db_session, mission_test):
        data = {"statut": "TERMINER"}
        updated = update_mission_by_id(db_session, mission_test.id_mission, data)
        
        assert updated is not None
        assert updated.statut == "TERMINER"

    def test_update_mission_multiple_fields(self, db_session, mission_test):
        data = {
            "statut": "TERMINER",
            "commentaire": "Nouveau commentaire",
            "itineraire": "Nouvel itineraire"
        }
        
        updated = update_mission_by_id(db_session, mission_test.id_mission, data)
        
        assert updated is not None
        assert updated.statut == "TERMINER"
        assert updated.commentaire == "Nouveau commentaire"
        assert updated.itineraire == "Nouvel itineraire"

    def test_update_mission_only_nom(self, db_session, mission_test):
        data = {"nom_mission": "Nouveau nom"}
        updated = update_mission_by_id(db_session, mission_test.id_mission, data)
        
        assert updated.nom_mission == "Nouveau nom"
        assert updated.statut == mission_test.statut

    def test_update_mission_ignore_protected_fields(self, db_session, mission_test):
        original_id = mission_test.id_mission
        original_date = mission_test.date_creation
        
        data = {
            "id_mission": 99999,
            "date_creation": "2000-01-01",
            "statut": "TERMINER"
        }
        
        updated = update_mission_by_id(db_session, mission_test.id_mission, data)
        
        assert updated.id_mission == original_id
        assert updated.date_creation == original_date
        assert updated.statut == "TERMINER"

    def test_update_mission_clear_optional_field(self, db_session, mission_test):
        data = {"commentaire": None}
        updated = update_mission_by_id(db_session, mission_test.id_mission, data)
        
        assert updated.commentaire is None

    def test_update_mission_not_exists(self, db_session):
        data = {"statut": "TERMINER"}
        
        with pytest.raises(ValueError, match="Id mission incorrect"):
            update_mission_by_id(db_session, 99999, data)

    def test_update_mission_with_same_values(self, db_session, mission_test):
        data = {
            "nom_mission": mission_test.nom_mission,
            "statut": mission_test.statut
        }
        
        updated = update_mission_by_id(db_session, mission_test.id_mission, data)
        assert updated is not None
        assert updated.nom_mission == mission_test.nom_mission


class TestIntegration:
    """Tests d'intégration CRUD complet"""
    
    def test_integration_full_crud(self, db_session, utilisateur_test, point_test):
        # CREATE
        data = {
            "nom_mission": "Mission CRUD",
            "id_point": point_test.numero_pei,
            "id_utilisateur": utilisateur_test.id_utilisateur,
            "commentaire": "Test integration"
        }
        created = create_mission(db_session, data)
        assert created.id_mission is not None
        
        # READ by ID
        retrieved_by_id = get_mission_by_id(db_session, created.id_mission)
        assert retrieved_by_id["nom_mission"] == "Mission CRUD"
        
        # READ ALL
        all_missions = get_all_mission(db_session)
        assert any(m["id_mission"] == created.id_mission for m in all_missions)
        
        # READ by Date
        today = date.today()
        missions_today = get_mission_by_date(db_session, today)
        assert any(m.id_mission == created.id_mission for m in missions_today)
        
        # UPDATE
        update_data = {"statut": "TERMINER", "commentaire": "Mission accomplie"}
        updated = update_mission_by_id(db_session, created.id_mission, update_data)
        assert updated.statut == "TERMINER"
        assert updated.commentaire == "Mission accomplie"
        
        # DELETE
        deleted = delete_mission_by_id(db_session, created.id_mission)
        assert deleted is True
        
        # VERIFY DELETE
        with pytest.raises(ValueError, match="Mission introuvable"):
            get_mission_by_id(db_session, created.id_mission)

    def test_integration_multiple_missions_same_day(self, db_session, utilisateur_test, point_test):
        today = date.today()
        created_ids = []
        
        for i in range(3):
            mission = models.Mission(
                nom_mission=f"Mission {i}",
                id_point=point_test.numero_pei,
                id_utilisateur=utilisateur_test.id_utilisateur,
                statut="EN COURS"
            )
            db_session.add(mission)
            db_session.commit()
            db_session.refresh(mission)
            created_ids.append(mission.id_mission)
        
        missions_today = get_mission_by_date(db_session, today)
        assert len(missions_today) == 3
        
        all_missions = get_all_mission(db_session)
        assert len(all_missions) == 3
        
        all_ids = [m["id_mission"] for m in all_missions]
        for created_id in created_ids:
            assert created_id in all_ids

    def test_integration_mission_lifecycle(self, db_session, utilisateur_test, point_test):
        """Test du cycle de vie complet d'une mission"""
        # Création
        data = {
            "nom_mission": "Mission Lifecycle",
            "id_point": point_test.numero_pei,
            "id_utilisateur": utilisateur_test.id_utilisateur
        }
        mission = create_mission(db_session, data)
        assert mission.statut == "EN COURS"
        
        # Passage à TERMINER
        update_mission_by_id(db_session, mission.id_mission, {"statut": "TERMINER"})
        updated = get_mission_by_id(db_session, mission.id_mission)
        assert updated["statut"] == "TERMINER"
        
        # Suppression
        assert delete_mission_by_id(db_session, mission.id_mission) is True


class TestEdgeCases:
    """Tests des cas limites"""
    
    def test_create_multiple_missions_same_point(self, db_session, utilisateur_test, point_test):
        """Test création de plusieurs missions pour le même point"""
        for i in range(3):
            data = {
                "nom_mission": f"Mission Point {i}",
                "id_point": point_test.numero_pei,
                "id_utilisateur": utilisateur_test.id_utilisateur
            }
            m = create_mission(db_session, data)
            assert m is not None
        
        all_missions = get_all_mission(db_session)
        assert len(all_missions) == 3

    def test_create_multiple_missions_same_user(self, db_session, utilisateur_test, point_test):
        """Test création de plusieurs missions pour le même utilisateur"""
        # Créer des points supplémentaires
        for i in range(3):
            transformer = Transformer.from_crs("EPSG:4326", "EPSG:2154")
            x, y = transformer.transform(48.8 + i * 0.1, 2.3 + i * 0.1)
            wkt = WKTElement(f"POINT({x} {y})", srid=2154)
            
            point = models.PointEau(
                numero_pei=20000 + i,
                statut="PUBLIC",
                type_nature="BI",
                geom=wkt,
                accessibilite="NC",
                disponibilite="DI",
                carto_ref=0,
                press_deb=0.0,
                debit_1_bar=0.0,
                vol_eau_mi=0.0,
                utilisateur=1
            )
            db_session.add(point)
            db_session.commit()
            
            data = {
                "nom_mission": f"Mission User {i}",
                "id_point": 20000 + i,
                "id_utilisateur": utilisateur_test.id_utilisateur
            }
            m = create_mission(db_session, data)
            assert m is not None
        
        all_missions = get_all_mission(db_session)
        assert len(all_missions) == 3

    def test_update_to_same_statut(self, db_session, mission_test):
        """Test mise à jour avec le même statut"""
        original_statut = mission_test.statut
        data = {"statut": original_statut}
        
        updated = update_mission_by_id(db_session, mission_test.id_mission, data)
        assert updated.statut == original_statut

    def test_get_mission_by_date_with_no_data(self, db_session):
        """Test get_by_date sans aucune mission en base"""
        today = date.today()
        missions = get_mission_by_date(db_session, today)
        assert missions == []