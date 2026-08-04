from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False, index=True)
    description = Column(Text, nullable=False)
    github_url = Column(String(500), nullable=False)
    tags = Column(String(300), nullable=False, default="")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
