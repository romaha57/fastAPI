import pytest
from datetime import datetime
from app.hotels.service import HotelService


@pytest.mark.parametrize(
    'date_from,date_to,location, count_hotels',
    [('2025-01-01', '2025-02-02', 'алтай', 3),
     ('2025-01-01', '2025-02-02', 'коми', 2)]
)
async def test_find_all_by_location(date_from, date_to, location, count_hotels):
    """Проверка получения отелей из БД по локации"""

    hotels = await HotelService.find_all(
        date_from=datetime.strptime(date_from, '%Y-%m-%d'),
        date_to=datetime.strptime(date_to, '%Y-%m-%d'),
        location=location
    )
    assert len(hotels) == count_hotels


@pytest.mark.parametrize(
    'date_from,date_to,hotel_name, count_hotels',
    [('2025-01-01', '2025-02-02', 'cosmos', 1),
     ('2025-01-01', '2025-02-02', 'resort', 2)]
)
async def test_find_all_by_hotel_name(date_from, date_to, hotel_name, count_hotels):
    """Проверка получения отелей из БД по названию"""

    hotels = await HotelService.find_all(
        date_from=datetime.strptime(date_from, '%Y-%m-%d'),
        date_to=datetime.strptime(date_to, '%Y-%m-%d'),
        hotel_name=hotel_name
    )
    assert len(hotels) == count_hotels
