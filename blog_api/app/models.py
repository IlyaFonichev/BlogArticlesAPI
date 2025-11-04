from datetime import datetime
from typing import Dict, List, Optional
from .schemas import ArticleCreate, ArticleUpdate, Article, Status


class ArticleStore:
    def __init__(self):
        self._articles: Dict[int, Article] = {}
        self._next_id = 1

    def get_all(self) -> List[Article]:
        return list(self._articles.values())

    def get_by_id(self, article_id: int) -> Optional[Article]:
        return self._articles.get(article_id)

    def create(self, article: ArticleCreate) -> Article:
        now = datetime.now()
        new_article = Article(
            id=self._next_id,
            title=article.title,
            content=article.content,
            status=article.status,
            created_at=now,
            updated_at=now
        )
        self._articles[self._next_id] = new_article
        self._next_id += 1
        return new_article

    def update(self, article_id: int, article_update: ArticleUpdate) -> Optional[Article]:
        if article_id not in self._articles:
            return None

        existing_article = self._articles[article_id]
        update_data = article_update.model_dump(exclude_unset=True)

        updated_article = existing_article.model_copy(update=update_data)
        updated_article.updated_at = datetime.now()

        self._articles[article_id] = updated_article
        return updated_article

    def delete(self, article_id: int) -> bool:
        if article_id in self._articles:
            del self._articles[article_id]
            return True
        return False

    def filter_articles(self, status: Optional[Status] = None, title_contains: Optional[str] = None) -> List[Article]:
        articles = self.get_all()

        if status:
            articles = [a for a in articles if a.status == status]

        if title_contains:
            articles = [a for a in articles if title_contains.lower() in a.title.lower()]

        return articles


article_store = ArticleStore()
