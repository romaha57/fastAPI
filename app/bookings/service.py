from datetime import date

from sqlalchemy import and_, func, insert, or_, select, update

from app.bookings.models import Booking
from app.database import async_session
from app.hotels.models import Hotel
from app.rooms.models import Room
from app.service.base import BaseService


class BookingService(BaseService):
    """Класс для работы с бронями в БД"""

    model = Booking

    @classmethod
    async def _check_room_left(cls,
                               room_id: int,
                               date_from: date,
                               date_to: date
                               ) -> int:
        """Проверка на количество забронированных номеров по его id и по датам """

        async with async_session() as session:
            # получаем количество забронированных на эту дату номеров
            booked_rooms = select(Booking).where(
                and_(
                    Booking.rooms_id == room_id,
                    or_(
                        and_(
                            Booking.date_from >= date_from,
                            Booking.date_from <= date_to
                        ),
                        and_(
                            Booking.date_from <= date_from,
                            Booking.date_to > date_from
                        )
                    )
                )
            ).cte('booked_rooms')

            # из общего количество номеров вычитаем количество забронированных
            rooms_left = select(
                Room.quantity - func.count(booked_rooms.c.rooms_id)
            ).select_from(Room).join(
                booked_rooms, booked_rooms.c.rooms_id == Room.id, isouter=True
            ).where(
                Room.id == room_id
            ).group_by(
                Room.quantity, booked_rooms.c.rooms_id
            )

            rooms_left = await session.execute(rooms_left)
            rooms_left: int = rooms_left.scalar()

            return rooms_left

    @classmethod
    async def create(cls,
                     room_id: int,
                     date_from: date,
                     date_to: date,
                     user_id: int
                     ):
        """Создание брони с учетом свободных номеров на эти даты"""

        rooms_left = await cls._check_room_left(
            room_id=room_id,
            date_from=date_from,
            date_to=date_to
        )
        # если есть свободные номера, то создаем бронь
        if rooms_left > 0:
            async with async_session() as session:
                get_price = select(Room.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_booking = insert(Booking).values(
                    rooms_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price
                ).returning(Booking)
                new_booking = await session.execute(add_booking)
                await session.commit()

                return new_booking.scalar()

    @classmethod
    async def update(cls,
                     rooms_id: int,
                     booking_id: int,
                     date_from: date,
                     date_to: date
                     ):
        """Изменение данных по брони"""

        rooms_left = await cls._check_room_left(
            room_id=rooms_id,
            date_from=date_from,
            date_to=date_to
        )
        if rooms_left > 0:
            async with async_session() as session:

                update_booking = update(Booking).filter_by(id=booking_id).values(
                    rooms_id=rooms_id,
                    date_from=date_from,
                    date_to=date_to,
                )
                await session.execute(update_booking)
                await session.commit()

        return rooms_left

    @classmethod
    async def get_all(cls, user_id: int):
        """Получение всех броней пользователя по user_id"""

        async with async_session() as session:
            query = select(
                cls.model.__table__.columns,
                Room.name.label('room_name'),
                Room.description.label('room_description'),
                Room.image_id.label('room_image'),
                Hotel.name.label('hotel_name')
            ).where(
                cls.model.user_id == user_id
            ).join(
                Room, Room.id == cls.model.rooms_id
            ).join(
                Hotel, Room.hotel_id == Hotel.id
            )

            bookings = await session.execute(query)
            return bookings.mappings().all()
