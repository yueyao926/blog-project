from pydantic import BaseModel


class SiteSettingOut(BaseModel):
    hero_image: str | None = None

    class Config:
        from_attributes = True
