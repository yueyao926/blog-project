from pydantic import BaseModel
from datetime import datetime

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


class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str
    cover_image: str | None = None
    created_at: datetime
    author_id: int
    summary: str
    author: AuthorOut

    class Config:
        from_attributes = True

class ArticleUpdate(BaseModel):
    title: str
    content: str
    cover_image: str | None = None
    summary: str