import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_user(setup_database, async_client: AsyncClient):
    # Create a user first
    response = await async_client.get("/user/get")
    assert response.status_code == 200
    data = response.json()
    assert data["user_name"] == "test-user"
    assert data["id"] == 13


@pytest.mark.asyncio
async def test_get_user_achievements_check(setup_database, async_client: AsyncClient):
    response = await async_client.get("/user/achievements/check")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["unlocked_achievement_ids"], list)
    assert len(data["unlocked_achievement_ids"]) == 0


@pytest.mark.asyncio
async def test_get_user_achievements_get(setup_database, async_client: AsyncClient):
    response = await async_client.get("/user/achievements/get")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["unlocked_achievement_ids"], list)
    assert len(data["unlocked_achievement_ids"]) == 0
