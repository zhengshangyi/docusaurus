# 九问网站后端服务

这是一个基于 FastAPI 和 MySQL 的后端服务，为九问官方网站提供数据接口。

## 功能特性

- 📄 **文档管理** - 存储和管理网站文档内容
- 📝 **博客管理** - 博客文章的增删改查
- 📰 **新闻资讯** - 新闻和公告管理
- 📅 **社区日历** - 社区活动和事件管理
- 👥 **社区介绍** - 社区介绍内容管理

## 技术栈

- **FastAPI** - 现代、快速的 Web 框架
- **SQLAlchemy** - Python ORM
- **MySQL** - 关系型数据库
- **Pydantic** - 数据验证和序列化
- **Uvicorn** - ASGI 服务器

## 项目结构

```
backend/
├── main.py                 # FastAPI 主应用
├── config.py               # 配置文件
├── database.py             # 数据库连接和会话管理
├── models.py               # 数据库模型定义
├── schemas.py              # Pydantic 数据模式
├── requirements.txt        # Python 依赖
├── .env.example           # 环境变量示例
├── README.md              # 项目说明
└── routers/               # API 路由
    ├── __init__.py
    ├── documents.py       # 文档相关路由
    ├── blogs.py           # 博客相关路由
    ├── news.py            # 新闻相关路由
    ├── community_calendar.py  # 社区日历路由
    └── community_intro.py      # 社区介绍路由
```

## 安装和配置

### 1. 安装 Python 依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `env.example` 为 `.env` 并修改配置：

```bash
cp env.example .env
```

编辑 `.env` 文件，设置数据库连接信息：

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=jiuwen_website
```

### 3. 创建 MySQL 数据库

```sql
CREATE DATABASE jiuwen_website CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 运行服务

```bash
# 开发模式（自动重载）
python main.py

# 或使用 uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 5. 访问 API 文档

启动服务后，访问以下地址查看 API 文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 接口说明

### 文档接口

- `GET /api/documents` - 获取文档列表
- `GET /api/documents/{id}` - 获取单个文档
- `GET /api/documents/slug/{slug}` - 通过 slug 获取文档
- `POST /api/documents` - 创建文档
- `PUT /api/documents/{id}` - 更新文档
- `DELETE /api/documents/{id}` - 删除文档

### 博客接口

- `GET /api/blogs` - 获取博客列表
- `GET /api/blogs/{id}` - 获取单个博客
- `GET /api/blogs/slug/{slug}` - 通过 slug 获取博客
- `POST /api/blogs` - 创建博客
- `PUT /api/blogs/{id}` - 更新博客
- `DELETE /api/blogs/{id}` - 删除博客

### 新闻接口

- `GET /api/news` - 获取新闻列表
- `GET /api/news/{id}` - 获取单条新闻
- `GET /api/news/slug/{slug}` - 通过 slug 获取新闻
- `POST /api/news` - 创建新闻
- `PUT /api/news/{id}` - 更新新闻
- `DELETE /api/news/{id}` - 删除新闻

### 社区日历接口

- `GET /api/community/calendar` - 获取日历事件列表
- `GET /api/community/calendar/{id}` - 获取单个事件
- `POST /api/community/calendar` - 创建事件
- `PUT /api/community/calendar/{id}` - 更新事件
- `DELETE /api/community/calendar/{id}` - 删除事件

### 社区介绍接口

- `GET /api/community/intro` - 获取社区介绍列表
- `GET /api/community/intro/{id}` - 获取单个介绍
- `GET /api/community/intro/section/{section_name}` - 通过区块名称获取
- `POST /api/community/intro` - 创建介绍
- `PUT /api/community/intro/{id}` - 更新介绍
- `DELETE /api/community/intro/{id}` - 删除介绍

## 数据库表结构

### documents (文档表)
- id, title, content, category, author, slug, status, view_count, created_at, updated_at

### blogs (博客表)
- id, title, content, excerpt, author, tags, cover_image, slug, status, view_count, created_at, updated_at

### news (新闻表)
- id, title, content, excerpt, author, category, cover_image, source, slug, status, is_featured, view_count, created_at, updated_at

### community_calendar (社区日历表)
- id, title, description, event_date, event_location, event_type, organizer, registration_url, status, created_at, updated_at

### community_intro (社区介绍表)
- id, section_name, title, content, image_url, order, is_active, created_at, updated_at

## 开发说明

### 添加新的数据模型

1. 在 `models.py` 中定义新的 SQLAlchemy 模型
2. 在 `schemas.py` 中定义对应的 Pydantic 模式
3. 在 `routers/` 目录下创建新的路由文件
4. 在 `main.py` 中注册新路由

### 数据库迁移

当前使用 SQLAlchemy 的 `create_all()` 方法自动创建表。生产环境建议使用 Alembic 进行数据库迁移管理。

## 部署

### 使用 Gunicorn + Uvicorn Workers

```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 使用 Docker

可以创建 Dockerfile 和 docker-compose.yml 来容器化部署。

## 许可证

MIT License

