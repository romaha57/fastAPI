from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.settings import settings
from app.users.auth import create_access_token, verify_password
from app.users.dependecies import get_current_user
from app.users.service import UserService


class AdminAuth(AuthenticationBackend):
    """Аутентификация в админке"""

    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        # проверяем существует ли такой пользователь в БД и правильный ли пароль ввел
        user = await UserService.get_object_or_none(email=email)
        if user and verify_password(password, user.password):
            access_token = create_access_token({'sub': str(user.id)})

            request.session.update({"token": access_token})

            return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()

        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False

        user = await get_current_user(token)
        if not user:
            return False

        return True


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
