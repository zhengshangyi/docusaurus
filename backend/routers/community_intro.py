"""
社区介绍相关 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models import CommunityIntro
from schemas import (
    CommunityIntroCreate,
    CommunityIntroUpdate,
    CommunityIntroResponse,
    MessageResponse,
    ListResponse
)

router = APIRouter(prefix="/api/community/intro", tags=["community-intro"])


@router.get("/", response_model=ListResponse)
def get_community_intros(
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """获取社区介绍列表"""
    query = db.query(CommunityIntro)
    
    if is_active is not None:
        query = query.filter(CommunityIntro.is_active == is_active)
    else:
        query = query.filter(CommunityIntro.is_active == True)
    
    intros = query.order_by(CommunityIntro.order.asc(), CommunityIntro.created_at.asc()).all()
    
    return {
        "total": len(intros),
        "items": [CommunityIntroResponse.model_validate(intro).model_dump() for intro in intros]
    }


@router.get("/{intro_id}", response_model=CommunityIntroResponse)
def get_community_intro(intro_id: int, db: Session = Depends(get_db)):
    """获取单个社区介绍"""
    intro = db.query(CommunityIntro).filter(CommunityIntro.id == intro_id).first()
    if not intro:
        raise HTTPException(status_code=404, detail="社区介绍不存在")
    return intro


@router.get("/section/{section_name}", response_model=CommunityIntroResponse)
def get_community_intro_by_section(section_name: str, db: Session = Depends(get_db)):
    """通过区块名称获取社区介绍"""
    intro = db.query(CommunityIntro).filter(CommunityIntro.section_name == section_name).first()
    if not intro:
        raise HTTPException(status_code=404, detail="社区介绍不存在")
    return intro


@router.post("/", response_model=CommunityIntroResponse)
def create_community_intro(intro: CommunityIntroCreate, db: Session = Depends(get_db)):
    """创建社区介绍"""
    # 检查 section_name 是否已存在
    existing = db.query(CommunityIntro).filter(
        CommunityIntro.section_name == intro.section_name
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="该区块名称已存在")
    
    db_intro = CommunityIntro(**intro.dict())
    db.add(db_intro)
    db.commit()
    db.refresh(db_intro)
    return db_intro


@router.put("/{intro_id}", response_model=CommunityIntroResponse)
def update_community_intro(
    intro_id: int,
    intro: CommunityIntroUpdate,
    db: Session = Depends(get_db)
):
    """更新社区介绍"""
    db_intro = db.query(CommunityIntro).filter(CommunityIntro.id == intro_id).first()
    if not db_intro:
        raise HTTPException(status_code=404, detail="社区介绍不存在")
    
    update_data = intro.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_intro, field, value)
    
    db.commit()
    db.refresh(db_intro)
    return db_intro


@router.delete("/{intro_id}", response_model=MessageResponse)
def delete_community_intro(intro_id: int, db: Session = Depends(get_db)):
    """删除社区介绍"""
    db_intro = db.query(CommunityIntro).filter(CommunityIntro.id == intro_id).first()
    if not db_intro:
        raise HTTPException(status_code=404, detail="社区介绍不存在")
    
    db.delete(db_intro)
    db.commit()
    return {"message": "社区介绍已删除"}

