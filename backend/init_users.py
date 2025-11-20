"""
初始化默认用户账号
"""
from database import SessionLocal
from models import User
from auth_utils import get_password_hash, get_user_by_username

def init_default_users():
    """创建默认用户账号"""
    db = SessionLocal()
    try:
        # 开发者账号
        users_to_create = [
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

        created_count = 0
        skipped_count = 0

        for user_data in users_to_create:
            # 检查用户是否已存在
            existing_user = get_user_by_username(db, user_data["username"])
            if existing_user:
                print(f"用户 {user_data['username']} 已存在，跳过创建")
                skipped_count += 1
                continue

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
            created_count += 1
            print(f"✓ 创建用户: {user_data['username']} (角色: {user_data['role']})")

        db.commit()
        print(f"\n完成！创建了 {created_count} 个用户，跳过了 {skipped_count} 个已存在的用户")
        
    except Exception as e:
        db.rollback()
        print(f"错误: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("开始初始化默认用户账号...")
    print("=" * 50)
    init_default_users()
    print("=" * 50)


