from pydantic import BaseModel, Field


class ObsidianArticleUpsert(BaseModel):
    article_id: int | None = None
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1)
    summary: str = ""
    cover_image: str | None = None
    category_id: int | None = None


class ObsidianArticleResult(BaseModel):
    article_id: int
    article_url: str
    created: bool


class ObsidianAssetUpload(BaseModel):
    filename: str = Field(min_length=1, max_length=255)
    content_base64: str = Field(min_length=1)


class ObsidianAssetResult(BaseModel):
    url: str
