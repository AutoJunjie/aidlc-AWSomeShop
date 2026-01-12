# Units of Work - AWSomeShop

## Architecture Overview
AWSomeShop 采用**微服务架构**，包含 5 个独立的工作单元：
- 4 个后端微服务（Auth, Products, Points, Redemptions）
- 1 个前端应用

---

## Unit 1: Auth Service

### Responsibilities
- 用户认证和授权
- JWT token 生成和验证
- 会话管理
- 密码加密和验证
- 角色权限检查

### Components (from Application Design)
- **Auth Module**: 完整的认证逻辑
- **Database Module**: User 表的 CRUD

### API Endpoints
- POST /api/auth/login
- POST /api/auth/logout
- GET /api/auth/me
- GET /api/auth/verify (内部服务间调用)

### Technology Stack
- Python FastAPI
- PostgreSQL (User 表)
- JWT library
- bcrypt (密码加密)

### Dependencies
- Database: PostgreSQL
- External: None

---

## Unit 2: Products Service

### Responsibilities
- 产品信息管理
- 产品 CRUD 操作
- 产品图片上传到 S3
- 产品状态管理

### Components (from Application Design)
- **Products Module**: 产品业务逻辑
- **S3 Module**: AWS S3 集成
- **Database Module**: Product 表的 CRUD

### API Endpoints
- GET /api/products
- GET /api/products/{id}
- POST /api/products (Admin only)
- PUT /api/products/{id} (Admin only)
- DELETE /api/products/{id} (Admin only)
- POST /api/products/{id}/image (Admin only)

### Technology Stack
- Python FastAPI
- PostgreSQL (Product 表)
- AWS S3 SDK (boto3)

### Dependencies
- Database: PostgreSQL
- External: AWS S3
- Service: Auth Service (权限验证)

---

## Unit 3: Points Service

### Responsibilities
- 员工积分管理
- 积分发放和扣除
- 积分历史记录
- 自动发放规则配置

### Components (from Application Design)
- **Points Module**: 积分业务逻辑
- **Database Module**: PointsTransaction 表的 CRUD，User.points_balance 更新

### API Endpoints
- GET /api/points/balance
- GET /api/points/history
- POST /api/points/credit (Admin only)
- POST /api/points/debit (Admin only)
- GET /api/points/users (Admin only)
- GET /api/points/auto-rules (Admin only)
- POST /api/points/auto-rules (Admin only)
- GET /api/points/check-balance/{user_id} (内部服务间调用)

### Technology Stack
- Python FastAPI
- PostgreSQL (PointsTransaction 表, User.points_balance)

### Dependencies
- Database: PostgreSQL
- Service: Auth Service (权限验证)

---

## Unit 4: Redemptions Service

### Responsibilities
- 产品兑换流程
- 积分扣除验证
- 兑换历史记录

### Components (from Application Design)
- **Redemptions Module**: 兑换业务逻辑
- **Database Module**: Redemption 表的 CRUD

### API Endpoints
- POST /api/redemptions
- GET /api/redemptions/history
- GET /api/redemptions/{id}

### Technology Stack
- Python FastAPI
- PostgreSQL (Redemption 表)

### Dependencies
- Database: PostgreSQL
- Service: Auth Service (用户验证)
- Service: Products Service (产品信息查询)
- Service: Points Service (积分余额检查和扣除)

---

## Unit 5: Frontend Application

### Responsibilities
- 用户界面展示
- 用户交互处理
- 调用后端微服务 API
- 客户端状态管理

### Components (from Application Design)
- **LoginPage**: 登录页面
- **ProductsPage**: 产品浏览和兑换
- **PointsPage**: 积分查询
- **RedemptionsPage**: 兑换历史
- **AdminProductsPage**: 产品管理
- **AdminPointsPage**: 积分管理
- **Shared Components**: Header, Navigation, ProductCard, etc.
- **Services Layer**: AuthService, ProductsService, PointsService, RedemptionsService

### Technology Stack
- React
- React Router (页面路由)
- Axios (HTTP 客户端)
- State Management (Context API 或 Redux)

### Dependencies
- Service: Auth Service (登录、验证)
- Service: Products Service (产品 CRUD)
- Service: Points Service (积分管理)
- Service: Redemptions Service (兑换操作)

---

## Code Organization Strategy (Greenfield)

### Repository Structure
```
awsomeshop/
├── services/
│   ├── auth-service/
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── models.py
│   │   │   ├── routes.py
│   │   │   ├── services.py
│   │   │   └── utils.py
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── products-service/
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── models.py
│   │   │   ├── routes.py
│   │   │   ├── services.py
│   │   │   └── s3_client.py
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── points-service/
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── models.py
│   │   │   ├── routes.py
│   │   │   └── services.py
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   └── redemptions-service/
│       ├── app/
│       │   ├── main.py
│       │   ├── models.py
│       │   ├── routes.py
│       │   └── services.py
│       ├── tests/
│       ├── Dockerfile
│       └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── LoginPage.jsx
│   │   │   ├── ProductsPage.jsx
│   │   │   ├── PointsPage.jsx
│   │   │   ├── RedemptionsPage.jsx
│   │   │   ├── AdminProductsPage.jsx
│   │   │   └── AdminPointsPage.jsx
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── Navigation.jsx
│   │   │   └── ProductCard.jsx
│   │   ├── services/
│   │   │   ├── authService.js
│   │   │   ├── productsService.js
│   │   │   ├── pointsService.js
│   │   │   └── redemptionsService.js
│   │   ├── App.jsx
│   │   └── index.js
│   ├── Dockerfile
│   └── package.json
│
├── infrastructure/
│   ├── docker-compose.yml
│   ├── kubernetes/
│   │   ├── auth-deployment.yaml
│   │   ├── products-deployment.yaml
│   │   ├── points-deployment.yaml
│   │   ├── redemptions-deployment.yaml
│   │   ├── frontend-deployment.yaml
│   │   └── postgres-deployment.yaml
│   └── terraform/ (optional)
│
└── README.md
```

### Deployment Configuration
- **Container Orchestration**: Kubernetes
- **Each Service**: Independent Docker container
- **Database**: Shared PostgreSQL instance (可选：每个服务独立数据库）
- **API Gateway**: Optional (Nginx/Kong/AWS API Gateway)
- **Service Discovery**: Kubernetes DNS

### Build and Deployment
- **CI/CD**: GitHub Actions / GitLab CI
- **Container Registry**: Docker Hub / AWS ECR
- **Deployment Strategy**: Rolling update
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack / CloudWatch

---

## Service Communication Patterns

### Synchronous Communication (REST API)
- Frontend → Backend Services: HTTP/REST
- Service-to-Service: HTTP/REST (内部 API)

### Authentication Flow
1. Frontend calls Auth Service for login
2. Auth Service returns JWT token
3. Frontend includes token in all subsequent requests
4. Each service validates token with Auth Service

### Service-to-Service Authentication
- Option 1: Service-to-service JWT tokens
- Option 2: API keys for internal communication
- Option 3: Mutual TLS (mTLS)

---

## Shared Resources

### Database
- **Option 1**: Shared PostgreSQL instance with separate schemas
  - auth_schema (User table)
  - products_schema (Product table)
  - points_schema (PointsTransaction table)
  - redemptions_schema (Redemption table)
  
- **Option 2**: Separate databases per service (recommended for true microservices)
  - auth_db
  - products_db
  - points_db
  - redemptions_db

### Configuration
- Environment variables for each service
- Kubernetes ConfigMaps and Secrets
- Service discovery via Kubernetes DNS

---

## Development Workflow

### Local Development
1. Use docker-compose for local environment
2. Each service runs in its own container
3. Frontend connects to localhost:PORT for each service

### Testing Strategy
- **Unit Tests**: Per service
- **Integration Tests**: Service-to-service interactions
- **E2E Tests**: Frontend → All services

### Deployment Order
1. Database setup
2. Auth Service (other services depend on it)
3. Products Service, Points Service (independent)
4. Redemptions Service (depends on Products and Points)
5. Frontend (depends on all backend services)
