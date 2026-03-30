import pytest
from datetime import datetime, timedelta
from app.models import BanUtilisateur, Utilisateur, RoleEnum
from app.DAO.ban.banUtilisateur import verifier_ban_utilisateur


@pytest.fixture
def user_test(db_session):
    """Crée un utilisateur test"""
    user = Utilisateur(
        nom="Dupont",
        prenom="Jean",
        email="jean.dupont@test.com",
        telephone="0601020304",
        mot_de_passe="h",
        role=RoleEnum.public
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


class TestVerifierBanNotBanned:
    """Tests pour utilisateur NON banni"""
    
    def test_utilisateur_not_banned_no_entry(self, db_session, user_test):
        """Pas d'entrée de ban = pas banni"""
        # Should not raise
        verifier_ban_utilisateur(db_session, user_test.id_utilisateur)
    
    def test_utilisateur_not_banned_ban_expired(self, db_session, user_test):
        """Ban expiré (date_fin < now) = pas banni"""
        ban = BanUtilisateur(
            id_utilisateur=user_test.id_utilisateur,
            date_debut=datetime.now() - timedelta(days=10),
            date_fin=datetime.now() - timedelta(days=1),  # Expiré il y a 1 jour
            raison="Raison old"
        )
        db_session.add(ban)
        db_session.commit()
        
        # Should not raise - le ban est expiré
        verifier_ban_utilisateur(db_session, user_test.id_utilisateur)


class TestVerifierBanBanned:
    """Tests pour utilisateur BANNI"""
    
    def test_utilisateur_banned_active(self, db_session, user_test):
        """Ban actif (date_fin > now) = banni"""
        future_date = datetime.now() + timedelta(days=7)
        ban = BanUtilisateur(
            id_utilisateur=user_test.id_utilisateur,
            date_debut=datetime.now(),
            date_fin=future_date,
            raison="Signalements abusifs"
        )
        db_session.add(ban)
        db_session.commit()
        
        # Should raise ValueError
        with pytest.raises(ValueError) as exc_info:
            verifier_ban_utilisateur(db_session, user_test.id_utilisateur)
        
        assert "Vous êtes banni jusqu'au" in str(exc_info.value)
        assert str(future_date) in str(exc_info.value)
    
    def test_utilisateur_banned_error_message_contains_date(self, db_session, user_test):
        """Message d'erreur contient la date fin du ban"""
        future_date = datetime.now() + timedelta(days=5)
        ban = BanUtilisateur(
            id_utilisateur=user_test.id_utilisateur,
            date_fin=future_date,
            raison="Proposition incorrigible"
        )
        db_session.add(ban)
        db_session.commit()
        
        with pytest.raises(ValueError) as exc_info:
            verifier_ban_utilisateur(db_session, user_test.id_utilisateur)
        
        error_msg = str(exc_info.value)
        assert "Vous êtes banni" in error_msg
        assert "jusqu'au" in error_msg


class TestVerifierBanMultipleUsers:
    """Tests avec plusieurs utilisateurs"""
    
    def test_ban_only_affects_target_user(self, db_session):
        """Ban d'un utilisateur n'affecte pas l'autre"""
        user1 = Utilisateur(
            nom="User1", prenom="One", email="user1@test.com",
            telephone="0601020304", mot_de_passe="h", role=RoleEnum.public
        )
        user2 = Utilisateur(
            nom="User2", prenom="Two", email="user2@test.com",
            telephone="0601020305", mot_de_passe="h", role=RoleEnum.public
        )
        db_session.add(user1)
        db_session.add(user2)
        db_session.commit()
        
        # Ban user1
        ban = BanUtilisateur(
            id_utilisateur=user1.id_utilisateur,
            date_fin=datetime.now() + timedelta(days=3),
            raison="Spam"
        )
        db_session.add(ban)
        db_session.commit()
        
        # user1 doit être banni
        with pytest.raises(ValueError):
            verifier_ban_utilisateur(db_session, user1.id_utilisateur)
        
        # user2 ne doit pas être banni
        verifier_ban_utilisateur(db_session, user2.id_utilisateur)
    
    def test_nonexistent_user_not_banned(self, db_session):
        """Utilisateur inexistant n'est pas banni"""
        # Should not raise - pas de ban trouvé
        verifier_ban_utilisateur(db_session, 9999)


class TestBanEdgeCases:
    """Tests des cas limites"""
    
    def test_ban_with_null_raison(self, db_session, user_test):
        """Ban sans raison spécifiée"""
        ban = BanUtilisateur(
            id_utilisateur=user_test.id_utilisateur,
            date_fin=datetime.now() + timedelta(days=2),
            raison=None  # Pas de raison
        )
        db_session.add(ban)
        db_session.commit()
        
        with pytest.raises(ValueError):
            verifier_ban_utilisateur(db_session, user_test.id_utilisateur)
    
    def test_multiple_bans_only_active_matters(self, db_session, user_test):
        """Si plusieurs bans, seul l'actif (date_fin > now) compte"""
        # Ban expiré
        old_ban = BanUtilisateur(
            id_utilisateur=user_test.id_utilisateur,
            date_fin=datetime.now() - timedelta(days=5),
            raison="Ancien ban"
        )
        db_session.add(old_ban)
        db_session.commit()
        
        # À ce stade, utilisateur ne doit pas être banni (old_ban est expiré)
        verifier_ban_utilisateur(db_session, user_test.id_utilisateur)
        
        # Ajouter un ban actif
        active_ban = BanUtilisateur(
            id_utilisateur=user_test.id_utilisateur,
            date_fin=datetime.now() + timedelta(days=3),
            raison="Nouveau ban"
        )
        db_session.add(active_ban)
        db_session.commit()
        
        # Maintenant utilisateur doit être banni (active_ban > now)
        with pytest.raises(ValueError):
            verifier_ban_utilisateur(db_session, user_test.id_utilisateur)
