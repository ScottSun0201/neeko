"""
FastAPI主应用入口
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.common.config.chatwork_config import settings
from app.common.utils.logger import logger
from app.db.database import init_db
from app.redis.redis_client import close_redis
from app.task.scheduler import start_scheduler, stop_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    logger.info("Neeko智能客服系统正在启动...")

    # 初始化数据库
    await init_db()
    logger.info("数据库初始化完成")

    # 启动定时任务
    start_scheduler()

    logger.info("系统启动完成")

    yield

    # 关闭时
    logger.info("系统正在关闭...")

    # 停止定时任务
    stop_scheduler()

    # 关闭Redis连接
    await close_redis()

    logger.info("系统已关闭")


# 创建FastAPI应用
app = FastAPI(
    title="Neeko 智能客服系统",
    description="基于AI的电商智能客服系统",
    version="1.0.0",
    lifespan=lifespan,
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 导入路由
from app.api import user_api, product, debug, openapi

# 注册路由
app.include_router(user_api.router, prefix="/users", tags=["用户"])
app.include_router(product.router, prefix="/product", tags=["产品"])
app.include_router(debug.router, prefix="/debug", tags=["调试"])
app.include_router(openapi.router, prefix="/openapi", tags=["开放API"])


@app.get("/ping")
async def ping():
    """健康检查"""
    return {"message": "pong"}


@app.get("/")
async def root():
    """根路径"""
    return {
        "name": "Neeko 智能客服系统",
        "version": "1.0.0",
        "status": "running",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.api.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.ENVIRONMENT == "development",
    )
