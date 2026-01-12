# Auth Service - Logical Components

## Component Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Auth Service                       │
├─────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │   Routes    │  │  Services   │  │   Models    │ │
│  │  (FastAPI)  │──│  (Business) │──│(SQLAlchemy) │ │
│  └─────────────┘  └─────────────┘  └─────────────┘ │
│         │                │                │         │
│         ▼                ▼                ▼         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │   Schemas   │  │   Security  │  │  Database   │ │
│  │ (Pydantic)  │  │(JWT/bcrypt) │  │  (asyncpg)  │ │
│  └─────────────┘  └─────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────┘
                          │
                          ▼
                   ┌─────────────┐
                   │ PostgreSQL  │
                   │  (User DB)  │
                   └─────────────┘
```

---

## Logical Components

### 1. Routes Layer
- **Purpose**: HTTP 请求处理和路由
- **Technology**: FastAPI Router
- **Responsibilities**: 请求验证、响应格式化、依赖注入

### 2. Services Layer
- **Purpose**: 业务逻辑实现
- **Components**:
  - `AuthService`: 登录、注册、Token 验证
  - `PasswordService`: 密码加密和验证

### 3. Models Layer
- **Purpose**: 数据库实体定义
- **Technology**: SQLAlchemy ORM
- **Entities**: User

### 4. Schemas Layer
- **Purpose**: 请求/响应数据验证
- **Technology**: Pydantic
- **Schemas**: LoginRequest, TokenResponse, UserResponse

### 5. Security Layer
- **Purpose**: 安全相关功能
- **Components**:
  - JWT 生成和验证
  - bcrypt 密码处理
  - 依赖注入 (get_current_user)

### 6. Database Layer
- **Purpose**: 数据库连接管理
- **Technology**: asyncpg + SQLAlchemy async
- **Features**: 连接池、会话管理

---

## Infrastructure Dependencies

| Component | Type | Purpose |
|-----------|------|---------|
| PostgreSQL | Database | 用户数据存储 |
| Environment Variables | Config | 敏感配置（JWT_SECRET, DATABASE_URL） |

---

## File Structure

```
auth-service/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app entry
│   ├── config.py         # Settings from env
│   ├── database.py       # DB connection
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── routes.py         # API routes
│   ├── services.py       # Business logic
│   └── security.py       # JWT & password utils
├── tests/
├── Dockerfile
├── requirements.txt
└── alembic/              # DB migrations
```
