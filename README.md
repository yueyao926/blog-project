# Full Stack Blog System

一个基于 Vue3 + FastAPI + PostgreSQL 的全栈博客系统。

---

## 项目简介

这是一个前后端分离的个人博客平台。

项目支持：

- 用户注册
- 用户登录
- JWT 身份认证
- 管理员权限控制
- 发布文章
- 编辑文章
- 删除文章
- Markdown 编辑器
- Markdown 渲染
- 图片上传
- 评论系统
- 点赞系统
- PostgreSQL 数据存储

---

## 技术栈

### Frontend

- Vue 3
- Vite
- Vue Router
- Axios
- Tailwind CSS
- md-editor-v3
- Marked
- Highlight.js

### Backend

- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- JWT Authentication
- Bcrypt Password Hashing

---

## 项目结构

```text
blog-project
│
├── backend
│   ├── app
│   │   ├── models
│   │   ├── routers
│   │   └── schemas
│   ├── database.py
│   ├── dependencies.py
│   └── main.py
│
├── frontend
│   ├── src
│   │   ├── pages
│   │   ├── components
│   │   ├── router
│   │   └── services
│
└── README.md
```

---

## 已实现功能

### 用户系统

- 用户注册
- 用户登录
- JWT Token
- 密码加密存储
- 获取当前用户
- 管理员权限控制

### 博客系统

- 发布文章
- 编辑文章
- 删除文章
- 查看文章详情
- 首页文章列表
- 文章摘要
- 封面图

### Markdown

- Markdown 编辑器
- Markdown 实时保存
- Markdown 渲染
- 代码高亮
- 图片插入

### 评论系统

- 发表评论
- 查看评论
- 评论与用户关联

### 点赞系统

- 点赞文章
- 取消点赞
- 点赞数量统计

### 文件上传

- 图片上传
- FastAPI 静态资源访问

---

## 数据库设计

### User

```text
id
username
email
password
is_admin
```

### Article

```text
id
title
summary
content
cover_image
author_id
created_at
```

### Comment

```text
id
content
user_id
article_id
created_at
```

### ArticleLike

```text
id
user_id
article_id
```

---

## 本地运行

### Backend

进入 backend：

```bash
cd backend
```

安装依赖：

```bash
pip install -r requirements.txt
```

启动：

```bash
uvicorn app.main:app --reload
```

后端地址：

```text
http://127.0.0.1:8000
```

---

### Frontend

进入 frontend：

```bash
cd frontend
```

安装依赖：

```bash
npm install
```

启动：

```bash
npm run dev
```

前端地址：

```text
http://localhost:5173
```

---

## 项目截图

待补充

---

## 后续计划

- 标签系统
- 搜索功能
- 收藏功能
- Docker 部署
- Linux 服务器部署
- Nginx
- HTTPS
- 域名访问

---

## Author

GitHub:

https://github.com/yueyao926