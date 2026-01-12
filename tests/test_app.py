import pytest
from httpx import AsyncClient, ASGITransport
from src.app import app

@pytest.mark.asyncio
async def test_get_activities():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data

@pytest.mark.asyncio
async def test_signup_and_unregister():
    test_email = "testuser@mergington.edu"
    activity = "Chess Club"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Sign up
        response = await ac.post(f"/activities/{activity}/signup?email={test_email}")
        assert response.status_code == 200
        assert f"Signed up {test_email}" in response.json()["message"]
        # Unregister
        response = await ac.post(f"/activities/{activity}/unregister?email={test_email}")
        assert response.status_code == 200
        assert f"Removed {test_email}" in response.json()["message"]

@pytest.mark.asyncio
async def test_signup_duplicate():
    test_email = "michael@mergington.edu"  # Already in Chess Club
    activity = "Chess Club"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(f"/activities/{activity}/signup?email={test_email}")
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

@pytest.mark.asyncio
async def test_unregister_not_found():
    test_email = "notfound@mergington.edu"
    activity = "Chess Club"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(f"/activities/{activity}/unregister?email={test_email}")
        assert response.status_code == 404
        assert "Participant not found" in response.json()["detail"]
