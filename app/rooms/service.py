from datetime import date

from sqlalchemy import select, func, or_, and_

from app.service.base import BaseService
from app.rooms.models import Room
from app.bookings.models import Booking

from app.database import async_session


class RoomService(BaseService):
    model = Room

    @classmethod
    async def get_all(cls,
                      hotel_id: int,
                      date_from: date,
                      date_to: date
                      ):
        async with async_session() as session:
            booked_rooms = select(
                Booking.rooms_id,
                func.count(Booking.rooms_id).label('rooms_booked')
            ).where(
                or_(
                    and_(
                        Booking.date_from >= date_from,
                        Booking.date_from <= date_to,
                    ),
                    and_(
                        Booking.date_from <= date_from,
                        Booking.date_to > date_from
                    )
                )
            ).group_by(
                Booking.rooms_id
            ).cte('booked_rooms')

            get_rooms = select(
                Room.__table__.columns,
                (Room.price * (date_to - date_from).days).label('total_cost'),
                (Room.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0)).label('rooms_left')
            ).join(
                booked_rooms, booked_rooms.c.rooms_id == Room.id, isouter=True
            )

            rooms = await session.execute(get_rooms)

            return rooms.mappings().all()


