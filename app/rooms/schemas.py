from pydantic import BaseModel
from typing import Optional


class RoomSchema(BaseModel):
    """Схема для номеров в отеле"""

    id: int
    hotel_id: int
    name: str
    description: Optional[str] = None
    price: int
    services: list[str]
    quantity: int
    image_id: int
    total_cost: int
    rooms_left: int