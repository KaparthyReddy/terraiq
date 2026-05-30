import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

BOUNDARY = {
    "type": "Polygon",
    "coordinates": [[[77.5, 12.9], [77.6, 12.9], [77.6, 13.0], [77.5, 13.0], [77.5, 12.9]]]
}


async def _auth_header(client: AsyncClient) -> dict:
    r = await client.post("/api/v1/auth/register", json={
        "email": "field_test@terraiq.io", "password": "Pass1234!", "full_name": "Field Tester"
    })
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


@pytest.mark.asyncio
async def test_create_and_list_fields():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        headers = await _auth_header(client)

        create = await client.post("/api/v1/fields/", json={
            "name": "North Block",
            "area_hectares": 4.5,
            "boundary": BOUNDARY,
            "centroid_lat": 12.95,
            "centroid_lon": 77.55,
            "crop_type": "wheat",
        }, headers=headers)
        assert create.status_code == 201
        field_id = create.json()["id"]

        lst = await client.get("/api/v1/fields/", headers=headers)
        assert lst.status_code == 200
        assert any(f["id"] == field_id for f in lst.json())
