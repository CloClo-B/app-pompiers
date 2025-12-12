import pytest
from app.DAO.DAOSignaler import (
    get_all_signale,
    get_signale_by_id_point,
    create_signale,
    delete_signale_by_id_point,
    update_signale,
)
from app import models
from geoalchemy2.elements import WKTElement
import uuid

@pytest.fixture(scope="function")
def point_eau(db_session):
    """Fixture pour créer un point d'eau pour les tests DAO"""
    unique_pei = int(str(uuid.uuid4().int)[:6])
    point = models.PointEau(
        numero_pei=unique_pei,
        nom="Point DAO Test",
        statut="PUBLIC",
        type_nature="BI",
        insee5="75001",
        geom=WKTElement("POINT (800000 6600000)", srid=2154)
    )
    db_session.add(point)
    db_session.commit()
    db_session.refresh(point)
    return point

@pytest.fixture(scope="function")
def signalement(db_session, point_eau):
    """Fixture pour créer un signalement initial pour DAO"""
    signale_data = {
        "id_point": point_eau.numero_pei,
        "probleme": "Fuite DAO",
        "photo": "https://example.com/photo_dao.jpg"
    }
    sig = create_signale(db_session, signale_data)
    yield sig
    # Cleanup
    delete_signale_by_id_point(db_session, point_eau.numero_pei)

def test_create_signale_success(db_session, point_eau):
    signale_data = {
        "id_point": point_eau.numero_pei,
        "probleme": "Problème DAO",
        "photo": None
    }
    new_sig = create_signale(db_session, signale_data)
    assert new_sig.id_point == point_eau.numero_pei
    assert new_sig.probleme == "Problème DAO"
    assert new_sig.photo is None

def test_create_signale_invalid_point(db_session):
    signale_data = {
        "id_point": 999999,
        "probleme": "Invalid Point",
        "photo": None
    }
    import pytest
    with pytest.raises(ValueError):
        create_signale(db_session, signale_data)

def test_get_all_signale(db_session, signalement):
    all_signales = get_all_signale(db_session)
    assert isinstance(all_signales, list)
    assert any(s['id_point'] == signalement.id_point for s in all_signales)

def test_get_signale_by_id_point(db_session, signalement):
    sigs = get_signale_by_id_point(db_session, signalement.id_point)
    assert len(sigs) >= 1
    assert sigs[0]['id_point'] == signalement.id_point
    assert sigs[0]['probleme'] == signalement.probleme

def test_delete_signale_by_id_point(db_session, signalement):
    result = delete_signale_by_id_point(db_session, signalement.id_point)
    assert result is True
    sigs = get_signale_by_id_point(db_session, signalement.id_point)
    assert sigs == []

def test_update_signale(db_session, signalement):
    update_data = {"probleme": "Problème mis à jour", "photo": "https://example.com/new.jpg"}
    updated_sig = update_signale(db_session, signalement.id_point, update_data)
    assert updated_sig.probleme == "Problème mis à jour"
    assert updated_sig.photo == "https://example.com/new.jpg"

def test_update_signale_nonexistent(db_session):
    updated_sig = update_signale(db_session, 999999, {"probleme": "Test"})
    assert updated_sig is None
