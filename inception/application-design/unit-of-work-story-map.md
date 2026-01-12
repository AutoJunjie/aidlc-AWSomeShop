# Unit of Work Story Map - AWSomeShop

## Story Assignment by Functional Module

### Unit 1: Auth Service

#### US-E1: 用户登录
**作为** 员工  
**我想要** 使用用户名和密码登录系统  
**以便** 访问我的积分和兑换产品

**Implementation in Auth Service**:
- Backend API: POST /api/auth/login
- Validate credentials
- Generate JWT token
- Return user info and token

**Implementation in Frontend**:
- LoginPage component
- Form validation
- API call to Auth Service
- Store token and redirect

---

### Unit 2: Products Service

#### US-E2: 浏览和兑换产品 (Product browsing part)
**作为** 员工  
**我想要** 浏览所有可兑换的虚拟产品并使用积分兑换  
**以便** 获得我想要的福利

**Implementation in Products Service**:
- Backend API: GET /api/products
- Backend API: GET /api/products/{id}
- Return product list and details

**Implementation in Frontend**:
- ProductsPage component
- Display product list
- Show product details

**Note**: 兑换部分由 Redemptions Service 实现

---

#### US-A1: 管理产品
**作为** 管理员  
**我想要** 添加、编辑和删除产品  
**以便** 维护最新的产品库

**Implementation in Products Service**:
- Backend API: POST /api/products
- Backend API: PUT /api/products/{id}
- Backend API: DELETE /api/products/{id}
- Backend API: POST /api/products/{id}/image
- S3 integration for image upload

**Implementation in Frontend**:
- AdminProductsPage component
- Product CRUD forms
- Image upload functionality

---

### Unit 3: Points Service

#### US-E3: 查看积分余额
**作为** 员工  
**我想要** 随时查看我的当前积分余额  
**以便** 了解我可以兑换什么产品

**Implementation in Points Service**:
- Backend API: GET /api/points/balance
- Return current user's points balance

**Implementation in Frontend**:
- Header component (显示余额)
- PointsPage component

---

#### US-E4: 查看积分历史
**作为** 员工  
**我想要** 查看我的积分获得和消费历史  
**以便** 了解积分的来源和去向

**Implementation in Points Service**:
- Backend API: GET /api/points/history
- Return user's points transaction history

**Implementation in Frontend**:
- PointsPage component
- Display transaction list with filters

---

#### US-A2: 管理员工积分
**作为** 管理员  
**我想要** 为员工发放或扣除积分  
**以便** 灵活管理积分系统

**Implementation in Points Service**:
- Backend API: POST /api/points/credit
- Backend API: POST /api/points/debit
- Backend API: GET /api/points/users
- Create transaction records
- Update user balance

**Implementation in Frontend**:
- AdminPointsPage component
- Credit/Debit forms
- User balance list

---

#### US-A3: 自动发放积分
**作为** 管理员  
**我想要** 配置系统按规则自动发放积分  
**以便** 减少手动操作工作量

**Implementation in Points Service**:
- Backend API: GET /api/points/auto-rules
- Backend API: POST /api/points/auto-rules
- Scheduled job for auto credit
- Rule configuration storage

**Implementation in Frontend**:
- AdminPointsPage component
- Auto-rule configuration form

---

### Unit 4: Redemptions Service

#### US-E2: 浏览和兑换产品 (Redemption part)
**作为** 员工  
**我想要** 浏览所有可兑换的虚拟产品并使用积分兑换  
**以便** 获得我想要的福利

**Implementation in Redemptions Service**:
- Backend API: POST /api/redemptions
- Validate product exists (call Products Service)
- Check points balance (call Points Service)
- Deduct points (call Points Service)
- Create redemption record
- Transaction management

**Implementation in Frontend**:
- ProductsPage component
- Redeem button and confirmation

---

#### US-E5: 查看兑换历史
**作为** 员工  
**我想要** 查看我过往的产品兑换记录  
**以便** 追踪我兑换过的产品

**Implementation in Redemptions Service**:
- Backend API: GET /api/redemptions/history
- Backend API: GET /api/redemptions/{id}
- Return user's redemption history

**Implementation in Frontend**:
- RedemptionsPage component
- Display redemption list

---

### Unit 5: Frontend Application

**All user stories have frontend implementation**:
- US-E1: LoginPage
- US-E2: ProductsPage (browse + redeem)
- US-E3: PointsPage + Header
- US-E4: PointsPage
- US-E5: RedemptionsPage
- US-A1: AdminProductsPage
- US-A2: AdminPointsPage
- US-A3: AdminPointsPage

---

## Story Coverage Matrix

| Story | Auth Service | Products Service | Points Service | Redemptions Service | Frontend |
|-------|--------------|------------------|----------------|---------------------|----------|
| US-E1 | ✅ Primary | - | - | - | ✅ |
| US-E2 | - | ✅ Browse | - | ✅ Redeem | ✅ |
| US-E3 | - | - | ✅ Primary | - | ✅ |
| US-E4 | - | - | ✅ Primary | - | ✅ |
| US-E5 | - | - | - | ✅ Primary | ✅ |
| US-A1 | - | ✅ Primary | - | - | ✅ |
| US-A2 | - | - | ✅ Primary | - | ✅ |
| US-A3 | - | - | ✅ Primary | - | ✅ |

**Legend**:
- ✅ Primary: 主要实现单元
- ✅: 参与实现
- -: 不涉及

---

## Cross-Service Story Implementation

### US-E2: 浏览和兑换产品
这个故事跨越多个服务：
1. **Products Service**: 提供产品列表和详情
2. **Points Service**: 提供积分余额查询
3. **Redemptions Service**: 处理兑换流程，协调 Products 和 Points
4. **Frontend**: 统一的用户界面

**Implementation Flow**:
```
1. User views products (Frontend → Products Service)
2. User sees balance (Frontend → Points Service)
3. User clicks redeem (Frontend → Redemptions Service)
4. Redemptions Service:
   - Validates product (→ Products Service)
   - Checks balance (→ Points Service)
   - Deducts points (→ Points Service)
   - Creates redemption record
5. Frontend updates UI with new balance
```

---

## Story Implementation Priority

### Phase 1: Core Authentication
- US-E1: 用户登录 (Auth Service + Frontend)

### Phase 2: Product Browsing
- US-E2 (Part 1): 浏览产品 (Products Service + Frontend)
- US-E3: 查看积分余额 (Points Service + Frontend)

### Phase 3: Redemption Flow
- US-E2 (Part 2): 兑换产品 (Redemptions Service + Frontend)
- US-E5: 查看兑换历史 (Redemptions Service + Frontend)

### Phase 4: Points Management
- US-E4: 查看积分历史 (Points Service + Frontend)
- US-A2: 管理员工积分 (Points Service + Frontend)

### Phase 5: Admin Features
- US-A1: 管理产品 (Products Service + Frontend)
- US-A3: 自动发放积分 (Points Service + Frontend)
