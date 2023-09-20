from fastapi import APIRouter, Depends

from app.bookings.service import BookingService
from app.bookings.schemas import BookingSchema

from app.users.models import User
from app.users.dependecies import get_current_user


router = APIRouter(
    prefix='/booking',
    tags=['Бронирование']
)


@router.get('', )
async def get_bookings(
        user: User = Depends(get_current_user)
):
    return await BookingService.get_all(user_id=user.id)
