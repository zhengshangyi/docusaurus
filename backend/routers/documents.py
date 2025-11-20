"""
文档相关 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Document
from schemas import DocumentCreate, DocumentUpdate, DocumentResponse, MessageResponse, ListResponse

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.get("/", response_model=ListResponse)
def get_documents(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取文档列表"""
    query = db.query(Document)
    
    if category:
        query = query.filter(Document.category == category)
    if status:
        query = query.filter(Document.status == status)
    else:
        query = query.filter(Document.status == "published")
    
    total = query.count()
    documents = query.order_by(Document.created_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": [DocumentResponse.model_validate(doc).model_dump() for doc in documents]
    }


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: int, db: Session = Depends(get_db)):
    """获取单个文档"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="文档不存在")
    
    # 增加浏览次数
    document.view_count += 1
    db.commit()
    db.refresh(document)
    
    return document


@router.get("/slug/{slug}", response_model=DocumentResponse)
def get_document_by_slug(slug: str, db: Session = Depends(get_db)):
    """通过 slug 获取文档"""
    document = db.query(Document).filter(Document.slug == slug).first()
    if not document:
        raise HTTPException(status_code=404, detail="文档不存在")
    
    # 增加浏览次数
    document.view_count += 1
    db.commit()
    db.refresh(document)
    
    return document


@router.post("/", response_model=DocumentResponse)
def create_document(document: DocumentCreate, db: Session = Depends(get_db)):
    """创建文档"""
    db_document = Document(**document.dict())
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


@router.put("/{document_id}", response_model=DocumentResponse)
def update_document(
    document_id: int,
    document: DocumentUpdate,
    db: Session = Depends(get_db)
):
    """更新文档"""
    db_document = db.query(Document).filter(Document.id == document_id).first()
    if not db_document:
        raise HTTPException(status_code=404, detail="文档不存在")
    
    update_data = document.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_document, field, value)
    
    db.commit()
    db.refresh(db_document)
    return db_document


@router.delete("/{document_id}", response_model=MessageResponse)
def delete_document(document_id: int, db: Session = Depends(get_db)):
    """删除文档"""
    db_document = db.query(Document).filter(Document.id == document_id).first()
    if not db_document:
        raise HTTPException(status_code=404, detail="文档不存在")
    
    db.delete(db_document)
    db.commit()
    return {"message": "文档已删除"}

