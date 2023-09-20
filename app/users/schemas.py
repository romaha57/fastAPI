from pydantic import BaseModel, EmailStr


class RegisterUserSchema(BaseModel):
    """Схема для регистрации пользователя"""

    email: EmailStr
    password: str


class LoginUserSchema(RegisterUserSchema):
    """Схема для логина пользователя"""

    pass
