from datetime import date

from fastapi import APIRouter

from app.rooms.models import Room
from app.rooms.schemas import RoomSchema
from app.rooms.service import RoomService


router = APIRouter(
    prefix='/rooms',
    tags=['Комнаты']
)


@router.get('/hotels/{hotel_id}', response_model=list[RoomSchema])
async def get_rooms(
        hotel_id: int,
        date_from: date,
        date_to: date
):
    return await RoomService.get_all(
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to
    )