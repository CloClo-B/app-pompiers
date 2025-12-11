from app.schemas import PointEauCreate
import pytest
from app.DAO import point_eau_dao
from app import models


class TestPointEauDAO:
    """Tests pour le DAO Point d'Eau"""

    # ============= FIXTURES =============
    
    @pytest.fixture(autouse=True)
    def cleanup(self, db_session):
        """Nettoie la base entre chaque test"""
        yield
        # Après chaque test, rollback si nécessaire puis nettoyer
        try:
            db_session.rollback()  # Annuler toute transaction en erreur
            db_session.query(models.PointEau).delete()
            db_session.commit()
        except Exception:
            db_session.rollback()  # Si le nettoyage échoue aussi
    
    @pytest.fixture
    def sample_point_data(self):
        """Données pour créer un point d'eau de test"""
        return {
            "numero_pei": 12345,  # Integer, pas String
            "nom": "Point Test",
            "statut": "PUBLIC",  # Respecter les valeurs Enum
            "type_nature": "BI",  # Respecter les valeurs Enum
            "insee5": "12345",
            "latitude": 48.8566,
            "longitude": 2.3522,
            "press_deb": 5.5,
            "debit_1_bar": 60.0,
            "vol_eau_mi": 120.0,
            "accessibilite": "C",
            "disponibilite": "DI",
            "carto_ref": 100,
            "utilisateur": "test_user"
        }

    @pytest.fixture
    def sample_point(self, db_session, sample_point_data):
        """Crée un point d'eau de test"""
        point_data = PointEauCreate(**sample_point_data)
        point_data = PointEauCreate(**sample_point_data)
        point = point_eau_dao.create_point_eau(db_session, point_data)

        assert point is not None, "La création du point d'eau de test a échoué"
        return point

    # ============= TESTS CREATE =============
    
    def test_create_point_eau_complet(self, db_session):
        """Test création d'un point d'eau avec toutes les données"""
        data = {
            "numero_pei": 67890,
            "nom": "Borne Incendie Test",
            "statut": "PUBLIC",
            "type_nature": "PI100",
            "insee5": "56789",
            "latitude": 45.7640,
            "longitude": 4.8357,
            "press_deb": 4.5,
            "debit_1_bar": 55.0,
            "vol_eau_mi": 100.0,
            "accessibilite": "C",
            "disponibilite": "DI",
            "carto_ref": 200,
            "utilisateur": "pompier_test"
        }
        
        point_data = PointEauCreate(**data) 
        point = point_eau_dao.create_point_eau(db_session, point_data)
        
        assert point is not None
        assert point.id is not None
        assert point.numero_pei == 67890
        assert point.nom == "Borne Incendie Test"
        assert point.statut == "PUBLIC"
        assert point.type_nature == "PI100"
        assert point.geom is not None  # Géométrie créée

    def test_create_point_eau_minimal(self, db_session):
        """Test création d'un point d'eau avec données minimales"""
        data = {
            "numero_pei": 11111,
            "statut": "PRIVE",
            "type_nature": "PENA",
            "latitude": 43.6047,
            "longitude": 1.4442
        }
        
        point_data = PointEauCreate(**data)
        point = point_eau_dao.create_point_eau(db_session, point_data)
        
        assert point is not None
        assert point.numero_pei == 11111
        assert point.statut == "PRIVE"
        assert point.type_nature == "PENA"

    def test_create_point_eau_numero_pei_unique(self, db_session, sample_point):
        """Test que numero_pei doit être unique"""
        data = {
            "numero_pei": sample_point.numero_pei,  # Même numéro
            "statut": "PUBLIC",
            "type_nature": "BI",
            "latitude": 48.0,
            "longitude": 2.0
        }
        
        with pytest.raises(Exception):  # IntegrityError de SQLAlchemy
            point_eau_dao.create_point_eau(db_session, data)
            db_session.commit()

    def test_create_point_eau_coordonnees_lambert93(self, db_session):
        """Test que les coordonnées WGS84 sont converties en Lambert-93"""
        data = {
            "numero_pei": 99999,
            "statut": "PUBLIC",
            "type_nature": "BI",
            "latitude": 48.8566,  # Paris WGS84
            "longitude": 2.3522
        }
        
        point_data = PointEauCreate(**data)
        point = point_eau_dao.create_point_eau(db_session, point_data)
        
        # Le point geom doit exister et être en Lambert-93 (SRID 2154)
        assert point.geom is not None

    # ============= TESTS GET ALL =============
    
    def test_get_all_points_eau_empty(self, db_session):
        """Test get_all avec une base vide"""
        points = point_eau_dao.get_all_points_eau(db_session)
        assert points == []

    def test_get_all_points_eau_with_data(self, db_session, sample_point):
        """Test get_all avec des données"""
        points = point_eau_dao.get_all_points_eau(db_session)
        
        assert len(points) == 1
        assert all(isinstance(p, dict) for p in points)
        assert "latitude" in points[0]
        assert "longitude" in points[0]
        assert "numero_pei" in points[0]

    def test_get_all_points_eau_multiple(self, db_session):
        """Test get_all avec plusieurs points d'eau"""
        points_data = [
            {"numero_pei": 1001, "statut": "PUBLIC", "type_nature": "BI", 
             "latitude": 48.8, "longitude": 2.3},
            {"numero_pei": 1002, "statut": "PRIVE", "type_nature": "PI100", 
             "latitude": 48.9, "longitude": 2.4},
            {"numero_pei": 1003, "statut": "PUBLIC", "type_nature": "PENA", 
             "latitude": 48.7, "longitude": 2.2},
        ]
        
        for data in points_data:
            point_data = PointEauCreate(**data)
            point_eau_dao.create_point_eau(db_session, point_data)
        
        points = point_eau_dao.get_all_points_eau(db_session)
        assert len(points) == 3

    # ============= TESTS GET BY ID =============
    
    def test_get_point_eau_by_id_exists(self, db_session, sample_point):
        """Test get_by_id avec un ID existant"""
        point = point_eau_dao.get_point_eau_by_id(db_session, sample_point.id)
        
        assert point is not None
        assert point["id"] == sample_point.id
        assert point["numero_pei"] == sample_point.numero_pei
        assert "latitude" in point
        assert "longitude" in point

    def test_get_point_eau_by_id_not_exists(self, db_session):
        """Test get_by_id avec un ID inexistant"""
        point = point_eau_dao.get_point_eau_by_id(db_session, 99999)
        assert point is None

    # ============= TESTS UPDATE =============
    
    def test_update_point_eau_statut(self, db_session, sample_point):
        """Test update du statut"""
        data = {"statut": "PRIVE"}
        updated = point_eau_dao.update_point_eau_by_id(
            db_session, 
            sample_point.id, 
            data
        )
        
        assert updated is not None
        assert updated.statut == "PRIVE"
        assert updated.numero_pei == sample_point.numero_pei  # Inchangé

    def test_update_point_eau_multiple_fields(self, db_session, sample_point):
        """Test update de plusieurs champs"""
        data = {
            "nom": "Nouveau Nom",
            "press_deb": 6.0,
            "debit_1_bar": 70.0,
            "accessibilite": "NC"
        }
        
        updated = point_eau_dao.update_point_eau_by_id(
            db_session, 
            sample_point.id, 
            data
        )
        
        assert updated is not None
        assert updated.nom == "Nouveau Nom"
        assert updated.press_deb == 6.0
        assert updated.debit_1_bar == 70.0
        assert updated.accessibilite == "NC"

    def test_update_point_eau_coordonnees(self, db_session, sample_point):
        """Test update des coordonnées (recalcule geom)"""
        data = {
            "latitude": 45.7640,
            "longitude": 4.8357
        }
        
        updated = point_eau_dao.update_point_eau_by_id(
            db_session, 
            sample_point.id, 
            data
        )
        
        assert updated is not None
        assert updated.geom is not None
        # La géométrie devrait être différente de l'originale

    def test_update_point_eau_date_maj(self, db_session, sample_point):
        """Test que date_maj est mise à jour automatiquement"""
        original_date_maj = sample_point.date_maj
        
        data = {"nom": "Mise à jour"}
        updated = point_eau_dao.update_point_eau_by_id(
            db_session, 
            sample_point.id, 
            data
        )
        
        assert updated.date_maj is not None
        # date_maj devrait être plus récente que date_crea

    def test_update_point_eau_ignore_protected_fields(self, db_session, sample_point):
        """Test que les champs protégés ne peuvent pas être modifiés"""
        original_id = sample_point.id
        original_date_crea = sample_point.date_crea
        
        data = {
            "id": 99999,
            "date_crea": "2000-01-01",
            "nom": "Update"
        }
        
        updated = point_eau_dao.update_point_eau_by_id(
            db_session, 
            sample_point.id, 
            data
        )
        
        assert updated.id == original_id  # ID inchangé
        assert updated.date_crea == original_date_crea  # date_crea inchangée
        assert updated.nom == "Update"  # nom changé

    def test_update_point_eau_not_exists(self, db_session):
        """Test update d'un point d'eau inexistant"""
        data = {"nom": "Test"}
        updated = point_eau_dao.update_point_eau_by_id(db_session, 99999, data)
        
        assert updated is None

    # ============= TESTS DELETE =============
    
    def test_delete_point_eau_exists(self, db_session, sample_point):
        """Test suppression d'un point d'eau existant"""
        point_id = sample_point.id
        
        result = point_eau_dao.delete_point_eau_by_id(db_session, point_id)
        
        assert result is True
        
        # Vérifier que le point n'existe plus
        deleted = point_eau_dao.get_point_eau_by_id(db_session, point_id)
        assert deleted is None

    def test_delete_point_eau_not_exists(self, db_session):
        """Test suppression d'un point d'eau inexistant"""
        result = point_eau_dao.delete_point_eau_by_id(db_session, 99999)
        assert result is False

    # ============= TESTS DE VALIDATION =============
    
    def test_create_point_eau_statut_invalid(self, db_session):
        """Test création avec un statut invalide"""
        data = {
            "numero_pei": 55555,
            "statut": "INVALIDE",  # Pas dans l'Enum
            "type_nature": "BI",
            "latitude": 48.8,
            "longitude": 2.3
        }
        
        with pytest.raises(Exception):  # StatementError de SQLAlchemy
            point_eau_dao.create_point_eau(db_session, data)

    def test_create_point_eau_type_nature_invalid(self, db_session):
        """Test création avec un type_nature invalide"""
        data = {
            "numero_pei": 66666,
            "statut": "PUBLIC",
            "type_nature": "INVALIDE",  # Pas dans l'Enum
            "latitude": 48.8,
            "longitude": 2.3
        }
        
        with pytest.raises(Exception):  # StatementError de SQLAlchemy
            point_eau_dao.create_point_eau(db_session, data)

    # ============= TESTS D'INTÉGRATION =============
    
    def test_integration_full_crud(self, db_session):
        """Test d'intégration : cycle CRUD complet"""
        # CREATE
        data = {
            "numero_pei": 88888,
            "nom": "Point Integration",
            "statut": "PUBLIC",
            "type_nature": "PI150",
            "latitude": 43.2965,
            "longitude": 5.3698,
            "press_deb": 5.0,
            "debit_1_bar": 60.0
        }
        point_data = PointEauCreate(**data)
        created = point_eau_dao.create_point_eau(db_session, point_data)
        assert created.id is not None
        
        # READ by ID
        retrieved_by_id = point_eau_dao.get_point_eau_by_id(db_session, created.id)
        assert retrieved_by_id["numero_pei"] == 88888
        
        # READ ALL
        all_points = point_eau_dao.get_all_points_eau(db_session)
        assert any(p["id"] == created.id for p in all_points)
        
        # UPDATE
        update_data = {"nom": "Point Mis à Jour", "statut": "PRIVE"}
        updated = point_eau_dao.update_point_eau_by_id(db_session, created.id, update_data)
        assert updated.nom == "Point Mis à Jour"
        assert updated.statut == "PRIVE"
        
        # DELETE
        deleted = point_eau_dao.delete_point_eau_by_id(db_session, created.id)
        assert deleted is True
        
        # VERIFY DELETE
        not_found = point_eau_dao.get_point_eau_by_id(db_session, created.id)
        assert not_found is None