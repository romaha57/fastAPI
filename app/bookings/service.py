from app.service.base import BaseService

from .models import Booking


class BookingService(BaseService):
    """Класс для работы с бронями в БД"""

    model = Booking
