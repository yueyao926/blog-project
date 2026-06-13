from pydantic import BaseModel
from datetime import datetime

from app.schemas.category import CategoryOut


class AuthorOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class ArticleCreate(BaseModel):
    title: str
    content: str
    summary: str
    cover_image: str | None = None
    category_id: int | None = None


class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str
    cover_image: str | None = None
    created_at: datetime
    author_id: int
    summary: str
    author: AuthorOut
    category_id: int | None = None
    category: CategoryOut | None = None

    class Config:
        from_attributes = True

class ArticleUpdate(BaseModel):
    title: str
    content: str
    cover_image: str | None = None
    summary: str
    category_id: int | None = None
