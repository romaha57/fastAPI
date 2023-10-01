import asyncio
import json

import pytest

from datetime import datetime
from sqlalchemy import insert

from app.database import engine, async_session, Base
from app.settings import settings
from app.hotels.models import Hotel
from app.rooms.models import Room
from app.users.models import User
from app.bookings.models import Booking


def open_mock_json(name: str) -> dict:
    """Получение тестовых данных из json файла"""

    with open(f'app/tests/mock_data/mock_{name}.json', encoding='utf-8') as file:
        mock_data = json.load(file)

    return mock_data


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    # проверка на тестовую БД
    assert settings.MODE == "TEST"

    # перед началом тестов удаляем и заново создаем таблицы в БД
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    hotels = open_mock_json("hotels")
    rooms = open_mock_json("rooms")
    users = open_mock_json("users")
    bookings = open_mock_json("bookings")

    # преобразуем дату для SQlAlchemy
    for booking in bookings:
        booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")

    async with async_session() as session:
        for Model, values in [
            (Hotel, hotels),
            (Room, rooms),
            (User, users),
            (Booking, bookings),
        ]:
            query = insert(Model).values(values)
            await session.execute(query)

        await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()



