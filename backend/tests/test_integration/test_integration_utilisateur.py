import pytest
import uuid
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.DAO.DAOUtilisateurs import (
    create_utilisateur,
    get_all_utilisateur,
    get_utilisateur_by_email,
    update_utilisateur_by_id,
    delete_utilisateur_by_id,
    verify_password
)
from app import models


class TestIntegrationUtilisateur:

    @pytest.fixture
    def unique_user_data(self):
        """Fournit un dictionnaire de données utilisateur unique pour chaque appel."""
        unique_id = uuid.uuid4().hex[:8]
        return {
            "nom": f"Nom_{unique_id}",
            "prenom": f"Prenom_{unique_id}",
            "email": f"user.{unique_id}@test.com",
            "mot_de_passe": "secret123",
            "role": models.RoleEnum.pompier,
            "telephone": f"06{unique_id}"
        }

    @pytest.fixture
    def user_in_db(self, db_session: Session, unique_user_data: dict):
        """Crée et retourne un utilisateur persistant dans la DB pour un test."""
        user = create_utilisateur(db_session, unique_user_data)
        yield user
        if db_session.get(models.Utilisateur, user.id_utilisateur):
            delete_utilisateur_by_id(db_session, user.id_utilisateur)




    def test_crud_utilisateur_full_cycle(self, db_session: Session, unique_user_data: dict):
        user = create_utilisateur(db_session, unique_user_data)
        assert user.id_utilisateur is not None
        assert user.nom == unique_user_data["nom"]
        assert user.mot_de_passe != unique_user_data["mot_de_passe"]
        assert verify_password(unique_user_data["mot_de_passe"], user.mot_de_passe)


        fetched = get_utilisateur_by_email(db_session, unique_user_data["email"])
        assert fetched is not None
        assert fetched.id_utilisateur == user.id_utilisateur

 
        new_password = "newpass123"
        update_data = {"prenom": "Pierre", "mot_de_passe": new_password}
        updated = update_utilisateur_by_id(db_session, user.id_utilisateur, update_data)
        
        assert updated.prenom == "Pierre"
        assert verify_password(new_password, updated.mot_de_passe)
        

        deleted = delete_utilisateur_by_id(db_session, user.id_utilisateur)
        assert deleted is True
        assert get_utilisateur_by_email(db_session, unique_user_data["email"]) is None




    def test_create_utilisateur_minimal_data_and_defaults(self, db_session: Session):
        user_data = {
            "nom": "Martin",
            "prenom": "Marie",
            "email": f"marie.{uuid.uuid4().hex}@test.com",
            "mot_de_passe": "password",
        }
        user = create_utilisateur(db_session, user_data)
        assert user.role == models.RoleEnum.public
        
        assert user.telephone == "" 


    def test_create_utilisateur_email_duplicate_fails(self, db_session: Session, unique_user_data: dict):
        create_utilisateur(db_session, unique_user_data)
        
        duplicate_user_data = unique_user_data.copy()
        duplicate_user_data["telephone"] = f"07{uuid.uuid4().hex[:8]}" 
        duplicate_user = create_utilisateur(db_session, duplicate_user_data)
        assert duplicate_user is None

        
    def test_update_utilisateur_email_conflict_raises_error(self, db_session: Session, unique_user_data: dict):
        user1 = create_utilisateur(db_session, unique_user_data)

        unique_id_2 = uuid.uuid4().hex[:8]
        user2_data = {
            "nom": "Test", "prenom": "Paul", "mot_de_passe": "123456", 
            "email": f"user.{unique_id_2}@test.com", 
            "telephone": f"08{unique_id_2}"
        }
        user2 = create_utilisateur(db_session, user2_data)

        update_data = {"email": user2.email}
        
        with pytest.raises((ValueError, IntegrityError)):
            update_utilisateur_by_id(db_session, user1.id_utilisateur, update_data)


    def test_update_utilisateur_password_hashing(self, db_session: Session, user_in_db: models.Utilisateur):
        old_hash = user_in_db.mot_de_passe
        new_password = "very_secure_new_password"
        
        update_data = {"mot_de_passe": new_password}
        updated = update_utilisateur_by_id(db_session, user_in_db.id_utilisateur, update_data)
        
        assert updated.mot_de_passe != old_hash
        assert verify_password(new_password, updated.mot_de_passe)


    def test_delete_utilisateur_inexistant_returns_false(self, db_session: Session):
        result = delete_utilisateur_by_id(db_session, 99999)
        assert result is False

    def test_get_utilisateur_email_inexistant_returns_none(self, db_session: Session):
        user = get_utilisateur_by_email(db_session, "inconnu@test.com")
        assert user is None

    def test_get_all_utilisateur_returns_list(self, db_session: Session, user_in_db: models.Utilisateur):
        users = get_all_utilisateur(db_session)
        assert isinstance(users, list)
        assert len(users) >= 1
        
        if users and isinstance(users[0], dict):
            emails = [u.get('email') for u in users]
        else:
             emails = [u.email for u in users]
             
        assert user_in_db.email in emails