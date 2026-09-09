import os

from dotenv import load_dotenv

load_dotenv("/mnt/.env")


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://username:password@localhost/mydatabase")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
