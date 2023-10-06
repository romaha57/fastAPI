from datetime import date

from sqlalchemy import and_, func, or_, select

from app.bookings.models import Booking
from app.database import async_session
from app.hotels.models import Hotel
from app.rooms.models import Room
from app.service.base import BaseService


class HotelService(BaseService):
    model = Hotel

    @classmethod
    async def find_all(cls,
                       date_from: date,
                       date_to: date,
                       location: str = None,
                       hotel_name: str = None
                       ):

        # создаем запрос на поиск по названию или локации
        if location:
            query = Hotel.location.like(f"%{location.capitalize()}%")
        else:
            query = Hotel.name.like(f"%{hotel_name.capitalize()}%")

        # таблица с room_id и количество броней этого номера на эти даты
        booked_rooms = (
            select(Booking.rooms_id, func.count(Booking.rooms_id).label("rooms_booked"))
            .select_from(Booking)
            .where(
                or_(
                    and_(
                        Booking.date_from >= date_from,
                        Booking.date_from <= date_to,
                    ),
                    and_(
                        Booking.date_from <= date_from,
                        Booking.date_to > date_from,
                    ),
                ),
            )
            .group_by(Booking.rooms_id)
            .cte("booked_rooms")
        )

        # таблица с hotel_id и количество свободных номеров в ней
        booked_hotels = (
            select(Room.hotel_id, func.sum(
                Room.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0)
            ).label("rooms_left"))
            .select_from(Room)
            .join(booked_rooms, booked_rooms.c.rooms_id == Room.id, isouter=True)
            .group_by(Room.hotel_id)
            .cte("booked_hotels")
        )

        # получаем отели где есть хотя бы 1 свободный номер
        get_hotels_with_rooms = (
            select(
                Hotel.__table__.columns,
                booked_hotels.c.rooms_left,
            )
            .join(booked_hotels, booked_hotels.c.hotel_id == Hotel.id, isouter=True)
            .where(
                and_(
                    booked_hotels.c.rooms_left > 0,
                    query,
                )
            )
        ).order_by('id')

        async with async_session() as session:
            hotels_with_rooms = await session.execute(get_hotels_with_rooms)

            return hotels_with_rooms.mappings().all()
