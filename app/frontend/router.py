from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

from app.hotels.router import get_hotels_by_location
from app.hotels.schemas import HotelSchema
from app.frontend.naming import TITLE_INDEX_PAGE, TITLE_HOTELS_PAGE
from app.users.router import login_user

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