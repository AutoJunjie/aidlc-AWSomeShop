# Products Service - Infrastructure Design

## 1. Container

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ ./app/
EXPOSE 8001
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

---

## 2. Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: products-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: products-service
  template:
    spec:
      containers:
      - name: products-service
        image: awsomeshop/products-service:latest
        ports:
        - containerPort: 8001
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: products-service
spec:
  selector:
    app: products-service
  ports:
  - port: 8001
```

---

## 3. Database

- 使用共享 PostgreSQL 实例
- Schema: `products_schema`
- 连接池: 最大10连接

---

## 4. S3 Configuration

- Bucket: `awsomeshop-products`
- 公开读取策略
- 生命周期: 无过期

---

## 5. Service Port

| 服务 | 端口 |
|------|------|
| Products Service | 8001 |
