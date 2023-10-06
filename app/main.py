import time

import uvicorn as uvicorn
from fastapi_versioning import VersionedFastAPI

from app.logger import logger
from app.bookings.router import router as router_bookings
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from app.frontend.router import router as router_html
from app.hotels.router import router as router_hotels
from redis import asyncio as aioredis
from app.rooms.router import router as router_rooms
from app.settings import settings
from sqladmin import Admin
from app.upload_file.router import router as router_file
from app.users.router import router as router_users
import sentry_sdk

from app.admin.auth import authentication_backend
from app.admin.main import BookingAdmin, HotelAdmin, RoomAdmin, UserAdmin
from app.database import engine


# подключение к sentry для мониторинга ошибок
sentry_sdk.init(
    dsn=settings.SENTRY_KEY,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)
app = FastAPI(
    title='Сервис по бронированию отелей',
    version='1.0.0',
    description='API для работы с бронями отеля'
)

origins = [
    'http://127.0.0.0:8000'
]

app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_users)
app.include_router(router_html)
app.include_router(router_file)

# добавление версионирования API
app = VersionedFastAPI(app,
                       version_format='{major}',
                       prefix_format='/v{major}'
                       )

# подключение админки
admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(HotelAdmin)
admin.add_view(BookingAdmin)
admin.add_view(RoomAdmin)

# load static files
app.mount('/static', StaticFiles(directory='app/static'), 'static')


@app.on_event('startup')
async def startup_redis():
    """Подключение к редису при старте приложения"""

    redis = aioredis.from_url(settings.REDIS_CONNECT)
    FastAPICache.init(RedisBackend(redis), prefix='cache')
    logger.info('Redis is connect')


@app.middleware('http')
async def request_execution_time(
        request: Request,
        call_next
):
    """Логгирование времени выполнения запроса"""

    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info('Request completed', extra={
        'process_time': round(process_time, 4),
        'endpoint': request.url
    })

    return response


if __name__ == '__main__':
    uvicorn.run('app.main:app', reload=True)
