import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    'hotel_id,date_from,date_to,status_code,count_rooms',
    [(1, '2025-01-01', '2025-02-02', 200, 2),
     (2, '2025-01-01', '2025-02-02', 200, 2),
     (6, '2025-01-01', '2025-02-02', 200, 1),
     (1000, '2025-01-01', '2025-02-02', 200, 0)]
)
async def test_get_rooms(hotel_id, date_from, date_to, status_code, count_rooms, ac: AsyncClient):
    """Проверка на получение номеров в определенном отеле по его id"""

    response = await ac.get(
        f'rooms/hotels/{hotel_id}?date_from={date_from}&date_to={date_to}'
    )

    assert response.status_code == status_code
    assert len(response.json()) == count_rooms
