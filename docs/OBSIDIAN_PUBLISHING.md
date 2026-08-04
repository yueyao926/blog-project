# 从 Obsidian 直接发布到博客

## 1. 配置博客服务

确认你已经注册了博客管理员账号，并且数据库中的该账号 `is_admin` 为 `true`。在项目根目录 `.env` 增加：

```dotenv
OBSIDIAN_API_TOKEN=一段至少48位的随机字符串
OBSIDIAN_AUTHOR_EMAIL=你的管理员邮箱
BLOG_PUBLIC_URL=http://localhost
```

可用 `python -c "import secrets; print(secrets.token_urlsafe(48))"` 生成 Token。线上部署时，`BLOG_PUBLIC_URL` 改成博客的 HTTPS 域名，例如 `https://blog.example.com`，然后重建服务：

```powershell
docker compose up -d --build
```

## 2. 安装 Obsidian 插件

1. 在 Vault 下新建 `.obsidian/plugins/direct-blog-publisher` 文件夹。
2. 将本仓库 `obsidian-plugin` 内的 `main.js`、`manifest.json`、`styles.css` 复制进去。
3. Obsidian → 设置 → 第三方插件，关闭安全模式并启用 **Direct Blog Publisher**。
4. 打开插件设置。API 地址在本地填 `http://localhost/api`，线上填 `https://你的域名/api`；Token 填写与 `.env` 相同的值。

## 3. 编写和发布

推荐文章头部使用以下属性；只有正文和标题是必需的，未写 `title` 时自动使用文件名：

```yaml
---
title: 我的第一篇文章
summary: 这是一段首页摘要
category_id: 1
cover_image: https://example.com/cover.jpg
---
```

正文可以使用 Obsidian 图片语法 `![[图片.png]]` 或 Markdown 相对路径 `![说明](assets/图片.png)`；发布时插件会自动上传并替换为博客可访问的 URL。

打开文章后按 `Ctrl/Cmd+P`，执行 **Direct Blog Publisher: 发布/更新当前文章到博客**。第一次发布会将以下属性写回笔记：

```yaml
blog_article_id: 文章数字 ID
blog_url: 可直接打开的预览地址
```

以后对同一笔记再次执行命令会更新原文章。不要删除 `blog_article_id`，否则会创建新文章。发布完成后点击属性里的 `blog_url` 即可预览。

## 常见问题

- `Invalid Obsidian token`：插件 Token 与服务端环境变量不一致，修改后需重启后端。
- `OBSIDIAN_AUTHOR_EMAIL must identify an administrator`：邮箱不存在或账号不是管理员。
- `category_id does not exist`：从博客分类列表确认数字 ID，或删除该属性以发布为未分类。
- 图片找不到：确认图片位于当前 Vault 内，且链接在 Obsidian 中可以正常打开。
