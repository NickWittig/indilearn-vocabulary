import asyncio
import logging
import os

import pytest
from api.config.config import DataConfig
from api.core.db.configs.test_config import TestConfig
from api.core.db.initializers.load_achievements import load_achievements
from api.core.db.initializers.load_items import load_items
from api.core.db.initializers.load_ranks import load_ranks
from api.core.db.initializers.load_users import load_users
from api.core.db.session import Base, get_db
from httpx import AsyncClient, BasicAuth
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.core.db.initializers import load_items

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("test_log.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

# Use the test database URL from TestConfig
SQLALCHEMY_DATABASE_URL = TestConfig.SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override the get_db dependency to use the testing database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def setup_database():
    # Create the tables
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    logger.info("Adding mock data to the database")
    load_achievements(session, DataConfig.PATH_TEST_ACHIEVEMENTS)
    load_items(session, DataConfig.PATH_TEST_ITEMS)
    load_ranks(session, DataConfig.PATH_TEST_RANKS)
    load_users(session, DataConfig.PATH_TEST_USERS)
    yield session

    # Drop the tables after tests
    Base.metadata.drop_all(bind=engine)
    session.close()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_client(event_loop):
    auth = BasicAuth(
        username=os.getenv("TEST_AUTH_USERNAME", "test-user"),
        password=os.getenv("TEST_AUTH_PASSWORD", "test-password"),
    )
    async with AsyncClient(app=app, base_url="http://test", auth=auth) as client:
        yield client
