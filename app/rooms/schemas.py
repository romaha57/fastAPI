from pydantic import BaseModel


class RoomSchema(BaseModel):
    """Схема для номеров в отеле"""

    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: list[str]
    quantity: int
    image_id: int
    total_cost: int
    rooms_left: int