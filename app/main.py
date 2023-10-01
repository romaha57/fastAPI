import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.main import UserAdmin, HotelAdmin, RoomAdmin, BookingAdmin
from app.database import engine

from bookings.router import router as router_bookings
from hotels.router import router as router_hotels
from users.router import router as router_users
from rooms.router import router as router_rooms
from frontend.router import router as router_html
from upload_file.router import router as router_file
from app.admin.auth import authentication_backend

from settings import settings

app = FastAPI(
    title='Сервис по бронированию отелей',
    version='1.0.0',
    description='API для работы с бронями отеля'
)


origins = [
    'http://127.0.0.0:8000'
]

app.mount('/static', StaticFiles(directory='app/static'), 'static')

app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_users)
app.include_router(router_html)
app.include_router(router_file)

# подключение админки
admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(HotelAdmin)
admin.add_view(BookingAdmin)
admin.add_view(RoomAdmin)


@app.on_event('startup')
async def startup_redis():
    """Подключение к редису при старте приложения"""

    redis = aioredis.from_url(settings.REDIS_CONNECT)
    FastAPICache.init(RedisBackend(redis), prefix='cache')


if __name__ == '__main__':
    uvicorn.run('app.main:app', reload=True)
