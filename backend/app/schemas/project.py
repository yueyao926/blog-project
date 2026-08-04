from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str = Field(min_length=1, max_length=1000)
    github_url: str = Field(min_length=1, max_length=500)
    tags: str = Field(default="", max_length=300)

    @field_validator("name", "description", "github_url", "tags")
    @classmethod
    def strip_text(cls, value: str) -> str:
        return value.strip()

    @field_validator("github_url")
    @classmethod
    def validate_github_url(cls, value: str) -> str:
        if not value.startswith(("https://github.com/", "http://github.com/")):
            raise ValueError("请输入有效的 GitHub 仓库地址")
        return value


class ProjectOut(ProjectCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
