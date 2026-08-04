from pydantic import BaseModel

from datetime import datetime


class CommentCreate(BaseModel):
    content: str
    parent_id: int | None = None


class CommentUser(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class CommentResponse(BaseModel):
    id: int
    content: str
    created_at: datetime

    user: CommentUser
    parent_id: int | None = None
    like_count: int = 0

    class Config:
        from_attributes = True
