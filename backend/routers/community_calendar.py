"""
社区日历相关 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from database import get_db
from models import CommunityCalendar
from schemas import (
    CommunityCalendarCreate,
    CommunityCalendarUpdate,
    CommunityCalendarResponse,
    MessageResponse,
    ListResponse
)

router = APIRouter(prefix="/api/community/calendar", tags=["community-calendar"])


@router.get("/", response_model=ListResponse)
def get_calendar_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    event_type: Optional[str] = None,
    status: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """获取社区日历事件列表"""
    query = db.query(CommunityCalendar)
    
    if event_type:
        query = query.filter(CommunityCalendar.event_type == event_type)
    if status:
        query = query.filter(CommunityCalendar.status == status)
    if start_date:
        query = query.filter(CommunityCalendar.event_date >= start_date)
    if end_date:
        query = query.filter(CommunityCalendar.event_date <= end_date)
    
    total = query.count()
    events = query.order_by(CommunityCalendar.event_date.asc()).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": [CommunityCalendarResponse.model_validate(event).model_dump() for event in events]
    }


@router.get("/{event_id}", response_model=CommunityCalendarResponse)
def get_calendar_event(event_id: int, db: Session = Depends(get_db)):
    """获取单个日历事件"""
    event = db.query(CommunityCalendar).filter(CommunityCalendar.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="事件不存在")
    return event


@router.post("/", response_model=CommunityCalendarResponse)
def create_calendar_event(event: CommunityCalendarCreate, db: Session = Depends(get_db)):
    """创建日历事件"""
    db_event = CommunityCalendar(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


@router.put("/{event_id}", response_model=CommunityCalendarResponse)
def update_calendar_event(
    event_id: int,
    event: CommunityCalendarUpdate,
    db: Session = Depends(get_db)
):
    """更新日历事件"""
    db_event = db.query(CommunityCalendar).filter(CommunityCalendar.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="事件不存在")
    
    update_data = event.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_event, field, value)
    
    db.commit()
    db.refresh(db_event)
    return db_event


@router.delete("/{event_id}", response_model=MessageResponse)
def delete_calendar_event(event_id: int, db: Session = Depends(get_db)):
    """删除日历事件"""
    db_event = db.query(CommunityCalendar).filter(CommunityCalendar.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="事件不存在")
    
    db.delete(db_event)
    db.commit()
    return {"message": "事件已删除"}

