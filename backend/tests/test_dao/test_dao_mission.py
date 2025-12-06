import pytest
from datetime import date
from app.DAO import mission_dao
from app import models


class TestMissionDAO:
    """Tests pour le DAO Mission"""

    # ============= FIXTURES =============
    
    @pytest.fixture(autouse=True)
    def cleanup(self, db_session):
        """Nettoie la base entre chaque test"""
        yield
        try:
            db_session.rollback()
            # Ordre important : supprimer missions avant utilisateurs et points
            db_session.query(models.Mission).delete()
            db_session.query(models.Utilisateur).delete()
            db_session.query(models.PointEau).delete()
            db_session.commit()
        except Exception:
            db_session.rollback()
    
    @pytest.fixture
    def utilisateur_test(self, db_session):
        """Crée un utilisateur de test"""
        user = models.Utilisateur(
            nom="Dupont",
            prenom="Jean",
            email="jean.dupont@test.com",
            telephone="0612345678",  # Requis
            mot_de_passe="hashed_password",
            role=models.RoleEnum.pompier
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

    @pytest.fixture
    def point_test(self, db_session):
        """Crée un point d'eau de test"""
        from pyproj import Transformer
        from geoalchemy2.elements import WKTElement
        
        # Conversion WGS84 -> Lambert-93
        transformer = Transformer.from_crs("EPSG:4326", "EPSG:2154")
        x, y = transformer.transform(48.8566, 2.3522)
        wkt = WKTElement(f"POINT({x} {y})", srid=2154)
        
        point = models.PointEau(
            numero_pei=12345,  # Integer, pas String
            statut="PUBLIC",  # Respecter Enum
            type_nature="BI",  # Respecter Enum
            geom=wkt
        )
        db_session.add(point)
        db_session.commit()
        db_session.refresh(point)
        return point

    @pytest.fixture
    def mission_test(self, db_session, utilisateur_test, point_test):
        """Crée une mission de test"""
        mission = models.Mission(
            nom_mission="Mission Test",
            id_point=point_test.id,
            id_utilisateur=utilisateur_test.id_utilisateur,
            statut="en_attente",
            commentaire="Mission de test"
        )
        db_session.add(mission)
        db_session.commit()
        db_session.refresh(mission)
        return mission

    # ============= TESTS GET ALL =============
    
    def test_get_all_mission_empty(self, db_session):
        """Test get_all avec une base vide"""
        missions = mission_dao.get_all_mission(db_session)
        assert missions == []
        assert isinstance(missions, list)

    def test_get_all_mission_with_data(self, db_session, mission_test):
        """Test get_all avec des données"""
        missions = mission_dao.get_all_mission(db_session)
        
        assert len(missions) == 1
        assert all(isinstance(m, dict) for m in missions)
        assert "nom_mission" in missions[0]
        assert "_sa_instance_state" not in missions[0]

    def test_get_all_mission_multiple(self, db_session, utilisateur_test, point_test):
        """Test get_all avec plusieurs missions"""
        for i in range(3):
            mission_dao.create_mission(db_session, {
                "nom_mission": f"Mission {i}",
                "id_point": point_test.id,
                "id_utilisateur": utilisateur_test.id_utilisateur
            })
        
        missions = mission_dao.get_all_mission(db_session)
        assert len(missions) == 3

    # ============= TESTS GET BY ID =============
    
    def test_get_mission_by_id_exists(self, db_session, mission_test):
        """Test get_by_id avec un ID existant"""
        m = mission_dao.get_mission_by_id(db_session, mission_test.id_mission)
        
        assert m is not None
        assert m.id_mission == mission_test.id_mission
        assert m.nom_mission == "Mission Test"

    def test_get_mission_by_id_not_exists(self, db_session):
        """Test get_by_id avec un ID inexistant"""
        m = mission_dao.get_mission_by_id(db_session, 99999)
        assert m is None

    # ============= TESTS GET BY DATE =============
    
    def test_get_mission_by_date_today(self, db_session, mission_test):
        """Test get_by_date avec la date d'aujourd'hui"""
        today = date.today()
        missions = mission_dao.get_mission_by_date(db_session, today)
        
        assert len(missions) >= 1
        assert any(m.id_mission == mission_test.id_mission for m in missions)

    def test_get_mission_by_date_no_missions(self, db_session):
        """Test get_by_date sans missions pour cette date"""
        from datetime import timedelta
        future_date = date.today() + timedelta(days=365)
        missions = mission_dao.get_mission_by_date(db_session, future_date)
        
        assert missions == []

    def test_get_mission_by_date_multiple(self, db_session, utilisateur_test, point_test):
        """Test get_by_date avec plusieurs missions aujourd'hui"""
        for i in range(3):
            mission_dao.create_mission(db_session, {
                "nom_mission": f"Mission {i}",
                "id_point": point_test.id,
                "id_utilisateur": utilisateur_test.id_utilisateur
            })
        
        today = date.today()
        missions = mission_dao.get_mission_by_date(db_session, today)
        assert len(missions) >= 3

    # ============= TESTS CREATE =============
    
    def test_create_mission_complet(self, db_session, utilisateur_test, point_test):
        """Test création d'une mission avec toutes les données"""
        data = {
            "nom_mission": "Nouvelle Mission",
            "id_point": point_test.id,
            "id_utilisateur": utilisateur_test.id_utilisateur,
            "statut": "en_cours",
            "commentaire": "Test complet",
            "itineraire": "Route A -> Route B"
        }
        
        m = mission_dao.create_mission(db_session, data)
        
        assert m is not None
        assert m.id_mission is not None
        assert m.nom_mission == "Nouvelle Mission"
        assert m.statut == "en_cours"
        assert m.commentaire == "Test complet"
        assert m.itineraire == "Route A -> Route B"

    def test_create_mission_minimal(self, db_session, utilisateur_test, point_test):
        """Test création d'une mission avec données minimales"""
        data = {
            "nom_mission": "Mission Min",
            "id_point": point_test.id,
            "id_utilisateur": utilisateur_test.id_utilisateur
        }
        
        m = mission_dao.create_mission(db_session, data)
        
        assert m is not None
        assert m.statut == "en attente"  # Valeur par défaut
        assert m.commentaire is None
        assert m.itineraire is None

    def test_create_mission_invalid_point(self, db_session, utilisateur_test):
        """Test création avec un id_point invalide"""
        data = {
            "nom_mission": "Mission Invalide",
            "id_point": 99999,
            "id_utilisateur": utilisateur_test.id_utilisateur
        }
        
        with pytest.raises(ValueError, match="id_point est invalide"):
            mission_dao.create_mission(db_session, data)

    def test_create_mission_invalid_user(self, db_session, point_test):
        """Test création avec un id_utilisateur invalide"""
        data = {
            "nom_mission": "Mission Invalide",
            "id_point": point_test.id,
            "id_utilisateur": 99999
        }
        
        with pytest.raises(ValueError, match="id_utilisateur est incorrect"):
            mission_dao.create_mission(db_session, data)

    # ============= TESTS DELETE =============
    
    def test_delete_mission_exists(self, db_session, mission_test):
        """Test suppression d'une mission existante"""
        mission_id = mission_test.id_mission
        result = mission_dao.delete_mission_by_id(db_session, mission_id)
        
        assert result is True
        
        # Vérifier que la mission n'existe plus
        deleted = mission_dao.get_mission_by_id(db_session, mission_id)
        assert deleted is None

    def test_delete_mission_not_exists(self, db_session):
        """Test suppression d'une mission inexistante"""
        result = mission_dao.delete_mission_by_id(db_session, 99999)
        assert result is False

    # ============= TESTS UPDATE =============
    
    def test_update_mission_statut(self, db_session, mission_test):
        """Test update du statut"""
        data = {"statut": "terminée"}
        updated = mission_dao.update_mission_by_id(
            db_session, 
            mission_test.id_mission, 
            data
        )
        
        assert updated is not None
        assert updated.statut == "terminée"
        assert updated.nom_mission == mission_test.nom_mission  # Inchangé

    def test_update_mission_multiple_fields(self, db_session, mission_test):
        """Test update de plusieurs champs"""
        data = {
            "statut": "en_cours",
            "commentaire": "Nouveau commentaire",
            "itineraire": "Nouvel itinéraire"
        }
        
        updated = mission_dao.update_mission_by_id(
            db_session, 
            mission_test.id_mission, 
            data
        )
        
        assert updated is not None
        assert updated.statut == "en_cours"
        assert updated.commentaire == "Nouveau commentaire"
        assert updated.itineraire == "Nouvel itinéraire"

    def test_update_mission_ignore_protected_fields(self, db_session, mission_test):
        """Test que les champs protégés ne peuvent pas être modifiés"""
        from datetime import datetime
        original_id = mission_test.id_mission
        original_date = mission_test.date_creation
        
        data = {
            "id_mission": 99999,
            "date_creation": datetime(2000, 1, 1),
            "statut": "en_cours"
        }
        
        updated = mission_dao.update_mission_by_id(
            db_session, 
            mission_test.id_mission, 
            data
        )
        
        assert updated.id_mission == original_id  # ID inchangé
        assert updated.date_creation == original_date  # date_creation inchangée
        assert updated.statut == "en_cours"  # statut changé

    def test_update_mission_not_exists(self, db_session):
        """Test update d'une mission inexistante"""
        data = {"statut": "terminée"}
        updated = mission_dao.update_mission_by_id(db_session, 99999, data)
        
        assert updated is None

    # ============= TESTS D'INTÉGRATION =============
    
    def test_integration_full_crud(self, db_session, utilisateur_test, point_test):
        """Test d'intégration : cycle CRUD complet"""
        # CREATE
        data = {
            "nom_mission": "Mission CRUD",
            "id_point": point_test.id,
            "id_utilisateur": utilisateur_test.id_utilisateur,
            "statut": "en_attente"
        }
        created = mission_dao.create_mission(db_session, data)
        assert created.id_mission is not None
        
        # READ by ID
        retrieved_by_id = mission_dao.get_mission_by_id(db_session, created.id_mission)
        assert retrieved_by_id.nom_mission == "Mission CRUD"
        
        # READ ALL
        all_missions = mission_dao.get_all_mission(db_session)
        assert any(m["id_mission"] == created.id_mission for m in all_missions)
        
        # READ by Date
        today = date.today()
        missions_today = mission_dao.get_mission_by_date(db_session, today)
        assert any(m.id_mission == created.id_mission for m in missions_today)
        
        # UPDATE
        update_data = {"statut": "terminée", "commentaire": "Mission accomplie"}
        updated = mission_dao.update_mission_by_id(db_session, created.id_mission, update_data)
        assert updated.statut == "terminée"
        assert updated.commentaire == "Mission accomplie"
        
        # DELETE
        deleted = mission_dao.delete_mission_by_id(db_session, created.id_mission)
        assert deleted is True
        
        # VERIFY DELETE
        not_found = mission_dao.get_mission_by_id(db_session, created.id_mission)
        assert not_found is None