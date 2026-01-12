# Auth Service - NFR Design

## Performance Implementation

### Database Connection Pool
```python
# SQLAlchemy 配置
SQLALCHEMY_POOL_SIZE = 10
SQLALCHEMY_MAX_OVERFLOW = 20
SQLALCHEMY_POOL_TIMEOUT = 30
```

### Password Hashing
- bcrypt 是 CPU 密集型，使用异步执行避免阻塞
- 考虑使用 passlib 的 CryptContext

## Security Implementation

### JWT Configuration
```python
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24
# JWT_SECRET 从环境变量读取
```

### Password Policy
- 最小长度：8 字符
- bcrypt salt rounds：12

### Error Messages
```python
# 统一返回，不暴露用户存在性
INVALID_CREDENTIALS = "Invalid username or password"
```

## Reliability Implementation

### Health Check Endpoint
```
GET /health
Response: {"status": "healthy", "database": "connected"}
```

### Database Retry
- 连接失败自动重试 3 次
- 指数退避：1s, 2s, 4s

## Observability Implementation

### Logging Format
```json
{
  "timestamp": "ISO8601",
  "level": "INFO|WARN|ERROR",
  "service": "auth-service",
  "event": "login_attempt",
  "user": "username",
  "success": true,
  "ip": "client_ip"
}
```

### Key Metrics (P1)
- `auth_login_total` - 登录总数
- `auth_login_failures` - 登录失败数
- `auth_request_duration_seconds` - 请求耗时

## Configuration

### Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| DATABASE_URL | Yes | - | PostgreSQL 连接串 |
| JWT_SECRET | Yes | - | JWT 签名密钥 |
| JWT_EXPIRATION_HOURS | No | 24 | Token 有效期 |
| LOG_LEVEL | No | INFO | 日志级别 |
