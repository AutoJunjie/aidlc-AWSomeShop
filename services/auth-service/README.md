# Auth Service

认证和授权服务 - AWSomeShop 项目的核心服务之一。

## 功能特性

- 用户登录 (JWT token)
- 用户登出
- 获取当前用户信息
- Token 验证（服务间调用）
- 健康检查
- 基于角色的访问控制 (RBAC)
- 密码加密 (bcrypt)

## 技术栈

- **FastAPI**: Python web 框架
- **SQLAlchemy**: ORM
- **PostgreSQL**: 数据库
- **JWT**: 认证 token
- **bcrypt**: 密码哈希
- **Docker**: 容器化

## 项目结构

```
auth-service/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 应用入口
│   ├── config.py            # 配置管理
│   ├── database.py          # 数据库连接和会话
│   ├── models.py            # SQLAlchemy 模型
│   ├── schemas.py           # Pydantic 模型
│   ├── auth.py              # JWT 和密码处理
│   └── routers/
│       ├── __init__.py
│       └── auth_router.py   # 认证 API 端点
├── tests/
│   ├── __init__.py
│   ├── test_auth.py         # 认证模块单元测试
│   ├── test_auth_router.py  # API 端点测试
│   └── test_models.py       # 数据模型测试
├── design/                  # 设计文档
├── requirements.txt         # Python 依赖
├── Dockerfile               # Docker 镜像定义
├── docker-compose.yml       # 多容器编排
├── .dockerignore           # Docker 构建排除文件
├── seed.py                 # 种子数据脚本
└── README.md               # 本文件
```

## 快速开始

### 使用 Docker Compose（推荐）

1. 启动服务：
```bash
docker-compose up -d
```

2. 查看日志：
```bash
docker-compose logs -f auth-service
```

3. 初始化种子数据：
```bash
docker-compose exec auth-service python seed.py
```

4. 访问服务：
- API: http://localhost:8001
- 健康检查: http://localhost:8001/health
- API 文档: http://localhost:8001/docs

5. 停止服务：
```bash
docker-compose down
```

### 本地开发

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 设置环境变量：
```bash
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/awsomeshop"
export JWT_SECRET="your-secret-key"
```

3. 初始化数据库：
```bash
python seed.py
```

4. 启动服务：
```bash
uvicorn app.main:app --reload --port 8000
```

## API 端点

### POST /api/auth/login
用户登录

**请求：**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**响应：**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "admin",
    "role": "admin"
  }
}
```

### POST /api/auth/logout
用户登出

**请求头：**
```
Authorization: Bearer <token>
```

### GET /api/auth/me
获取当前用户信息

**请求头：**
```
Authorization: Bearer <token>
```

**响应：**
```json
{
  "id": 1,
  "username": "admin",
  "role": "admin",
  "points_balance": 0
}
```

### GET /api/auth/verify
验证 token 有效性（服务间调用）

**请求头：**
```
Authorization: Bearer <token>
```

**响应：**
```json
{
  "valid": true,
  "user_id": 1,
  "role": "admin"
}
```

### GET /health
健康检查

**响应：**
```json
{
  "status": "healthy",
  "database": "connected"
}
```

## 测试

运行所有测试：
```bash
pytest
```

运行特定测试文件：
```bash
pytest tests/test_auth.py
```

运行带覆盖率的测试：
```bash
pytest --cov=app --cov-report=html
```

## 环境变量

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| DATABASE_URL | 是 | - | PostgreSQL 连接字符串 |
| JWT_SECRET | 是 | - | JWT 签名密钥 |
| JWT_EXPIRATION_HOURS | 否 | 24 | Token 有效期（小时） |
| LOG_LEVEL | 否 | INFO | 日志级别 |
| SQLALCHEMY_POOL_SIZE | 否 | 10 | 数据库连接池大小 |
| SQLALCHEMY_MAX_OVERFLOW | 否 | 20 | 最大溢出连接数 |
| SQLALCHEMY_POOL_TIMEOUT | 否 | 30 | 连接超时（秒） |

## 默认用户

使用 `seed.py` 创建的默认用户：

| 用户名 | 密码 | 角色 | 积分 |
|--------|------|------|------|
| admin | admin123 | admin | 0 |
| employee1 | test123 | employee | 1000 |
| employee2 | test123 | employee | 500 |

## 错误码

| 错误码 | 说明 |
|--------|------|
| AUTH001 | 用户名或密码错误 |
| AUTH002 | Token 过期 |
| AUTH003 | Token 无效 |
| AUTH004 | 缺少 Token |
| AUTH005 | 用户不存在 |

## 安全注意事项

1. **生产环境必须修改 JWT_SECRET**
2. 使用 HTTPS 传输
3. 定期更新依赖包
4. 限制 CORS 允许的域名
5. 实施速率限制防止暴力破解
6. 考虑实现 token 黑名单机制

## 性能优化

- 数据库连接池配置
- 密码验证使用异步处理
- Token 验证缓存
- 数据库查询优化

## 监控和日志

服务使用结构化日志，记录：
- 登录尝试（成功/失败）
- Token 验证
- 用户操作
- 错误和异常

## 许可证

内部项目 - AWSomeShop
