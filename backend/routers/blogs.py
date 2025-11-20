"""
博客相关 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Blog
from schemas import BlogCreate, BlogUpdate, BlogResponse, MessageResponse, ListResponse

router = APIRouter(prefix="/api/blogs", tags=["blogs"])


@router.get("/", response_model=ListResponse)
def get_blogs(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    tag: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取博客列表"""
    query = db.query(Blog)
    
    if tag:
        query = query.filter(Blog.tags.contains(tag))
    if status:
        query = query.filter(Blog.status == status)
    else:
        query = query.filter(Blog.status == "published")
    
    total = query.count()
    blogs = query.order_by(Blog.created_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": [BlogResponse.model_validate(blog).model_dump() for blog in blogs]
    }


@router.get("/{blog_id}", response_model=BlogResponse)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    """获取单个博客"""
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="博客不存在")
    
    # 增加浏览次数
    blog.view_count += 1
    db.commit()
    db.refresh(blog)
    
    return blog


@router.get("/slug/{slug}", response_model=BlogResponse)
def get_blog_by_slug(slug: str, db: Session = Depends(get_db)):
    """通过 slug 获取博客"""
    blog = db.query(Blog).filter(Blog.slug == slug).first()
    if not blog:
        raise HTTPException(status_code=404, detail="博客不存在")
    
    # 增加浏览次数
    blog.view_count += 1
    db.commit()
    db.refresh(blog)
    
    return blog


@router.post("/", response_model=BlogResponse)
def create_blog(blog: BlogCreate, db: Session = Depends(get_db)):
    """创建博客"""
    db_blog = Blog(**blog.dict())
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog


@router.put("/{blog_id}", response_model=BlogResponse)
def update_blog(
    blog_id: int,
    blog: BlogUpdate,
    db: Session = Depends(get_db)
):
    """更新博客"""
    db_blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not db_blog:
        raise HTTPException(status_code=404, detail="博客不存在")
    
    update_data = blog.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_blog, field, value)
    
    db.commit()
    db.refresh(db_blog)
    return db_blog


@router.delete("/{blog_id}", response_model=MessageResponse)
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    """删除博客"""
    db_blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not db_blog:
        raise HTTPException(status_code=404, detail="博客不存在")
    
    db.delete(db_blog)
    db.commit()
    return {"message": "博客已删除"}

