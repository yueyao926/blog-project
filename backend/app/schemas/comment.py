from pydantic import BaseModel

from datetime import datetime


class CommentCreate(BaseModel):
    content: str


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

    class Config:
        from_attributes = True