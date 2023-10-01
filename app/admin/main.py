from sqladmin import ModelView
from sqlalchemy import Select

from app.users.models import User
from app.hotels.models import Hotel
from app.bookings.models import Booking
from app.rooms.models import Room


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email] + [User.booking]
    can_delete = False
    save_as = True
    name = 'Пользователь'
    name_plural = 'Пользователи'
    icon = 'fa-solid fa-user'
    column_searchable_list = [User.id, User.email]
    column_labels = {User.booking: 'Бронь пользователя'}

    def search_query(self, stmt: Select, term: str) -> Select:
        """Поиск по email пользователя"""

        return stmt.filter(User.email.icontains(term))


class HotelAdmin(ModelView, model=Hotel):
    column_list = [col.name for col in Hotel.__table__.columns] + [Hotel.room]
    save_as = True
    name = 'Отель'
    name_plural = 'Отели'
    icon = 'fa-solid fa-hotel'
    column_searchable_list = [Hotel.id, Hotel.name]
    column_sortable_list = [Hotel.stars]
    column_labels = {
        Hotel.name: 'Название',
        Hotel.room: 'номер',
        Hotel.stars: 'Звезд',
        Hotel.services: 'Удобства',
        Hotel.location: 'Адрес',
        Hotel.rooms_quantity: 'Количество комнат'
    }

    def search_query(self, stmt: Select, term: str) -> Select:
        """Поиск по названию отеля"""

        return stmt.filter(Hotel.name.icontains(term))


class BookingAdmin(ModelView, model=Booking):
    column_list = [col.name for col in Booking.__table__.columns] + [Booking.room, Booking.user]
    save_as = True
    name = 'Бронь'
    name_plural = 'Брони'
    icon = 'fa-solid fa-tag'
    column_searchable_list = [Booking.id, Booking.date_from, Booking.date_to]
    column_sortable_list = [Booking.date_from, Booking.date_to, Booking.user_id, Booking.rooms_id]
    column_labels = {
        Booking.user: 'Забронировал',
        Booking.room: 'Номер',
        Booking.price: 'Цена',
        Booking.date_to: 'Дата выселения',
        Booking.date_from: 'Дата заселения',
        Booking.total_cost: 'Общая стоимость',
        Booking.total_days: 'Общее кол-во дней',
        Booking.id: 'ID брони',
        Booking.rooms_id: 'ID комнаты',
        Booking.user_id: 'ID пользователя'
    }

    def search_query(self, stmt: Select, term: str) -> Select:
        """Поиск по названию номера в броне"""

        return stmt.filter(Booking.room.icontains(term))




class RoomAdmin(ModelView, model=Room):
    column_list = [Room.id, Room.name, Room.services, Room.price, Room.hotel_id, Room.description]
    save_as = True
    name = 'Номер'
    name_plural = 'Номера'
    icon = 'fa-solid fa-bed'
    column_searchable_list = [Room.id, Room.hotel]
    column_sortable_list = [Room.hotel_id, Room.price]
    column_labels = {
        Room.name: 'Название',
        Room.price: 'Цена',
        Room.services: 'Удобства',
        Room.booking: 'Брони',
        Room.description: 'Описание',
        Room.hotel: 'Отель',
        Room.quantity: 'Количество',
        Room.hotel_id: 'ID отеля'
    }

    def search_query(self, stmt: Select, term: str) -> Select:
        """Поиск по названию номера"""

        return stmt.filter(Room.name.icontains(term))
