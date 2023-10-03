from datetime import datetime, date
from fastapi import APIRouter, Depends

from app.bookings.service import BookingService
from app.bookings.schemas import CreateBookingSchema, BookingsByUserSchema, BaseBookingSchema
from app.exceptions import NoAvailableRoomsException, InvalidUpdateBookingException, InvalidDateException
from app.tasks.tasks import send_email

from app.users.models import User
from app.users.dependecies import get_current_user


router = APIRouter(
    prefix='/booking',
    tags=['Бронирование']
)


@router.get('', response_model=list[BookingsByUserSchema])
async def get_bookings(
        user: User = Depends(get_current_user)
):
    return await BookingService.get_all(user_id=user.id)


@router.post('', response_model=CreateBookingSchema)
async def create_booking(
        room_id: int,
        date_from: date,
        date_to: date,
        user: User = Depends(get_current_user)
):
    if date_to <= date_from or date_from < datetime.utcnow().date():
        raise InvalidDateException()

    new_booking = await BookingService.create(
        room_id=room_id,
        date_from=date_from,
        date_to=date_to,
        user_id=user.id
    )
    if not new_booking:
        raise NoAvailableRoomsException()

    # преобразуем sqlalchemy модель в словарь
    booking_data = new_booking.__dict__
    del booking_data['_sa_instance_state']

    # отправка письма с подтверждением брони
    # send_email.delay(booking_data, user.email)

    return new_booking


@router.patch('/{booking_id}')
async def update_booking(
        booking_id: int,
        rooms_id: int,
        date_from: date,
        date_to: date,
        user: User = Depends(get_current_user)

):
    if date_to <= date_from or date_from < datetime.utcnow().date():
        raise InvalidDateException()

    rooms_left = await BookingService.update(
        booking_id=booking_id,
        rooms_id=rooms_id,
        date_from=date_from,
        date_to=date_to
    )
    if not rooms_left:
        raise NoAvailableRoomsException()

    return {'msg': 'booking was updated'}


@router.delete('/{booking_id}')
async def delete_booking(
        booking_id: int,
        user: User = Depends(get_current_user)
):
    await BookingService.delete(id=booking_id)
    return {'msg': f'delete booking_id = {booking_id}'}
