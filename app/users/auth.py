from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from app.settings import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str) -> str:
    """Хэширует пароль"""

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка совпадений пароля с хэшом"""

    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """Создание токена доступа при аутентификации пользователя"""

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({'exp': expire})
    access_token = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        settings.ALGORITHM
    )

    return access_token
