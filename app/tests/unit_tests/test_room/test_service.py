import pytest
from datetime import datetime

from app.rooms.service import RoomService


@pytest.mark.parametrize(
    'hotel_id,date_from,date_to,count_rooms',
    [(1, '2025-01-01', '2025-02-02', 2),
     (2, '2025-01-01', '2025-02-02', 2),
     (6, '2025-01-01', '2025-02-02', 1),
     (1000, '2025-01-01', '2025-02-02', 0)]
)
async def test_get_all(hotel_id, date_from, date_to, count_rooms):
    """Проверка получение свободных комнат по отелю(hotel_id)"""

    rooms = await RoomService.get_all(
        hotel_id=hotel_id,
        date_from=datetime.strptime(date_from, '%Y-%m-%d'),
        date_to=datetime.strptime(date_from, '%Y-%m-%d')
    )

    assert len(rooms) == count_rooms

    # если номер существует, то проверяем наличие поля total_cost и rooms_left
    if hotel_id != 1000:
        assert 'total_cost' in rooms[0]
        assert 'rooms_left' in rooms[0]


