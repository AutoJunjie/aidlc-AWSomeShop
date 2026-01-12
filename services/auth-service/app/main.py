from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys
from contextlib import asynccontextmanager

from app.config import settings
from app.database import init_db, check_db_connection
from app.routers import auth_router
from app.schemas import HealthResponse

# 配置日志
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    logger.info("Starting auth-service...")
    try:
        init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        # 不阻止应用启动，但记录错误
    
    yield
    
    # 关闭时执行
    logger.info("Shutting down auth-service...")


# 创建 FastAPI 应用
app = FastAPI(
    title="Auth Service",
    description="Authentication and Authorization Service for AWSomeShop",
    version="1.0.0",
    lifespan=lifespan
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth_router.router)


@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check():
    """
    健康检查端点
    
    Returns:
        HealthResponse: 服务和数据库状态
    """
    db_status = "connected" if check_db_connection() else "disconnected"
    return HealthResponse(
        status="healthy" if db_status == "connected" else "unhealthy",
        database=db_status
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理器"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error_code": "INTERNAL_ERROR",
            "message": "Internal server error",
            "detail": str(exc) if settings.log_level == "DEBUG" else None
        }
    )


@app.get("/", tags=["root"])
async def root():
    """根路径"""
    return {
        "service": "auth-service",
        "version": "1.0.0",
        "status": "running"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
