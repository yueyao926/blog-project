from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.dependencies import (
    get_db,
    get_current_user
)

from app.models.article_like import (
    ArticleLike
)

from app.models.user import User

router = APIRouter(
    prefix="/likes",
    tags=["Likes"]
)


@router.post("/{article_id}")
def toggle_like(
    article_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    existing_like = db.query(
        ArticleLike
    ).filter(
        ArticleLike.article_id == article_id,
        ArticleLike.user_id == current_user.id
    ).first()

    # 已点赞 -> 取消点赞
    if existing_like:

        db.delete(existing_like)

        db.commit()

        return {
            "liked": False
        }

    # 未点赞 -> 点赞
    new_like = ArticleLike(
        article_id=article_id,
        user_id=current_user.id
    )

    db.add(new_like)

    db.commit()

    return {
        "liked": True
    }

@router.get("/{article_id}")
def get_like_count(
    article_id: int,

    db: Session = Depends(get_db)
):

    count = db.query(
        ArticleLike
    ).filter(
        ArticleLike.article_id == article_id
    ).count()

    return {
        "count": count
    }