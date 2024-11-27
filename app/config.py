import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    DB_PORT = int(os.getenv("DB_PORT"))
    SECRET_KEY = os.getenv("SECRET_KEY")


settings = Settings()