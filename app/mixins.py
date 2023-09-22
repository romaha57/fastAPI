class InitExceptionMixin:
    """Миксин для создания собственных исключений"""

    status_code = 400
    detail = 'ошибка'

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)
