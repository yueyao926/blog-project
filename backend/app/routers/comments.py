from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.models.article import Article
from app.models.comment import Comment
from app.models.comment_like import CommentLike
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentResponse

router = APIRouter(prefix="/comments", tags=["Comments"])


def serialize_comment(item: Comment) -> CommentResponse:
    return CommentResponse(
        id=item.id,
        content=item.content,
        created_at=item.created_at,
        user=item.user,
        parent_id=item.parent_id,
        like_count=len(item.likes),
    )


@router.get("/article/{article_id}", response_model=list[CommentResponse])
def get_comments(article_id: int, db: Session = Depends(get_db)):
    comments = (
        db.query(Comment)
        .filter(Comment.article_id == article_id)
        .order_by(Comment.created_at.asc())
        .all()
    )
    return [serialize_comment(item) for item in comments]


@router.post("/article/{article_id}", response_model=CommentResponse)
def create_comment(
    article_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not db.query(Article).filter(Article.id == article_id).first():
        raise HTTPException(status_code=404, detail="Article not found")
    if comment.parent_id is not None:
        parent = db.query(Comment).filter(
            Comment.id == comment.parent_id,
            Comment.article_id == article_id,
        ).first()
        if not parent:
            raise HTTPException(status_code=404, detail="Parent comment not found")

    new_comment = Comment(
        content=comment.content.strip(),
        article_id=article_id,
        user_id=current_user.id,
        parent_id=comment.parent_id,
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return serialize_comment(new_comment)


@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    target = db.query(Comment).filter(Comment.id == comment_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Comment not found")
    if target.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You can only delete your own comments")
    db.delete(target)
    db.commit()
    return {"message": "Comment deleted"}


@router.post("/{comment_id}/like")
def toggle_comment_like(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not db.query(Comment).filter(Comment.id == comment_id).first():
        raise HTTPException(status_code=404, detail="Comment not found")
    existing = db.query(CommentLike).filter(
        CommentLike.comment_id == comment_id,
        CommentLike.user_id == current_user.id,
    ).first()
    if existing:
        db.delete(existing)
        liked = False
    else:
        db.add(CommentLike(comment_id=comment_id, user_id=current_user.id))
        liked = True
    db.commit()
    count = db.query(CommentLike).filter(CommentLike.comment_id == comment_id).count()
    return {"liked": liked, "count": count}
