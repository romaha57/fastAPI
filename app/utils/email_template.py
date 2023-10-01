from email.message import EmailMessage

from pydantic import EmailStr

from app.settings import settings


def get_email_template(
        booking_data: dict,
        email_to: EmailStr
):
    """Создание шаблона для отправки письма"""

    email = EmailMessage()

    # для теста отправка происходит самому себе
    email_to = settings.SMTP_USER

    email['Subject'] = 'Подтвердите бронирование'
    email['From'] = settings.SMTP_USER
    email['To'] = email_to

    email.set_content(
        f"""
            <h1>Подтверждение бронирования</h1>
            <h3>C {booking_data.get('date_from')} по {booking_data.get('date_to')}</h3>
        """,
        subtype='html'
    )

    return email
