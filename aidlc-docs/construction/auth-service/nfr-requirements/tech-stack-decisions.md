# Auth Service - Tech Stack Decisions

## Runtime & Framework

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Language | Python 3.11+ | 项目需求指定 |
| Framework | FastAPI | 项目需求指定，高性能异步框架 |
| ASGI Server | Uvicorn | FastAPI 推荐，生产级性能 |

---

## Security Libraries

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Password Hashing | bcrypt (passlib) | 行业标准，cost=12 |
| JWT | python-jose | 成熟稳定，支持 HS256 |
| Validation | Pydantic | FastAPI 内置，类型安全 |

---

## Database

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Database | PostgreSQL | 项目需求指定 |
| ORM | SQLAlchemy 2.0 | 异步支持，成熟生态 |
| Migration | Alembic | SQLAlchemy 配套工具 |
| Driver | asyncpg | 异步 PostgreSQL 驱动 |

---

## Dependencies Summary

```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
sqlalchemy[asyncio]>=2.0.0
asyncpg>=0.29.0
alembic>=1.12.0
passlib[bcrypt]>=1.7.4
python-jose[cryptography]>=3.3.0
pydantic>=2.5.0
pydantic-settings>=2.1.0
```

---

## Configuration

| Item | Source | Example |
|------|--------|---------|
| DATABASE_URL | Environment | postgresql+asyncpg://... |
| JWT_SECRET | Environment | 随机生成的密钥 |
| JWT_ALGORITHM | Code | HS256 |
| JWT_EXPIRE_HOURS | Environment | 24 |
| BCRYPT_ROUNDS | Code | 12 |
