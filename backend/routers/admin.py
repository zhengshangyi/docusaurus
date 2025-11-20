"""
管理台路由（管理员和 root 用户可访问）
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import SiteConfig, News
from schemas import (
    SiteConfigCreate, SiteConfigUpdate, SiteConfigResponse,
    NewsCreate, NewsUpdate, NewsResponse
)
from dependencies import require_admin

router = APIRouter(prefix="/api/admin", tags=["管理台"])


# 网站配置管理
@router.get("/config", response_model=List[SiteConfigResponse])
async def get_all_configs(
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    """获取所有网站配置"""
    configs = db.query(SiteConfig).all()
    return configs


@router.get("/config/{key}", response_model=SiteConfigResponse)
async def get_config(
    key: str,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    """获取指定配置"""
    config = db.query(SiteConfig).filter(SiteConfig.key == key).first()
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="配置不存在"
        )
    return config


@router.post("/config", response_model=SiteConfigResponse)
async def create_config(
    config_data: SiteConfigCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    """创建网站配置"""
    # 检查是否已存在
    existing = db.query(SiteConfig).filter(SiteConfig.key == config_data.key).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="配置键已存在"
        )
    
    config = SiteConfig(**config_data.dict())
    db.add(config)
    db.commit()
    db.refresh(config)
    return config


@router.put("/config/{key}", response_model=SiteConfigResponse)
async def update_config(
    key: str,
    config_data: SiteConfigUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    """更新网站配置"""
    config = db.query(SiteConfig).filter(SiteConfig.key == key).first()
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="配置不存在"
        )
    
    update_data = config_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(config, field, value)
    
    db.commit()
    db.refresh(config)
    return config


@router.delete("/config/{key}")
async def delete_config(
    key: str,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    """删除网站配置"""
    config = db.query(SiteConfig).filter(SiteConfig.key == key).first()
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="配置不存在"
        )
    
    db.delete(config)
    db.commit()
    return {"message": "配置已删除"}


# 新闻资讯管理（管理员可以创建、更新、删除）
@router.post("/news", response_model=NewsResponse)
async def create_news(
    news_data: NewsCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    """创建新闻资讯"""
    news = News(**news_data.dict())
    db.add(news)
    db.commit()
    db.refresh(news)
    return news


@router.put("/news/{news_id}", response_model=NewsResponse)
async def update_news(
    news_id: int,
    news_data: NewsUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    """更新新闻资讯"""
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="新闻不存在"
        )
    
    update_data = news_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(news, field, value)
    
    db.commit()
    db.refresh(news)
    return news


@router.delete("/news/{news_id}")
async def delete_news(
    news_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    """删除新闻资讯"""
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="新闻不存在"
        )
    
    db.delete(news)
    db.commit()
    return {"message": "新闻已删除"}


