from sqlalchemy import JSON, Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Hotel(Base):
    """Модель отеля"""

    __tablename__ = 'hotels'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    services = Column(JSON, nullable=False)
    stars = Column(Integer, nullable=False)
    rooms_quantity = Column(Integer, nullable=False)
    image_id = Column(Integer, nullable=False)

    room = relationship('Room', back_populates='hotel')

    def __str__(self):
        return f'{self.name}'
