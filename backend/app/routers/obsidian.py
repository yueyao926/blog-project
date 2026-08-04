import base64
import binascii
import os
import secrets
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.article import Article
from app.models.category import Category
from app.models.user import User
from app.schemas.obsidian import (
    ObsidianArticleResult,
    ObsidianArticleUpsert,
    ObsidianAssetResult,
    ObsidianAssetUpload,
)

router = APIRouter(prefix="/integrations/obsidian", tags=["Obsidian"])


def require_obsidian_token(
    x_obsidian_token: str | None = Header(default=None),
) -> None:
    expected = os.getenv("OBSIDIAN_API_TOKEN", "")
    if not expected:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Obsidian integration is not configured",
        )
    if not x_obsidian_token or not secrets.compare_digest(x_obsidian_token, expected):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Obsidian token",
        )


def get_author(db: Session) -> User:
    author_email = os.getenv("OBSIDIAN_AUTHOR_EMAIL", "")
    author = db.query(User).filter(User.email == author_email).first()
    if not author or not author.is_admin:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OBSIDIAN_AUTHOR_EMAIL must identify an administrator",
        )
    return author


def public_url(path: str) -> str:
    base = os.getenv("BLOG_PUBLIC_URL", "http://localhost").rstrip("/")
    return f"{base}{path}"


@router.post("/articles", response_model=ObsidianArticleResult)
def upsert_article(
    payload: ObsidianArticleUpsert,
    db: Session = Depends(get_db),
    _: None = Depends(require_obsidian_token),
):
    author = get_author(db)
    article = None
    created = payload.article_id is None

    if payload.article_id is not None:
        article = db.query(Article).filter(Article.id == payload.article_id).first()
        if not article:
            raise HTTPException(status_code=404, detail="Article to update was not found")
        if article.author_id != author.id:
            raise HTTPException(status_code=403, detail="Cannot update another author's article")

    if payload.category_id is not None:
        category = db.query(Category).filter(Category.id == payload.category_id).first()
        if not category:
            raise HTTPException(status_code=422, detail="category_id does not exist")

    if article is None:
        article = Article(author_id=author.id)
        db.add(article)

    article.title = payload.title.strip()
    article.content = payload.content
    article.summary = payload.summary
    article.cover_image = payload.cover_image
    article.category_id = payload.category_id
    db.commit()
    db.refresh(article)

    return ObsidianArticleResult(
        article_id=article.id,
        article_url=public_url(f"/articles/{article.id}"),
        created=created,
    )


@router.post("/assets", response_model=ObsidianAssetResult)
def upload_asset(
    payload: ObsidianAssetUpload,
    _: None = Depends(require_obsidian_token),
):
    extension = Path(payload.filename).suffix.lower()
    allowed = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
    if extension not in allowed:
        raise HTTPException(status_code=415, detail="Unsupported image type")

    try:
        content = base64.b64decode(payload.content_base64, validate=True)
    except (binascii.Error, ValueError):
        raise HTTPException(status_code=422, detail="Invalid base64 content")

    max_bytes = 10 * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(status_code=413, detail="Image exceeds 10 MB")

    uploads = Path("uploads")
    uploads.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid4().hex}{extension}"
    (uploads / filename).write_bytes(content)
    return ObsidianAssetResult(url=public_url(f"/uploads/{filename}"))
