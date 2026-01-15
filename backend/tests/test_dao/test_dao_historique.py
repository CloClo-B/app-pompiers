import pytest
import random
from app.DAO import DAOHistorique
from app import models

class TestHistoriqueDAO:
    """Tests pour le DAO Historique utilisant la db_session PostgreSQL"""

    # ============= FIXTURES =============

    @pytest.fixture
    def utilisateur_test(self, db_session):
        """Crée un utilisateur unique pour lier les historiques"""
        # Utilisation de random pour garantir l'unicité des champs contraints
        unique_id = random.randint(1000, 9999)
        user = models.Utilisateur(
            nom="Testeur",
            prenom="Historique",
            email=f"test.hist{unique_id}@example.com",
            telephone=f"07{random.randint(10000000, 99999999)}",
            mot_de_passe="password_hash",
            role="public"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

    @pytest.fixture
    def historiques_test(self, db_session, utilisateur_test):
        """Crée des entrées d'historique pour les tests de récupération"""
        logs_data = [
            {"action": "Connexion", "cible": "Auth", "ip": "127.0.0.1"},
            {"action": "Création", "cible": "Point Eau", "ip": "192.168.1.1"},
            {"action": "Suppression", "cible": "Mission", "ip": "10.0.0.1"}
        ]
        
        logs = []
        for data in logs_data:
            h = models.Historique(
                id_utilisateur=utilisateur_test.id_utilisateur,
                action=data["action"],
                cible=data["cible"],
                ip=data["ip"]
            )
            db_session.add(h)
            logs.append(h)
            
        db_session.commit()
        for h in logs:
            db_session.refresh(h)
        return logs

    # ============= TESTS GET ALL =============

    def test_get_all_historique_empty(self, db_session):
        """Vérifie que la table est vide (grâce au clean_database de conftest)"""
        result = DAOHistorique.get_all_historique(db_session)
        assert result == []

    def test_get_all_historique_with_data(self, db_session, historiques_test):
        """Vérifie la récupération de tous les logs et le format dictionnaire"""
        result = DAOHistorique.get_all_historique(db_session)

        assert len(result) == 3
        # On vérifie que c'est bien une liste de dictionnaires
        assert isinstance(result[0], dict)
        
        # on vérifie que les actions créées sont bien présentes dans le résultat
        actions_recuperees = [h["action"] for h in result]
        assert "Connexion" in actions_recuperees
        assert "Création" in actions_recuperees
        assert "Suppression" in actions_recuperees

        # On vérifie la présence des clés obligatoires
        assert "id_log" in result[0]
        assert "ip" in result[0]

    # ============= TESTS GET BY ID / USER =============

    def test_get_historique_by_id(self, db_session, historiques_test):
        target_log = historiques_test[0]
        result = DAOHistorique.get_historique_by_id(db_session, target_log.id_log)
        
        assert result is not None
        assert result.id_log == target_log.id_log
        assert result.action == target_log.action

    def test_get_historique_by_utilisateur(self, db_session, utilisateur_test, historiques_test):
        result = DAOHistorique.get_historique_by_utilisateur(
            db_session, 
            utilisateur_test.id_utilisateur
        )
        assert len(result) == 3
        assert result[0].id_utilisateur == utilisateur_test.id_utilisateur

    # ============= TEST CREATE =============

    def test_create_historique(self, db_session, utilisateur_test):
        new_log_data = {
            "id_utilisateur": utilisateur_test.id_utilisateur,
            "action": "TEST_ACTION",
            "cible": "UNIT_TEST",
            "ip": "8.8.8.8"
        }
        
        created = DAOHistorique.create_historique(db_session, new_log_data)
        
        assert created.id_log is not None
        assert created.action == "TEST_ACTION"
        
        # Vérification en base
        db_log = DAOHistorique.get_historique_by_id(db_session, created.id_log)
        assert db_log.ip == "8.8.8.8"

    # ============= TEST DERNIERES ACTIONS =============

    def test_get_derniere_action_limit(self, db_session, historiques_test):
        # On demande seulement 2 actions sur les 3 créées
        result = DAOHistorique.get_derniere_action(db_session, limit=2)
        assert len(result) == 2