from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    哈希密码
    
    Args:
        password: 明文密码
        
    Returns:
        str: 哈希后的密码
    """
    return pwd_context.hash(password, rounds=settings.bcrypt_salt_rounds)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    
    Args:
        plain_password: 明文密码
        hashed_password: 哈希密码
        
    Returns:
        bool: 密码是否匹配
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"Password verification error: {e}")
        return False


def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建 JWT token
    
    Args:
        data: token payload 数据
        expires_delta: 过期时间间隔
        
    Returns:
        str: JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=settings.jwt_expiration_hours)
    
    to_encode.update({"exp": expire})
    
    try:
        encoded_jwt = jwt.encode(
            to_encode,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm
        )
        return encoded_jwt
    except Exception as e:
        logger.error(f"Token creation error: {e}")
        raise


def decode_access_token(token: str) -> Optional[Dict]:
    """
    解码并验证 JWT token
    
    Args:
        token: JWT token
        
    Returns:
        Optional[Dict]: token payload，如果无效则返回 None
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm]
        )
        return payload
    except JWTError as e:
        logger.warning(f"Token decode error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected token decode error: {e}")
        return None


def extract_token_from_header(authorization: Optional[str]) -> Optional[str]:
    """
    从 Authorization header 提取 token
    
    Args:
        authorization: Authorization header 值
        
    Returns:
        Optional[str]: 提取的 token，如果格式不正确则返回 None
    """
    if not authorization:
        return None
    
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    
    return parts[1]


def validate_password_strength(password: str) -> bool:
    """
    验证密码强度
    
    Args:
        password: 密码
        
    Returns:
        bool: 密码是否符合强度要求
    """
    return len(password) >= settings.password_min_length
