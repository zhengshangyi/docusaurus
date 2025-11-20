"""
数据库连接和会话管理
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# 创建数据库引擎
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,  # 连接前检查连接是否有效
    pool_recycle=3600,   # 连接回收时间（秒）
    echo=settings.DEBUG  # 是否打印 SQL 语句
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础模型类
Base = declarative_base()


def get_db():
    """
    获取数据库会话的依赖注入函数
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    初始化数据库，创建所有表
    """
    from models import (
        Document, Blog, News, CommunityCalendar, CommunityIntro,
        Discussion, DiscussionReply, User, SiteConfig
    )
    Base.metadata.create_all(bind=engine)
    
    # 创建默认用户
    _create_default_users()


def _create_default_users():
    """
    创建默认用户账号
    """
    from models import User
    from auth_utils import get_password_hash, get_user_by_username
    
    db = SessionLocal()
    try:
        # 默认用户列表
        default_users = [
            {
                "username": "developer001",
                "email": "developer001@jiuwen.com",
                "password": "123456",
                "role": "developer"
            },
            {
                "username": "developer002",
                "email": "developer002@jiuwen.com",
                "password": "123456",
                "role": "developer"
            },
            {
                "username": "管理员001",
                "email": "admin001@jiuwen.com",
                "password": "Poisson@123",
                "role": "admin"
            },
            {
                "username": "jiuwen_root",
                "email": "root@jiuwen.com",
                "password": "Poisson@123",
                "role": "root"
            },
        ]
        
        for user_data in default_users:
            # 检查用户是否已存在
            existing_user = get_user_by_username(db, user_data["username"])
            if not existing_user:
                # 创建新用户
                hashed_password = get_password_hash(user_data["password"])
                user = User(
                    username=user_data["username"],
                    email=user_data["email"],
                    hashed_password=hashed_password,
                    role=user_data["role"],
                    is_active=True
                )
                db.add(user)
                print(f"✓ 创建默认用户: {user_data['username']} ({user_data['role']})")
            else:
                print(f"⚠ 用户已存在，跳过: {user_data['username']}")
        
        db.commit()
    except Exception as e:
        print(f"❌ 创建默认用户时出错: {e}")
        db.rollback()
    finally:
        db.close()

