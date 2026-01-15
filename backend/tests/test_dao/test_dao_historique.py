import pytest
from datetime import datetime
from app.DAO.DAOHistorique import (
    get_all_historique,
    get_historique_by_id,
    get_historique_by_utilisateur,
    get_derniere_action,
    create_historique
)
from app import models
from sqlalchemy.exc import IntegrityError

#========== FIXTURE ==========
@pytest.fixture
def utilisateur_test(db_session):
    """Fixture pour créer un utilisateur de test"""
    user = models.Utilisateur(
        nom="Logs",
        prenom="Admin",
        email="admin.logs@test.com",
        telephone="0102030405",
        mot_de_passe="hashed_password_secure",
        role="admin"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def historique_test(db_session, utilisateur_test):
    """Fixture pour créer une entrée d'historique de test"""
    log = models.Historique(
        id_utilisateur=utilisateur_test.id_utilisateur,
        action="CONNEXION",
        cible="LOGIN_PAGE",
        ip="127.0.0.1"
    )
    db_session.add(log)
    db_session.commit()
    db_session.refresh(log)
    return log


# ============= TESTS UNITAIRES =============
class TestHistoriqueDAOUnitaire:
    """Tests unitaires"""

    """Vérifie qu'une base vide retourne une liste vide."""
    def test_get_all_historique_empty(self, db_session):
        logs = get_all_historique(db_session)
        assert logs == []
    

    """Vérifie que le DAO transforme bien les objets ORM en dictionnaires pour l'API."""
    def test_get_all_historique_returns_list_of_dicts(self, db_session, historique_test):
        logs = get_all_historique(db_session)
        assert len(logs) >= 1
        assert isinstance(logs[0], dict)
        assert logs[0]["action"] == "CONNEXION"


    """Vérifie la récupération précise par clé primaire."""
    def test_get_historique_by_id_exists(self, db_session, historique_test):
        log = get_historique_by_id(db_session, historique_test.id_log)
        assert log is not None
        assert log.id_log == historique_test.id_log
    

    """Vérifie le comportement en cas d'ID inconnu (doit retourner None)."""
    def test_get_historique_by_id_not_exists(self, db_session):
        log = get_historique_by_id(db_session, 99999)
        assert log is None


    """Vérifie le filtrage des actions par utilisateur spécifique."""
    def test_get_historique_by_utilisateur_exists(self, db_session, utilisateur_test, historique_test):
        logs = get_historique_by_utilisateur(db_session, utilisateur_test.id_utilisateur)
        assert len(logs) >= 1
        assert logs[0].id_utilisateur == utilisateur_test.id_utilisateur


    """vérifie que le paramètre limit restreint correctement le nombre de résultats."""
    def test_get_derniere_action_limit(self, db_session, historique_test):
        logs = get_derniere_action(db_session, limit=1)
        assert len(logs) == 1


# ============= TESTS FONCTIONNELS =============
class TestHistoriqueDAOFonctionnel:
    """Tests fonctionnels"""
    
    def test_create_historique_minimal(self, db_session, utilisateur_test):
        data = {
            "id_utilisateur": utilisateur_test.id_utilisateur,
            "action": "UPDATE_POINT",
            "cible": "PEI_123",
            "ip": "192.168.1.1"
        }
        log = create_historique(db_session, data)
        
        assert log.id_log is not None
        assert log.action == "UPDATE_POINT"
        assert log.ip == "192.168.1.1"
        assert isinstance(log.date_action, datetime)

    def test_get_derniere_action_sorting(self, db_session, utilisateur_test):
        """Vérifie que les actions sont bien triées de la plus récente à la plus ancienne"""
        # Création de deux logs à la suite
        create_historique(db_session, {"id_utilisateur": utilisateur_test.id_utilisateur, "action": "FIRST", "cible": "T1"})
        create_historique(db_session, {"id_utilisateur": utilisateur_test.id_utilisateur, "action": "SECOND", "cible": "T2"})
        
        recent_logs = get_derniere_action(db_session, limit=2)
        assert recent_logs[0].action == "SECOND"
        assert recent_logs[1].action == "FIRST"


# ============= TESTS INTÉGRATION =============
class TestHistoriqueDAOIntegration:
    """Tests d'intégration"""
    
    def test_user_activity_flow(self, db_session, utilisateur_test):
        # Simuler une série d'actions utilisateur
        actions = ["LOGIN", "VIEW_MAP", "LOGOUT"]
        for act in actions:
            create_historique(db_session, {
                "id_utilisateur": utilisateur_test.id_utilisateur,
                "action": act,
                "cible": "SYSTEM"
            })
        
        # Récupérer tout l'historique de cet utilisateur
        user_history = get_historique_by_utilisateur(db_session, utilisateur_test.id_utilisateur)
        
        assert len(user_history) == 3
        # Vérification de l'ordre décroissant
        assert user_history[0].action == "LOGOUT"
        assert user_history[-1].action == "LOGIN"


# ============= TESTS SÉCURITÉ =============
class TestHistoriqueDAOSecurity:
    """Tests de sécurité """
    
    def test_create_historique_missing_required_action(self, db_session, utilisateur_test):
        """Vérifie que la création échoue si l'action (obligatoire) est manquante"""
        data = {
            "id_utilisateur": utilisateur_test.id_utilisateur,
            "cible": "TEST"
        }
        with pytest.raises(KeyError):
            create_historique(db_session, data)

    def test_create_historique_invalid_user(self, db_session):
        """Vérifie la contrainte de clé étrangère sur l'utilisateur"""
        data = {
            "id_utilisateur": 99999, # ID inexistant
            "action": "HACK_ATTEMPT",
            "cible": "DATABASE",
            "ip": "0.0.0.0"
        }

        with pytest.raises(IntegrityError):
            create_historique(db_session, data)

    def test_sql_injection_on_ip_field(self, db_session, utilisateur_test):
        """Vérifie que les entrées malveillantes sont traitées comme du texte (via ORM)"""
        malicious_ip = "127.0.0.1'; DROP TABLE historiques; --"
        data = {
            "id_utilisateur": utilisateur_test.id_utilisateur,
            "action": "ATTACK",
            "cible": "SERVER",
            "ip": malicious_ip
        }
        log = create_historique(db_session, data)
        
        assert log.ip == malicious_ip
        # Vérifier que la table existe toujours
        assert get_all_historique(db_session) is not None