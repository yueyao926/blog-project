from sqlalchemy import Column, Integer, String
from sqlalchemy import Boolean

from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True, index=True)

    email = Column(String, unique=True, index=True)

    password = Column(String)

    is_admin = Column(Boolean, default=False)

    articles = relationship(
        "Article",
        back_populates="author"
    )

    comments = relationship(
        "Comment",
        back_populates="user"
    )