import pytest
from app.DAO import DAOHistorique
from app import models
import random


class TestHistoriqueDAO:
    """Tests pour le DAO Historique"""
    # ============= FIXTURES =============

    @pytest.fixture
    def utilisateur_test(self, db_session):
        """Crée un utilisateur valide pour les tests"""
        unique_number = random.randint(10000, 99999)

        user = models.Utilisateur(
            nom="Dupont",
            prenom="Jean",
            email=f"jean.dupont{unique_number}@test.com",
            telephone=f"06{random.randint(1000000, 9999999)}",
            mot_de_passe="hashed",
            role=models.RoleEnum.pompier
        )

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

    @pytest.fixture
    def historiques_test(self, db_session, utilisateur_test):
        """Crée 3 entrées d'historique valides pour un utilisateur"""
        actions = ["Connexion", "Création point d'eau", "Modification mission"]
        logs = []

        for action in actions:
            h = models.Historique(
                id_utilisateur=utilisateur_test.id_utilisateur,
                action=action,
                cible="test",
                ip="127.0.0.1",
            )
            db_session.add(h)
            logs.append(h)

        db_session.commit()
        for h in logs:
            db_session.refresh(h)

        return logs

    # ============= TESTS GET ALL =============

    def test_get_all_historique_empty(self, db_session):
        """La table historique doit être vide avant tout"""
        result = DAOHistorique.get_all_historique(db_session)
        assert result == []

    def test_get_all_historique_with_data(self, db_session, historiques_test):
        result = DAOHistorique.get_all_historique(db_session)

        assert len(result) == 3
        assert all(isinstance(h, dict) for h in result)

        for h in result:
            assert "id_log" in h              # anciennement id_historique
            assert "id_utilisateur" in h
            assert "action" in h
            assert "cible" in h
            assert "ip" in h

        assert all("_sa_instance_state" not in h for h in result)


    # ============= TEST GET BY UTILISATEUR =============

    def test_get_historique_by_utilisateur(self, db_session, utilisateur_test, historiques_test):
        """Récupère tout l'historique d’un utilisateur spécifique"""

        result = DAOHistorique.get_historique_by_utilisateur(
            db_session,
            utilisateur_test.id_utilisateur
        )

        assert len(result) == 3
        assert all(h.id_utilisateur == utilisateur_test.id_utilisateur for h in result)

    def test_get_historique_by_utilisateur_no_logs(self, db_session, utilisateur_test):
        """Un utilisateur sans logs doit retourner une liste vide"""
        result = DAOHistorique.get_historique_by_utilisateur(
            db_session,
            utilisateur_test.id_utilisateur
        )
        assert result == []

    def test_get_historique_by_utilisateur_not_exist(self, db_session):
        """Un id utilisateur inexistant ne doit rien retourner"""
        result = DAOHistorique.get_historique_by_utilisateur(db_session, 99999)
        assert result == []
