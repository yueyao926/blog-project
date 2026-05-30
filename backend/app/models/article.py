from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from app.database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String,
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    summary = Column(String)

    cover_image = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    author_id = Column(
        Integer,
        ForeignKey("users.id")
        
    )

    author = relationship(
    "User",
    back_populates="articles"
    )

    comments = relationship(
    "Comment",
    back_populates="article",
    cascade="all, delete"
    )