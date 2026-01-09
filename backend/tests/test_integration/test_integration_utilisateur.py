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
        """Fournit des données utilisateur valides et uniques."""
        unique_id = uuid.uuid4().hex[:6]
        return {
            "nom": f"Nom{unique_id}",
            "prenom": f"Prenom{unique_id}",
            "email": f"test.{unique_id}@fenalim.fr",
            "mot_de_passe": "MotDePasseTresSecret123!",
            "telephone": f"06{random_digits(8)}",  # Générateur de 8 chiffres
            "role": models.RoleEnum.pompier
        }

    @pytest.fixture
    def user_in_db(self, db_session: Session, unique_user_data: dict):
        """Fixture pour avoir un utilisateur prêt en base."""
        user = create_utilisateur(db_session, unique_user_data)
        yield user
        db_session.query(models.Utilisateur).filter_by(id_utilisateur=user.id_utilisateur).delete()
        db_session.commit()

    # ================= TESTS CRUD =================

    def test_create_utilisateur_success(self, db_session: Session, unique_user_data: dict):
        """Vérifie la création et le hachage automatique du mot de passe."""
        user = create_utilisateur(db_session, unique_user_data)
        
        assert user is not None
        assert user.id_utilisateur is not None
        assert user.email == unique_user_data["email"]
        assert user.mot_de_passe != unique_user_data["mot_de_passe"]
        assert verify_password(unique_user_data["mot_de_passe"], user.mot_de_passe)

    def test_get_utilisateur_by_email(self, db_session: Session, user_in_db: models.Utilisateur):
        """Vérifie la récupération par email."""
        fetched = get_utilisateur_by_email(db_session, user_in_db.email)
        assert fetched is not None
        assert fetched.id_utilisateur == user_in_db.id_utilisateur

    def test_update_utilisateur_info_and_password(self, db_session: Session, user_in_db: models.Utilisateur):
        """Vérifie la mise à jour des infos et le re-hachage du mot de passe."""
        new_password = "NouveauMotDePasse456!"
        update_data = {
            "prenom": "NouveauPrenom",
            "mot_de_passe": new_password
        }
        
        updated = update_utilisateur_by_id(db_session, user_in_db.id_utilisateur, update_data)
        
        assert updated.prenom == "NouveauPrenom"
        assert verify_password(new_password, updated.mot_de_passe)

    def test_delete_utilisateur(self, db_session: Session, unique_user_data: dict):
        """Vérifie la suppression physique de l'utilisateur."""
        user = create_utilisateur(db_session, unique_user_data)
        user_id = user.id_utilisateur
        
        result = delete_utilisateur_by_id(db_session, user_id)
        assert result is True
        
        assert db_session.get(models.Utilisateur, user_id) is None

    # ================= TESTS DE CONTRAINTES =================

    def test_duplicate_email_returns_none(self, db_session: Session, unique_user_data: dict):
        create_utilisateur(db_session, unique_user_data)
        
        # On tente de créer un autre utilisateur avec le même email
        data2 = unique_user_data.copy()
        data2["telephone"] = "0700000000" 

        result = create_utilisateur(db_session, data2)
        assert result is None

    def test_duplicate_telephone_fails(self, db_session: Session, unique_user_data: dict):
        """Vérifie que le système empêche les doublons de téléphone."""
        create_utilisateur(db_session, unique_user_data)
        data2 = unique_user_data.copy()
        data2["email"] = f"diff{uuid.uuid4().hex[:4]}@test.com"
        with pytest.raises(IntegrityError):
            create_utilisateur(db_session, data2)
            db_session.flush() #

    def test_get_all_utilisateurs_format(self, db_session: Session, user_in_db: models.Utilisateur):
        users = get_all_utilisateur(db_session)
        assert len(users) >= 1
        first_user = users[0]
        if isinstance(first_user, dict):
            assert any(u['id_utilisateur'] == user_in_db.id_utilisateur for u in users)
        else:
            assert any(u.id_utilisateur == user_in_db.id_utilisateur for u in users)



def random_digits(n):
    import random
    import string
    return ''.join(random.choices(string.digits, k=n))