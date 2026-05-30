from sqlalchemy import (
    Column,
    Integer,
    ForeignKey
)

from app.database import Base


class ArticleLike(Base):
    __tablename__ = "article_likes"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    article_id = Column(
        Integer,
        ForeignKey("articles.id")
    )