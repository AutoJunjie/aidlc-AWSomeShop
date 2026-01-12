# Products Service - NFR Design

## 1. Performance

| 指标 | 目标 |
|------|------|
| API 响应时间 | < 200ms (P95) |
| 图片上传 | < 3s (5MB文件) |
| 并发支持 | 100-500 用户 |

---

## 2. Security

### 认证
- JWT Token 验证 (调用 Auth Service)
- Admin 操作需要 role=admin

### S3 安全
- 使用 IAM Role 访问 S3
- 图片设置为公开读取

---

## 3. Configuration

| 环境变量 | 说明 | 示例 |
|----------|------|------|
| DATABASE_URL | PostgreSQL连接 | postgresql://... |
| AUTH_SERVICE_URL | Auth服务地址 | http://auth:8000 |
| S3_BUCKET | S3桶名 | awsomeshop-products |
| AWS_REGION | AWS区域 | us-east-1 |

---

## 4. Health Check

- **Endpoint**: GET /health
- **检查项**: 数据库连接, S3连接

---

## 5. Logging

- 格式: JSON
- 级别: INFO (生产), DEBUG (开发)
- 记录: 请求ID, 用户ID, 操作类型
