# Auth Service - NFR Design Patterns

## Stateless Design Pattern

**Purpose**: 支持水平扩展，无需会话同步

**Implementation**:
- JWT Token 包含所有必要用户信息
- 服务端不存储会话状态
- 任意实例可处理任意请求

---

## Security Patterns

### Password Hashing Pattern
- Algorithm: bcrypt
- Cost Factor: 12
- Salt: 自动生成（bcrypt 内置）

### Token-Based Authentication
- Type: JWT (JSON Web Token)
- Algorithm: HS256
- Secret: 环境变量配置
- Expiration: 24 hours

---

## Logging Pattern

### Structured Logging
```json
{
  "timestamp": "ISO8601",
  "level": "INFO|WARN|ERROR",
  "event": "login_attempt|login_success|login_failure",
  "username": "string",
  "ip": "string",
  "user_agent": "string",
  "duration_ms": "number"
}
```

### Audit Events
| Event | Level | Logged Fields |
|-------|-------|---------------|
| login_success | INFO | username, ip, user_agent |
| login_failure | WARN | username, ip, reason |
| token_invalid | WARN | ip, reason |

---

## Error Handling Pattern

### Consistent Error Response
```json
{
  "detail": "Human readable message"
}
```

### Error Mapping
| Exception | HTTP Status | Message |
|-----------|-------------|---------|
| InvalidCredentials | 401 | 用户名或密码错误 |
| TokenExpired | 401 | 认证令牌已过期 |
| TokenInvalid | 401 | 无效的认证令牌 |
| AccountDisabled | 401 | 账户已禁用 |
| PermissionDenied | 403 | 权限不足 |
| UserExists | 409 | 用户名已存在 |

---

## Health Check Pattern

### Endpoint
- Path: `/health`
- Method: GET
- Auth: None

### Response
```json
{
  "status": "healthy",
  "database": "connected"
}
```
