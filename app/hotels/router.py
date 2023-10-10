import datetime
from datetime import date, datetime

from fastapi import APIRouter, UploadFile
from fastapi_cache.decorator import cache

from app.exceptions import HotelDoesNotExist, InvalidDateException
from app.hotels.schemas import HotelSchema
from app.hotels.service import HotelService
from app.utils.check_date import check_date
from app.utils.utils_files import check_json_format, load_data


router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)


@router.get('/{location}', response_model=list[HotelSchema])
@cache(expire=30)
async def get_hotels_by_location(
        location: str,
        date_from: date,
        date_to: date
):
    if check_date(date_from, date_to):
        raise InvalidDateException()

    return await HotelService.find_all(
        location=location,
        date_from=date_from,
        date_to=date_to
    )


@router.get('/search/{hotel_name}', response_model=list[HotelSchema])
@cache(expire=30)
async def get_hotels_by_hotel_name(
        hotel_name: str,
        date_from: date,
        date_to: date
):
    if check_date(date_from, date_to):
        raise InvalidDateException()

    return await HotelService.find_all(
        hotel_name=hotel_name,
        date_from=date_from,
        date_to=date_to
    )


@router.get('/id/{hotel_id}')
async def get_hotel(
        hotel_id: int
):
    hotel = await HotelService.get_by_id(id=hotel_id)
    if not hotel:
        raise HotelDoesNotExist()

    return hotel


@router.post('/load-json-hotels')
async def load_hotels_json(
        file: UploadFile
):
    if check_json_format(file):
        hotel_data = load_data(file)

        for hotel in hotel_data:
            await HotelService.create_object(
                name=hotel.get('name'),
                location=hotel.get('location'),
                services=hotel.get('services'),
                stars=hotel.get('stars'),
                rooms_quantity=hotel.get('rooms_quantity'),
                image_id=hotel.get('image_id')
            )

        return {'msg': 'hotels was added'}
