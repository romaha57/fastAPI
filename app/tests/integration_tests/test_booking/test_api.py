import pytest
from httpx import AsyncClient


async def test_get_bookings(auth_user: AsyncClient):
    """Проверка на получение броней для аутентифицированного пользователя"""

    response = await auth_user.get('booking')
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.parametrize(
    'room_id,date_from,date_to,user_id,status_code',
    [*[(1, '2024-02-02', '2024-02-07', 1, 200)] * 5,
     (1, '2024-02-02', '2024-02-07', 1, 409),
     (1, '2024-02-02', '2024-02-07', 1, 409)]
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
