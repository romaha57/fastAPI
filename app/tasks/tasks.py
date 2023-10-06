import smtplib
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from app.settings import settings
from app.tasks.settings_celery import celery
from app.utils.email_template import get_email_template


@celery.task
def save_resized_img(path: str):
    """Обрезаем фото до разрешения 500 на 500 и сохраняем"""

    path = Path(path)

    img = Image.open(path)
    image = img.resize((500, 500))
    image.save(f'app/static/images/resized_{path.name}')


@celery.task
def send_email(
        booking_data: dict,
        email_to: EmailStr
):
    message = get_email_template(booking_data, email_to)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(message)
