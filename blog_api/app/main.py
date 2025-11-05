from fastapi import FastAPI, HTTPException, status, Query
from typing import List, Optional
from .models import article_store
from .schemas import Article, ArticleCreate, ArticleUpdate, Status

app = FastAPI(
    title="Blog Articles API",
    description="API для управления статьями блога",
    version="1.0.0"
)


@app.get(
    "/articles/",
    response_model=List[Article],
    summary="Получить список статей",
    description="Возвращает список всех статей с возможностью фильтрации"
)
async def list_articles(
        status: Optional[Status] = Query(
            None,
            description="Фильтр по статусу статьи"
        ),
        title_contains: Optional[str] = Query(
            None,
            description="Фильтр по содержанию в заголовке"
        ),
        skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
        limit: int = Query(100, ge=1, le=1000, description="Максимальное количество записей")
):
    """
    Получить список статей с возможностью фильтрации и пагинации.
    - status: Фильтр по статусу (draft, published)
    - title_contains: Поиск по части заголовка
    - skip: Пропустить первые N записей
    - limit: Ограничить количество результатов
    """
    articles = article_store.filter_articles(status=status, title_contains=title_contains)
    return articles[skip:skip + limit]


@app.get(
    "/articles/{article_id}",
    response_model=Article,
    summary="Получить статью по ID",
    responses={
        404: {"description": "Статья не найдена"}
    }
)
async def get_article(article_id: int):
    """
    Получить конкретную статью по её идентификатору.
    - article_id: ID статьи
    """
    article = article_store.get_by_id(article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Статья не найдена"
        )
    return article


@app.post(
    "/articles/",
    response_model=Article,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую статью",
    responses={
        201: {"description": "Статья успешно создана"}
    }
)
async def create_article(article: ArticleCreate):
    """
    Создать новую статью.
    - title: Заголовок статьи (обязательный)
    - content: Содержание статьи (обязательный)
    - status: Статус статьи (draft/published, по умолчанию draft)
    """
    return article_store.create(article)


@app.put(
    "/articles/{article_id}",
    response_model=Article,
    summary="Обновить статью",
    responses={
        404: {"description": "Статья не найдена"}
    }
)
async def update_article(article_id: int, article_update: ArticleUpdate):
    """
    Полностью обновить статью.
    - article_id: ID статьи для обновления
    - title: Новый заголовок (опционально)
    - content: Новое содержание (опционально)
    - status: Новый статус (опционально)
    """
    updated_article = article_store.update(article_id, article_update)
    if not updated_article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Статья не найдена"
        )
    return updated_article


@app.delete(
    "/articles/{article_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить статью",
    responses={
        204: {"description": "Статья успешно удалена"},
        404: {"description": "Статья не найдена"}
    }
)
async def delete_article(article_id: int):
    """
    Удалить статью по ID.
    - article_id: ID статьи для удаления
    """
    if not article_store.delete(article_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Статья не найдена"
        )


@app.get("/")
async def root():
    return {"message": "Blog Articles API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
