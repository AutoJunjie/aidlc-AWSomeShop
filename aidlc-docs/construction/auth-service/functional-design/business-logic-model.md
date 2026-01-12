# Auth Service - Business Logic Model

## Login Flow

```
Input: username, password
│
├─► Validate input (non-empty)
│   └─► Error: "用户名和密码不能为空"
│
├─► Find user by username (case-insensitive)
│   └─► Not found: Error "用户名或密码错误"
│
├─► Check user.is_active
│   └─► False: Error "账户已禁用"
│
├─► Verify password (bcrypt)
│   └─► Invalid: Error "用户名或密码错误"
│
└─► Generate JWT Token
    └─► Return: { token, user: {id, username, role} }
```

---

## Register Flow

```
Input: username, password
│
├─► Validate username format
│   └─► Invalid: Error "用户名格式不正确"
│
├─► Check username uniqueness
│   └─► Exists: Error "用户名已存在"
│
├─► Validate password complexity
│   └─► Invalid: Error "密码不符合要求"
│
├─► Hash password (bcrypt)
│
├─► Determine role
│   ├─► First user: role = 'admin'
│   └─► Otherwise: role = 'employee'
│
└─► Create user record
    └─► Return: { user: {id, username, role} }
```

---

## Token Verification Flow

```
Input: token (from Authorization header)
│
├─► Extract token from "Bearer {token}"
│   └─► Missing: Error 401 "未提供认证令牌"
│
├─► Decode and verify JWT signature
│   └─► Invalid: Error 401 "无效的认证令牌"
│
├─► Check token expiration
│   └─► Expired: Error 401 "认证令牌已过期"
│
├─► Extract user_id from payload
│
├─► Find user by id
│   └─► Not found: Error 401 "用户不存在"
│
├─► Check user.is_active
│   └─► False: Error 401 "账户已禁用"
│
└─► Return: User object
```

---

## Get Current User Flow

```
Input: token
│
├─► Verify token (Token Verification Flow)
│
└─► Return: { id, username, role, points_balance }
```

---

## Role Check Flow (for protected endpoints)

```
Input: token, required_role
│
├─► Verify token (Token Verification Flow)
│   └─► Returns: user
│
├─► Check user.role
│   └─► role != required_role: Error 403 "权限不足"
│
└─► Allow access
```

---

## Password Validation Logic

```python
def validate_password(password: str) -> bool:
    if len(password) < 8:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.islower() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    return True
```

---

## JWT Token Structure

### Header
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

### Payload
```json
{
  "user_id": 1,
  "username": "john_doe",
  "role": "employee",
  "exp": 1736697600,
  "iat": 1736611200
}
```

### Token Expiration
- Issued At (iat): Token 生成时间
- Expiration (exp): iat + 24 hours

---

## Error Response Format

```json
{
  "detail": "错误描述信息"
}
```

### HTTP Status Codes
| Code | Usage |
|------|-------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未认证/Token 无效 |
| 403 | 权限不足 |
| 409 | 冲突（如用户名已存在） |
