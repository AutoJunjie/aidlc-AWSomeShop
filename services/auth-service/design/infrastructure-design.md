# Auth Service - Infrastructure Design

## Container

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Resource Limits
```yaml
resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "500m"
```

## Database

### PostgreSQL Schema
- Database: `awsomeshop`
- Schema: `auth` (或共享 public schema)
- Table: `users`

### Connection
```
postgresql://user:password@postgres:5432/awsomeshop
```

## Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: auth-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: auth-service
  template:
    spec:
      containers:
      - name: auth-service
        image: awsomeshop/auth-service:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        - name: JWT_SECRET
          valueFrom:
            secretKeyRef:
              name: jwt-secret
              key: secret
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

## Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: auth-service
spec:
  selector:
    app: auth-service
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP
```

## Local Development (docker-compose)

```yaml
auth-service:
  build: ./services/auth-service
  ports:
    - "8001:8000"
  environment:
    - DATABASE_URL=postgresql://postgres:postgres@db:5432/awsomeshop
    - JWT_SECRET=dev-secret-key
  depends_on:
    - db
```
