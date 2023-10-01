import asyncio
from datetime import date

from fastapi import APIRouter

from fastapi_cache.decorator import cache

from app.exceptions import HotelDoesNotExist
from app.hotels.service import HotelService
from app.hotels.schemas import HotelSchema


router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)


@router.get('/{location}', response_model=list[HotelSchema])
@cache(expire=30)
async def get_hotels(
        location: str,
        date_from: date,
        date_to: date
):
    await asyncio.sleep(5)
    return await HotelService.find_all(
        location=location,
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
