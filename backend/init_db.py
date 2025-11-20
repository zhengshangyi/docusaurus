"""
数据库初始化脚本
用于创建数据库和表结构
"""
import sys
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text
from config import settings
from database import init_db, engine

def create_database():
    """创建数据库（如果不存在）"""
    # 连接到 MySQL 服务器（不指定数据库）
    # 对密码进行 URL 编码，处理特殊字符
    encoded_password = quote_plus(settings.DB_PASSWORD)
    db_url = f"mysql+pymysql://{settings.DB_USER}:{encoded_password}@{settings.DB_HOST}:{settings.DB_PORT}/"
    temp_engine = create_engine(db_url)
    
    with temp_engine.connect() as conn:
        # 检查数据库是否存在
        result = conn.execute(text(f"SHOW DATABASES LIKE '{settings.DB_NAME}'"))
        if result.fetchone():
            print(f"数据库 '{settings.DB_NAME}' 已存在")
        else:
            # 创建数据库
            conn.execute(text(f"CREATE DATABASE {settings.DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            conn.commit()
            print(f"数据库 '{settings.DB_NAME}' 创建成功")

def init_tables():
    """初始化数据库表"""
    try:
        init_db()
        print("数据库表创建成功")
    except Exception as e:
        print(f"创建数据库表时出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("开始初始化数据库...")
    print(f"数据库配置: {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
    
    try:
        # 创建数据库
        create_database()
        
        # 创建表
        init_tables()
        
        print("\n数据库初始化完成！")
        print("你现在可以启动后端服务了：")
        print("  python main.py")
        print("  或")
        print("  ./run.sh")
        
    except Exception as e:
        print(f"初始化失败: {e}")
        sys.exit(1)

