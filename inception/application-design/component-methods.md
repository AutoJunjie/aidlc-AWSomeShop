# Component Methods - AWSomeShop

## Backend Component Methods

### Auth Module

#### `login(username: str, password: str) -> dict`
- **Purpose**: 验证用户凭据并生成 JWT token
- **Input**: username (用户名), password (密码)
- **Output**: {token: str, user: User}
- **Business Rules**: 详细规则将在 Functional Design 定义

#### `logout(token: str) -> bool`
- **Purpose**: 使 token 失效
- **Input**: token (JWT token)
- **Output**: success (bool)

#### `get_current_user(token: str) -> User`
- **Purpose**: 根据 token 获取当前用户信息
- **Input**: token (JWT token)
- **Output**: User object

#### `verify_password(plain_password: str, hashed_password: str) -> bool`
- **Purpose**: 验证密码
- **Input**: plain_password, hashed_password
- **Output**: is_valid (bool)

#### `hash_password(password: str) -> str`
- **Purpose**: 加密密码
- **Input**: password (明文密码)
- **Output**: hashed_password (加密后密码)

---

### Products Module

#### `get_products(is_active: bool = True) -> List[Product]`
- **Purpose**: 获取产品列表
- **Input**: is_active (是否只返回上架产品)
- **Output**: List of Product objects

#### `get_product_by_id(product_id: int) -> Product`
- **Purpose**: 获取产品详情
- **Input**: product_id
- **Output**: Product object

#### `create_product(name: str, description: str, points_cost: int, image_url: str) -> Product`
- **Purpose**: 创建新产品
- **Input**: name, description, points_cost, image_url
- **Output**: Created Product object

#### `update_product(product_id: int, data: dict) -> Product`
- **Purpose**: 更新产品信息
- **Input**: product_id, data (更新字段)
- **Output**: Updated Product object

#### `delete_product(product_id: int) -> bool`
- **Purpose**: 删除/下架产品
- **Input**: product_id
- **Output**: success (bool)

#### `upload_product_image(product_id: int, image_file: File) -> str`
- **Purpose**: 上传产品图片到 S3
- **Input**: product_id, image_file
- **Output**: image_url (S3 URL)

---

### Points Module

#### `get_user_balance(user_id: int) -> int`
- **Purpose**: 获取用户积分余额
- **Input**: user_id
- **Output**: balance (int)

#### `get_points_history(user_id: int) -> List[PointsTransaction]`
- **Purpose**: 获取用户积分历史
- **Input**: user_id
- **Output**: List of PointsTransaction objects

#### `credit_points(user_id: int, amount: int, reason: str, admin_id: int) -> PointsTransaction`
- **Purpose**: 为用户发放积分
- **Input**: user_id, amount, reason, admin_id
- **Output**: Created PointsTransaction object
- **Business Rules**: 详细规则将在 Functional Design 定义

#### `debit_points(user_id: int, amount: int, reason: str, admin_id: int) -> PointsTransaction`
- **Purpose**: 扣除用户积分
- **Input**: user_id, amount, reason, admin_id
- **Output**: Created PointsTransaction object
- **Business Rules**: 详细规则将在 Functional Design 定义

#### `get_all_users_balance() -> List[dict]`
- **Purpose**: 获取所有用户积分余额
- **Input**: None
- **Output**: List of {user_id, username, balance}

#### `get_auto_rules() -> List[AutoRule]`
- **Purpose**: 获取自动发放规则
- **Input**: None
- **Output**: List of AutoRule objects

#### `create_auto_rule(amount: int, frequency: str) -> AutoRule`
- **Purpose**: 创建自动发放规则
- **Input**: amount, frequency (monthly/weekly)
- **Output**: Created AutoRule object

---

### Redemptions Module

#### `redeem_product(user_id: int, product_id: int) -> Redemption`
- **Purpose**: 兑换产品
- **Input**: user_id, product_id
- **Output**: Created Redemption object
- **Business Rules**: 详细规则将在 Functional Design 定义

#### `get_redemption_history(user_id: int) -> List[Redemption]`
- **Purpose**: 获取用户兑换历史
- **Input**: user_id
- **Output**: List of Redemption objects

#### `get_redemption_by_id(redemption_id: int) -> Redemption`
- **Purpose**: 获取兑换详情
- **Input**: redemption_id
- **Output**: Redemption object

---

### Database Module

#### `get_db_session() -> Session`
- **Purpose**: 获取数据库会话
- **Output**: SQLAlchemy Session

#### `create_tables()`
- **Purpose**: 创建数据库表
- **Output**: None

#### `run_migrations()`
- **Purpose**: 运行数据库迁移
- **Output**: None

---

### S3 Module

#### `upload_file(file: File, bucket: str, key: str) -> str`
- **Purpose**: 上传文件到 S3
- **Input**: file, bucket, key
- **Output**: file_url (S3 URL)

#### `generate_presigned_url(bucket: str, key: str, expiration: int) -> str`
- **Purpose**: 生成预签名 URL
- **Input**: bucket, key, expiration (seconds)
- **Output**: presigned_url

#### `delete_file(bucket: str, key: str) -> bool`
- **Purpose**: 删除 S3 文件
- **Input**: bucket, key
- **Output**: success (bool)

---

## Frontend Component Methods

### LoginPage

#### `handleLogin(username: string, password: string) -> void`
- **Purpose**: 处理登录表单提交
- **Input**: username, password
- **Output**: None (redirects on success)

#### `validateForm() -> boolean`
- **Purpose**: 验证表单输入
- **Output**: is_valid (boolean)

---

### ProductsPage

#### `fetchProducts() -> void`
- **Purpose**: 从 API 获取产品列表
- **Output**: None (updates state)

#### `handleRedeem(productId: number) -> void`
- **Purpose**: 处理产品兑换
- **Input**: productId
- **Output**: None (shows success/error message)

#### `showProductDetail(productId: number) -> void`
- **Purpose**: 显示产品详情
- **Input**: productId
- **Output**: None (opens modal)

---

### PointsPage

#### `fetchPointsBalance() -> void`
- **Purpose**: 获取积分余额
- **Output**: None (updates state)

#### `fetchPointsHistory() -> void`
- **Purpose**: 获取积分历史
- **Output**: None (updates state)

---

### RedemptionsPage

#### `fetchRedemptionHistory() -> void`
- **Purpose**: 获取兑换历史
- **Output**: None (updates state)

---

### AdminProductsPage

#### `fetchProducts() -> void`
- **Purpose**: 获取所有产品
- **Output**: None (updates state)

#### `handleCreateProduct(data: ProductData) -> void`
- **Purpose**: 创建新产品
- **Input**: ProductData
- **Output**: None (refreshes list)

#### `handleUpdateProduct(productId: number, data: ProductData) -> void`
- **Purpose**: 更新产品
- **Input**: productId, ProductData
- **Output**: None (refreshes list)

#### `handleDeleteProduct(productId: number) -> void`
- **Purpose**: 删除产品
- **Input**: productId
- **Output**: None (refreshes list)

#### `handleImageUpload(productId: number, file: File) -> void`
- **Purpose**: 上传产品图片
- **Input**: productId, file
- **Output**: None (updates product)

---

### AdminPointsPage

#### `fetchAllUsersBalance() -> void`
- **Purpose**: 获取所有用户积分
- **Output**: None (updates state)

#### `handleCreditPoints(userId: number, amount: number, reason: string) -> void`
- **Purpose**: 发放积分
- **Input**: userId, amount, reason
- **Output**: None (refreshes list)

#### `handleDebitPoints(userId: number, amount: number, reason: string) -> void`
- **Purpose**: 扣除积分
- **Input**: userId, amount, reason
- **Output**: None (refreshes list)

#### `handleCreateAutoRule(amount: number, frequency: string) -> void`
- **Purpose**: 创建自动发放规则
- **Input**: amount, frequency
- **Output**: None (refreshes rules)

---

### Services Layer (Frontend)

#### AuthService
- `login(username, password) -> Promise<{token, user}>`
- `logout() -> Promise<void>`
- `getCurrentUser() -> Promise<User>`

#### ProductsService
- `getProducts() -> Promise<Product[]>`
- `getProductById(id) -> Promise<Product>`
- `createProduct(data) -> Promise<Product>`
- `updateProduct(id, data) -> Promise<Product>`
- `deleteProduct(id) -> Promise<void>`
- `uploadImage(id, file) -> Promise<string>`

#### PointsService
- `getBalance() -> Promise<number>`
- `getHistory() -> Promise<PointsTransaction[]>`
- `creditPoints(userId, amount, reason) -> Promise<PointsTransaction>`
- `debitPoints(userId, amount, reason) -> Promise<PointsTransaction>`
- `getAllUsersBalance() -> Promise<UserBalance[]>`
- `getAutoRules() -> Promise<AutoRule[]>`
- `createAutoRule(amount, frequency) -> Promise<AutoRule>`

#### RedemptionsService
- `redeemProduct(productId) -> Promise<Redemption>`
- `getHistory() -> Promise<Redemption[]>`
- `getRedemptionById(id) -> Promise<Redemption>`
