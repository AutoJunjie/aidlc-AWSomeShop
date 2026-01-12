"""
种子数据脚本 - 用于开发环境初始化测试用户
"""
from app.database import SessionLocal, init_db
from app.models import User
from app.auth import hash_password
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_users():
    """创建种子用户数据"""
    db = SessionLocal()
    
    try:
        # 检查是否已有用户
        existing_users = db.query(User).count()
        if existing_users > 0:
            logger.info(f"Database already has {existing_users} users. Skipping seed.")
            return
        
        # 创建管理员用户
        admin = User(
            username="admin",
            password_hash=hash_password("admin123"),
            role="admin",
            points_balance=0
        )
        
        # 创建测试员工
        employee1 = User(
            username="employee1",
            password_hash=hash_password("test123"),
            role="employee",
            points_balance=1000
        )
        
        employee2 = User(
            username="employee2",
            password_hash=hash_password("test123"),
            role="employee",
            points_balance=500
        )
        
        # 添加到数据库
        db.add_all([admin, employee1, employee2])
        db.commit()
        
        logger.info("Seed data created successfully:")
        logger.info("  - Admin user: admin / admin123")
        logger.info("  - Employee1: employee1 / test123 (1000 points)")
        logger.info("  - Employee2: employee2 / test123 (500 points)")
        
    except Exception as e:
        logger.error(f"Error creating seed data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    logger.info("Initializing database...")
    init_db()
    
    logger.info("Creating seed data...")
    seed_users()
    
    logger.info("Done!")
