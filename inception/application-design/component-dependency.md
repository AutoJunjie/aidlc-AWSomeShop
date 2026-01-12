# Component Dependencies - AWSomeShop

## Backend Component Dependency Matrix

| Component | Depends On | Used By |
|-----------|------------|---------|
| Auth Module | Database Module | AuthService, All protected APIs |
| Products Module | Database Module, S3 Module | ProductService |
| Points Module | Database Module | PointsService, RedemptionService |
| Redemptions Module | Database Module, Points Module | RedemptionService |
| Database Module | None | All modules |
| S3 Module | None | Products Module |

---

## Backend Dependency Graph

```
                    ┌─────────────────┐
                    │  API Routes     │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Services Layer │
                    │  (Orchestration)│
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼────────┐  ┌────────▼────────┐  ┌───────▼────────┐
│  Auth Module   │  │ Products Module │  │ Points Module  │
└───────┬────────┘  └────────┬────────┘  └───────┬────────┘
        │                    │                    │
        │           ┌────────▼────────┐           │
        │           │  S3 Module      │           │
        │           └─────────────────┘           │
        │                                         │
        └────────────────┬───────────────────────┘
                         │
                ┌────────▼────────┐
                │ Database Module │
                └─────────────────┘
```

---

## Frontend Component Dependency Matrix

| Component | Depends On | Used By |
|-----------|------------|---------|
| LoginPage | AuthService | App Router |
| ProductsPage | ProductsService, PointsService, RedemptionsService | App Router |
| PointsPage | PointsService | App Router |
| RedemptionsPage | RedemptionsService | App Router |
| AdminProductsPage | ProductsService | App Router |
| AdminPointsPage | PointsService | App Router |
| Shared Components | None | All Pages |
| AuthService | API Client | LoginPage, All Pages |
| ProductsService | API Client | ProductsPage, AdminProductsPage |
| PointsService | API Client | ProductsPage, PointsPage, AdminPointsPage |
| RedemptionsService | API Client | ProductsPage, RedemptionsPage |
| API Client | None | All Services |

---

## Frontend Dependency Graph

```
                    ┌─────────────────┐
                    │   App Router    │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼────────┐  ┌────────▼────────┐  ┌───────▼────────┐
│  LoginPage     │  │ ProductsPage    │  │ AdminPages     │
└───────┬────────┘  └────────┬────────┘  └───────┬────────┘
        │                    │                    │
        │           ┌────────▼────────┐           │
        │           │ Shared Components│          │
        │           └─────────────────┘           │
        │                                         │
        └────────────────┬───────────────────────┘
                         │
                ┌────────▼────────┐
                │ Services Layer  │
                │ (API Calls)     │
                └────────┬────────┘
                         │
                ┌────────▼────────┐
                │   API Client    │
                └────────┬────────┘
                         │
                ┌────────▼────────┐
                │  Backend APIs   │
                └─────────────────┘
```

---

## Communication Patterns

### 1. Backend Internal Communication

#### Auth Module → Database Module
```
Purpose: 查询用户信息
Flow: Auth.get_user() -> Database.query(User)
Data: User credentials, User object
```

#### Products Module → Database Module
```
Purpose: 产品 CRUD
Flow: Products.create() -> Database.insert(Product)
Data: Product data, Product object
```

#### Products Module → S3 Module
```
Purpose: 图片上传
Flow: Products.upload_image() -> S3.upload_file()
Data: Image file, S3 URL
```

#### Points Module → Database Module
```
Purpose: 积分操作
Flow: Points.credit() -> Database.insert(PointsTransaction) + Database.update(User.balance)
Data: Transaction data, Updated balance
```

#### Redemptions Module → Points Module
```
Purpose: 扣除积分
Flow: Redemptions.redeem() -> Points.debit()
Data: User ID, Amount, Transaction record
```

#### Redemptions Module → Database Module
```
Purpose: 创建兑换记录
Flow: Redemptions.redeem() -> Database.insert(Redemption)
Data: Redemption data, Redemption object
```

---

### 2. Frontend to Backend Communication

#### LoginPage → Backend Auth API
```
Method: POST /api/auth/login
Request: {username, password}
Response: {token, user}
```

#### ProductsPage → Backend Products API
```
Method: GET /api/products
Request: None
Response: [Product]
```

#### ProductsPage → Backend Redemptions API
```
Method: POST /api/redemptions
Request: {product_id}
Response: {redemption, updated_balance}
```

#### PointsPage → Backend Points API
```
Method: GET /api/points/balance
Request: None (user from token)
Response: {balance}

Method: GET /api/points/history
Request: None (user from token)
Response: [PointsTransaction]
```

#### AdminProductsPage → Backend Products API
```
Method: POST /api/products
Request: {name, description, points_cost, image}
Response: {product}

Method: PUT /api/products/{id}
Request: {updated_fields}
Response: {product}

Method: DELETE /api/products/{id}
Request: None
Response: {success}
```

#### AdminPointsPage → Backend Points API
```
Method: POST /api/points/credit
Request: {user_id, amount, reason}
Response: {transaction}

Method: POST /api/points/debit
Request: {user_id, amount, reason}
Response: {transaction}

Method: GET /api/points/users
Request: None
Response: [{user_id, username, balance}]
```

---

## Data Flow Examples

### Example 1: User Login Flow
```
1. User enters credentials in LoginPage
2. LoginPage calls AuthService.login()
3. AuthService sends POST /api/auth/login via API Client
4. Backend Auth API receives request
5. AuthService (backend) validates credentials
6. AuthService queries Database for user
7. AuthService generates JWT token
8. Backend returns {token, user}
9. Frontend AuthService stores token
10. LoginPage redirects to ProductsPage
```

### Example 2: Product Redemption Flow
```
1. User clicks "Redeem" on ProductsPage
2. ProductsPage calls RedemptionsService.redeemProduct()
3. RedemptionsService sends POST /api/redemptions
4. Backend Redemptions API receives request
5. RedemptionService validates user and product
6. RedemptionService checks points balance
7. RedemptionService starts transaction
8. RedemptionService calls Points.debit()
9. Points Module updates user balance
10. RedemptionService creates redemption record
11. RedemptionService commits transaction
12. Backend returns {redemption, updated_balance}
13. ProductsPage updates UI with new balance
14. ProductsPage shows success message
```

### Example 3: Admin Credit Points Flow
```
1. Admin enters user and amount in AdminPointsPage
2. AdminPointsPage calls PointsService.creditPoints()
3. PointsService sends POST /api/points/credit
4. Backend Points API receives request
5. PointsService validates admin permission
6. PointsService creates transaction record
7. PointsService updates user balance
8. Backend returns {transaction}
9. AdminPointsPage refreshes user balance list
10. AdminPointsPage shows success message
```

---

## Dependency Management Rules

### Backend
1. **No circular dependencies**: Services can call modules, modules cannot call services
2. **Database Module is leaf**: No dependencies on other modules
3. **S3 Module is leaf**: No dependencies on other modules
4. **Auth Module is cross-cutting**: Can be used by all services for permission checks

### Frontend
1. **Pages depend on Services**: Pages never call API Client directly
2. **Services depend on API Client**: Services encapsulate all HTTP logic
3. **Shared Components are stateless**: No dependencies on services
4. **API Client is singleton**: Single instance shared across all services
