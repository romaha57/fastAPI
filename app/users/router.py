from fastapi import APIRouter, HTTPException, status, Response

from users.schemas import RegisterUserSchema, LoginUserSchema
from users.service import UserService
from users.auth import hash_password, verify_password, create_access_token

router = APIRouter(
    prefix='/users',
    tags=['Пользователи']
)


@router.post('/register')
async def register_user(
        user_data: RegisterUserSchema
):
    if await UserService.get_object_or_none(email=user_data.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    hashed_password = hash_password(user_data.password)
    await UserService.create_object(
        email=user_data.email,
        password=hashed_password
    )


@router.post('/login')
async def login_user(
        response: Response,
        user_data: LoginUserSchema
):
    user = await UserService.get_object_or_none(email=user_data.email)
    if user and verify_password(user_data.password, user.password):
        access_token = create_access_token({'sub': str(user.id)})
        response.set_cookie('access_token', access_token, httponly=True)

        return {'access_token': access_token}

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


