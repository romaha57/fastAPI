import asyncio
import datetime
from datetime import date, datetime

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.exceptions import HotelDoesNotExist, InvalidDateException
from app.hotels.schemas import HotelSchema
from app.hotels.service import HotelService

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
    if date_to <= date_from or date_to < datetime.utcnow().date():
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
    if date_to <= date_from or date_from < datetime.utcnow().date():
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
