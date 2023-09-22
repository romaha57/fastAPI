from fastapi import APIRouter, HTTPException, status, Response, Depends

from users.schemas import RegisterUserSchema, LoginUserSchema
from users.service import UserService
from users.auth import hash_password, verify_password, create_access_token
from users.dependecies import get_current_user
from users.models import User
from app.exceptions import UserAlreadyExistException, LoginException

router = APIRouter(
    prefix='/users',
    tags=['Пользователи']
)


@router.post('/register')
async def register_user(
        user_data: RegisterUserSchema
):
    if await UserService.get_object_or_none(email=user_data.email):
        raise UserAlreadyExistException()

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

    raise LoginException()


@router.post('/logout')
def logout_user(
        response: Response
):
    response.delete_cookie('access_token')

    return {'msg': 'user logout'}


@router.get('/account')
def account_user(
        user: User = Depends(get_current_user)
):
    return user
