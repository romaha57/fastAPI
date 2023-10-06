import pytest
from httpx import AsyncClient

# Если ошибка AssertionError: You must call init first!, то надо в router закомментить @сache()


@pytest.mark.parametrize(
    'location,date_from,date_to,count_hotels,status_code',
    [('Алтай', '2100-01-01', '2100-02-02', 3, 200),
     ('коми', '2100-01-01', '2100-02-02', 2, 200),
     ('test_location', '2100-01-01', '2100-02-02', 0, 200),
     ('алтай', '2100-01-01', '2000-02-02', 1, 409)]
)
async def test_get_hotels_by_location(location, date_from, date_to, count_hotels, status_code, ac: AsyncClient):
    """Проверка на получение отелей по локации"""

    response = await ac.get(
        f'hotels/{location}?date_from={date_from}&date_to={date_to}')

    # проверяем количество найденных отелей по локации
    assert response.status_code == status_code
    assert len(response.json()) == count_hotels


@pytest.mark.parametrize(
    'hotel_name,date_from,date_to,count_hotels,status_code',
    [('skala', '2100-01-01', '2100-02-02', 1, 200),
     ('Resort', '2100-01-01', '2100-02-02', 2, 200),
     ('skala', '2100-01-01', '2000-02-02', 1, 409)]
)
async def test_get_hotels_by_hotel_name(hotel_name, date_from, date_to, count_hotels, status_code, ac: AsyncClient):
    """Проверка на получение отелей по названию"""

    response = await ac.get(
        f'hotels/search/{hotel_name}?date_from={date_from}&date_to={date_to}')

    # проверяем количество найденных отелей по названию
    assert response.status_code == status_code
    assert len(response.json()) == count_hotels


@pytest.mark.parametrize(
    'hotel_id,status_code',
    [(1, 200),
     (2, 200),
     (1000, 400)]
)
async def test_get_hotel(hotel_id, status_code, ac: AsyncClient):
    """Проверка на получение конкретного отеля по его id"""

    response = await ac.get(
        f'hotels/id/{hotel_id}'
    )

    # если нет отеля, то 400 ошибка, если есть то проверяем его id
    assert response.status_code == status_code
    if response.status_code != 400:
        assert dict(response.json()).get('id') == hotel_id
