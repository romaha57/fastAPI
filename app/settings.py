from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Класс настроек для всего проекта"""

    MODE: Literal['DEV', 'TEST', 'PROD']
    LOG_LVL: Literal['INFO', 'DEBUG']

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_NAME: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: int
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

    SENTRY_KEY: str

    ELASTICSEARCH_URL: str
    ELASTICSEARCH_INDEX_NAME: str

    class Config:
        env_file = '.env'


settings = Settings()
