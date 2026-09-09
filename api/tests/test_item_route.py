import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_item(setup_database, async_client: AsyncClient):
    response = await async_client.get("/item/get")
    assert response.status_code == 200
    data = response.json()
    assert data is not None
    assert isinstance(data["id"], int)
    assert isinstance(data["question"], str)


@pytest.mark.asyncio
async def test_check_item_solution_correct(setup_database, async_client: AsyncClient):
    response = await async_client.post("/item/check", json={"item_id": 0, "user_solution": "a"})
    assert response.status_code == 200  # Assuming no items exist for checking initially
    data = response.json()
    assert data["correct"] is True


@pytest.mark.asyncio
async def test_check_item_solution_wrong(setup_database, async_client: AsyncClient):
    response = await async_client.post("/item/check", json={"item_id": 0, "user_solution": "b"})
    assert response.status_code == 200  # Assuming no items exist for checking initially
    data = response.json()
    assert data["correct"] is False
