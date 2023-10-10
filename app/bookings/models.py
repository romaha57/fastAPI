from sqlalchemy import Column, Computed, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database import Base


class Booking(Base):
    """Модель бронирования"""

    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    rooms_id = Column(ForeignKey('rooms.id'))
    user_id = Column(ForeignKey('users.id'))
    date_from = Column(Date)
    date_to = Column(Date)
    price = Column(Integer)

    # вычисляемые поля в БД
    total_days = Column(Integer, Computed('date_to - date_from'))
    total_cost = Column(Integer, Computed('(date_to - date_from) * price'))

    user = relationship('User', back_populates='booking')
    room = relationship('Room', back_populates='booking')

    def __str__(self):
        return f'Booking #{self.id}'
