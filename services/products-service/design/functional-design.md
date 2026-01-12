# Products Service - Functional Design

## 1. Service Overview

Products Service 负责产品信息管理，包括 CRUD 操作和图片上传到 S3。

### 技术栈
- Python FastAPI
- PostgreSQL
- AWS S3 (boto3)

---

## 2. Data Model

### Product Entity

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | int | PK, 自增 | 主键 |
| name | varchar(100) | NOT NULL | 产品名称 |
| description | varchar(1000) | - | 产品描述 |
| points_cost | int | NOT NULL, >0 | 所需积分 |
| image_url | varchar(500) | - | 图片URL |
| is_active | bool | DEFAULT TRUE | 是否上架 |
| created_at | timestamp | DEFAULT NOW | 创建时间 |
| updated_at | timestamp | DEFAULT NOW | 更新时间 |

---

## 3. API Endpoints

### Public APIs (需登录)

| Method | Endpoint | 权限 | 说明 |
|--------|----------|------|------|
| GET | /api/products | User | 获取产品列表 |
| GET | /api/products/{id} | User | 获取产品详情 |

### Admin APIs

| Method | Endpoint | 权限 | 说明 |
|--------|----------|------|------|
| POST | /api/products | Admin | 创建产品 |
| PUT | /api/products/{id} | Admin | 更新产品 |
| DELETE | /api/products/{id} | Admin | 删除产品(软删除) |
| POST | /api/products/{id}/image | Admin | 上传图片 |

### Internal API (服务间调用)

| Method | Endpoint | 说明 |
|--------|----------|------|
| GET | /internal/products/{id} | 内部查询产品 |

---

## 4. API Details

### GET /api/products
**Query**: `?is_active=true`  
**Response**:
```json
{"products": [{"id": 1, "name": "...", "points_cost": 100, "image_url": "...", "is_active": true}]}
```

### POST /api/products
**Request**:
```json
{"name": "AWS杯", "description": "限量版", "points_cost": 100}
```
**Validation**: name(1-100字符), points_cost(正整数)

### POST /api/products/{id}/image
**Request**: multipart/form-data, file字段  
**限制**: jpeg/png/webp, 最大5MB  
**S3路径**: `products/{product_id}/{timestamp}.{ext}`

---

## 5. Business Rules

- 产品删除采用软删除 (is_active=false)
- 图片上传到 S3，返回公开 URL
- 积分成本必须为正整数

---

## 6. Dependencies

- **依赖**: Auth Service (JWT验证)
- **被依赖**: Redemptions Service (查询产品)

---

## 7. Error Codes

| Code | Error | 说明 |
|------|-------|------|
| 400 | INVALID_FILE_TYPE | 文件类型不支持 |
| 400 | FILE_TOO_LARGE | 文件超过5MB |
| 401 | UNAUTHORIZED | 未登录 |
| 403 | FORBIDDEN | 非管理员 |
| 404 | PRODUCT_NOT_FOUND | 产品不存在 |
