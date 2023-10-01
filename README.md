# fastAPI







Примечание:
- в качестве гет параметров можно использовать класс как аргумент эндпоинта
- alembic init migrations
- в migrations/env добавили путь для импортов, импорты Base и моделей, добавили config.set_main_options, прописали target_metadata
- переместили alembic.ini в корень и поменяли путь в файле(script_location)
- alembic revision --autogenerate -m 'message' - создание миграций
- alembic upgrade head - применение миграций(alembic downgrade -1)
- celery -A app.tasks.settings_celery:celery flower --loglevel=INFO запуск визуального интерфейса для отложенных задач
- celery -A app.tasks.settings_celery:celery worker --loglevel=INFO запуск воркера
