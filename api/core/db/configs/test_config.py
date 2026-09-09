import os

from dotenv import load_dotenv

load_dotenv("/mnt/.env")


class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL", "postgresql://test_user:your_password@localhost/test_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
