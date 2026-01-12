# Auth Service - Deployment Architecture

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Host                           │
│  ┌─────────────────────────────────────────────────┐    │
│  │            awsomeshop-network                    │    │
│  │                                                  │    │
│  │  ┌──────────────┐       ┌──────────────┐        │    │
│  │  │ auth-service │       │      db      │        │    │
│  │  │   :8001      │──────▶│    :5432     │        │    │
│  │  │  (FastAPI)   │       │ (PostgreSQL) │        │    │
│  │  └──────────────┘       └──────────────┘        │    │
│  │         │                      │                │    │
│  └─────────│──────────────────────│────────────────┘    │
│            │                      │                      │
│       port:8001              volume:postgres_data        │
└────────────│──────────────────────────────────────────────┘
             │
        localhost:8001
```

---

## Docker Compose Service Definition

```yaml
# Auth Service portion of docker-compose.yml
services:
  auth-service:
    build:
      context: ./services/auth-service
      dockerfile: Dockerfile
    ports:
      - "8001:8001"
    environment:
      - DATABASE_URL=postgresql+asyncpg://awsomeshop:${DB_PASSWORD}@db:5432/awsomeshop
      - JWT_SECRET=${JWT_SECRET}
      - JWT_EXPIRE_HOURS=24
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped
    networks:
      - awsomeshop-network
```

---

## Shared Infrastructure (All Services)

```yaml
# Shared portion of docker-compose.yml
services:
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=awsomeshop
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=awsomeshop
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U awsomeshop"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - awsomeshop-network

volumes:
  postgres_data:

networks:
  awsomeshop-network:
    driver: bridge
```

---

## Environment File (.env)

```
DB_PASSWORD=your-secure-password
JWT_SECRET=your-jwt-secret-key
```

---

## Port Allocation

| Service | Internal Port | External Port |
|---------|---------------|---------------|
| auth-service | 8001 | 8001 |
| products-service | 8002 | 8002 |
| points-service | 8003 | 8003 |
| redemptions-service | 8004 | 8004 |
| frontend | 3000 | 3000 |
| db | 5432 | - (internal only) |
