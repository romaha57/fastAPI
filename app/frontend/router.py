from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

from app.frontend.naming import TITLE_HOTELS_PAGE, TITLE_INDEX_PAGE
from app.hotels.router import get_hotels_by_location
from app.hotels.schemas import HotelSchema


router = APIRouter(
    prefix='/site',
    tags=['Фронтенд']
)

templates = Jinja2Templates(directory='app/frontend/templates')


@router.get('/')
async def index(
        request: Request
):
    return templates.TemplateResponse(
        name='index.html',
        context={
            'request': request,
            'title': TITLE_INDEX_PAGE
        }
    )


@router.get('/hotels', response_class=HTMLResponse)
async def hotels_html(
        request: Request,
        hotels: list[HotelSchema] = Depends(get_hotels_by_location)
):
    return templates.TemplateResponse(
        name='hotels.html',
        context={
            'request': request,
            'hotels': hotels,
            'title': TITLE_HOTELS_PAGE
        }
    )


@router.get('/login', response_class=HTMLResponse)
async def login(
        request: Request,
):
    return templates.TemplateResponse(
        name='login.html',
        context={
            'request': request
        }
    )
