from fastapi import APIRouter


router = APIRouter(
    prefix='/rooms',
    tags=['Комнаты']
)


@router.get('')
def get_rooms():
    return 'rooms'