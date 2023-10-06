import pytest
from httpx import AsyncClient

from app.users.service import UserService


@pytest.mark.parametrize(
    'id,email,status_code',
    [(1, 'test@test.com', 200),
     (2, 'artem@example.com', 200),
     (100, '', 400)]
)
async def test_user_get_by_id(id, email, status_code, ac: AsyncClient):
    """Проверка получение пользователя по id и соответствующие статус коды"""

    user = await UserService.get_by_id(id=id)
    if id in (1, 2):
        assert user.id == id
        assert user.email == email
    else:
        assert user is None


@pytest.mark.parametrize(
    'filters, count_users',
    [({}, 3),
     ({'email': 'artem@example.com'}, 1)]
)
async def test_user_get_all(filters, count_users, ac: AsyncClient):
    """Проверка получение пользователей по фильтрам(и без фильтров)"""

    users = await UserService.get_all(**filters)

    assert len(users) == count_users

    if filters:
        user_by_email = await UserService.get_all(**filters)
        assert len(user_by_email) == count_users
        assert user_by_email[0].email == 'artem@example.com'


@pytest.mark.parametrize(
    'email, is_exist',
    [('test@test.com', True),
     ('artem@example.com', True),
     ('empty@mail.ru', False)]
)
async def test_get_object_or_none(email, is_exist, ac: AsyncClient):
    """Проверка получение пользователя или None, если такого нет в БД"""

    user = await UserService.get_object_or_none(email=email)
    if is_exist:
        assert user.email == email
    else:
        assert user is None


@pytest.mark.parametrize(
    'email,password',
    [('one@mail.ru', 'password'),
     ('two@mail.ru', 'password')]
)
async def test_create_user(email, password, ac: AsyncClient):
    """Проверка создания пользователя в БД"""

    new_user = await UserService.create_object(
        email=email,
        password=password
    )

    assert new_user is None


@pytest.mark.parametrize(
    'user_id',
    [3, 4]
)
async def test_delete_user(user_id, ac: AsyncClient):
    """Проверка удаление пользователя из БД"""

    delete_user = await UserService.delete(id=user_id)
    assert delete_user is None
