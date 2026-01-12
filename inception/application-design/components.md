# Application Components - AWSomeShop

## Backend Components

### 1. Auth Module
**Purpose**: 处理用户认证和授权

**Responsibilities**:
- 用户登录验证
- 会话管理
- JWT token 生成和验证
- 角色权限检查
- 密码加密和验证

**Interfaces**:
- POST /api/auth/login
- POST /api/auth/logout
- GET /api/auth/me

---

### 2. Products Module
**Purpose**: 管理产品信息

**Responsibilities**:
- 产品 CRUD 操作
- 产品列表查询
- 产品详情查询
- 产品图片上传到 S3
- 产品状态管理（上架/下架）

**Interfaces**:
- GET /api/products
- GET /api/products/{id}
- POST /api/products (Admin only)
- PUT /api/products/{id} (Admin only)
- DELETE /api/products/{id} (Admin only)
- POST /api/products/{id}/image (Admin only)

---

### 3. Points Module
**Purpose**: 管理员工积分

**Responsibilities**:
- 查询员工积分余额
- 积分发放（手动/自动）
- 积分扣除
- 积分历史记录
- 自动发放规则配置

**Interfaces**:
- GET /api/points/balance
- GET /api/points/history
- POST /api/points/credit (Admin only)
- POST /api/points/debit (Admin only)
- GET /api/points/users (Admin only)
- GET /api/points/auto-rules (Admin only)
- POST /api/points/auto-rules (Admin only)

---

### 4. Redemptions Module
**Purpose**: 处理产品兑换流程

**Responsibilities**:
- 产品兑换处理
- 积分扣除验证
- 兑换历史记录
- 兑换状态管理

**Interfaces**:
- POST /api/redemptions
- GET /api/redemptions/history
- GET /api/redemptions/{id}

---

### 5. Database Module
**Purpose**: 数据持久化层

**Responsibilities**:
- 数据库连接管理
- ORM 模型定义
- 数据库迁移
- 查询优化

**Models**:
- User
- Product
- PointsTransaction
- Redemption

---

### 6. S3 Module
**Purpose**: AWS S3 集成

**Responsibilities**:
- 图片上传到 S3
- 生成预签名 URL
- 图片删除

---

## Frontend Components

### 1. LoginPage
**Purpose**: 用户登录页面

**Responsibilities**:
- 显示登录表单
- 验证用户输入
- 调用登录 API
- 处理登录成功/失败
- 重定向到主页

---

### 2. ProductsPage (Employee)
**Purpose**: 员工产品浏览和兑换页面

**Responsibilities**:
- 显示产品列表
- 显示产品详情
- 显示当前积分余额
- 处理产品兑换
- 显示兑换成功/失败消息

---

### 3. PointsPage (Employee)
**Purpose**: 员工积分管理页面

**Responsibilities**:
- 显示当前积分余额
- 显示积分历史记录
- 区分积分获得和消费

---

### 4. RedemptionsPage (Employee)
**Purpose**: 员工兑换历史页面

**Responsibilities**:
- 显示兑换历史列表
- 显示兑换详情
- 按时间排序

---

### 5. AdminProductsPage
**Purpose**: 管理员产品管理页面

**Responsibilities**:
- 显示所有产品列表
- 添加新产品
- 编辑产品信息
- 删除/下架产品
- 上传产品图片

---

### 6. AdminPointsPage
**Purpose**: 管理员积分管理页面

**Responsibilities**:
- 显示所有员工积分余额
- 为员工发放积分
- 扣除员工积分
- 配置自动发放规则
- 查看积分操作日志

---

### 7. Shared Components
**Purpose**: 跨页面共享的 UI 组件

**Components**:
- Header (显示用户信息和积分余额)
- Navigation (导航菜单)
- ProductCard (产品卡片)
- PointsDisplay (积分显示)
- Modal (弹窗)
- Form components (输入框、按钮等)

---

### 8. Services Layer (Frontend)
**Purpose**: 封装 API 调用

**Services**:
- AuthService (登录、登出、获取当前用户)
- ProductsService (产品 CRUD)
- PointsService (积分查询和管理)
- RedemptionsService (兑换操作)
