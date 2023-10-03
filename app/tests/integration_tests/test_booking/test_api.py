import datetime

import pytest
from httpx import AsyncClient

from app.bookings.service import BookingService


async def test_get_bookings(auth_user: AsyncClient):
    """Проверка на получение броней для аутентифицированного пользователя"""

    response = await auth_user.get('booking')
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.parametrize(
    'room_id,date_from,date_to,user_id,status_code',
    [*[(1, '2024-02-02', '2024-02-07', 1, 200)] * 5,
     (1, '2024-02-02', '2024-02-07', 1, 409),
     (1, '2024-02-02', '2024-02-07', 1, 409),
     (1, '2024-02-02', '2000-01-01', 1, 409)]
)
async def test_create_booking(room_id, date_from, date_to, user_id, status_code, auth_user: AsyncClient):
    """Проверка создания броней, а также проверка, что при бронировании уже занятого номера выходит 409 ошибка"""

    response = await auth_user.post(
        'booking',
        params={
            'room_id': room_id,
            'date_from': date_from,
            'date_to': date_to,
            'user_id': user_id
        }
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    'booking_id,old_room_id,new_room_id,old_date_from,new_date_from,old_date_to,new_date_to,status_code',
    [(1, 1, 2, '2023-06-15', '3000-01-01', '2023-06-30', '3000-02-02', 200),
     (1, 2, 2, '3000-01-01', '2500-01-01', '3000-02-02', '2100-02-02', 409),
     (1, 2, 2, '3000-01-01', '1000-01-01', '3000-02-02', '1000-02-02', 409)]
)
async def test_update_booking(booking_id, old_room_id, new_room_id,
                              old_date_from, new_date_from, old_date_to, new_date_to,
                              status_code, auth_user: AsyncClient):
    """Проверка на изменение данных в брони"""

    # сначала получаем бронь с id=1
    booking = await BookingService.get_by_id(id=booking_id)
    assert booking.rooms_id == old_room_id
    assert str(booking.date_from) == old_date_from
    assert str(booking.date_to) == old_date_to

    response = await auth_user.patch(
        f'booking/{booking_id}',
        params={
            'booking_id': booking_id,
            'rooms_id': new_room_id,
            'date_from': new_date_from,
            'date_to': new_date_to
        })

    assert response.status_code == status_code

    # если произошла ошибка по датам(дата выезда < даты заезда или дата заезда меньше текущей),
    # то проверяем только код ответа
    if response.status_code != 409:
        booking = await BookingService.get_by_id(id=booking_id)
        assert booking.rooms_id == new_room_id
        assert str(booking.date_from) == new_date_from
        assert str(booking.date_to) == new_date_to


@pytest.mark.parametrize(
    'booking_id, status_code',
    [(4, 204),
     (5, 204),
     (6, 204),
     (7, 204),
     (8, 204)]

)
async def test_delete_booking(booking_id, status_code, auth_user: AsyncClient):
    """Проверка удаления броней"""

    response = await auth_user.delete(f'booking/{booking_id}')
    assert response.status_code
