from datetime import date

from fastapi import APIRouter, UploadFile

from app.exceptions import InvalidDateException
from app.rooms.schemas import RoomSchema
from app.rooms.service import RoomService
from app.utils.check_date import check_date
from app.utils.utils_files import check_json_format, load_data


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
    if not check_date(date_from, date_to):
        raise InvalidDateException()

    return await RoomService.get_all(
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to
    )


@router.post('/load-json-rooms')
async def load_rooms_json(
        file: UploadFile
):
    if check_json_format(file):
        hotel_data = load_data(file)

        for hotel in hotel_data:
            await RoomService.create_object(
                hotel_id=hotel.get('hotel_id'),
                name=hotel.get('name'),
                description=hotel.get('description'),
                price=hotel.get('price'),
                services=hotel.get('services'),
                quantity=hotel.get('quantity'),
                image_id=hotel.get('image_id'),
            )

        return {'msg': 'rooms was added'}
