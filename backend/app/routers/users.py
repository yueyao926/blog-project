from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password

from app.core.auth import create_access_token
from app.core.security import verify_password

from app.schemas.token import Token

from app.dependencies import get_current_user

from app.schemas.user import UserResponse
from app.schemas.user import UserOut

from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies import get_current_admin

router = APIRouter(
    tags=["Users"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_username = db.query(User).filter(
        User.username == user.username
    ).first()

    if existing_username:
        raise HTTPException(
            status_code=400,
            detail="用户名已存在"
        )

    existing_email = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="邮箱已被注册"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()

        if db.query(User).filter(
            User.username == user.username
        ).first():
            raise HTTPException(
                status_code=400,
                detail="用户名已存在"
            )

        if db.query(User).filter(
            User.email == user.email
        ).first():
            raise HTTPException(
                status_code=400,
                detail="邮箱已被注册"
            )

        raise HTTPException(
            status_code=400,
            detail="注册信息已存在"
        )

    db.refresh(new_user)

    return {
        "message": "注册成功",
        "user_id": new_user.id
    }

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # 查找用户
    user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    # 用户不存在
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # 验证密码
    if not verify_password(
        form_data.password,
        user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # 生成 token
    access_token = create_access_token(
        data={
            "sub": user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get(
    "/me",
    response_model=UserOut
)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user


@router.get(
    "/admin/users",
    response_model=list[UserOut]
)
def get_admin_users(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    return db.query(User).order_by(User.id.asc()).all()

@router.get("/admin-test")
def admin_test(
    admin: User = Depends(get_current_admin)
):
    return {
        "message": "你是管理员"
    }
