from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.dependencies import (
    get_db,
    get_current_user
)

from app.models.comment import Comment
from app.models.article import Article
from app.models.user import User

from app.schemas.comment import (
    CommentCreate,
    CommentResponse
)

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)

@router.get(
    "/article/{article_id}",
    response_model=list[CommentResponse]
)
def get_comments(
    article_id: int,
    db: Session = Depends(get_db)
):
    comments = (
        db.query(Comment)
        .filter(
            Comment.article_id == article_id
        )
        .order_by(
            Comment.created_at.desc()
        )
        .all()
    )

    return comments

@router.post(
    "/article/{article_id}",
    response_model=CommentResponse
)
def create_comment(
    article_id: int,

    comment: CommentCreate,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
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

    new_comment = Comment(
        content=comment.content,
        article_id=article_id,
        user_id=current_user.id
    )

    db.add(new_comment)

    db.commit()

    db.refresh(new_comment)

    return new_comment