"""
讨论相关 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models import Discussion, DiscussionReply
from schemas import (
    DiscussionCreate,
    DiscussionUpdate,
    DiscussionResponse,
    DiscussionReplyCreate,
    DiscussionReplyResponse,
    MessageResponse,
    ListResponse
)

router = APIRouter(prefix="/api/discussions", tags=["discussions"])


@router.get("/", response_model=ListResponse)
def get_discussions(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取讨论列表"""
    query = db.query(Discussion)
    
    if category:
        query = query.filter(Discussion.category == category)
    if status:
        query = query.filter(Discussion.status == status)
    
    total = query.count()
    discussions = query.order_by(Discussion.created_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": [DiscussionResponse.model_validate(disc).model_dump() for disc in discussions]
    }


@router.get("/{discussion_id}", response_model=DiscussionResponse)
def get_discussion(discussion_id: int, db: Session = Depends(get_db)):
    """获取单个讨论"""
    discussion = db.query(Discussion).filter(Discussion.id == discussion_id).first()
    if not discussion:
        raise HTTPException(status_code=404, detail="讨论不存在")
    
    # 增加浏览次数
    discussion.view_count += 1
    db.commit()
    db.refresh(discussion)
    
    return discussion


@router.post("/", response_model=DiscussionResponse)
def create_discussion(discussion: DiscussionCreate, db: Session = Depends(get_db)):
    """创建讨论"""
    db_discussion = Discussion(**discussion.dict())
    db.add(db_discussion)
    db.commit()
    db.refresh(db_discussion)
    return db_discussion


@router.put("/{discussion_id}", response_model=DiscussionResponse)
def update_discussion(
    discussion_id: int,
    discussion: DiscussionUpdate,
    db: Session = Depends(get_db)
):
    """更新讨论"""
    db_discussion = db.query(Discussion).filter(Discussion.id == discussion_id).first()
    if not db_discussion:
        raise HTTPException(status_code=404, detail="讨论不存在")
    
    update_data = discussion.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_discussion, field, value)
    
    db.commit()
    db.refresh(db_discussion)
    return db_discussion


@router.delete("/{discussion_id}", response_model=MessageResponse)
def delete_discussion(discussion_id: int, db: Session = Depends(get_db)):
    """删除讨论"""
    db_discussion = db.query(Discussion).filter(Discussion.id == discussion_id).first()
    if not db_discussion:
        raise HTTPException(status_code=404, detail="讨论不存在")
    
    # 删除相关的回复
    db.query(DiscussionReply).filter(DiscussionReply.discussion_id == discussion_id).delete()
    
    db.delete(db_discussion)
    db.commit()
    return {"message": "讨论已删除"}


# 回复相关接口
@router.get("/{discussion_id}/replies", response_model=ListResponse)
def get_discussion_replies(
    discussion_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取讨论的回复列表"""
    # 检查讨论是否存在
    discussion = db.query(Discussion).filter(Discussion.id == discussion_id).first()
    if not discussion:
        raise HTTPException(status_code=404, detail="讨论不存在")
    
    query = db.query(DiscussionReply).filter(DiscussionReply.discussion_id == discussion_id)
    total = query.count()
    replies = query.order_by(DiscussionReply.created_at.asc()).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": [DiscussionReplyResponse.model_validate(reply).model_dump() for reply in replies]
    }


@router.post("/{discussion_id}/replies", response_model=DiscussionReplyResponse)
def create_discussion_reply(
    discussion_id: int,
    reply: DiscussionReplyCreate,
    db: Session = Depends(get_db)
):
    """创建讨论回复"""
    # 检查讨论是否存在
    discussion = db.query(Discussion).filter(Discussion.id == discussion_id).first()
    if not discussion:
        raise HTTPException(status_code=404, detail="讨论不存在")
    
    # 创建回复
    db_reply = DiscussionReply(
        discussion_id=discussion_id,
        content=reply.content,
        author=reply.author
    )
    db.add(db_reply)
    
    # 更新讨论的回复数量
    discussion.reply_count += 1
    db.commit()
    db.refresh(db_reply)
    
    return db_reply


@router.delete("/replies/{reply_id}", response_model=MessageResponse)
def delete_discussion_reply(reply_id: int, db: Session = Depends(get_db)):
    """删除讨论回复"""
    db_reply = db.query(DiscussionReply).filter(DiscussionReply.id == reply_id).first()
    if not db_reply:
        raise HTTPException(status_code=404, detail="回复不存在")
    
    # 更新讨论的回复数量
    discussion = db.query(Discussion).filter(Discussion.id == db_reply.discussion_id).first()
    if discussion and discussion.reply_count > 0:
        discussion.reply_count -= 1
    
    db.delete(db_reply)
    db.commit()
    return {"message": "回复已删除"}



