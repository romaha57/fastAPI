import pytest

from app.bookings.service import BookingService


@pytest.mark.parametrize(
    'user_id,count_bookings',
    [(1, 2),
     (2, 1),
     (3, 0)]
)
async def test_booking_service_get_all(count_bookings, user_id):
    """Проверяем получение броней по user_id и работу join'ов"""

    bookings = await BookingService.get_all(user_id)
    assert len(bookings) == count_bookings
    if count_bookings:
        assert bookings[0]['room_name']
        assert bookings[0]['hotel_name']
