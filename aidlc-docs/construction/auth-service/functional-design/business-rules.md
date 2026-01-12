# Auth Service - Business Rules

## BR-1: Authentication Rules

### BR-1.1: Login Validation
- 用户名和密码均为必填
- 用户名不区分大小写
- 密码区分大小写
- 验证失败返回通用错误消息（不透露具体原因）

### BR-1.2: Password Verification
- 使用 bcrypt 算法验证密码
- 比对输入密码与存储的 hash 值

### BR-1.3: Account Status Check
- 仅 is_active = true 的用户可登录
- 非激活账户返回 "账户已禁用" 错误

---

## BR-2: Token Rules

### BR-2.1: Token Generation
- 登录成功后生成 JWT Token
- Token 有效期: 24 小时
- Token Payload 包含: user_id, username, role, exp

### BR-2.2: Token Validation
- 验证 Token 签名有效性
- 验证 Token 未过期
- 验证 Token 中的 user_id 对应有效用户

### BR-2.3: Token Lifecycle
- 无 Refresh Token 机制
- Token 过期后需重新登录
- 允许多设备同时登录（多个有效 Token）

---

## BR-3: Authorization Rules

### BR-3.1: Role-Based Access
| Role | Permissions |
|------|-------------|
| employee | 浏览产品、兑换产品、查看自己的积分和历史 |
| admin | 所有 employee 权限 + 产品管理 + 积分管理 |

### BR-3.2: Permission Check
- 每个 API 请求需验证 Token
- 管理员接口需验证 role = 'admin'
- 权限不足返回 403 Forbidden

---

## BR-4: Password Security Rules

### BR-4.1: Password Complexity
- 最少 8 个字符
- 至少 1 个大写字母 (A-Z)
- 至少 1 个小写字母 (a-z)
- 至少 1 个数字 (0-9)

### BR-4.2: Password Storage
- 使用 bcrypt 算法加密
- 不存储明文密码
- Hash 轮数: 12 (默认)

---

## BR-5: User Registration Rules

### BR-5.1: Admin Registration
- 提供管理员注册功能
- 首个注册用户自动成为 admin
- 后续用户默认为 employee
- Admin 可将其他用户提升为 admin

### BR-5.2: Username Validation
- 长度: 3-50 字符
- 允许字符: 字母、数字、下划线
- 不允许重复用户名

---

## BR-6: Session Rules

### BR-6.1: Multi-Device Support
- 允许同一用户多设备同时登录
- 每次登录生成独立 Token
- 各 Token 独立过期

### BR-6.2: Logout
- 客户端删除 Token 即完成登出
- 服务端无需维护 Token 黑名单（MVP 简化）
