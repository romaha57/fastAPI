from datetime import datetime

from pydantic import BaseModel, field_serializer


class NewsSchema(BaseModel):
    """Модель для новостей"""

    title: str
    description: str
    created_at: datetime

    @field_serializer("created_at")
    def convert_datetime(self, dt: datetime, _info):
        """Преобразуем дату к удобно-читаемому виду"""

        return dt.strftime('%Y-%m-%d %H:%M')
