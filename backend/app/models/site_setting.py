from sqlalchemy import Column, Integer, String

from app.database import Base


class SiteSetting(Base):
    __tablename__ = "site_settings"

    id = Column(Integer, primary_key=True, default=1)
    hero_image = Column(String, nullable=True)
