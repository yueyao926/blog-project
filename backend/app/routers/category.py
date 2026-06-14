from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.dependencies import get_current_admin

from app.models.article import Article
from app.models.category import Category
from app.models.article import Article
from app.models.user import User

from app.schemas.category import (
    CategoryCreate,
    CategoryOut,
)

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.post(
    "",
    response_model=CategoryOut
)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    if category.parent_id is not None:
        parent = db.query(Category).filter(
            Category.id == category.parent_id
        ).first()

        if not parent:
            raise HTTPException(
                status_code=404,
                detail="Parent category not found"
            )

    new_category = Category(
        name=category.name,
        parent_id=category.parent_id,
    )

    db.add(new_category)

    db.commit()

    db.refresh(new_category)

    return new_category


@router.get(
    "",
    response_model=list[CategoryOut]
)
def get_categories(
    db: Session = Depends(get_db),
):
    categories = db.query(Category).order_by(
        Category.id.asc()
    ).all()

    return categories


@router.put(
    "/{category_id}",
    response_model=CategoryOut
)
def update_category(
    category_id: int,
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    existing = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    if category.parent_id is not None:
        if category.parent_id == category_id:
            raise HTTPException(
                status_code=400,
                detail="Category cannot be its own parent"
            )

        parent = db.query(Category).filter(
            Category.id == category.parent_id
        ).first()

        if not parent:
            raise HTTPException(
                status_code=404,
                detail="Parent category not found"
            )

    existing.name = category.name
    existing.parent_id = category.parent_id

    db.commit()

    db.refresh(existing)

    return existing


@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    db.query(Category).filter(
        Category.parent_id == category_id
    ).update(
        {Category.parent_id: category.parent_id},
        synchronize_session=False,
    )

    db.query(Article).filter(
        Article.category_id == category_id
    ).update(
        {Article.category_id: None},
        synchronize_session=False,
    )

    has_articles = db.query(Article).filter(
        Article.category_id == category_id
    ).first()

    if has_articles:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete category with articles"
        )

    db.delete(category)

    db.commit()

    return {
        "message": "Category deleted successfully"
    }
