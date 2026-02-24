"""
Redis客户端连接
"""
import redis.asyncio as aioredis
from app.common.config.chatwork_config import settings
from app.common.utils.logger import logger

# 创建Redis连接池
redis_pool = None


async def get_redis_client():
    """获取Redis异步客户端"""
    global redis_pool
    if redis_pool is None:
        redis_pool = aioredis.ConnectionPool(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
            db=settings.REDIS_DB,
            decode_responses=True,
            max_connections=100,
        )
    return aioredis.Redis(connection_pool=redis_pool)


async def close_redis():
    """关闭Redis连接池"""
    global redis_pool
    if redis_pool:
        await redis_pool.disconnect()
        redis_pool = None
        logger.info("Redis连接池已关闭")
