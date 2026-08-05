import os

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app.database import engine, Base
from app.routers import users
from app.routers import articles
from app.routers import comments
from app.routers import likes
from app.routers import category
from app.routers import obsidian
from app.routers import projects
from app.routers import site_settings
from app.models.article import Article
from app.models.comment import Comment
from app.models.article_like import ArticleLike
from app.models.category import Category
from app.models.comment_like import CommentLike
from app.models.project import Project
from app.models.site_setting import SiteSetting
from sqlalchemy import inspect, text

app = FastAPI()

from fastapi.staticfiles import StaticFiles

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

FRONTEND_ORIGIN = os.getenv(
    "FRONTEND_ORIGIN",
    "http://localhost:5173"
)

origins = [
    FRONTEND_ORIGIN,
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# Idempotent compatibility migration for existing databases.
with engine.begin() as connection:
    inspector = inspect(connection)
    article_columns = {column["name"] for column in inspector.get_columns("articles")}
    comment_columns = {column["name"] for column in inspector.get_columns("comments")}
    if "view_count" not in article_columns:
        connection.execute(text("ALTER TABLE articles ADD COLUMN view_count INTEGER NOT NULL DEFAULT 0"))
    if "parent_id" not in comment_columns:
        connection.execute(text("ALTER TABLE comments ADD COLUMN parent_id INTEGER REFERENCES comments(id) ON DELETE CASCADE"))

app.include_router(users.router)
app.include_router(articles.router)
app.include_router(comments.router)
app.include_router(likes.router)
app.include_router(category.router)
app.include_router(obsidian.router)
app.include_router(projects.router)
app.include_router(site_settings.router)
@app.get("/")
def root():
    return {"message": "博客后端启动成功"}


from fastapi import UploadFile, File
import shutil

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "url": f"http://127.0.0.1:8000/{file_path}"
    }
