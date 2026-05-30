import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        reg = await client.post("/api/v1/auth/register", json={
            "email": "farmer@terraiq.io",
            "password": "Str0ng!Pass",
            "full_name": "Test Farmer",
        })
        assert reg.status_code == 201
        data = reg.json()
        assert "access_token" in data
        assert data["user"]["email"] == "farmer@terraiq.io"

        login = await client.post("/api/v1/auth/login", json={
            "email": "farmer@terraiq.io",
            "password": "Str0ng!Pass",
        })
        assert login.status_code == 200
        assert "access_token" in login.json()


@pytest.mark.asyncio
async def test_login_wrong_password():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post("/api/v1/auth/login", json={
            "email": "farmer@terraiq.io",
            "password": "wrongpassword",
        })
        assert resp.status_code == 401
