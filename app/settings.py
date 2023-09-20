from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Класс настроек для всего проекта"""

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: int
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = '.env'


settings = Settings()

