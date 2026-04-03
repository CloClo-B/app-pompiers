from app import models
from geoalchemy2.elements import WKTElement

def test_create_signalement(db_session):
    user = models.Utilisateur(
        nom="Test", prenom="Signal",
        email="signal@test.com",
        telephone="0600000011",
        mot_de_passe="hash",
        role=models.RoleEnum.pompier
    )

    point = models.PointEau(
        numero_pei=7777,
        statut="PUBLIC",
        type_nature="BI",
        accessibilite="C",
        disponibilite="DI",
        carto_ref=1,
        press_deb=1.0,
        debit_1_bar=10.0,
        vol_eau_mi=5.0,
        utilisateur=1,
        geom=WKTElement("POINT(700000 6600000)", srid=2154)
    )

    db_session.add_all([user, point])
    db_session.commit()

    signal = models.Signaler(
        id_point=point.numero_pei,
        id_utilisateur=user.id_utilisateur,
        probleme="Fuite",
        photo="test.jpg"
    )

    db_session.add(signal)
    db_session.commit()
    db_session.refresh(signal)

    assert signal.id is not None
    assert signal.probleme == "Fuite"
