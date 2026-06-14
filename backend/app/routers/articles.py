from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query
)

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.models.article import Article
from app.models.user import User

from app.models.article_like import ArticleLike
from app.models.comment import Comment

from app.schemas.article import (
    ArticleCreate,
    ArticleUpdate,
    ArticleResponse
)

from app.dependencies import get_current_admin


router = APIRouter(
    prefix="/articles",
    tags=["Articles"]
)


@router.post(
    "",
    response_model=ArticleResponse
)
def create_article(
    article: ArticleCreate,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_admin
    )
):
    new_article = Article(
        title=article.title,
        content=article.content,
        cover_image=article.cover_image,
        author_id=current_user.id ,
        summary=article.summary,
        category_id=article.category_id,
    )

    db.add(new_article)

    db.commit()

    db.refresh(new_article)

    return new_article

@router.get(
    "",
    response_model=list[ArticleResponse]
)
def get_articles(
    keyword: str | None = Query(None),

    db: Session = Depends(get_db)
):
    query = db.query(Article)

    if keyword:
        query = query.filter(
            Article.title.ilike(f"%{keyword}%")
        )

    articles = query.order_by(
        Article.created_at.desc()
    ).all()

    return articles

@router.get(
    "/{article_id}",
    response_model=ArticleResponse
)
def get_article(
    article_id: int,
    db: Session = Depends(get_db)
):
    article = db.query(Article).filter(
        Article.id == article_id
    ).first()

    if not article:
        raise HTTPException(
            status_code=404,
            detail="Article not found"
        )

    return article

@router.delete("/{article_id}")
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    article = db.query(Article).filter(Article.id == article_id).first()

    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")

    db.query(ArticleLike).filter(
        ArticleLike.article_id == article_id
    ).delete(synchronize_session=False)

    db.query(Comment).filter(
        Comment.article_id == article_id
    ).delete(synchronize_session=False)

    db.delete(article)
    db.commit()

    return {"message": "删除成功"}

@router.put(
    "/{article_id}",
    response_model=ArticleResponse
)
def update_article(
    article_id: int,

    updated_article: ArticleUpdate,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_admin
    )
):
    article = db.query(Article).filter(
        Article.id == article_id
    ).first()

    if not article:
        raise HTTPException(
            status_code=404,
            detail="Article not found"
        )

    article.title = updated_article.title

    article.summary = updated_article.summary

    article.cover_image = updated_article.cover_image

    article.content = updated_article.content

    article.category_id = updated_article.category_id

    db.commit()

    db.refresh(article)

    return article
