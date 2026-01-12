# Auth Service - Functional Design

## Overview
Auth Service 负责用户认证和授权，是所有其他服务的依赖项。

## API Endpoints

### POST /api/auth/login
**Purpose**: 用户登录

**Request**:
```json
{
  "username": "string",
  "password": "string"
}
```

**Response (200)**:
```json
{
  "token": "jwt_token_string",
  "user": {
    "id": 1,
    "username": "string",
    "role": "employee|admin"
  }
}
```

**Error Responses**:
- 400: 缺少必填字段
- 401: 用户名或密码错误

**Business Rules**:
- BR-1: username 和 password 均为必填
- BR-2: 密码使用 bcrypt 验证
- BR-3: JWT token 有效期 24 小时
- BR-4: token payload 包含 user_id, username, role

---

### POST /api/auth/logout
**Purpose**: 用户登出

**Request Headers**:
- Authorization: Bearer {token}

**Response (200)**:
```json
{
  "message": "Logged out successfully"
}
```

**Business Rules**:
- BR-5: 客户端负责清除本地 token
- BR-6: 服务端可选实现 token 黑名单（MVP 阶段不实现）

---

### GET /api/auth/me
**Purpose**: 获取当前用户信息

**Request Headers**:
- Authorization: Bearer {token}

**Response (200)**:
```json
{
  "id": 1,
  "username": "string",
  "role": "employee|admin",
  "points_balance": 1000
}
```

**Error Responses**:
- 401: token 无效或过期

---

### GET /api/auth/verify (Internal)
**Purpose**: 服务间调用，验证 token 有效性

**Request Headers**:
- Authorization: Bearer {token}

**Response (200)**:
```json
{
  "valid": true,
  "user_id": 1,
  "role": "employee|admin"
}
```

**Response (401)**:
```json
{
  "valid": false,
  "error": "Invalid or expired token"
}
```

---

## Data Model

### User Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'employee',
    points_balance INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Constraints
CHECK (role IN ('employee', 'admin'))
CHECK (points_balance >= 0)
```

---

## Business Logic

### Password Hashing
- Algorithm: bcrypt
- Salt rounds: 12

### JWT Token
- Algorithm: HS256
- Secret: 环境变量 JWT_SECRET
- Expiration: 24 hours
- Payload:
  ```json
  {
    "sub": "user_id",
    "username": "string",
    "role": "string",
    "exp": "timestamp"
  }
  ```

### Role-Based Access
| Role | Permissions |
|------|-------------|
| employee | 查看自己的信息、积分、兑换 |
| admin | 所有 employee 权限 + 管理产品、管理积分 |

---

## Error Handling

| Error Code | Message | Scenario |
|------------|---------|----------|
| AUTH001 | Invalid credentials | 用户名或密码错误 |
| AUTH002 | Token expired | JWT 过期 |
| AUTH003 | Invalid token | JWT 格式错误或签名无效 |
| AUTH004 | Missing token | 请求头缺少 Authorization |
| AUTH005 | User not found | 用户不存在 |

---

## Seed Data (Development)

```sql
-- Admin user (password: admin123)
INSERT INTO users (username, password_hash, role, points_balance)
VALUES ('admin', '$2b$12$...', 'admin', 0);

-- Test employees (password: test123)
INSERT INTO users (username, password_hash, role, points_balance)
VALUES 
  ('employee1', '$2b$12$...', 'employee', 1000),
  ('employee2', '$2b$12$...', 'employee', 500);
```
