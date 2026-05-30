import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

BOUNDARY = {
    "type": "Polygon",
    "coordinates": [[[77.5, 12.9], [77.6, 12.9], [77.6, 13.0], [77.5, 13.0], [77.5, 12.9]]]
}


@pytest.mark.asyncio
async def test_recommendations_generated_on_anomaly():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        reg = await client.post("/api/v1/auth/register", json={
            "email": "rec_test@terraiq.io", "password": "Pass1234!", "full_name": "Rec Tester"
        })
        headers = {"Authorization": f"Bearer {reg.json()['access_token']}"}

        field = await client.post("/api/v1/fields/", json={
            "name": "Rec Field", "area_hectares": 3.0,
            "boundary": BOUNDARY, "centroid_lat": 12.95, "centroid_lon": 77.55,
        }, headers=headers)
        field_id = field.json()["id"]

        # Anomalous pH triggers recommendation
        await client.post("/api/v1/sensors/ingest", json={
            "field_id": field_id, "sensor_id": "SNS-002", "ph": 4.1,
        }, headers=headers)

        recs = await client.get(f"/api/v1/recommendations/{field_id}", headers=headers)
        assert recs.status_code == 200
        assert len(recs.json()) >= 1
        assert recs.json()[0]["trigger"] == "sensor"
