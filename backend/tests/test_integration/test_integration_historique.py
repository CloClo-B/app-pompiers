import pytest
import uuid
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from app import models
from app.DAO.DAOHistorique import create_historique, get_all_historique

class TestHistoriqueIntegration:
    """Tests d'intégration pour Historique"""
    
    # ============= FIXTURES =============
    @pytest.fixture
    def sample_utilisateur(self, db_session):
        """Crée un utilisateur pour les tests"""
        utilisateur = models.Utilisateur(
            nom="Dupont",
            prenom="Jean",
            email=f"jean.histo.{uuid.uuid4()}@test.com",
            telephone=f"0602{str(uuid.uuid4().int)[:6]}",
            mot_de_passe="hashed_password",
            role=models.RoleEnum.pompier
        )
        db_session.add(utilisateur)
        db_session.commit()
        db_session.refresh(utilisateur)
        return utilisateur
    
    @pytest.fixture
    def historique_base(self, db_session, sample_utilisateur):
        """Historique réutilisable"""
        payload = {
            "id_utilisateur": sample_utilisateur.id_utilisateur,
            "action": "Action de base",
            "cible": "Historique réutilisable",
            "ip": "127.0.0.1"
        }
        return create_historique(db_session, payload)
    
    # ======== CAS NORMAL ========
    def test_creer_historique_normal(self, db_session, sample_utilisateur):
        """Test de création d'historique normal"""
        payload = {
            "id_utilisateur": sample_utilisateur.id_utilisateur,
            "action": "Vérification du point",
            "cible": "Point #123",
            "ip": "192.168.1.1"
        }
        historique = create_historique(db_session, payload)
        
        assert historique.id_log is not None
        assert historique.action == payload["action"]
        assert historique.cible == payload["cible"]
        assert historique.ip == payload["ip"]
        
        # Vérifier dans get_all
        all_histos = get_all_historique(db_session)
        assert any(h["action"] == payload["action"] for h in all_histos)
    
    # ======== CAS LIMITE ========
    def test_creer_historique_champs_optionnels_none(self, db_session, sample_utilisateur):
        """Test avec champs optionnels à None"""
        payload = {
            "id_utilisateur": sample_utilisateur.id_utilisateur,
            "action": "Action limite",
            "cible": None,
            "ip": None
        }
        historique = create_historique(db_session, payload)
        assert historique.cible is None
        assert historique.ip is None
    
    def test_creer_historique_cible_vide(self, db_session, sample_utilisateur):
        """Test avec cible vide"""
        payload = {
            "id_utilisateur": sample_utilisateur.id_utilisateur,
            "action": "Action limite",
            "cible": "",
            "ip": "127.0.0.1"
        }
        historique = create_historique(db_session, payload)
        assert historique.cible == ""
    
    def test_creer_historique_date_auto(self, db_session, sample_utilisateur):
        """Vérifie que date_action se remplit automatiquement"""
        payload = {
            "id_utilisateur": sample_utilisateur.id_utilisateur,
            "action": "Action date par défaut",
            "cible": "Test",
            "ip": "127.0.0.1"
        }
        historique = create_historique(db_session, payload)
        assert isinstance(historique.date_action, datetime)
        # Vérifier que la date est récente (moins de 5 secondes)
        assert (datetime.now() - historique.date_action).seconds < 5
    
    # ======== CAS D'ERREUR ========
    def test_creer_historique_missing_action(self, db_session, sample_utilisateur):
        """Test sans champ obligatoire 'action'"""
        payload = {
            "id_utilisateur": sample_utilisateur.id_utilisateur,
            "cible": "Test"
        }
        with pytest.raises((KeyError, IntegrityError)):
            create_historique(db_session, payload)
    
    def test_creer_historique_utilisateur_inexistant(self, db_session):
        """Test avec utilisateur inexistant"""
        payload = {
            "id_utilisateur": 99999,
            "action": "Utilisateur inexistant",
            "cible": "Erreur attendue",
            "ip": "127.0.0.1"
        }
        with pytest.raises(IntegrityError):
            create_historique(db_session, payload)
            db_session.commit()
            
    # ======== CAS GET_ALL ========
    def test_get_all_historique_vide(self, db_session):
        """Test get_all sur une base vide"""
        all_histos = get_all_historique(db_session)
        assert all_histos == []
    
    def test_get_all_historique_renvoie_liste(self, db_session, sample_utilisateur):
        """Test get_all avec plusieurs entrées"""
        payload1 = {
            "id_utilisateur": sample_utilisateur.id_utilisateur,
            "action": "Action1",
            "cible": "Test1",
            "ip": "127.0.0.1"
        }
        payload2 = {
            "id_utilisateur": sample_utilisateur.id_utilisateur,
            "action": "Action2",
            "cible": "Test2",
            "ip": "192.168.1.1"
        }
        create_historique(db_session, payload1)
        create_historique(db_session, payload2)
        
        all_histos = get_all_historique(db_session)
        assert len(all_histos) == 2
        
        actions = [h["action"] for h in all_histos]
        assert "Action1" in actions
        assert "Action2" in actions
    
    def test_get_all_historique_format(self, db_session, sample_utilisateur):
        """Test que get_all retourne le bon format"""
        payload = {
            "id_utilisateur": sample_utilisateur.id_utilisateur,
            "action": "Test format",
            "cible": "Format",
            "ip": "127.0.0.1"
        }
        create_historique(db_session, payload)
        
        all_histos = get_all_historique(db_session)
        assert len(all_histos) == 1
        
        histo = all_histos[0]
        assert isinstance(histo, dict)
        assert "action" in histo
        assert "cible" in histo
        assert "ip" in histo
        assert "id_utilisateur" in histo
        # Vérifier qu'il n'y a pas de champs SQLAlchemy internes
        assert "_sa_instance_state" not in histo
    
    # ======== CAS MULTIPLES UTILISATEURS ========
    def test_historique_multiples_utilisateurs(self, db_session):
        """Test avec plusieurs utilisateurs"""
        # Créer 2 utilisateurs
        user1 = models.Utilisateur(
            nom="User1", prenom="Test1",
            email=f"user1.{uuid.uuid4()}@test.com",
            telephone=f"0601{str(uuid.uuid4().int)[:6]}",
            mot_de_passe="pass1", role=models.RoleEnum.public
        )
        user2 = models.Utilisateur(
            nom="User2", prenom="Test2",
            email=f"user2.{uuid.uuid4()}@test.com",
            telephone=f"0602{str(uuid.uuid4().int)[:6]}",
            mot_de_passe="pass2", role=models.RoleEnum.pompier
        )
        db_session.add_all([user1, user2])
        db_session.commit()
        db_session.refresh(user1)
        db_session.refresh(user2)
        
        # Créer historiques pour chaque utilisateur
        create_historique(db_session, {
            "id_utilisateur": user1.id_utilisateur,
            "action": "Action User1",
            "cible": "Test1",
            "ip": "1.1.1.1"
        })
        create_historique(db_session, {
            "id_utilisateur": user2.id_utilisateur,
            "action": "Action User2",
            "cible": "Test2",
            "ip": "2.2.2.2"
        })
        
        all_histos = get_all_historique(db_session)
        assert len(all_histos) == 2
        
        # Vérifier que les actions sont distinctes
        actions = [h["action"] for h in all_histos]
        assert "Action User1" in actions
        assert "Action User2" in actions
    
    # ======== CAS ROLLBACK ========
    def test_rollback_en_cas_erreur(self, db_session, sample_utilisateur):
        """Test que le rollback fonctionne en cas d'erreur"""
        # Créer un historique valide
        create_historique(db_session, {
            "id_utilisateur": sample_utilisateur.id_utilisateur,
            "action": "Action avant erreur",
            "cible": "Test",
            "ip": "127.0.0.1"
        })
        
        # Tenter de créer un historique invalide
        try:
            create_historique(db_session, {
                "id_utilisateur": 99999,  # ID inexistant
                "action": "Action invalide",
                "cible": "Test",
                "ip": "127.0.0.1"
            })
            db_session.commit()
        except IntegrityError:
            db_session.rollback()
        
        # Vérifier que le premier historique existe toujours
        all_histos = get_all_historique(db_session)
        assert len(all_histos) == 1
        assert all_histos[0]["action"] == "Action avant erreur"
