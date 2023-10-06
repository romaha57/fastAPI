from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.logger import logger
from app.settings import settings

if settings.MODE == 'TEST':
    DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_PARAMS = {'poolclass': NullPool}
    logger.info('Test DB is selected')
else:
    DATABASE_URL = settings.DATABASE_URL
    DATABASE_PARAMS = {}
    logger.info('Prod DB is selected')


engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
logger.info('Connect DB', extra={
    'DB': DATABASE_URL
})


class Base(DeclarativeBase):
    """Базовый класс для создания моделей и миграций"""
    pass
