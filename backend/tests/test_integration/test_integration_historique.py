from app import models

def test_historique_fk_user(db_session):
    user = models.Utilisateur(
        nom="Log", prenom="User",
        email="log@test.com",
        telephone="0600000010",
        mot_de_passe="hash",
        role=models.RoleEnum.admin
    )
    db_session.add(user)
    db_session.commit()

    log = models.Historique(
        id_utilisateur=user.id_utilisateur,
        action="Connexion",
        ip="127.0.0.1"
    )

    db_session.add(log)
    db_session.commit()
    db_session.refresh(log)

    assert log.id_log is not None
    assert log.action == "Connexion"
