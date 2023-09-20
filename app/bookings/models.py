from sqlalchemy import Column, Integer, Computed, ForeignKey, Date

from app.database import Base


class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    rooms_id = Column(ForeignKey('rooms.id'))
    user_id = Column(ForeignKey('users.id'))
    date_from = Column(Date)
    date_to = Column(Date)
    price = Column(Integer)
    total_days = Column(Integer, Computed('date_to - date_from'))
    total_cost = Column(Integer, Computed('(date_to - date_from) * price'))
