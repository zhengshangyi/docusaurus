"""
新闻资讯相关 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models import News
from schemas import NewsCreate, NewsUpdate, NewsResponse, MessageResponse, ListResponse

router = APIRouter(prefix="/api/news", tags=["news"])


@router.get("/", response_model=ListResponse)
def get_news(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category: Optional[str] = None,
    is_featured: Optional[bool] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取新闻列表"""
    query = db.query(News)
    
    if category:
        query = query.filter(News.category == category)
    if is_featured is not None:
        query = query.filter(News.is_featured == is_featured)
    if status:
        query = query.filter(News.status == status)
    else:
        query = query.filter(News.status == "published")
    
    total = query.count()
    news_list = query.order_by(News.is_featured.desc(), News.created_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": [NewsResponse.model_validate(news).model_dump() for news in news_list]
    }


@router.get("/{news_id}", response_model=NewsResponse)
def get_news_item(news_id: int, db: Session = Depends(get_db)):
    """获取单条新闻"""
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="新闻不存在")
    
    # 增加浏览次数
    news.view_count += 1
    db.commit()
    db.refresh(news)
    
    return news


@router.get("/slug/{slug}", response_model=NewsResponse)
def get_news_by_slug(slug: str, db: Session = Depends(get_db)):
    """通过 slug 获取新闻"""
    news = db.query(News).filter(News.slug == slug).first()
    if not news:
        raise HTTPException(status_code=404, detail="新闻不存在")
    
    # 增加浏览次数
    news.view_count += 1
    db.commit()
    db.refresh(news)
    
    return news


@router.post("/", response_model=NewsResponse)
def create_news(news: NewsCreate, db: Session = Depends(get_db)):
    """创建新闻"""
    db_news = News(**news.dict())
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news


@router.put("/{news_id}", response_model=NewsResponse)
def update_news(
    news_id: int,
    news: NewsUpdate,
    db: Session = Depends(get_db)
):
    """更新新闻"""
    db_news = db.query(News).filter(News.id == news_id).first()
    if not db_news:
        raise HTTPException(status_code=404, detail="新闻不存在")
    
    update_data = news.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_news, field, value)
    
    db.commit()
    db.refresh(db_news)
    return db_news


@router.delete("/{news_id}", response_model=MessageResponse)
def delete_news(news_id: int, db: Session = Depends(get_db)):
    """删除新闻"""
    db_news = db.query(News).filter(News.id == news_id).first()
    if not db_news:
        raise HTTPException(status_code=404, detail="新闻不存在")
    
    db.delete(db_news)
    db.commit()
    return {"message": "新闻已删除"}

