import pytest
from datetime import datetime
from app.models import SignalementQuota, Utilisateur, RoleEnum
from app.DAO.compteur.quotaSignalement import verifier_quota_signalement


@pytest.fixture
def public_user(db_session):
    """Crée un utilisateur avec rôle public"""
    user = Utilisateur(
        nom="Public", prenom="User",
        email="public@test.com",
        telephone="0601020304",
        mot_de_passe="h",
        role=RoleEnum.public
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def pompier_user(db_session):
    """Crée un utilisateur avec rôle pompier"""
    user = Utilisateur(
        nom="Pompier", prenom="Jean",
        email="pompier@test.com",
        telephone="0601020305",
        mot_de_passe="h",
        role=RoleEnum.pompier
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def admin_user(db_session):
    """Crée un utilisateur avec rôle admin"""
    user = Utilisateur(
        nom="Admin", prenom="System",
        email="admin@test.com",
        telephone="0601020306",
        mot_de_passe="h",
        role=RoleEnum.admin
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


class TestSignalementQuotaPublicUser:
    """Tests quota signalement pour utilisateur public (limite 3)"""
    
    def test_first_signalement_no_error(self, db_session, public_user):
        """Premier signalement crée l'entrée quota"""
        verifier_quota_signalement(db_session, public_user.id_utilisateur, "public")
        
        quota = db_session.query(SignalementQuota).filter(
            SignalementQuota.id_utilisateur == public_user.id_utilisateur
        ).first()
        
        assert quota is not None
        assert quota.nb_signalements == 1
    
    def test_signalement_increment_counter(self, db_session, public_user):
        """Chaque appel incrémente le compteur"""
        for i in range(1, 4):
            verifier_quota_signalement(db_session, public_user.id_utilisateur, public_user.role)
            
            quota = db_session.query(SignalementQuota).filter(
                SignalementQuota.id_utilisateur == public_user.id_utilisateur
            ).first()
            assert quota.nb_signalements == i
    
    def test_limit_3_reached(self, db_session, public_user):
        """À 3, l'utilisateur public doit être bloqué"""
        # Atteindre 3
        for _ in range(3):
            verifier_quota_signalement(db_session, public_user.id_utilisateur, public_user.role)
        
        # 4e appel doit générer une erreur
        with pytest.raises(ValueError) as exc_info:
            verifier_quota_signalement(db_session, public_user.id_utilisateur, public_user.role)
        
        assert "Limite quotidienne de 3 atteinte" in str(exc_info.value)


class TestSignalementQuotaPompierUser:
    """Tests quota signalement pour pompier/commandement (limite 10)"""
    
    def test_pompier_limit_10_reached(self, db_session, pompier_user):
        """Pompier autorisé jusqu'à 10"""
        # Atteindre 10
        for _ in range(10):
            verifier_quota_signalement(db_session, pompier_user.id_utilisateur, pompier_user.role)
        
        # 11e appel doit générer une erreur
        with pytest.raises(ValueError) as exc_info:
            verifier_quota_signalement(db_session, pompier_user.id_utilisateur, pompier_user.role)
        
        assert "Limite quotidienne de 10 atteinte" in str(exc_info.value)
    
    def test_commandement_limit_10_reached(self, db_session, pompier_user):
        """Commandement a aussi limite 10"""
        # Atteindre 10
        for _ in range(10):
            verifier_quota_signalement(db_session, pompier_user.id_utilisateur, "commandement")
        
        # 11e appel doit générer une erreur
        with pytest.raises(ValueError) as exc_info:
            verifier_quota_signalement(db_session, pompier_user.id_utilisateur, "commandement")
        
        assert "Limite quotidienne de 10 atteinte" in str(exc_info.value)


class TestSignalementQuotaAdminUser:
    """Tests quota signalement pour admin (pas de limite)"""
    
    def test_admin_no_limit(self, db_session, admin_user):
        """Admin n'a pas de limite (pas de vérification)"""
        # Admin est complètement ignoré par la fonction
        # car il n'y a pas de clause spéciale pour "admin"
        # La fonction ne devrait pas ajouter de contrainte
        for _ in range(20):
            verifier_quota_signalement(db_session, admin_user.id_utilisateur, admin_user.role)
        
        # Vérifier que le compteur augmente sans limite
        quota = db_session.query(SignalementQuota).filter(
            SignalementQuota.id_utilisateur == admin_user.id_utilisateur
        ).first()
        
        # Pour admin, il n'y a pas de logique spéciale, donc pas de vérification
        # La fonction ne lève pas d'erreur
        assert quota is not None


class TestSignalementQuotaEdgeCases:
    """Tests des cas limites"""
    
    def test_different_users_independent_quotas(self, db_session, public_user, pompier_user):
        """Les quotas d'utilisateurs différents sont indépendants"""
        # Public user atteint limite 3
        for _ in range(3):
            verifier_quota_signalement(db_session, public_user.id_utilisateur, public_user.role)
        
        # Pompier user peut toujours signaler
        verifier_quota_signalement(db_session, pompier_user.id_utilisateur, pompier_user.role)
        
        # Public user bloqué
        with pytest.raises(ValueError):
            verifier_quota_signalement(db_session, public_user.id_utilisateur, public_user.role)
        
        # Pompier peut toujours continuer jusqu'à 10
        for _ in range(9):
            verifier_quota_signalement(db_session, pompier_user.id_utilisateur, pompier_user.role)
    
    def test_quota_persists_across_calls(self, db_session, public_user):
        """Le quota persiste entre les appels"""
        verifier_quota_signalement(db_session, public_user.id_utilisateur, public_user.role)
        
        quota1 = db_session.query(SignalementQuota).filter(
            SignalementQuota.id_utilisateur == public_user.id_utilisateur
        ).first()
        assert quota1.nb_signalements == 1
        
        # Nouvel appel à la DB pour simuler nouvelle requête
        verifier_quota_signalement(db_session, public_user.id_utilisateur, public_user.role)
        
        quota2 = db_session.query(SignalementQuota).filter(
            SignalementQuota.id_utilisateur == public_user.id_utilisateur
        ).first()
        assert quota2.nb_signalements == 2
