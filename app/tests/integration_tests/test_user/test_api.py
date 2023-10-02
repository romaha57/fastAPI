import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    'email,password,status_code',
    [('test@mail.ru', 'password', 200),
     ('incorrectmail', 'password', 422),
     ('test@mail.ru', 'password1', 409),
     ('new_test@mail.ru', '', 409),
     ('', 'password', 422)
     ]
)
async def test_register_user(email, password, status_code, ac: AsyncClient):
    """Проверка регистрации пользователя с верными и неверными данными"""

    response = await ac.post(
        '/users/register',
        json={
            'email': email,
            'password': password
        })

    assert response.status_code == status_code


@pytest.mark.parametrize(
    'email,password,status_code',
    [('test@test.com', 'test', 200),
     ('artem@example.com', 'artem', 200),
     ('wrong@mail.com', 'wrong', 401),
     ('test@test.com', '', 401)]
)
async def test_login_user(email, password, status_code, ac: AsyncClient):
    """Проверка входа в систему и соответствующих статус кодов"""

    response = await ac.post(
        'users/login',
        json={
            'email': email,
            'password': password
        }
    )

    assert response.status_code == status_code


@pytest.mark.parametrize(
    'status_code',
    [200]
)
async def test_logout_user(status_code, ac: AsyncClient):
    """Проверка логаута из системы """

    response = await ac.post('users/logout')
    assert response.status_code == status_code
    assert response.json() == {'msg': 'user logout'}


@pytest.mark.parametrize(
    'status_code',
    [401]
)
async def test_account_user_unauthenticated(status_code, ac: AsyncClient):
    """Проверка на получение своего аккаунта для не аутентифицированного пользователя"""

    response = await ac.get('users/account')
    assert response.status_code == status_code


@pytest.mark.parametrize(
    'status_code',
    [200]
)
async def test_account_user_authenticated(status_code, auth_user: AsyncClient):
    """Проверка на получение своего аккаунта для аутентифицированного пользователя"""

    response = await auth_user.get('users/account')
    assert response.status_code == status_code
