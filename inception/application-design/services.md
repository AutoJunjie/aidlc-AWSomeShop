# Service Layer Design - AWSomeShop

## Backend Service Layer

### Service Orchestration Pattern
采用 **Service Layer Pattern**，在 API 路由和数据访问层之间提供业务逻辑编排。

---

### 1. AuthService
**Responsibilities**:
- 编排用户认证流程
- 协调密码验证和 token 生成
- 管理用户会话

**Orchestration**:
```
login() flow:
1. 验证用户输入
2. 查询用户（Database Module）
3. 验证密码（Auth Module）
4. 生成 JWT token（Auth Module）
5. 返回 token 和用户信息
```

**Dependencies**:
- Database Module (查询用户)
- Auth Module (密码验证、token 生成)

---

### 2. ProductService
**Responsibilities**:
- 编排产品管理流程
- 协调产品 CRUD 和图片上传
- 验证产品数据

**Orchestration**:
```
create_product() flow:
1. 验证产品数据
2. 创建产品记录（Database Module）
3. 如果有图片，上传到 S3（S3 Module）
4. 更新产品图片 URL（Database Module）
5. 返回产品信息

upload_image() flow:
1. 验证产品存在（Database Module）
2. 上传图片到 S3（S3 Module）
3. 更新产品图片 URL（Database Module）
4. 返回图片 URL
```

**Dependencies**:
- Database Module (产品 CRUD)
- S3 Module (图片上传)
- Products Module (业务逻辑)

---

### 3. PointsService
**Responsibilities**:
- 编排积分管理流程
- 协调积分发放、扣除和查询
- 验证积分操作合法性

**Orchestration**:
```
credit_points() flow:
1. 验证用户存在（Database Module）
2. 验证管理员权限（Auth Module）
3. 创建积分交易记录（Database Module）
4. 更新用户积分余额（Database Module）
5. 返回交易记录

debit_points() flow:
1. 验证用户存在（Database Module）
2. 验证管理员权限（Auth Module）
3. 检查积分余额是否足够（Points Module）
4. 创建积分交易记录（Database Module）
5. 更新用户积分余额（Database Module）
6. 返回交易记录
```

**Dependencies**:
- Database Module (积分 CRUD)
- Auth Module (权限验证)
- Points Module (业务逻辑)

---

### 4. RedemptionService
**Responsibilities**:
- 编排产品兑换流程
- 协调积分扣除和兑换记录
- 验证兑换条件

**Orchestration**:
```
redeem_product() flow:
1. 验证用户存在（Database Module）
2. 验证产品存在且上架（Database Module）
3. 检查用户积分是否足够（Points Module）
4. 开始数据库事务
5. 扣除用户积分（Points Module）
6. 创建兑换记录（Database Module）
7. 提交事务
8. 返回兑换记录

如果任何步骤失败，回滚事务
```

**Dependencies**:
- Database Module (兑换记录 CRUD)
- Points Module (积分扣除)
- Products Module (产品查询)

---

## Frontend Service Layer

### Service Communication Pattern
采用 **API Service Pattern**，封装所有 HTTP 请求，提供统一的错误处理和状态管理。

---

### 1. API Client
**Responsibilities**:
- 统一 HTTP 请求配置
- 自动添加认证 token
- 统一错误处理
- 请求/响应拦截

**Configuration**:
```
Base URL: /api
Headers: 
  - Authorization: Bearer {token}
  - Content-Type: application/json
Error Handling:
  - 401: Redirect to login
  - 403: Show permission error
  - 500: Show server error
```

---

### 2. AuthService (Frontend)
**Responsibilities**:
- 封装认证 API 调用
- 管理本地 token 存储
- 提供登录状态查询

**Methods**:
- `login()`: POST /api/auth/login
- `logout()`: POST /api/auth/logout + clear local token
- `getCurrentUser()`: GET /api/auth/me
- `isAuthenticated()`: Check local token validity

---

### 3. ProductsService (Frontend)
**Responsibilities**:
- 封装产品 API 调用
- 处理图片上传

**Methods**:
- `getProducts()`: GET /api/products
- `getProductById(id)`: GET /api/products/{id}
- `createProduct(data)`: POST /api/products
- `updateProduct(id, data)`: PUT /api/products/{id}
- `deleteProduct(id)`: DELETE /api/products/{id}
- `uploadImage(id, file)`: POST /api/products/{id}/image (multipart/form-data)

---

### 4. PointsService (Frontend)
**Responsibilities**:
- 封装积分 API 调用
- 提供积分状态查询

**Methods**:
- `getBalance()`: GET /api/points/balance
- `getHistory()`: GET /api/points/history
- `creditPoints(userId, amount, reason)`: POST /api/points/credit
- `debitPoints(userId, amount, reason)`: POST /api/points/debit
- `getAllUsersBalance()`: GET /api/points/users
- `getAutoRules()`: GET /api/points/auto-rules
- `createAutoRule(amount, frequency)`: POST /api/points/auto-rules

---

### 5. RedemptionsService (Frontend)
**Responsibilities**:
- 封装兑换 API 调用
- 处理兑换流程

**Methods**:
- `redeemProduct(productId)`: POST /api/redemptions
- `getHistory()`: GET /api/redemptions/history
- `getRedemptionById(id)`: GET /api/redemptions/{id}

---

## Service Interaction Patterns

### Pattern 1: Request-Response (Synchronous)
用于大多数 CRUD 操作：
```
Frontend Component -> Frontend Service -> API Client -> Backend API -> Backend Service -> Database
```

### Pattern 2: Transaction Management (Backend)
用于需要原子性的操作（如兑换）：
```
Backend Service:
1. Begin Transaction
2. Execute multiple operations
3. Commit if all succeed
4. Rollback if any fails
```

### Pattern 3: Error Propagation
```
Backend: Throw specific exceptions
Frontend: Catch and display user-friendly messages
```

---

## Cross-Cutting Concerns

### Authentication & Authorization
- **Backend**: JWT middleware 验证所有受保护的 API
- **Frontend**: API Client 自动添加 token，401 时重定向登录

### Logging
- **Backend**: 记录所有 API 请求和错误
- **Frontend**: 记录 API 错误和用户操作

### Validation
- **Backend**: 验证所有输入数据
- **Frontend**: 客户端验证提供即时反馈

### Error Handling
- **Backend**: 返回标准错误格式 {error: string, details: object}
- **Frontend**: 统一错误处理和用户提示
