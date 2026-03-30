import pytest
from app.DAO.DAOUtilisateurs import (
    get_all_utilisateur,
    get_utilisateur_by_id,
    get_utilisateur_by_email,
    create_utilisateur,
    delete_utilisateur_by_id,
    update_utilisateur_by_id,
    update_own_profile,
    change_password,
    verify_user_password,
    hash_password,
    verify_password
)

@pytest.fixture
def sample_user_data():
    """Données d'exemple pour créer un utilisateur"""
    return {
        "nom": "Dupont",
        "prenom": "Jean",
        "email": "jean.dupont@example.com",
        "telephone": "0601020304",
        "mot_de_passe": "Password123!",
        "role": "public"
    }


class TestPasswordHashing:
    """Tests pour le hashage des mots de passe"""
    
    def test_hash_password(self):
        password = "TestPassword123"
        hashed = hash_password(password)
        assert hashed != password
        assert len(hashed) > 0
    
    def test_verify_password_correct(self):
        password = "TestPassword123"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self):
        password = "TestPassword123"
        hashed = hash_password(password)
        assert verify_password("WrongPassword", hashed) is False


class TestCreateUtilisateur:
    """Tests pour la création d'utilisateurs"""
    
    def test_create_utilisateur_success(self, db_session, sample_user_data):
        user = create_utilisateur(db_session, sample_user_data)
        assert user is not None
        assert user.email == "jean.dupont@example.com"
        assert user.nom == "Dupont"
        assert user.mot_de_passe != "Password123!"  # Vérifie le hashage
    
    def test_create_utilisateur_duplicate_email(self, db_session, sample_user_data):
        create_utilisateur(db_session, sample_user_data)
        duplicate = create_utilisateur(db_session, sample_user_data)
        assert duplicate is None
    
    def test_create_utilisateur_default_role(self, db_session, sample_user_data):
        del sample_user_data["role"]
        user = create_utilisateur(db_session, sample_user_data)
        assert user.role == "public"


class TestGetUtilisateur:
    """Tests pour la récupération d'utilisateurs"""
    
    def test_get_all_utilisateur_empty(self, db_session):
        users = get_all_utilisateur(db_session)
        assert users == []
    
    def test_get_all_utilisateur_with_data(self, db_session, sample_user_data):
        create_utilisateur(db_session, sample_user_data)
        users = get_all_utilisateur(db_session)
        
        assert len(users) == 1
        assert "mot_de_passe" not in users[0]
        assert users[0]["email"] == "jean.dupont@example.com"
    
    def test_get_utilisateur_by_id_exists(self, db_session, sample_user_data):
        user = create_utilisateur(db_session, sample_user_data)
        found = get_utilisateur_by_id(db_session, user.id_utilisateur)
        
        assert found is not None
        assert found.email == "jean.dupont@example.com"
    
    def test_get_utilisateur_by_id_not_exists(self, db_session):
        found = get_utilisateur_by_id(db_session, 9999)
        assert found is None
    
    def test_get_utilisateur_by_email_exists(self, db_session, sample_user_data):
        create_utilisateur(db_session, sample_user_data)
        found = get_utilisateur_by_email(db_session, "jean.dupont@example.com")
        
        assert found is not None
        assert found.nom == "Dupont"
    
    def test_get_utilisateur_by_email_not_exists(self, db_session):
        found = get_utilisateur_by_email(db_session, "inexistant@example.com")
        assert found is None


class TestDeleteUtilisateur:
    """Tests pour la suppression d'utilisateurs"""
    
    def test_delete_utilisateur_success(self, db_session, sample_user_data):
        user = create_utilisateur(db_session, sample_user_data)
        result = delete_utilisateur_by_id(db_session, user.id_utilisateur)
        
        assert result is True
        assert get_utilisateur_by_id(db_session, user.id_utilisateur) is None
    
    def test_delete_utilisateur_not_exists(self, db_session):
        result = delete_utilisateur_by_id(db_session, 9999)
        assert result is False


class TestUpdateUtilisateur:
    """Tests pour la mise à jour d'utilisateurs par admin"""
    
    def test_update_utilisateur_success(self, db_session, sample_user_data):
        user = create_utilisateur(db_session, sample_user_data)
        update_data = {"nom": "Martin", "prenom": "Pierre"}
        updated = update_utilisateur_by_id(db_session, user.id_utilisateur, update_data)
        
        assert updated.nom == "Martin"
        assert updated.prenom == "Pierre"
        assert updated.email == "jean.dupont@example.com"
    
    def test_update_utilisateur_not_exists(self, db_session):
        updated = update_utilisateur_by_id(db_session, 9999, {"nom": "Test"})
        assert updated is None
    
    def test_update_utilisateur_email_duplicate(self, db_session, sample_user_data):
        user1 = create_utilisateur(db_session, sample_user_data)
        
        user2_data = sample_user_data.copy()
        user2_data["email"] = "autre.user@test.com"
        user2_data["telephone"] = "0699999999"
        user2 = create_utilisateur(db_session, user2_data)
        
        with pytest.raises(ValueError, match="Email déjà utilisé"):
            update_utilisateur_by_id(db_session, user2.id_utilisateur, {"email": user1.email})

    
    def test_update_utilisateur_password(self, db_session, sample_user_data):
        user = create_utilisateur(db_session, sample_user_data)
        old_hash = user.mot_de_passe
        
        update_data = {"mot_de_passe": "NewPassword456!"}
        updated = update_utilisateur_by_id(db_session, user.id_utilisateur, update_data)
        
        assert updated.mot_de_passe != old_hash
        assert verify_password("NewPassword456!", updated.mot_de_passe)
    
    def test_update_utilisateur_cannot_change_id(self, db_session, sample_user_data):
        user = create_utilisateur(db_session, sample_user_data)
        original_id = user.id_utilisateur
        
        update_data = {"id_utilisateur": 9999, "nom": "Martin"}
        updated = update_utilisateur_by_id(db_session, user.id_utilisateur, update_data)
        
        assert updated.id_utilisateur == original_id
        assert updated.nom == "Martin"


class TestUpdateOwnProfile:
    """Tests pour la mise à jour du profil par l'utilisateur lui-même"""
    
    def test_update_own_profile_success(self, db_session, sample_user_data):
        user = create_utilisateur(db_session, sample_user_data)
        update_data = {"nom": "Nouveau", "telephone": "0699887766"}
        updated = update_own_profile(db_session, user.id_utilisateur, update_data)
        
        assert updated.nom == "Nouveau"
        assert updated.telephone == "0699887766"
    
    def test_update_own_profile_not_exists(self, db_session):
        updated = update_own_profile(db_session, 9999, {"nom": "Test"})
        assert updated is None
    
    def test_update_own_profile_ignore_role(self, db_session, sample_user_data):
        user = create_utilisateur(db_session, sample_user_data)
        
        update_data = {"role": "admin"}
        updated = update_own_profile(db_session, user.id_utilisateur, update_data)
        
        assert updated.role == "public"
    
    def test_update_own_profile_duplicate_email(self, db_session, sample_user_data):
        user1 = create_utilisateur(db_session, sample_user_data)
        
        user2_data = sample_user_data.copy()
        user2_data["email"] = "unique@example.com"
        user2_data["telephone"] = "0701020304"
        user2 = create_utilisateur(db_session, user2_data)
        
        with pytest.raises(ValueError, match="Email déjà utilisé"):
            update_own_profile(db_session, user2.id_utilisateur, {"email": user1.email})
    
    def test_update_own_profile_duplicate_telephone(self, db_session, sample_user_data):
        user1 = create_utilisateur(db_session, sample_user_data)
        
        user2_data = sample_user_data.copy()
        user2_data["email"] = "second@example.com"
        user2_data["telephone"] = "0707070707"
        user2 = create_utilisateur(db_session, user2_data)
        
        with pytest.raises(ValueError, match="Numéro de téléphone déjà utilisé"):
            update_own_profile(db_session, user2.id_utilisateur, {"telephone": user1.telephone})
    
    def test_update_own_profile_only_allowed_fields(self, db_session, sample_user_data):
        user = create_utilisateur(db_session, sample_user_data)
        
        update_data = {
            "nom": "Nouveau",
            "mot_de_passe": "HackedPassword",  
            "role": "admin"  
        }
        updated = update_own_profile(db_session, user.id_utilisateur, update_data)
        
        assert updated.nom == "Nouveau"
        assert updated.role == "public"
        assert verify_password("Password123!", updated.mot_de_passe)


class TestChangePassword:
    """Tests pour le changement de mot de passe"""
    
    def test_change_password_success(self, db_session, sample_user_data):
        user = create_utilisateur(db_session, sample_user_data)
        result = change_password(db_session, user.id_utilisateur, "Password123!", "NewPass123!")
        
        assert result is True
        assert verify_user_password(db_session, user.id_utilisateur, "NewPass123!")
        assert not verify_user_password(db_session, user.id_utilisateur, "Password123!")
    
    def test_change_password_wrong_old_password(self, db_session, sample_user_data):
        user = create_utilisateur(db_session, sample_user_data)
        
        with pytest.raises(ValueError, match="Ancien mot de passe incorrect"):
            change_password(db_session, user.id_utilisateur, "WrongPassword", "NewPass123!")
    
    def test_change_password_user_not_exists(self, db_session):
        result = change_password(db_session, 9999, "old", "new")
        assert result is False


class TestVerifyUserPassword:
    """Tests pour la vérification du mot de passe utilisateur"""
    
    def test_verify_user_password_correct(self, db_session, sample_user_data):
        user = create_utilisateur(db_session, sample_user_data)
        result = verify_user_password(db_session, user.id_utilisateur, "Password123!")
        assert result is True
    
    def test_verify_user_password_incorrect(self, db_session, sample_user_data):
        user = create_utilisateur(db_session, sample_user_data)
        result = verify_user_password(db_session, user.id_utilisateur, "WrongPassword")
        assert result is False
    
    def test_verify_user_password_user_not_exists(self, db_session):
        result = verify_user_password(db_session, 9999, "password")
        assert result is False