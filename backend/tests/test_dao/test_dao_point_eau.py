import pytest
from sqlalchemy.exc import IntegrityError
from app.DAO.DAOPointsEau import (
    get_all_points_eau,
    get_point_eau_by_id,
    get_point_eau_by_numero_pei,
    create_point_eau,
    update_point_eau_by_id,
    delete_point_eau_by_id,
    delete_point_eau_by_numero_pei
)


@pytest.fixture
def sample_point_data():
    """Données pour créer un point d'eau de test"""
    return {
        "numero_pei": 12345,
        "nom": "Point Test",
        "statut": "public",
        "type_nature": "bi",
        "insee5": "12345",
        "latitude": 48.8566,
        "longitude": 2.3522,
        "press_deb": 5.5,
        "debit_1_bar": 60.0,
        "vol_eau_mi": 120.0,
        "accessibilite": "C",
        "disponibilite": "DI",
        "carto_ref": 100,
        "utilisateur": 1
    }


@pytest.fixture
def sample_point(db_session, sample_point_data):
    """Crée un point d'eau de test"""
    point = create_point_eau(db_session, sample_point_data)
    assert point is not None
    return point


class TestCreatePointEau:
    """Tests pour la création de points d'eau"""
    
    def test_create_point_eau_complet(self, db_session):
        data = {
            "numero_pei": 67890,
            "nom": "Borne Incendie Test",
            "statut": "public",
            "type_nature": "pi100",
            "insee5": "56789",
            "latitude": 45.7640,
            "longitude": 4.8357,
            "press_deb": 4.5,
            "debit_1_bar": 55.0,
            "vol_eau_mi": 100.0,
            "accessibilite": "C",
            "disponibilite": "DI",
            "carto_ref": 200,
            "utilisateur": 1
        }
        
        point = create_point_eau(db_session, data)
        
        assert point is not None
        assert point.id is not None
        assert point.numero_pei == 67890
        assert point.nom == "Borne Incendie Test"
        assert point.statut == "PUBLIC"
        assert point.type_nature == "PI100"
        assert point.geom is not None

    def test_create_point_eau_minimal(self, db_session):
        data = {
            "numero_pei": 11111,
            "statut": "prive",
            "type_nature": "pena",
            "latitude": 43.6047,
            "longitude": 1.4442,
            "accessibilite": "NC",
            "disponibilite": "DI",
            "carto_ref": 0,
            "press_deb": 0.0,
            "debit_1_bar": 0.0,
            "vol_eau_mi": 0.0,
            "utilisateur": 1
        }
        
        point = create_point_eau(db_session, data)
        
        assert point is not None
        assert point.numero_pei == 11111
        assert point.statut == "PRIVE"
        assert point.type_nature == "PENA"

    def test_create_point_eau_numero_pei_unique(self, db_session, sample_point):
        data = {
            "numero_pei": sample_point.numero_pei,
            "statut": "public",
            "type_nature": "bi",
            "latitude": 48.0,
            "longitude": 2.0,
            "accessibilite": "NC",
            "disponibilite": "DI",
            "carto_ref": 0,
            "press_deb": 0.0,
            "debit_1_bar": 0.0,
            "vol_eau_mi": 0.0,
            "utilisateur": 1
        }
        
        with pytest.raises(ValueError, match="existe déjà"):
            create_point_eau(db_session, data)

    def test_create_point_eau_coordonnees_lambert93(self, db_session):
        data = {
            "numero_pei": 99999,
            "statut": "public",
            "type_nature": "bi",
            "latitude": 48.8566,
            "longitude": 2.3522,
            "accessibilite": "NC",
            "disponibilite": "DI",
            "carto_ref": 0,
            "press_deb": 0.0,
            "debit_1_bar": 0.0,
            "vol_eau_mi": 0.0,
            "utilisateur": 1
        }
        
        point = create_point_eau(db_session, data)
        assert point.geom is not None

    def test_create_point_eau_uppercase_conversion(self, db_session):
        """Test que statut et type_nature sont convertis en majuscules"""
        data = {
            "numero_pei": 77777,
            "statut": "public",
            "type_nature": "bi",
            "latitude": 48.0,
            "longitude": 2.0,
            "accessibilite": "C",
            "disponibilite": "DI",
            "carto_ref": 1,
            "press_deb": 5.0,
            "debit_1_bar": 60.0,
            "vol_eau_mi": 0.0,
            "utilisateur": 1
        }
        
        point = create_point_eau(db_session, data)
        assert point.statut == "PUBLIC"
        assert point.type_nature == "BI"


class TestGetAllPointsEau:
    """Tests pour la récupération de tous les points d'eau"""
    
    def test_get_all_points_eau_empty(self, db_session):
        points = get_all_points_eau(db_session)
        assert points == []

    def test_get_all_points_eau_with_data(self, db_session, sample_point):
        points = get_all_points_eau(db_session)
        
        assert len(points) == 1
        assert all(isinstance(p, dict) for p in points)
        assert "latitude" in points[0]
        assert "longitude" in points[0]
        assert "numero_pei" in points[0]

    def test_get_all_points_eau_multiple(self, db_session):
        points_data = [
            {"numero_pei": 1001, "statut": "public", "type_nature": "bi", 
             "latitude": 48.8, "longitude": 2.3, "accessibilite": "C", "disponibilite": "DI", "carto_ref": 1, "press_deb": 0.0, "debit_1_bar": 0.0, "vol_eau_mi": 0.0, "utilisateur": 1},
            {"numero_pei": 1002, "statut": "prive", "type_nature": "pi100", 
             "latitude": 48.9, "longitude": 2.4, "accessibilite": "C", "disponibilite": "DI", "carto_ref": 1, "press_deb": 0.0, "debit_1_bar": 0.0, "vol_eau_mi": 0.0, "utilisateur": 1},
            {"numero_pei": 1003, "statut": "public", "type_nature": "pena", 
             "latitude": 48.7, "longitude": 2.2, "accessibilite": "C", "disponibilite": "DI", "carto_ref": 1, "press_deb": 0.0, "debit_1_bar": 0.0, "vol_eau_mi": 0.0, "utilisateur": 1},
        ]
        
        for data in points_data:
            create_point_eau(db_session, data)
        
        points = get_all_points_eau(db_session)
        assert len(points) == 3


class TestGetPointEauById:
    """Tests pour la récupération par ID"""
    
    def test_get_point_eau_by_id_exists(self, db_session, sample_point):
        point = get_point_eau_by_id(db_session, sample_point.id)
        
        assert point is not None
        assert point["id"] == sample_point.id
        assert point["numero_pei"] == sample_point.numero_pei
        assert "latitude" in point
        assert "longitude" in point

    def test_get_point_eau_by_id_not_exists(self, db_session):
        point = get_point_eau_by_id(db_session, 99999)
        assert point is None


class TestGetPointEauByNumeroPei:
    """Tests pour la récupération par numéro PEI"""
    
    def test_get_point_eau_by_numero_pei_exists(self, db_session, sample_point):
        point = get_point_eau_by_numero_pei(db_session, sample_point.numero_pei)
        
        assert point is not None
        assert point["numero_pei"] == sample_point.numero_pei
        assert point["id"] == sample_point.id
        assert "latitude" in point
        assert "longitude" in point
    
    def test_get_point_eau_by_numero_pei_not_exists(self, db_session):
        with pytest.raises(ValueError, match="Numéro PEI incorrect"):
            get_point_eau_by_numero_pei(db_session, 99999)


class TestUpdatePointEau:
    """Tests pour la mise à jour de points d'eau"""
    
    def test_update_point_eau_statut(self, db_session, sample_point):
        data = {"statut": "PRIVE"}
        updated = update_point_eau_by_id(db_session, sample_point.id, data)
        
        assert updated is not None
        assert updated.statut == "PRIVE"
        assert updated.numero_pei == sample_point.numero_pei

    def test_update_point_eau_multiple_fields(self, db_session, sample_point):
        data = {
            "nom": "Nouveau Nom",
            "press_deb": 6.0,
            "debit_1_bar": 70.0,
            "accessibilite": "NC"
        }
        
        updated = update_point_eau_by_id(db_session, sample_point.id, data)
        
        assert updated is not None
        assert updated.nom == "Nouveau Nom"
        assert updated.press_deb == 6.0
        assert updated.debit_1_bar == 70.0
        assert updated.accessibilite == "NC"

    def test_update_point_eau_coordonnees(self, db_session, sample_point):
        data = {
            "latitude": 45.7640,
            "longitude": 4.8357
        }
        
        updated = update_point_eau_by_id(db_session, sample_point.id, data)
        
        assert updated is not None
        assert updated.geom is not None

    def test_update_point_eau_date_maj(self, db_session, sample_point):
        original_date_maj = sample_point.date_maj
        
        data = {"nom": "Mise à jour"}
        updated = update_point_eau_by_id(db_session, sample_point.id, data)
        
        assert updated.date_maj is not None
        if original_date_maj:
            assert updated.date_maj >= original_date_maj

    def test_update_point_eau_ignore_protected_fields(self, db_session, sample_point):
        original_id = sample_point.id
        original_date_crea = sample_point.date_crea
        
        data = {
            "id": 99999,
            "date_crea": "2000-01-01",
            "nom": "Update"
        }
        
        updated = update_point_eau_by_id(db_session, sample_point.id, data)
        
        assert updated.id == original_id
        assert updated.date_crea == original_date_crea
        assert updated.nom == "Update"

    def test_update_point_eau_not_exists(self, db_session):
        data = {"nom": "Test"}
        with pytest.raises(ValueError, match="Id point incorrect"):
            update_point_eau_by_id(db_session, 99999, data)


class TestDeletePointEau:
    """Tests pour la suppression de points d'eau"""
    
    def test_delete_point_eau_by_id_exists(self, db_session, sample_point):
        point_id = sample_point.id
        
        result = delete_point_eau_by_id(db_session, point_id)
        
        assert result is True
        
        deleted = get_point_eau_by_id(db_session, point_id)
        assert deleted is None

    def test_delete_point_eau_by_id_not_exists(self, db_session):
        result = delete_point_eau_by_id(db_session, 99999)
        assert result is False
    
    def test_delete_point_eau_by_numero_pei_exists(self, db_session, sample_point):
        numero_pei = sample_point.numero_pei
        
        result = delete_point_eau_by_numero_pei(db_session, numero_pei)
        
        assert result is True
        
        with pytest.raises(ValueError, match="Numéro PEI incorrect"):
            get_point_eau_by_numero_pei(db_session, numero_pei)
    
    def test_delete_point_eau_by_numero_pei_not_exists(self, db_session):
        result = delete_point_eau_by_numero_pei(db_session, 99999)
        assert result is False


class TestIntegration:
    """Tests d'intégration CRUD complet"""
    
    def test_integration_full_crud(self, db_session):
        # CREATE
        data = {
            "numero_pei": 88888,
            "nom": "Point Integration",
            "statut": "public",
            "type_nature": "pi150",
            "latitude": 43.2965,
            "longitude": 5.3698,
            "press_deb": 5.0,
            "debit_1_bar": 60.0,
            "vol_eau_mi": 0.0,
            "accessibilite": "C",
            "disponibilite": "DI",
            "carto_ref": 1,
            "utilisateur": 1
        }
        created = create_point_eau(db_session, data)
        assert created.id is not None

        retrieved_by_id = get_point_eau_by_id(db_session, created.id)
        assert retrieved_by_id["numero_pei"] == 88888
        

        retrieved_by_numero = get_point_eau_by_numero_pei(db_session, 88888)
        assert retrieved_by_numero["id"] == created.id
        

        all_points = get_all_points_eau(db_session)
        assert any(p["id"] == created.id for p in all_points)
        

        update_data = {"nom": "Point Mis à Jour", "statut": "PRIVE"}
        updated = update_point_eau_by_id(db_session, created.id, update_data)
        assert updated.nom == "Point Mis à Jour"
        assert updated.statut == "PRIVE"
        

        deleted = delete_point_eau_by_id(db_session, created.id)
        assert deleted is True
        

        not_found = get_point_eau_by_id(db_session, created.id)
        assert not_found is None
    
    def test_integration_crud_with_numero_pei(self, db_session):
        """Test CRUD en utilisant numero_pei"""
        data = {
            "numero_pei": 77777,
            "statut": "public",
            "type_nature": "bi",
            "latitude": 48.0,
            "longitude": 2.0,
            "accessibilite": "C",
            "disponibilite": "DI",
            "carto_ref": 1,
            "press_deb": 5.0,
            "debit_1_bar": 60.0,
            "vol_eau_mi": 0.0,
            "utilisateur": 1
        }
        created = create_point_eau(db_session, data)
        
        found = get_point_eau_by_numero_pei(db_session, 77777)
        assert found is not None
        assert found["id"] == created.id
        
        deleted = delete_point_eau_by_numero_pei(db_session, 77777)
        assert deleted is True
        

        with pytest.raises(ValueError, match="Numéro PEI incorrect"):
            get_point_eau_by_numero_pei(db_session, 77777)


class TestEdgeCases:
    """Tests des cas limites"""
    
    def test_create_with_empty_optional_fields(self, db_session):
        """Test avec des champs optionnels vides"""
        data = {
            "numero_pei": 55555,
            "statut": "public",
            "type_nature": "bi",
            "latitude": 48.0,
            "longitude": 2.0,
            "nom": "",
            "insee5": "",
            "accessibilite": "NC",
            "disponibilite": "DI",
            "carto_ref": 0,
            "press_deb": 0.0,
            "debit_1_bar": 0.0,
            "vol_eau_mi": 0.0,
            "utilisateur": 1
        }
        
        point = create_point_eau(db_session, data)
        assert point is not None
        assert point.nom is None
        assert point.insee5 is None
    
    def test_update_with_none_values(self, db_session, sample_point):
        """Test mise à jour avec valeurs None"""
        data = {
            "press_deb": None,
            "debit_1_bar": None
        }
        
        with pytest.raises(IntegrityError):
            update_point_eau_by_id(db_session, sample_point.id, data)
    
    def test_multiple_deletes_same_point(self, db_session, sample_point):
        """Test suppression multiple du même point"""
        point_id = sample_point.id
        
        # Première suppression
        result1 = delete_point_eau_by_id(db_session, point_id)
        assert result1 is True
        
        # Deuxième suppression
        result2 = delete_point_eau_by_id(db_session, point_id)
        assert result2 is False