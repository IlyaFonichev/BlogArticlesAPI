from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class Status(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"


class ArticleBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Заголовок статьи")
    content: str = Field(..., min_length=1, description="Содержание статьи")
    status: Status = Field(default=Status.DRAFT, description="Статус статьи")


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Заголовок статьи")
    content: Optional[str] = Field(None, min_length=1, description="Содержание статьи")
    status: Optional[Status] = Field(None, description="Статус статьи")


class Article(ArticleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
