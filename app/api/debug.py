"""
调试相关API
"""
from fastapi import APIRouter
from app.redis.redis_client import get_redis_client
from app.db.database import engine
from app.common.utils.logger import logger

router = APIRouter()


@router.get("/debug/redis")
async def check_redis():
    """检查Redis连接"""
    try:
        redis = await get_redis_client()
        await redis.ping()
        return {"status": "ok", "message": "Redis连接正常"}
    except Exception as e:
        logger.error(f"Redis连接失败: {str(e)}")
        return {"status": "error", "message": str(e)}


@router.get("/debug/mysql")
async def check_mysql():
    """检查MySQL连接"""
    try:
        async with engine.connect() as conn:
            result = await conn.execute("SELECT 1")
            return {"status": "ok", "message": "MySQL连接正常", "result": 1}
    except Exception as e:
        logger.error(f"MySQL连接失败: {str(e)}")
        return {"status": "error", "message": str(e)}
