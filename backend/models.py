"""
数据库模型定义
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Date, ForeignKey, BigInteger, JSON
from sqlalchemy.orm import relationship
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


# ============================================
# 多版本文档相关模型
# ============================================

class DocVersion(Base):
    """文档版本表"""
    __tablename__ = "doc_versions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    version_name = Column(String(50), unique=True, nullable=False, index=True, comment="版本名称")
    label = Column(String(100), comment="版本显示标签")
    is_current = Column(Boolean, default=False, comment="是否为当前版本")
    is_latest = Column(Boolean, default=False, comment="是否为最新稳定版本")
    description = Column(Text, comment="版本描述")
    release_date = Column(Date, comment="发布日期")
    status = Column(String(20), default="active", index=True, comment="状态")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关系
    nodes = relationship("DocNode", back_populates="version", cascade="all, delete-orphan")
    assets = relationship("DocAsset", back_populates="version", cascade="all, delete-orphan")


class DocNode(Base):
    """文档节点表（统一存储文档和目录）"""
    __tablename__ = "doc_nodes"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    version_id = Column(Integer, ForeignKey("doc_versions.id", ondelete="CASCADE"), nullable=False, index=True, comment="所属版本ID")
    parent_id = Column(Integer, ForeignKey("doc_nodes.id", ondelete="CASCADE"), index=True, comment="父节点ID")
    node_type = Column(String(20), nullable=False, index=True, comment="节点类型（doc/category）")
    title = Column(String(255), nullable=False, comment="标题/标签")
    slug = Column(String(255), index=True, comment="URL友好标识")
    file_path = Column(String(500), comment="文件路径")
    content = Column(Text, comment="文档内容（Markdown/MDX）")
    frontmatter = Column(JSON, comment="Frontmatter元数据")
    description = Column(Text, comment="描述/摘要")
    author = Column(String(100), comment="作者")
    order = Column(Integer, default=0, index=True, comment="显示顺序")
    sidebar_position = Column(Integer, comment="侧边栏位置")
    is_active = Column(Boolean, default=True, comment="是否启用")
    view_count = Column(Integer, default=0, comment="浏览次数")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关系
    version = relationship("DocVersion", back_populates="nodes")
    parent = relationship("DocNode", remote_side=[id], backref="children")
    category_config = relationship("DocCategoryConfig", back_populates="node", uselist=False, cascade="all, delete-orphan")
    assets = relationship("DocAsset", back_populates="node", cascade="all, delete-orphan")


class DocCategoryConfig(Base):
    """目录配置表"""
    __tablename__ = "doc_category_config"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    node_id = Column(Integer, ForeignKey("doc_nodes.id", ondelete="CASCADE"), unique=True, nullable=False, comment="关联的目录节点ID")
    label = Column(String(255), comment="目录显示标签")
    position = Column(Integer, default=0, comment="目录位置")
    collapsed = Column(Boolean, default=False, comment="是否默认折叠")
    link_type = Column(String(20), comment="链接类型")
    link_id = Column(String(255), comment="链接ID")
    custom_props = Column(JSON, comment="自定义属性")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关系
    node = relationship("DocNode", back_populates="category_config")


class DocAsset(Base):
    """文档资源表"""
    __tablename__ = "doc_assets"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    version_id = Column(Integer, ForeignKey("doc_versions.id", ondelete="CASCADE"), nullable=False, index=True, comment="所属版本ID")
    node_id = Column(Integer, ForeignKey("doc_nodes.id", ondelete="SET NULL"), index=True, comment="关联的文档节点ID")
    asset_type = Column(String(20), nullable=False, comment="资源类型")
    file_name = Column(String(255), nullable=False, comment="文件名")
    file_path = Column(String(500), nullable=False, comment="文件路径")
    file_size = Column(BigInteger, comment="文件大小（字节）")
    mime_type = Column(String(100), comment="MIME类型")
    url = Column(String(500), comment="访问URL")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    
    # 关系
    version = relationship("DocVersion", back_populates="assets")
    node = relationship("DocNode", back_populates="assets")

