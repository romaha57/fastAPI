from elasticsearch import Elasticsearch

from app.elastic_api.mappings import MAPPINGS
from app.settings import settings


class ESElasticSearch:
    """Класс для работы с api elasticsearch"""

    es_client = Elasticsearch(settings.ELASTICSEARCH_URL)

    @classmethod
    def create_index(cls):
        """Создание индекса в elastic"""

        cls.es_client.indices.create(
            index=settings.ELASTICSEARCH_INDEX_NAME,
            body={
                'mappings': MAPPINGS
            },
            ignore=400
        )

    @classmethod
    def get_news(cls) -> dict:
        """Получение всех новостей(100 штук)"""

        result = cls.es_client.search(
            index=settings.ELASTICSEARCH_INDEX_NAME,
            body={
                "query": {
                    "match_all": {}
                }
            },
            size=100
        )
        return result['hits']['hits']

    @classmethod
    def create_news(cls, news_data: str) -> dict:
        """Создание новости"""

        news = cls.es_client.index(
            index=settings.ELASTICSEARCH_INDEX_NAME,
            body=news_data
        )

        return news

    @classmethod
    def get_news_by_title(cls, news_title: str):
        news = cls.es_client.search(
            index=settings.ELASTICSEARCH_INDEX_NAME,
            body={
                'query': {
                    'match': {
                        'title': news_title
                    }
                }
            }
        )

        return news['hits']['hits']
