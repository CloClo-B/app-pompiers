import pytest
import os
import tempfile
from app.DAO.DAOSignaler import (
    get_all_signale,
    get_signale_by_id_point,
    create_signale,
    delete_signale_by_id_point,
    update_signale,
)
from app import models
from geoalchemy2.elements import WKTElement
from pyproj import Transformer


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
        numero_pei=54321,
        nom="Point Signalement Test",
        statut="PUBLIC",
        type_nature="BI",
        insee5="75001",
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
def signalement_test(db_session, point_test, utilisateur_test):
    """Crée un signalement de test"""
    signalement = models.Signaler(
        id_point=point_test.numero_pei,
        probleme="Fuite d'eau",
        photo="test_photo.jpg",
        id_utilisateur=utilisateur_test.id_utilisateur
    )
    db_session.add(signalement)
    db_session.commit()
    db_session.refresh(signalement)
    return signalement


class TestGetAllSignale:
    """Tests pour la récupération de tous les signalements"""
    
    def test_get_all_signale_empty(self, db_session):
        signalements = get_all_signale(db_session)
        assert signalements == []
        assert isinstance(signalements, list)
    
    def test_get_all_signale_with_data(self, db_session, signalement_test):
        signalements = get_all_signale(db_session)
        
        assert len(signalements) >= 1
        assert isinstance(signalements, list)
        assert all(isinstance(s, dict) for s in signalements)
        assert any(s["id"] == signalement_test.id for s in signalements)
    
    def test_get_all_signale_multiple(self, db_session, point_test, utilisateur_test):
        """Test avec plusieurs signalements"""
        for i in range(3):
            sig = models.Signaler(
                id_point=point_test.numero_pei,
                probleme=f"Probleme {i}",
                photo=f"photo_{i}.jpg",
                id_utilisateur=utilisateur_test.id_utilisateur
            )
            db_session.add(sig)
            db_session.commit()
        
        signalements = get_all_signale(db_session)
        assert len(signalements) >= 3
    
    def test_get_all_signale_contains_expected_fields(self, db_session, signalement_test):
        """Test que les signalements contiennent tous les champs attendus"""
        signalements = get_all_signale(db_session)
        
        sig = signalements[0]
        assert "id" in sig
        assert "id_point" in sig
        assert "probleme" in sig
        assert "photo" in sig
        assert "id_utilisateur" in sig
        assert "date_creation" in sig


class TestGetSignaleByIdPoint:
    """Tests pour la récupération par ID point"""
    
    def test_get_signale_by_id_point_exists(self, db_session, signalement_test, point_test):
        signalements = get_signale_by_id_point(db_session, point_test.numero_pei)
        
        assert len(signalements) >= 1
        assert signalements[0]["id_point"] == point_test.numero_pei
        assert signalements[0]["probleme"] == signalement_test.probleme
    
    def test_get_signale_by_id_point_not_exists(self, db_session):
        signalements = get_signale_by_id_point(db_session, 99999)
        assert signalements == []
    
    def test_get_signale_by_id_point_multiple(self, db_session, point_test, utilisateur_test):
        """Test plusieurs signalements pour le même point"""
        for i in range(3):
            sig = models.Signaler(
                id_point=point_test.numero_pei,
                probleme=f"Probleme {i}",
                photo=f"photo_{i}.jpg",
                id_utilisateur=utilisateur_test.id_utilisateur
            )
            db_session.add(sig)
            db_session.commit()
        
        signalements = get_signale_by_id_point(db_session, point_test.numero_pei)
        assert len(signalements) == 3
        assert all(s["id_point"] == point_test.numero_pei for s in signalements)
    
    def test_get_signale_by_id_point_contains_expected_fields(self, db_session, signalement_test, point_test):
        """Test que les champs retournés sont corrects"""
        signalements = get_signale_by_id_point(db_session, point_test.numero_pei)
        
        sig = signalements[0]
        assert "id" in sig
        assert "id_point" in sig
        assert "probleme" in sig
        assert "photo" in sig
        assert "id_utilisateur" in sig
        assert "date_creation" in sig


class TestCreateSignale:
    """Tests pour la création de signalements"""
    
    def test_create_signale_complet(self, db_session, point_test, utilisateur_test):
        signale_data = {
            "id_point": point_test.numero_pei,
            "probleme": "Probleme complet",
            "photo": "photo_complete.jpg",
            "id_utilisateur": utilisateur_test.id_utilisateur
        }
        
        signalement = create_signale(db_session, signale_data)
        
        assert signalement is not None
        assert signalement.id is not None
        assert signalement.id_point == point_test.numero_pei
        assert signalement.probleme == "Probleme complet"
        assert signalement.photo == "photo_complete.jpg"
        assert signalement.id_utilisateur == utilisateur_test.id_utilisateur
        assert signalement.date_creation is not None
    
    def test_create_signale_without_photo(self, db_session, point_test, utilisateur_test):
        """Test création sans photo (en envoyant une chaîne vide pour respecter le NOT NULL)"""
        signale_data = {
            "id_point": point_test.numero_pei,
            "probleme": "Probleme sans photo",
            "photo": "",  
            "id_utilisateur": utilisateur_test.id_utilisateur
        }
        
        signalement = create_signale(db_session, signale_data)
        
        assert signalement is not None
        assert signalement.photo == ""
    
    def test_create_signale_invalid_point(self, db_session, utilisateur_test):
        """Test création avec un id_point invalide"""
        signale_data = {
            "id_point": 99999,
            "probleme": "Probleme",
            "photo": "", 
            "id_utilisateur": utilisateur_test.id_utilisateur
        }
        
        with pytest.raises(ValueError, match="id_point est invalide"):
            create_signale(db_session, signale_data)
    
    def test_create_signale_invalid_user(self, db_session, point_test):
        """Test création avec un id_utilisateur invalide"""
        signale_data = {
            "id_point": point_test.numero_pei,
            "probleme": "Probleme",
            "photo": None,
            "id_utilisateur": 99999
        }
        
        with pytest.raises(ValueError, match="id_utilisateur est introuvable"):
            create_signale(db_session, signale_data)
    
    def test_create_multiple_signale_same_point(self, db_session, point_test, utilisateur_test):
        """Test création de plusieurs signalements pour le même point"""
        for i in range(3):
            signale_data = {
                "id_point": point_test.numero_pei,
                "probleme": f"Probleme {i}",
                "photo": f"photo_{i}.jpg",
                "id_utilisateur": utilisateur_test.id_utilisateur
            }
            sig = create_signale(db_session, signale_data)
            assert sig is not None
        
        signalements = get_signale_by_id_point(db_session, point_test.numero_pei)
        assert len(signalements) == 3


class TestDeleteSignale:
    """Tests pour la suppression de signalements"""
    
    def test_delete_signale_by_id_point_exists(self, db_session, signalement_test, point_test):
        result = delete_signale_by_id_point(db_session, point_test.numero_pei)
        
        assert result is True
        
        signalements = get_signale_by_id_point(db_session, point_test.numero_pei)
        assert signalements == []
    
    def test_delete_signale_by_id_point_not_exists(self, db_session):
        result = delete_signale_by_id_point(db_session, 99999)
        assert result is False
    
    def test_delete_signale_multiple(self, db_session, point_test, utilisateur_test):
        """Test suppression de plusieurs signalements d'un coup"""
        # Créer 3 signalements
        for i in range(3):
            sig = models.Signaler(
                id_point=point_test.numero_pei,
                probleme=f"Probleme {i}",
                photo=f"photo_{i}.jpg",
                id_utilisateur=utilisateur_test.id_utilisateur
            )
            db_session.add(sig)
            db_session.commit()
        
        # Vérifier qu'ils existent
        signalements = get_signale_by_id_point(db_session, point_test.numero_pei)
        assert len(signalements) == 3
        
        # Supprimer tous les signalements du point
        result = delete_signale_by_id_point(db_session, point_test.numero_pei)
        assert result is True
        
        # Vérifier qu'ils ont été supprimés
        signalements = get_signale_by_id_point(db_session, point_test.numero_pei)
        assert signalements == []
    
    def test_delete_signale_with_real_photo(self, db_session, point_test, utilisateur_test):
        """Test suppression avec fichier photo réel"""
        # Créer un fichier temporaire
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.jpg') as f:
            temp_photo = f.name
            f.write("test photo content")
        
        try:
            # Créer signalement avec photo réelle
            sig = models.Signaler(
                id_point=point_test.numero_pei,
                probleme="Probleme avec photo",
                photo=temp_photo,
                id_utilisateur=utilisateur_test.id_utilisateur
            )
            db_session.add(sig)
            db_session.commit()
            
            # Vérifier que le fichier existe
            assert os.path.exists(temp_photo)
            
            # Supprimer le signalement
            result = delete_signale_by_id_point(db_session, point_test.numero_pei)
            assert result is True
            
            # Vérifier que le fichier a été supprimé
            assert not os.path.exists(temp_photo)
        
        finally:
            # Nettoyage au cas où
            if os.path.exists(temp_photo):
                os.remove(temp_photo)
    
    def test_delete_signale_twice(self, db_session, signalement_test, point_test):
        """Test suppression deux fois de suite"""
        result1 = delete_signale_by_id_point(db_session, point_test.numero_pei)
        assert result1 is True
        
        result2 = delete_signale_by_id_point(db_session, point_test.numero_pei)
        assert result2 is False


class TestUpdateSignale:
    """Tests pour la mise à jour de signalements"""
    
    def test_update_signale_probleme(self, db_session, signalement_test, point_test):
        update_data = {"probleme": "Probleme mis a jour"}
        updated = update_signale(db_session, point_test.numero_pei, update_data)
        
        assert updated is not None
        assert updated.probleme == "Probleme mis a jour"
        assert updated.id_point == point_test.numero_pei
    
    def test_update_signale_photo(self, db_session, signalement_test, point_test):
        update_data = {"photo": "nouvelle_photo.jpg"}
        updated = update_signale(db_session, point_test.numero_pei, update_data)
        
        assert updated is not None
        assert updated.photo == "nouvelle_photo.jpg"
    
    def test_update_signale_multiple_fields(self, db_session, signalement_test, point_test):
        update_data = {
            "probleme": "Nouveau probleme",
            "photo": "nouvelle_photo.jpg"
        }
        updated = update_signale(db_session, point_test.numero_pei, update_data)
        
        assert updated is not None
        assert updated.probleme == "Nouveau probleme"
        assert updated.photo == "nouvelle_photo.jpg"
    
    def test_update_signale_ignore_id_point(self, db_session, signalement_test, point_test):
        """Test que id_point ne peut pas être modifié"""
        original_id_point = signalement_test.id_point
        
        update_data = {
            "id_point": 88888,
            "probleme": "Probleme modifie"
        }
        updated = update_signale(db_session, point_test.numero_pei, update_data)
        
        assert updated.id_point == original_id_point
        assert updated.probleme == "Probleme modifie"
    
    def test_update_signale_not_exists(self, db_session):
        update_data = {"probleme": "Test"}
        updated = update_signale(db_session, 99999, update_data)
        
        assert updated is None
    
    def test_update_signale_clear_photo(self, db_session, signalement_test, point_test):
        """Test pour vider la photo (remplacement par une chaîne vide)"""
        update_data = {"photo": ""}  
        updated = update_signale(db_session, point_test.numero_pei, update_data)
        
        assert updated is not None
        assert updated.photo == ""
    
    def test_update_signale_with_same_values(self, db_session, signalement_test, point_test):
        """Test mise à jour avec les mêmes valeurs"""
        update_data = {
            "probleme": signalement_test.probleme,
            "photo": signalement_test.photo
        }
        updated = update_signale(db_session, point_test.numero_pei, update_data)
        
        assert updated is not None
        assert updated.probleme == signalement_test.probleme


class TestIntegration:
    """Tests d'intégration CRUD complet"""
    
    def test_integration_full_crud(self, db_session, point_test, utilisateur_test):
        signale_data = {
            "id_point": point_test.numero_pei,
            "probleme": "Integration CRUD",
            "photo": "integration.jpg",
            "id_utilisateur": utilisateur_test.id_utilisateur
        }
        created = create_signale(db_session, signale_data)
        assert created.id is not None
        
        signalements = get_signale_by_id_point(db_session, point_test.numero_pei)
        assert len(signalements) >= 1
        assert any(s["id"] == created.id for s in signalements)
        
        all_signalements = get_all_signale(db_session)
        assert any(s["id"] == created.id for s in all_signalements)

        update_data = {"probleme": "Probleme mis a jour", "photo": "nouvelle.jpg"}
        updated = update_signale(db_session, point_test.numero_pei, update_data)
        assert updated.probleme == "Probleme mis a jour"
        assert updated.photo == "nouvelle.jpg"

        deleted = delete_signale_by_id_point(db_session, point_test.numero_pei)
        assert deleted is True

        signalements = get_signale_by_id_point(db_session, point_test.numero_pei)
        assert signalements == []
    
    def test_integration_multiple_points(self, db_session, utilisateur_test):
        """Test avec plusieurs points d'eau"""
        transformer = Transformer.from_crs("EPSG:4326", "EPSG:2154")
        
        # Créer 2 points d'eau
        points = []
        for i in range(2):
            x, y = transformer.transform(48.8 + i * 0.1, 2.3 + i * 0.1)
            wkt = WKTElement(f"POINT({x} {y})", srid=2154)
            
            point = models.PointEau(
                numero_pei=60000 + i,
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
            db_session.refresh(point)
            points.append(point)
        
        # Créer signalements pour chaque point
        for i, point in enumerate(points):
            signale_data = {
                "id_point": point.numero_pei,
                "probleme": f"Probleme point {i}",
                "photo": f"photo_{i}.jpg",
                "id_utilisateur": utilisateur_test.id_utilisateur
            }
            create_signale(db_session, signale_data)
        
        # Vérifier que chaque point a son signalement
        for point in points:
            sigs = get_signale_by_id_point(db_session, point.numero_pei)
            assert len(sigs) == 1


class TestEdgeCases:
    """Tests des cas limites"""
    
    def test_create_signale_empty_probleme(self, db_session, point_test, utilisateur_test):
        """Test création avec problème vide mais photo présente"""
        signale_data = {
            "id_point": point_test.numero_pei,
            "probleme": "",
            "photo": "photo_par_defaut.jpg",
            "id_utilisateur": utilisateur_test.id_utilisateur
        }
        
        signalement = create_signale(db_session, signale_data)
        assert signalement is not None
        assert signalement.probleme == ""
    
    def test_update_signale_empty_fields(self, db_session, signalement_test, point_test):
        """Test mise à jour avec champs vides"""
        update_data = {"probleme": ""}
        updated = update_signale(db_session, point_test.numero_pei, update_data)
        
        assert updated is not None
        assert updated.probleme == ""
    
    def test_get_signale_by_id_point_after_multiple_creates(self, db_session, point_test, utilisateur_test):
        """Test récupération après plusieurs créations successives"""
        for i in range(5):
            signale_data = {
                "id_point": point_test.numero_pei,
                "probleme": f"Probleme {i}",
                "photo": f"photo_{i}.jpg",
                "id_utilisateur": utilisateur_test.id_utilisateur
            }
            create_signale(db_session, signale_data)
        
        signalements = get_signale_by_id_point(db_session, point_test.numero_pei)
        assert len(signalements) == 5
        
        # Vérifier que tous ont le bon id_point
        assert all(s["id_point"] == point_test.numero_pei for s in signalements)