from datetime import datetime

from fastapi import Depends, Request
from jose import JWTError, jwt
from sqlalchemy import Row

from app.exceptions import (
    ExpiredTokenException,
    TokenDoesNotExistException,
    TokenIncorrectException,
    UserDoesNotExistException,
)
from app.settings import settings
from app.users.service import UserService


def get_token(request: Request) -> str:
    """Получение токена доступа из куки запроса"""

    token = request.cookies.get('access_token')
    if not token:
        raise TokenDoesNotExistException()
    return token


async def get_current_user(token: str = Depends(get_token)) -> Row:
    """Декодирование jwt и получение user по его id из токена"""

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise TokenIncorrectException()

    expire = payload.get('exp')
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise ExpiredTokenException()
    user_id = payload.get('sub')
    if not user_id:
        raise TokenIncorrectException()

    user = await UserService.get_by_id(id=int(user_id))
    if not user:
        raise UserDoesNotExistException()

    return user
