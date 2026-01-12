# Auth Service - Infrastructure Design

## Deployment Model
- **Container Runtime**: Docker
- **Orchestration**: Docker Compose
- **Environment**: Local development / Single server

---

## Container Configuration

### Auth Service Container
| Property | Value |
|----------|-------|
| Base Image | python:3.11-slim |
| Port | 8001 |
| Healthcheck | GET /health |
| Restart Policy | unless-stopped |

### Environment Variables
| Variable | Description | Example |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL 连接串 | postgresql+asyncpg://user:pass@db:5432/awsomeshop |
| JWT_SECRET | JWT 签名密钥 | random-secret-key |
| JWT_EXPIRE_HOURS | Token 有效期 | 24 |

---

## Database Infrastructure

### PostgreSQL Container
| Property | Value |
|----------|-------|
| Image | postgres:15-alpine |
| Port | 5432 |
| Volume | postgres_data:/var/lib/postgresql/data |

### Database Configuration
| Variable | Value |
|----------|-------|
| POSTGRES_USER | awsomeshop |
| POSTGRES_PASSWORD | (from .env) |
| POSTGRES_DB | awsomeshop |

---

## Network Configuration

| Network | Purpose |
|---------|---------|
| awsomeshop-network | 服务间通信 |

### Service Discovery
- 使用 Docker Compose 内置 DNS
- 服务名即主机名 (auth-service, db)

---

## Dockerfile Specification

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
```
