"""
数据库模型定义
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from database import Base


class Document(Base):
    """文档表"""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False, comment="文档标题")
    content = Column(Text, nullable=False, comment="文档内容")
    category = Column(String(100), comment="文档分类")
    author = Column(String(100), comment="作者")
    slug = Column(String(255), unique=True, index=True, comment="URL 友好标识")
    status = Column(String(20), default="published", comment="状态：draft/published")
    view_count = Column(Integer, default=0, comment="浏览次数")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")


class Blog(Base):
    """博客表"""
    __tablename__ = "blogs"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False, comment="博客标题")
    content = Column(Text, nullable=False, comment="博客内容")
    excerpt = Column(Text, comment="摘要")
    author = Column(String(100), comment="作者")
    tags = Column(String(500), comment="标签，逗号分隔")
    cover_image = Column(String(500), comment="封面图片 URL")
    slug = Column(String(255), unique=True, index=True, comment="URL 友好标识")
    status = Column(String(20), default="published", comment="状态：draft/published")
    view_count = Column(Integer, default=0, comment="浏览次数")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")


class News(Base):
    """新闻资讯表"""
    __tablename__ = "news"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False, comment="新闻标题")
    content = Column(Text, nullable=False, comment="新闻内容")
    excerpt = Column(Text, comment="摘要")
    author = Column(String(100), comment="作者")
    category = Column(String(100), comment="新闻分类")
    cover_image = Column(String(500), comment="封面图片 URL")
    source = Column(String(200), comment="来源")
    slug = Column(String(255), unique=True, index=True, comment="URL 友好标识")
    status = Column(String(20), default="published", comment="状态：draft/published")
    is_featured = Column(Boolean, default=False, comment="是否置顶")
    view_count = Column(Integer, default=0, comment="浏览次数")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")


class CommunityCalendar(Base):
    """社区日历表"""
    __tablename__ = "community_calendar"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False, comment="活动标题")
    description = Column(Text, comment="活动描述")
    event_date = Column(DateTime, nullable=False, comment="活动日期")
    event_location = Column(String(255), comment="活动地点")
    event_type = Column(String(50), comment="活动类型：meetup/webinar/conference/workshop")
    organizer = Column(String(100), comment="组织者")
    registration_url = Column(String(500), comment="报名链接")
    status = Column(String(20), default="upcoming", comment="状态：upcoming/ongoing/completed/cancelled")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")


class CommunityIntro(Base):
    """社区介绍表"""
    __tablename__ = "community_intro"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    section_name = Column(String(100), unique=True, nullable=False, comment="区块名称")
    title = Column(String(255), comment="标题")
    content = Column(Text, nullable=False, comment="内容")
    image_url = Column(String(500), comment="图片 URL")
    order = Column(Integer, default=0, comment="显示顺序")
    is_active = Column(Boolean, default=True, comment="是否启用")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")


class Discussion(Base):
    """讨论/问题表"""
    __tablename__ = "discussions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False, comment="问题标题")
    content = Column(Text, nullable=False, comment="问题内容")
    category = Column(String(50), nullable=False, comment="分类：usage/bug/feature/other")
    author = Column(String(100), comment="提问者")
    status = Column(String(20), default="open", comment="状态：open/solved")
    view_count = Column(Integer, default=0, comment="浏览次数")
    reply_count = Column(Integer, default=0, comment="回复数量")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")


class DiscussionReply(Base):
    """讨论回复表"""
    __tablename__ = "discussion_replies"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    discussion_id = Column(Integer, nullable=False, index=True, comment="讨论ID")
    content = Column(Text, nullable=False, comment="回复内容")
    author = Column(String(100), comment="回复者")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")


class User(Base):
    """用户表"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False, index=True, comment="用户名")
    email = Column(String(255), unique=True, nullable=False, index=True, comment="邮箱")
    hashed_password = Column(String(255), nullable=False, comment="加密后的密码")
    role = Column(String(20), default="developer", nullable=False, comment="角色：developer/admin/root")
    is_active = Column(Boolean, default=True, comment="是否激活")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")


class SiteConfig(Base):
    """网站配置表"""
    __tablename__ = "site_config"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    key = Column(String(100), unique=True, nullable=False, index=True, comment="配置键")
    value = Column(Text, comment="配置值")
    description = Column(String(500), comment="配置描述")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

