import pytest
from app.DAO import utilisateur_dao
from app import models


class TestUtilisateurDAO:
    """Tests pour le DAO Utilisateur"""
    
    @pytest.fixture
    def sample_user_data(self):
        """Données pour créer un utilisateur de test"""
        return {
            "nom": "Dupont",
            "prenom": "Jean",
            "email": "jean.dupont@test.com",
            "telephone": "0612345678",
            "mot_de_passe": "password123",
            "role": "pompier"
        }

    @pytest.fixture
    def sample_user(self, db_session, sample_user_data):
        """Crée un utilisateur de test"""
        user = utilisateur_dao.create_utilisateur(db_session, sample_user_data)
        assert user is not None, "La création de l'utilisateur de test a échoué"
        return user

    # ============= TESTS CREATE =============
    
    def test_create_utilisateur_complet(self, db_session):
        """Test création d'un utilisateur avec toutes les données"""
        data = {
            "nom": "Martin",
            "prenom": "Marie",
            "email": "marie.martin@test.com",
            "telephone": "0687654321",
            "mot_de_passe": "securepwd",
            "role": "public"
        }
        user = utilisateur_dao.create_utilisateur(db_session, data)
        
        assert user is not None
        assert user.id_utilisateur is not None
        assert user.nom == "Martin"
        assert user.prenom == "Marie"
        assert user.email == "marie.martin@test.com"
        assert user.telephone == "0687654321"
        assert user.role == models.RoleEnum.public
        # Le mot de passe doit être hashé
        assert user.mot_de_passe != "securepwd"

    def test_create_utilisateur_minimal(self, db_session):
        """Test création d'un utilisateur avec données minimales (rôle par défaut)"""
        data = {
            "nom": "Test",
            "prenom": "User",
            "email": "test.user@test.com",
            "telephone": "0611111111",
            "mot_de_passe": "testpass"
        }
        user = utilisateur_dao.create_utilisateur(db_session, data)
        
        assert user is not None
        assert user.role == models.RoleEnum.public  # Rôle par défaut

    def test_create_utilisateur_email_deja_utilise(self, db_session, sample_user):
        """Test création d'un utilisateur avec un email déjà utilisé"""
        data = {
            "nom": "Autre",
            "prenom": "User",
            "email": sample_user.email,  # Email déjà utilisé
            "telephone": "0699999999",
            "mot_de_passe": "password"
        }
        user = utilisateur_dao.create_utilisateur(db_session, data)
        
        # Devrait retourner None si l'email existe déjà
        assert user is None

    # ============= TESTS GET ALL =============
    
    def test_get_all_utilisateur_empty(self, db_session):
        """Test get_all avec une base vide"""
        utilisateurs = utilisateur_dao.get_all_utilisateur(db_session)
        assert utilisateurs == []

    def test_get_all_utilisateur_with_data(self, db_session, sample_user):
        """Test get_all avec des données"""
        utilisateurs = utilisateur_dao.get_all_utilisateur(db_session)
        
        assert len(utilisateurs) == 1
        assert all(isinstance(u, dict) for u in utilisateurs)
        # Vérifier que les mots de passe ne sont pas retournés
        assert all("mot_de_passe" not in u for u in utilisateurs)
        assert all("_sa_instance_state" not in u for u in utilisateurs)

    def test_get_all_utilisateur_multiple(self, db_session):
        """Test get_all avec plusieurs utilisateurs"""
        users_data = [
            {"nom": "User1", "prenom": "Test1", "email": "user1@test.com", 
             "telephone": "0601010101", "mot_de_passe": "pass1"},
            {"nom": "User2", "prenom": "Test2", "email": "user2@test.com", 
             "telephone": "0602020202", "mot_de_passe": "pass2"},
            {"nom": "User3", "prenom": "Test3", "email": "user3@test.com", 
             "telephone": "0603030303", "mot_de_passe": "pass3"},
        ]
        
        for data in users_data:
            utilisateur_dao.create_utilisateur(db_session, data)
        
        utilisateurs = utilisateur_dao.get_all_utilisateur(db_session)
        assert len(utilisateurs) == 3

    # ============= TESTS GET BY ID =============
    
    def test_get_utilisateur_by_id_exists(self, db_session, sample_user):
        """Test get_by_id avec un ID existant"""
        user = utilisateur_dao.get_utilisateur_by_id(db_session, sample_user.id_utilisateur)
        
        assert user is not None
        assert user.id_utilisateur == sample_user.id_utilisateur
        assert user.email == sample_user.email

    def test_get_utilisateur_by_id_not_exists(self, db_session):
        """Test get_by_id avec un ID inexistant"""
        user = utilisateur_dao.get_utilisateur_by_id(db_session, 99999)
        assert user is None

    # ============= TESTS GET BY EMAIL =============
    
    def test_get_utilisateur_by_email_exists(self, db_session, sample_user):
        """Test get_by_email avec un email existant"""
        user = utilisateur_dao.get_utilisateur_by_email(db_session, sample_user.email)
        
        assert user is not None
        assert user.email == sample_user.email
        assert user.nom == sample_user.nom

    def test_get_utilisateur_by_email_not_exists(self, db_session):
        """Test get_by_email avec un email inexistant"""
        user = utilisateur_dao.get_utilisateur_by_email(db_session, "inexistant@test.com")
        assert user is None

    # ============= TESTS UPDATE =============
    
    def test_update_utilisateur_nom_prenom(self, db_session, sample_user):
        """Test update du nom et prénom"""
        data = {"nom": "UpdatedNom", "prenom": "UpdatedPrenom"}
        updated = utilisateur_dao.update_utilisateur_by_id(
            db_session, 
            sample_user.id_utilisateur, 
            data
        )
        
        assert updated is not None
        assert updated.nom == "UpdatedNom"
        assert updated.prenom == "UpdatedPrenom"
        assert updated.email == sample_user.email  # Inchangé

    def test_update_utilisateur_mot_de_passe(self, db_session, sample_user):
        """Test update du mot de passe (doit être hashé)"""
        old_password_hash = sample_user.mot_de_passe
        data = {"mot_de_passe": "nouveau_mot_de_passe"}
        
        updated = utilisateur_dao.update_utilisateur_by_id(
            db_session, 
            sample_user.id_utilisateur, 
            data
        )
        
        assert updated is not None
        assert updated.mot_de_passe != "nouveau_mot_de_passe"  # Doit être hashé
        assert updated.mot_de_passe != old_password_hash  # Doit être différent

    def test_update_utilisateur_email_unique(self, db_session):
        """Test update avec un email déjà utilisé par un autre utilisateur"""
        # Créer deux utilisateurs
        user1 = utilisateur_dao.create_utilisateur(db_session, {
            "nom": "User1", "prenom": "Test1", "email": "user1@test.com",
            "telephone": "0601010101", "mot_de_passe": "pass1"
        })
        user2 = utilisateur_dao.create_utilisateur(db_session, {
            "nom": "User2", "prenom": "Test2", "email": "user2@test.com",
            "telephone": "0602020202", "mot_de_passe": "pass2"
        })
        
        # Essayer de changer l'email de user2 pour celui de user1
        data = {"email": "user1@test.com"}
        
        with pytest.raises(ValueError, match="Email déjà utilisé"):
            utilisateur_dao.update_utilisateur_by_id(db_session, user2.id_utilisateur, data)

    def test_update_utilisateur_ignore_id(self, db_session, sample_user):
        """Test que l'ID ne peut pas être modifié"""
        original_id = sample_user.id_utilisateur
        data = {"id_utilisateur": 99999, "nom": "UpdatedNom"}
        
        updated = utilisateur_dao.update_utilisateur_by_id(
            db_session, 
            sample_user.id_utilisateur, 
            data
        )
        
        assert updated.id_utilisateur == original_id  # ID inchangé
        assert updated.nom == "UpdatedNom"  # Nom changé

    def test_update_utilisateur_not_exists(self, db_session):
        """Test update d'un utilisateur inexistant"""
        data = {"nom": "Test"}
        updated = utilisateur_dao.update_utilisateur_by_id(db_session, 99999, data)
        
        assert updated is None

    # ============= TESTS DELETE =============
    
    def test_delete_utilisateur_exists(self, db_session, sample_user):
        """Test suppression d'un utilisateur existant"""
        user_id = sample_user.id_utilisateur
        email = sample_user.email
        
        result = utilisateur_dao.delete_utilisateur_by_id(db_session, user_id)
        
        assert result is True
        
        # Vérifier que l'utilisateur n'existe plus
        remaining = utilisateur_dao.get_utilisateur_by_email(db_session, email)
        assert remaining is None

    def test_delete_utilisateur_not_exists(self, db_session):
        """Test suppression d'un utilisateur inexistant"""
        result = utilisateur_dao.delete_utilisateur_by_id(db_session, 99999)
        assert result is False

    # ============= TESTS PASSWORD HASHING =============
    
    def test_hash_password(self):
        """Test que le hashage fonctionne"""
        password = "test_password"
        hashed = utilisateur_dao.hash_password(password)
        
        assert hashed != password
        assert len(hashed) > 20  # Un hash Argon2 est long

    def test_verify_password_correct(self):
        """Test vérification d'un mot de passe correct"""
        password = "test_password"
        hashed = utilisateur_dao.hash_password(password)
        
        assert utilisateur_dao.verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test vérification d'un mot de passe incorrect"""
        password = "test_password"
        wrong_password = "wrong_password"
        hashed = utilisateur_dao.hash_password(password)
        
        assert utilisateur_dao.verify_password(wrong_password, hashed) is False

    # ============= TESTS D'INTÉGRATION =============
    
    def test_integration_full_crud(self, db_session):
        """Test d'intégration : cycle CRUD complet"""
        # CREATE
        data = {
            "nom": "Integration",
            "prenom": "Test",
            "email": "integration@test.com",
            "telephone": "0655555555",
            "mot_de_passe": "password",
            "role": "commandement"
        }
        created = utilisateur_dao.create_utilisateur(db_session, data)
        assert created.id_utilisateur is not None
        
        # READ by ID
        retrieved_by_id = utilisateur_dao.get_utilisateur_by_id(
            db_session, 
            created.id_utilisateur
        )
        assert retrieved_by_id.email == "integration@test.com"
        
        # READ by Email
        retrieved_by_email = utilisateur_dao.get_utilisateur_by_email(
            db_session, 
            "integration@test.com"
        )
        assert retrieved_by_email.id_utilisateur == created.id_utilisateur
        
        # UPDATE
        update_data = {"nom": "UpdatedName", "role": "admin"}
        updated = utilisateur_dao.update_utilisateur_by_id(
            db_session, 
            created.id_utilisateur, 
            update_data
        )
        assert updated.nom == "UpdatedName"
        assert updated.role == models.RoleEnum.admin
        
        # DELETE
        deleted = utilisateur_dao.delete_utilisateur_by_id(
            db_session, 
            created.id_utilisateur
        )
        assert deleted is True
        
        # VERIFY DELETE
        not_found = utilisateur_dao.get_utilisateur_by_id(
            db_session, 
            created.id_utilisateur
        )
        assert not_found is None