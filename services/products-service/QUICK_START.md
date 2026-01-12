# Products Service - Quick Start Guide

## Prerequisites

- Python 3.11+
- Docker & Docker Compose
- PostgreSQL (or use Docker Compose)

## Running Unit Tests

### Install Dependencies

```bash
cd services/products-service
pip install -r requirements.txt
```

### Run All Tests

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run tests with coverage report
pytest tests/ -v --cov=app --cov-report=html

# Run specific test file
pytest tests/test_product_service.py -v

# Run tests matching pattern
pytest tests/ -k "test_create" -v
```

### Expected Test Results

- Total: 96 test functions
- All tests should pass
- Coverage should be > 90%

## Running with Docker Compose

### Start All Services

```bash
# From repository root
cd /projects/sandbox/aidlc-AWSomeShop

# Start services
docker-compose up -d

# View logs
docker-compose logs -f products-service

# Check service status
docker-compose ps
```

### Verify Service is Running

```bash
# Check health
curl http://localhost:8001/health

# Expected response:
# {"status":"healthy","database":true,"s3":true}

# Check root endpoint
curl http://localhost:8001/

# Expected response:
# {"service":"Products Service","version":"1.0.0","status":"running"}
```

### Stop Services

```bash
docker-compose down

# Remove volumes (clean slate)
docker-compose down -v
```

## Running Without Docker Compose

### Start PostgreSQL

```bash
docker run -d \
  --name postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=awsomeshop \
  -p 5432:5432 \
  postgres:15-alpine
```

### Configure Environment

```bash
cd services/products-service
cp .env.example .env

# Edit .env and configure:
# - DATABASE_URL
# - AUTH_SERVICE_URL (if available)
# - S3_BUCKET, AWS_REGION, AWS credentials
```

### Run Development Server

```bash
uvicorn app.main:app --reload --port 8001
```

### Access API Documentation

```bash
# Swagger UI
open http://localhost:8001/docs

# ReDoc
open http://localhost:8001/redoc
```

## Testing API Endpoints

### Public Endpoints (Require Authentication)

```bash
# Get products list
curl -H "Authorization: Bearer <token>" \
  http://localhost:8001/api/products

# Get product by ID
curl -H "Authorization: Bearer <token>" \
  http://localhost:8001/api/products/1
```

### Admin Endpoints (Require Admin Role)

```bash
# Create product
curl -X POST \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Product","points_cost":100}' \
  http://localhost:8001/api/products

# Update product
curl -X PUT \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Updated Name"}' \
  http://localhost:8001/api/products/1

# Upload image
curl -X POST \
  -H "Authorization: Bearer <admin_token>" \
  -F "file=@image.jpg" \
  http://localhost:8001/api/products/1/image

# Delete product
curl -X DELETE \
  -H "Authorization: Bearer <admin_token>" \
  http://localhost:8001/api/products/1
```

### Internal Endpoints (No Authentication)

```bash
# Get product (internal)
curl http://localhost:8001/internal/products/1
```

## Troubleshooting

### Database Connection Issues

```bash
# Check if database is running
docker ps | grep postgres

# Check database logs
docker logs awsomeshop-db

# Connect to database
docker exec -it awsomeshop-db psql -U postgres -d awsomeshop
```

### Service Not Starting

```bash
# Check service logs
docker-compose logs products-service

# Common issues:
# - Database not ready: Wait for DB health check
# - Port conflict: Change port in docker-compose.yml
# - Environment variables: Check .env or docker-compose.yml
```

### Tests Failing

```bash
# Ensure dependencies are installed
pip install -r requirements.txt

# Run with verbose output to see details
pytest tests/ -v -s

# Check specific failing test
pytest tests/test_product_service.py::TestProductService::test_create_product -v
```

## Development Workflow

1. **Make changes** to code in `app/`
2. **Write tests** in `tests/`
3. **Run tests**: `pytest tests/ -v`
4. **Check syntax**: `python3 -m py_compile app/*.py`
5. **Build Docker**: `docker build -t products-service .`
6. **Test with compose**: `docker-compose up -d`
7. **Verify**: `curl http://localhost:8001/health`

## Additional Resources

- Design Documentation: `design/` directory
- API Documentation: http://localhost:8001/docs (when running)
- FastAPI Docs: https://fastapi.tiangolo.com/
- PostgreSQL Docs: https://www.postgresql.org/docs/
- Boto3 S3 Docs: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
