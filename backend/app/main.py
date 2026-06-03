from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app.database import engine, Base
from app.routers import users
from app.routers import articles
from app.routers import comments
from app.routers import likes
from app.routers import category
from app.models.article import Article
from app.models.comment import Comment
from app.models.article_like import ArticleLike
from app.models.category import Category

app = FastAPI()

from fastapi.staticfiles import StaticFiles

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(articles.router)
app.include_router(comments.router)
app.include_router(likes.router)
app.include_router(category.router)
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