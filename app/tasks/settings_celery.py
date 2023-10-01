from celery import Celery

from app.settings import settings


celery = Celery(
    main='tasks',
    broker=settings.REDIS_CONNECT,
    include=['app.tasks.tasks'],
    broker_connection_retry_on_startup=True
)
