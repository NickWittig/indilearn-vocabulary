import logging

import pytest
from httpx import AsyncClient

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_get_achievement(setup_database, async_client: AsyncClient):
    logger.info("Starting test_get_achievement")
    response = await async_client.get("/achievement/get/1")
    logger.info(f"Response status code: {response.status_code}")
    assert response.status_code == 200  # Mock data should ensure this exists
    data = response.json()
    logger.info(f"Response data: {data}")
    assert data["name_en"] == "Omniscient"


@pytest.mark.asyncio
async def test_get_nonexistent_achievement(setup_database, async_client: AsyncClient):
    logger.info("Starting test_get_nonexistent_achievement")
    response = await async_client.get("/achievement/get/999")
    logger.info(f"Response status code: {response.status_code}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_all_achievements(setup_database, async_client: AsyncClient):
    logger.info("Starting test_get_all_achievements")
    response = await async_client.get("/achievement/get_all")
    logger.info(f"Response status code: {response.status_code}")
    assert response.status_code == 200
    data = response.json()
    logger.info(f"Response data: {data}")
    assert isinstance(data, list)
    assert len(data) == 7  # Should match the number of mock achievements
