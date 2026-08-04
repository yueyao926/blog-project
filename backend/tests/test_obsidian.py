import base64
import os
from pathlib import Path

import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.models import article, article_like, category, comment, user  # noqa: F401
from app.models.user import User
from app.routers.obsidian import require_obsidian_token, upload_asset, upsert_article
from app.schemas.obsidian import ObsidianArticleUpsert, ObsidianAssetUpload


@pytest.fixture()
def db(monkeypatch):
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    session.add(User(username="admin", email="admin@example.com", password="x", is_admin=True))
    session.commit()
    monkeypatch.setenv("OBSIDIAN_AUTHOR_EMAIL", "admin@example.com")
    monkeypatch.setenv("BLOG_PUBLIC_URL", "https://blog.example.com")
    yield session
    session.close()


def test_create_then_update_article(db):
    created = upsert_article(
        ObsidianArticleUpsert(title="First", content="# body", summary="summary"), db, None
    )
    assert created.created is True
    assert created.article_url == f"https://blog.example.com/articles/{created.article_id}"

    updated = upsert_article(
        ObsidianArticleUpsert(
            article_id=created.article_id, title="Updated", content="new body"
        ),
        db,
        None,
    )
    assert updated.created is False
    assert updated.article_id == created.article_id


def test_token_is_required(monkeypatch):
    monkeypatch.setenv("OBSIDIAN_API_TOKEN", "correct-token")
    with pytest.raises(HTTPException) as error:
        require_obsidian_token("wrong-token")
    assert error.value.status_code == 401


def test_upload_asset(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("BLOG_PUBLIC_URL", "https://blog.example.com")
    result = upload_asset(
        ObsidianAssetUpload(
            filename="image.png",
            content_base64=base64.b64encode(b"png bytes").decode("ascii"),
        ),
        None,
    )
    assert result.url.startswith("https://blog.example.com/uploads/")
    assert len(list(Path("uploads").glob("*.png"))) == 1
