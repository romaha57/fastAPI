from datetime import datetime

from fastapi import HTTPException, Depends, status, Request
from jose import jwt, JWTError
from sqlalchemy import Row

from app.users.service import UserService
from app.settings import settings


def get_token(request: Request) -> str:
    """Получение токена доступа из куки запроса"""

    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return token


async def get_current_user(token: str = Depends(get_token)) -> Row:
    """Декодирование jwt и получение user по его id из токена"""

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    expire = payload.get('exp')
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    user = await UserService.get_by_id(id=int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return user
