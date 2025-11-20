"""
Pydantic 数据模式定义（用于 API 请求和响应）
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# 文档相关 Schema
class DocumentBase(BaseModel):
    title: str
    content: str
    category: Optional[str] = None
    author: Optional[str] = None
    slug: Optional[str] = None
    status: str = "published"


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    author: Optional[str] = None
    status: Optional[str] = None


class DocumentResponse(DocumentBase):
    id: int
    view_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# 博客相关 Schema
class BlogBase(BaseModel):
    title: str
    content: str
    excerpt: Optional[str] = None
    author: Optional[str] = None
    tags: Optional[str] = None
    cover_image: Optional[str] = None
    slug: Optional[str] = None
    status: str = "published"


class BlogCreate(BlogBase):
    pass


class BlogUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    excerpt: Optional[str] = None
    author: Optional[str] = None
    tags: Optional[str] = None
    cover_image: Optional[str] = None
    status: Optional[str] = None


class BlogResponse(BlogBase):
    id: int
    view_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# 新闻相关 Schema
class NewsBase(BaseModel):
    title: str
    content: str
    excerpt: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    cover_image: Optional[str] = None
    source: Optional[str] = None
    slug: Optional[str] = None
    status: str = "published"
    is_featured: bool = False


class NewsCreate(NewsBase):
    pass


class NewsUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    excerpt: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    cover_image: Optional[str] = None
    source: Optional[str] = None
    status: Optional[str] = None
    is_featured: Optional[bool] = None


class NewsResponse(NewsBase):
    id: int
    view_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# 社区日历相关 Schema
class CommunityCalendarBase(BaseModel):
    title: str
    description: Optional[str] = None
    event_date: datetime
    event_location: Optional[str] = None
    event_type: Optional[str] = None
    organizer: Optional[str] = None
    registration_url: Optional[str] = None
    status: str = "upcoming"


class CommunityCalendarCreate(CommunityCalendarBase):
    pass


class CommunityCalendarUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    event_date: Optional[datetime] = None
    event_location: Optional[str] = None
    event_type: Optional[str] = None
    organizer: Optional[str] = None
    registration_url: Optional[str] = None
    status: Optional[str] = None


class CommunityCalendarResponse(CommunityCalendarBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# 社区介绍相关 Schema
class CommunityIntroBase(BaseModel):
    section_name: str
    title: Optional[str] = None
    content: str
    image_url: Optional[str] = None
    order: int = 0
    is_active: bool = True


class CommunityIntroCreate(CommunityIntroBase):
    pass


class CommunityIntroUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None
    order: Optional[int] = None
    is_active: Optional[bool] = None


class CommunityIntroResponse(CommunityIntroBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# 讨论相关 Schema
class DiscussionBase(BaseModel):
    title: str
    content: str
    category: str  # usage/bug/feature/other
    author: Optional[str] = None
    status: str = "open"  # open/solved


class DiscussionCreate(DiscussionBase):
    pass


class DiscussionUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None


class DiscussionResponse(DiscussionBase):
    id: int
    view_count: int
    reply_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# 讨论回复相关 Schema
class DiscussionReplyBase(BaseModel):
    discussion_id: int
    content: str
    author: Optional[str] = None


class DiscussionReplyCreate(DiscussionReplyBase):
    pass


class DiscussionReplyResponse(DiscussionReplyBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# 通用响应 Schema
class MessageResponse(BaseModel):
    message: str


class ListResponse(BaseModel):
    total: int
    items: List[dict]


# 用户相关 Schema
class UserBase(BaseModel):
    username: str
    email: str
    role: str = "developer"


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# 认证相关 Schema
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


# 网站配置相关 Schema
class SiteConfigBase(BaseModel):
    key: str
    value: Optional[str] = None
    description: Optional[str] = None


class SiteConfigCreate(SiteConfigBase):
    pass


class SiteConfigUpdate(BaseModel):
    value: Optional[str] = None
    description: Optional[str] = None


class SiteConfigResponse(SiteConfigBase):
    id: int
    updated_at: datetime
    
    class Config:
        from_attributes = True

