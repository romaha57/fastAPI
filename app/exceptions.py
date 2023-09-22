from fastapi import HTTPException, status

from app.mixins import InitExceptionMixin


class TokenDoesNotExistException(InitExceptionMixin, HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Токен не найден'


class TokenIncorrectException(InitExceptionMixin, HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Неверный формат токена'


class ExpiredTokenException(InitExceptionMixin, HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'токен истек'


class UserDoesNotExistException(InitExceptionMixin, HTTPException):
    status = status.HTTP_409_CONFLICT
    detail = 'Пользователь не найден'


class UserAlreadyExistException(InitExceptionMixin, HTTPException):
    status = status.HTTP_409_CONFLICT
    detail = 'пользователь с таким email уже существует'


class LoginException(InitExceptionMixin, HTTPException):
    status = status.HTTP_400_BAD_REQUEST
    detail = 'ошибка входа'



