import json
import os
import shutil

from fastapi import UploadFile


def check_json_format(file: UploadFile):
    """Проверяем формат файла на json"""

    if file.filename.endswith('.json'):
        return True

    return False


def load_data(file: UploadFile) -> list[dict]:
    """Сохраянем файл с данными, считываем в словарь, удаляем файл и возвращаем данные"""

    path = f'app/static/files/{file.filename}'
    try:
        os.mkdir('app/static/files')
    except FileExistsError:
        pass
    with open(path, 'wb+') as saved_file:
        shutil.copyfileobj(file.file, saved_file)

    with open(path, 'r') as json_file:
        data = json.load(json_file)

    # удаляем файл
    os.remove(path)

    return data
