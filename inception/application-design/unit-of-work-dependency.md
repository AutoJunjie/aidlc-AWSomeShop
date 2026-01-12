# Unit of Work Dependencies - AWSomeShop

## Dependency Matrix

| Unit | Depends On | Used By | Dependency Type |
|------|------------|---------|-----------------|
| Auth Service | PostgreSQL | All Services, Frontend | Strong |
| Products Service | PostgreSQL, AWS S3, Auth Service | Redemptions Service, Frontend | Medium |
| Points Service | PostgreSQL, Auth Service | Redemptions Service, Frontend | Medium |
| Redemptions Service | PostgreSQL, Auth Service, Products Service, Points Service | Frontend | Strong |
| Frontend | Auth Service, Products Service, Points Service, Redemptions Service | End Users | Strong |

---

## Dependency Graph

```
                    ┌─────────────────┐
                    │   End Users     │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │    Frontend     │
                    │   Application   │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼────────┐  ┌────────▼────────┐  ┌───────▼────────┐
│ Auth Service   │  │Products Service │  │ Points Service │
└───────┬────────┘  └────────┬────────┘  └───────┬────────┘
        │                    │                    │
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                    ┌────────▼────────┐
                    │  Redemptions    │
                    │    Service      │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼────────┐  ┌────────▼────────┐  ┌───────▼────────┐
│  PostgreSQL    │  │     AWS S3      │  │  Auth Service  │
└────────────────┘  └─────────────────┘  └────────────────┘
```

---

## Detailed Dependencies

### Unit 1: Auth Service

**Dependencies**:
- **PostgreSQL**: User 表存储
  - Type: Data storage
  - Criticality: High
  - Failure Impact: Service unavailable

**Used By**:
- **All Backend Services**: Token 验证
  - Type: Authentication
  - Communication: HTTP REST (GET /api/auth/verify)
  - Criticality: High
  
- **Frontend**: 用户登录
  - Type: Authentication
  - Communication: HTTP REST
  - Criticality: High

**Failure Impact**:
- Auth Service down → All services cannot authenticate users
- Mitigation: Token caching, graceful degradation

---

### Unit 2: Products Service

**Dependencies**:
- **PostgreSQL**: Product 表存储
  - Type: Data storage
  - Criticality: High
  - Failure Impact: Service unavailable

- **AWS S3**: 产品图片存储
  - Type: File storage
  - Criticality: Medium
  - Failure Impact: Image upload fails, but service continues

- **Auth Service**: 管理员权限验证
  - Type: Authorization
  - Communication: HTTP REST
  - Criticality: High for admin operations

**Used By**:
- **Redemptions Service**: 产品信息查询
  - Type: Data query
  - Communication: HTTP REST (GET /api/products/{id})
  - Criticality: High
  
- **Frontend**: 产品浏览和管理
  - Type: CRUD operations
  - Communication: HTTP REST
  - Criticality: High

**Failure Impact**:
- Products Service down → Cannot browse or redeem products
- S3 down → Cannot upload images, but existing products work
- Mitigation: Cache product data in Frontend

---

### Unit 3: Points Service

**Dependencies**:
- **PostgreSQL**: PointsTransaction 表, User.points_balance
  - Type: Data storage
  - Criticality: High
  - Failure Impact: Service unavailable

- **Auth Service**: 用户验证和管理员权限
  - Type: Authentication & Authorization
  - Communication: HTTP REST
  - Criticality: High

**Used By**:
- **Redemptions Service**: 积分余额检查和扣除
  - Type: Balance check and deduction
  - Communication: HTTP REST (GET /api/points/check-balance, POST /api/points/debit)
  - Criticality: High
  
- **Frontend**: 积分查询和管理
  - Type: Query and management
  - Communication: HTTP REST
  - Criticality: High

**Failure Impact**:
- Points Service down → Cannot redeem products, cannot view balance
- Mitigation: Cache balance in Frontend (with staleness warning)

---

### Unit 4: Redemptions Service

**Dependencies**:
- **PostgreSQL**: Redemption 表存储
  - Type: Data storage
  - Criticality: High
  - Failure Impact: Service unavailable

- **Auth Service**: 用户验证
  - Type: Authentication
  - Communication: HTTP REST
  - Criticality: High

- **Products Service**: 产品信息验证
  - Type: Product validation
  - Communication: HTTP REST (GET /api/products/{id})
  - Criticality: High
  - Failure Impact: Cannot validate product, redemption fails

- **Points Service**: 积分余额检查和扣除
  - Type: Balance check and deduction
  - Communication: HTTP REST (GET /api/points/check-balance, POST /api/points/debit)
  - Criticality: High
  - Failure Impact: Cannot check balance or deduct points, redemption fails

**Used By**:
- **Frontend**: 产品兑换和历史查询
  - Type: Redemption operations
  - Communication: HTTP REST
  - Criticality: High

**Failure Impact**:
- Redemptions Service down → Cannot redeem products
- Products Service down → Cannot validate products, redemption blocked
- Points Service down → Cannot check/deduct points, redemption blocked
- Mitigation: Implement retry logic, transaction rollback

---

### Unit 5: Frontend Application

**Dependencies**:
- **Auth Service**: 用户登录和验证
  - Type: Authentication
  - Communication: HTTP REST
  - Criticality: High
  - Failure Impact: Cannot login

- **Products Service**: 产品浏览和管理
  - Type: CRUD operations
  - Communication: HTTP REST
  - Criticality: High
  - Failure Impact: Cannot view or manage products

- **Points Service**: 积分查询和管理
  - Type: Query and management
  - Communication: HTTP REST
  - Criticality: High
  - Failure Impact: Cannot view or manage points

- **Redemptions Service**: 产品兑换和历史
  - Type: Redemption operations
  - Communication: HTTP REST
  - Criticality: High
  - Failure Impact: Cannot redeem products

**Used By**:
- **End Users**: 员工和管理员
  - Type: User interface
  - Criticality: High

**Failure Impact**:
- Frontend down → Users cannot access system
- Any backend service down → Partial functionality loss
- Mitigation: Show service status, graceful error handling

---

## Service Communication Patterns

### Pattern 1: Frontend → Backend Services
**Type**: Synchronous HTTP REST
**Authentication**: JWT token in Authorization header
**Error Handling**: HTTP status codes, JSON error responses

```
Frontend → Auth Service: Login, verify token
Frontend → Products Service: CRUD products
Frontend → Points Service: Query/manage points
Frontend → Redemptions Service: Redeem products, view history
```

---

### Pattern 2: Service-to-Service (Internal)
**Type**: Synchronous HTTP REST
**Authentication**: Service-to-service token or API key
**Error Handling**: Retry logic, circuit breaker

```
All Services → Auth Service: Verify user token
Redemptions Service → Products Service: Get product info
Redemptions Service → Points Service: Check balance, deduct points
```

---

### Pattern 3: Service → Database
**Type**: Direct database connection
**Connection Pooling**: Yes
**Transaction Management**: Per service

```
Each Service → PostgreSQL: CRUD operations on respective tables
```

---

### Pattern 4: Products Service → AWS S3
**Type**: AWS SDK (boto3)
**Authentication**: AWS credentials (IAM role)
**Error Handling**: Retry with exponential backoff

```
Products Service → AWS S3: Upload/delete product images
```

---

## Dependency Management Strategies

### 1. Service Discovery
- **Kubernetes DNS**: Services discover each other via DNS names
- **Example**: `http://auth-service:8000`, `http://products-service:8001`

### 2. Circuit Breaker Pattern
- Implement circuit breaker for service-to-service calls
- Prevent cascading failures
- Fallback strategies when dependencies fail

### 3. Retry Logic
- Exponential backoff for transient failures
- Maximum retry attempts: 3
- Timeout: 5 seconds per request

### 4. Health Checks
- Each service exposes `/health` endpoint
- Kubernetes liveness and readiness probes
- Monitor service availability

### 5. Database Connection Pooling
- Shared PostgreSQL instance with connection pooling
- Max connections per service: 20
- Connection timeout: 30 seconds

---

## Deployment Order (Based on Dependencies)

### Phase 1: Infrastructure
1. PostgreSQL database
2. AWS S3 bucket setup

### Phase 2: Core Services
3. Auth Service (no service dependencies)

### Phase 3: Independent Services
4. Products Service (depends on Auth)
5. Points Service (depends on Auth)

### Phase 4: Dependent Services
6. Redemptions Service (depends on Auth, Products, Points)

### Phase 5: Frontend
7. Frontend Application (depends on all backend services)

---

## Failure Scenarios and Mitigation

### Scenario 1: Auth Service Down
**Impact**: All services cannot authenticate users
**Mitigation**:
- Token caching with TTL
- Graceful degradation (read-only mode)
- High availability deployment (multiple replicas)

### Scenario 2: Products Service Down
**Impact**: Cannot browse products, redemption fails
**Mitigation**:
- Frontend caches product list
- Show cached data with staleness warning
- Redemption service returns clear error

### Scenario 3: Points Service Down
**Impact**: Cannot check balance, redemption fails
**Mitigation**:
- Frontend caches last known balance
- Redemption service queues requests for retry
- Show service unavailable message

### Scenario 4: Redemptions Service Down
**Impact**: Cannot redeem products
**Mitigation**:
- Show clear error message
- Allow users to retry later
- No data loss (transaction not started)

### Scenario 5: Database Down
**Impact**: All services unavailable
**Mitigation**:
- Database replication (master-slave)
- Automatic failover
- Regular backups

### Scenario 6: AWS S3 Down
**Impact**: Cannot upload new product images
**Mitigation**:
- Existing images still accessible (cached URLs)
- Queue image uploads for retry
- Allow product creation without images
