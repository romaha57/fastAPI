from app.service.base import BaseService
from app.users.models import User


class UserService(BaseService):
    """Класс для работы с пользователями в БД"""

    model = User
