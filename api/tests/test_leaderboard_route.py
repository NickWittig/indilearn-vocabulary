import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_leaderboard(setup_database, async_client: AsyncClient):
    response = await async_client.get("/leaderboard/get")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 10  # Assuming it returns top 10 users
