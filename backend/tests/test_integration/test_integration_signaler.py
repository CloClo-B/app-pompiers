import uuid
import pytest
from httpx import AsyncClient
from geoalchemy2.elements import WKTElement
from app import models
from app.schemas import SignalerCreate

class TestSignalerCRUD:

    @pytest.fixture(scope="function")
    def point_eau_for_signaler(self, db_session):
        """Fixture pour créer un PointEau de référence pour les signalements."""
        unique_pei = int(str(uuid.uuid4().int)[:6])
        point = models.PointEau(
            numero_pei=unique_pei,
            nom="Point pour Signalement",
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
    def signalement_initial(self, db_session, point_eau_for_signaler):
        """Fixture pour créer un signalement initial pour les tests GET/DELETE."""
        signalement = models.Signaler(
            id_point=point_eau_for_signaler.numero_pei,
            probleme="Fuite détectée",
            photo="https://example.com/photo1.jpg"
        )
        db_session.add(signalement)
        db_session.commit()
        db_session.refresh(signalement)
        yield signalement
        # cleanup
        db_session.delete(signalement)
        db_session.commit()

    @pytest.mark.asyncio
    async def test_create_signalement_success(self, point_eau_for_signaler, client: AsyncClient):
        payload = SignalerCreate(
            id_point=point_eau_for_signaler.numero_pei,
            probleme="Bouche incendie endommagée",
            photo="https://example.com/photo_test.jpg"
        )
        response = await client.post("/signaler/", json=payload.model_dump(mode='json'))
        assert response.status_code == 200

        data = response.json()
        assert data['id_point'] == point_eau_for_signaler.numero_pei
        assert data['probleme'] == "Bouche incendie endommagée"
        assert data['photo'] == "https://example.com/photo_test.jpg"

        await client.delete(f"/signaler/{point_eau_for_signaler.numero_pei}")

    @pytest.mark.asyncio
    async def test_create_signalement_without_photo(self, point_eau_for_signaler, client: AsyncClient):
        payload = SignalerCreate(
            id_point=point_eau_for_signaler.numero_pei,
            probleme="Accès difficile",
            photo=None
        )
        response = await client.post("/signaler/", json=payload.model_dump(mode='json'))
        assert response.status_code == 200

        data = response.json()
        assert data['id_point'] == point_eau_for_signaler.numero_pei
        assert data['probleme'] == "Accès difficile"
        assert data['photo'] is None

        await client.delete(f"/signaler/{point_eau_for_signaler.numero_pei}")

    @pytest.mark.asyncio
    async def test_create_signalement_invalid_point(self, client: AsyncClient):
        payload = SignalerCreate(
            id_point=999999999,
            probleme="Test problème",
            photo=None
        )
        response = await client.post("/signaler/", json=payload.model_dump(mode='json'))
        assert response.status_code == 500
        data = response.json()
        assert "invalide" in data['detail']

    @pytest.mark.asyncio
    async def test_list_signalements_empty(self, client: AsyncClient):
        response = await client.get("/signaler/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_list_signalements_with_data(self, signalement_initial, client: AsyncClient):
        response = await client.get("/signaler/")
        assert response.status_code == 200
        data = response.json()
        found = any(s['id_point'] == signalement_initial.id_point for s in data)
        assert found
        assert len(data) >= 1

    @pytest.mark.asyncio
    async def test_get_signalement_by_id_point_success(self, signalement_initial, client: AsyncClient):
        response = await client.get(f"/signaler/{signalement_initial.id_point}")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]['id_point'] == signalement_initial.id_point
        assert data[0]['probleme'] == "Fuite détectée"

    @pytest.mark.asyncio
    async def test_get_signalement_by_id_point_not_found(self, client: AsyncClient):
        response = await client.get("/signaler/99999999")
        assert response.status_code == 404
        assert response.json()['detail'] == 'Not Found'

    @pytest.mark.asyncio
    async def test_delete_signalement_success(self, signalement_initial, client: AsyncClient):
        response = await client.delete(f"/signaler/{signalement_initial.id_point}")
        assert response.status_code == 200
        assert "supprimé" in response.json()['detail']

        response_get = await client.get(f"/signaler/{signalement_initial.id_point}")
        assert response_get.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_signalement_not_found(self, client: AsyncClient):
        response = await client.delete("/signaler/99999999")
        assert response.status_code == 404
        assert response.json()['detail'] == 'Not Found'

    @pytest.mark.asyncio
    async def test_multiple_signalements_same_point(self, point_eau_for_signaler, client: AsyncClient):
        payload1 = SignalerCreate(
            id_point=point_eau_for_signaler.numero_pei,
            probleme="Problème 1",
            photo=None
        )
        payload2 = SignalerCreate(
            id_point=point_eau_for_signaler.numero_pei,
            probleme="Problème 2",
            photo=None
        )

        response1 = await client.post("/signaler/", json=payload1.model_dump(mode='json'))
        response2 = await client.post("/signaler/", json=payload2.model_dump(mode='json'))
        assert response1.status_code == 200
        assert response2.status_code == 200

        response_get = await client.get(f"/signaler/{point_eau_for_signaler.numero_pei}")
        data = response_get.json()
        assert len(data) >= 2

        await client.delete(f"/signaler/{point_eau_for_signaler.numero_pei}")

    @pytest.mark.skip(reason="Route UPDATE non fournie dans le router")
    def test_update_signalement_success(self, signalement_initial):
        pass
