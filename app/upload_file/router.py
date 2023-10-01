import shutil

from fastapi import APIRouter, UploadFile

from app.tasks.tasks import save_resized_img


router = APIRouter(
    prefix='/file',
    tags=['Загрузка файлов']
)


@router.post('')
async def upload_file(
        file: UploadFile,
        name: int
):
    file_extension = file.filename.split('.')[1]
    path = f'app/static/images/{name}.{file_extension}'
    with open(path, 'wb+') as saved_file:
        shutil.copyfileobj(file.file, saved_file)
    save_resized_img.delay(path)
