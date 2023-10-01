from datetime import date

from pydantic import BaseModel


class BaseBookingSchema(BaseModel):
    """Базовое отображение бронирований"""

    id: int
    rooms_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_days: int
    total_cost: int


class CreateBookingSchema(BaseBookingSchema):
    """Схема для отображения бронирований при создании"""
    pass


class BookingsByUserSchema(BaseBookingSchema):
    """Схема для отображения бронирований пользователя"""

    room_name: str
    room_description: str
    room_image: int
    hotel_name: str
