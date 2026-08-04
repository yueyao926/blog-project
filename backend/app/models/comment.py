from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey,
    DateTime
)

from sqlalchemy.sql import func

from sqlalchemy.orm import backref, relationship

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

    parent_id = Column(
        Integer,
        ForeignKey("comments.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    article = relationship(
        "Article",
        back_populates="comments"
    )

    user = relationship(
        "User",
        back_populates="comments"
    )

    replies = relationship(
        "Comment",
        cascade="all, delete-orphan",
        backref=backref("parent", remote_side=[id]),
        single_parent=True,
    )

    likes = relationship(
        "CommentLike",
        cascade="all, delete-orphan",
        back_populates="comment",
    )
