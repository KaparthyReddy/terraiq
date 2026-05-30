import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

BOUNDARY = {
    "type": "Polygon",
    "coordinates": [[[77.5, 12.9], [77.6, 12.9], [77.6, 13.0], [77.5, 13.0], [77.5, 12.9]]]
}


@pytest.mark.asyncio
async def test_ingest_reading():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        reg = await client.post("/api/v1/auth/register", json={
            "email": "sensor_test@terraiq.io", "password": "Pass1234!", "full_name": "Sensor Tester"
        })
        headers = {"Authorization": f"Bearer {reg.json()['access_token']}"}

        field = await client.post("/api/v1/fields/", json={
            "name": "Sensor Field", "area_hectares": 2.0,
            "boundary": BOUNDARY, "centroid_lat": 12.95, "centroid_lon": 77.55,
        }, headers=headers)
        field_id = field.json()["id"]

        reading = await client.post("/api/v1/sensors/ingest", json={
            "field_id": field_id,
            "sensor_id": "SNS-001",
            "ph": 4.2,
            "moisture_pct": 35.0,
            "nitrogen_ppm": 8.0,
        }, headers=headers)
        assert reading.status_code == 201
        assert reading.json()["ph"] == 4.2
