from pydantic import BaseModel


class HotelSchema(BaseModel):
    """Схема для отелей"""

    id: int
    name: str
    location: str
    services: list[str]
    stars: int
    rooms_quantity: int
    image_id: int
