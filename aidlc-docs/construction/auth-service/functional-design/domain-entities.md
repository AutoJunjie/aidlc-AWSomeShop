# Auth Service - Domain Entities

## Entity: User

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| id | Integer | PK, Auto-increment | 用户唯一标识 |
| username | String(50) | Unique, Not Null | 用户名 |
| password_hash | String(255) | Not Null | bcrypt 加密后的密码 |
| role | Enum | Not Null, Default: 'employee' | 角色: employee / admin |
| points_balance | Integer | Not Null, Default: 0 | 积分余额 |
| is_active | Boolean | Not Null, Default: true | 账户是否激活 |
| created_at | Timestamp | Not Null, Default: now() | 创建时间 |
| updated_at | Timestamp | Not Null | 更新时间 |

### Role Enum Values
- `employee`: 普通员工
- `admin`: 管理员

---

## Entity Relationships

```
User (1) ----< PointsTransaction (N)
User (1) ----< Redemption (N)
```

Note: PointsTransaction 和 Redemption 实体由其他服务管理，Auth Service 仅管理 User 实体。

---

## Data Validation Rules

### Username
- 长度: 3-50 字符
- 格式: 字母、数字、下划线
- 唯一性: 系统内唯一

### Password (明文输入)
- 最少 8 位
- 必须包含大写字母
- 必须包含小写字母
- 必须包含数字
