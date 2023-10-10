from datetime import date, datetime


def check_date(date_from: date, date_to: date) -> bool:
    """Проверка даты, которую ввел пользователь"""

    # если текущие время больше введенного пользователем или
    # дата выселения меньше даты заселения
    if date_to <= date_from or date_from < datetime.utcnow().date():
        return False

    return True
