from fastapi import APIRouter

from app.elastic_api.schemas import NewsSchema
from app.elastic_api.service import ESElasticSearch


router = APIRouter(
    prefix='/elastic',
    tags=['Работа с ElasticSearch']
)


@router.get('/create-index')
async def create_index():
    ESElasticSearch.create_index()

    return {'msg': 'index was created'}


@router.get('/all-news')
async def get_all_news():
    return ESElasticSearch.get_news()


@router.post('/create_news')
async def create_news(
    news_data: NewsSchema
):
    return ESElasticSearch.create_news(
        news_data.model_dump_json()
    )


@router.get('/search/{news_title}')
async def get_news_by_title(
        news_title: str
):
    return ESElasticSearch.get_news_by_title(news_title)
