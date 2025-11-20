"""
FastAPI 主应用文件
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from database import init_db
from routers import (
    documents,
    blogs,
    news,
    community_calendar,
    community_intro,
    discussions,
    auth,
    admin,
    users,
    docs_versions
)

# 创建 FastAPI 应用实例
app = FastAPI(
    title="九问网站后端 API",
    description="九问官方网站后端服务，提供文档、博客、新闻、社区日历等数据接口",
    version="1.0.0"
)

# 添加缓存控制中间件，禁用 API 响应缓存
@app.middleware("http")
async def add_cache_control_header(request: Request, call_next):
    """为所有 API 响应添加禁用缓存的头"""
    response = await call_next(request)
    # 只对 API 路径添加缓存控制头
    if request.url.path.startswith("/api/") or request.url.path.startswith("/health"):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response

# 配置 CORS
# 开发环境允许所有来源，生产环境限制为特定域名
if settings.DEBUG:
    # 开发环境：允许所有来源
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=r".*",  # 允许所有来源
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
else:
    # 生产环境：只允许配置的来源
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

# 注册路由
app.include_router(documents.router)
app.include_router(blogs.router)
app.include_router(news.router)
app.include_router(community_calendar.router)
app.include_router(community_intro.router)
app.include_router(discussions.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(docs_versions.router)


@app.get("/")
async def root():
    """根路径，返回 API 信息"""
    return {
        "message": "九问网站后端 API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "documents": "/api/documents",
            "blogs": "/api/blogs",
            "news": "/api/news",
            "community_calendar": "/api/community/calendar",
            "community_intro": "/api/community/intro",
            "discussions": "/api/discussions"
        }
    }


@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy"}


@app.on_event("startup")
async def startup_event():
    """应用启动时初始化数据库"""
    init_db()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.DEBUG
    )

