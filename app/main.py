import uvicorn as uvicorn
from fastapi import FastAPI

from bookings.router import router as router_bookings
from hotels.router import router as router_hotels
from users.router import router as router_users
from rooms.router import router as router_rooms


app = FastAPI(
    title='Сервис по бронированию отелей',
    version='1.0.0',
    description='API для работы с бронями отеля'
)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_users)


@app.get('/test')
def test():
    pass


if __name__ == '__main__':
    uvicorn.run('app.main:app', reload=True)
