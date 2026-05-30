from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey,
    DateTime
)

from sqlalchemy.sql import func

from sqlalchemy.orm import relationship

from app.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    content = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    article_id = Column(
        Integer,
        ForeignKey("articles.id")
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    article = relationship(
        "Article",
        back_populates="comments"
    )

    user = relationship(
        "User",
        back_populates="comments"
    )