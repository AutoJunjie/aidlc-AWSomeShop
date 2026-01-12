# Products Service

AWSomeShop 产品服务 - 管理产品信息的微服务

## 功能特性

- 产品 CRUD 操作
- 产品图片上传到 AWS S3
- JWT 身份验证
- RESTful API
- 健康检查端点

## 技术栈

- **框架**: FastAPI
- **数据库**: PostgreSQL
- **云存储**: AWS S3 (boto3)
- **认证**: JWT
- **测试**: pytest

## 项目结构

```
products-service/
├── app/
│   ├── config.py           # 配置管理
│   ├── database.py         # 数据库连接
│   ├── models.py           # 数据库模型
│   ├── schemas.py          # Pydantic schemas
│   ├── main.py             # FastAPI 应用入口
│   ├── middleware/         # 中间件
│   │   └── auth.py        # JWT 认证
│   ├── routes/            # API 路由
│   │   ├── products.py    # 产品 API
│   │   ├── internal.py    # 内部 API
│   │   └── health.py      # 健康检查
│   └── services/          # 业务逻辑层
│       ├── product_service.py
│       └── s3_service.py
├── tests/                 # 单元测试
├── requirements.txt       # Python 依赖
├── Dockerfile            # Docker 配置
└── .env.example          # 环境变量示例

## API 端点

### 公开 API (需要登录)

- `GET /api/products` - 获取产品列表
- `GET /api/products/{id}` - 获取产品详情

### 管理员 API

- `POST /api/products` - 创建产品
- `PUT /api/products/{id}` - 更新产品
- `DELETE /api/products/{id}` - 删除产品 (软删除)
- `POST /api/products/{id}/image` - 上传产品图片

### 内部 API (服务间调用)

- `GET /internal/products/{id}` - 内部查询产品

### 健康检查

- `GET /health` - 健康检查

## 环境变量

参见 `.env.example` 文件。

主要配置项:
- `DATABASE_URL`: PostgreSQL 连接字符串
- `AUTH_SERVICE_URL`: 认证服务地址
- `S3_BUCKET`: S3 存储桶名称
- `AWS_REGION`: AWS 区域

## 运行测试

```bash
# 安装依赖
pip install -r requirements.txt

# 运行所有测试
pytest

# 运行测试并显示覆盖率
pytest --cov=app tests/
```

## Docker 部署

```bash
# 构建镜像
docker build -t products-service .

# 运行容器
docker run -p 8001:8001 \
  -e DATABASE_URL=postgresql://... \
  -e AUTH_SERVICE_URL=http://... \
  products-service
```

## 开发

```bash
# 安装依赖
pip install -r requirements.txt

# 运行开发服务器
uvicorn app.main:app --reload --port 8001
```

## 设计文档

详细的设计文档位于 `design/` 目录:
- `functional-design.md` - 功能设计
- `infrastructure-design.md` - 基础设施设计
- `nfr-design.md` - 非功能需求

## 架构

该服务遵循分层架构:
1. **路由层** (`routes/`) - 处理 HTTP 请求
2. **服务层** (`services/`) - 业务逻辑
3. **数据访问层** (`models.py`, `database.py`) - 数据持久化

## 错误代码

- `400 INVALID_FILE_TYPE` - 不支持的文件类型
- `400 FILE_TOO_LARGE` - 文件超过 5MB
- `401 UNAUTHORIZED` - 未登录
- `403 FORBIDDEN` - 权限不足
- `404 PRODUCT_NOT_FOUND` - 产品不存在
