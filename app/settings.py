from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Класс настроек для всего проекта"""

    MODE: Literal['DEV', 'TEST', 'PROD']

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: int
    DATABASE_URL: str

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_NAME: str
    TEST_DB_USER: str
    TEST_DB_PASSWORD: int
    TEST_DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str

    REDIS_CONNECT: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str

    class Config:
        env_file = '.env'


settings = Settings()
