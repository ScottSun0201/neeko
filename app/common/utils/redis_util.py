"""
Redis工具函数
"""
from typing import Optional, Dict, Any, List
from app.redis.redis_client import get_redis_client
from app.common.utils.logger import logger
from app.common.utils.datetime_u import get_current_date_str


async def handle_sainiu_message(res_data: Dict[str, Any]) -> bool:
    """
    消息去重处理

    Args:
        res_data: 赛牛消息数据

    Returns:
        True表示新消息可处理，False表示重复消息跳过
    """
    try:
        redis = await get_redis_client()
        buyer_uid = res_data.get("buyerUid", "")
        login_id = res_data.get("loginId", "")
        timestamp = res_data.get("time", "")

        # 生成去重Key
        dedup_key = f"{buyer_uid}_{login_id}_{timestamp}"

        # 检查是否存在
        exists = await redis.exists(dedup_key)
        if exists:
            logger.info(f"重复消息被过滤: {dedup_key}")
            return False

        # 写入Redis，TTL 24小时
        await redis.setex(dedup_key, 86400, "1")
        return True

    except Exception as e:
        logger.error(f"消息去重处理失败: {str(e)}")
        return True  # 出错时默认允许处理


async def set_active_user(user_key: str, ttl: int = 20):
    """
    设置活跃用户标记

    Args:
        user_key: 用户标识
        ttl: 过期时间(秒)
    """
    try:
        redis = await get_redis_client()
        active_key = f"active_user:&&{user_key}&&last_active"

        # 设置活跃标记
        await redis.setex(active_key, ttl, "1")

        # 添加到活跃用户集合
        await redis.sadd("active_user", active_key)

        logger.debug(f"用户活跃标记已设置: {user_key}")

    except Exception as e:
        logger.error(f"设置活跃用户失败: {str(e)}")


async def check_inactive_users() -> Optional[Dict[str, Any]]:
    """
    检查非活跃用户（20秒未发消息）

    Returns:
        非活跃用户数据或None
    """
    try:
        redis = await get_redis_client()

        # 获取所有活跃用户Key
        active_keys = await redis.smembers("active_user")

        for key in active_keys:
            # 检查Key是否过期
            exists = await redis.exists(key)
            if not exists:
                # 用户已非活跃
                # 提取用户标识
                user_key = key.replace("active_user:&&", "").replace("&&last_active", "")

                # 读取初始数据
                initial_data_key = f"one@{user_key}"
                initial_data = await redis.hgetall(initial_data_key)

                if initial_data:
                    # 删除活跃标记
                    await redis.srem("active_user", key)

                    logger.info(f"检测到非活跃用户: {user_key}")
                    return initial_data

        return None

    except Exception as e:
        logger.error(f"检查非活跃用户失败: {str(e)}")
        return None


async def get_handle_zj_message(key: str) -> bool:
    """
    检查是否已转接人工

    Args:
        key: 用户标识

    Returns:
        True表示已转接，False表示未转接
    """
    try:
        redis = await get_redis_client()
        zj_key = f"ai_zj_{key}"
        exists = await redis.exists(zj_key)
        return bool(exists)

    except Exception as e:
        logger.error(f"检查转接标记失败: {str(e)}")
        return False


async def set_handle_zj_message(key: str, ttl: int = 200):
    """
    设置转接人工标记

    Args:
        key: 用户标识
        ttl: 过期时间(秒)，默认200秒
    """
    try:
        redis = await get_redis_client()
        zj_key = f"ai_zj_{key}"
        await redis.setex(zj_key, ttl, "1")
        logger.info(f"转接标记已设置: {key}, TTL={ttl}s")

    except Exception as e:
        logger.error(f"设置转接标记失败: {str(e)}")


async def sadd_redis(key: str, value: str):
    """添加到Redis Set"""
    try:
        redis = await get_redis_client()
        await redis.sadd(key, value)
    except Exception as e:
        logger.error(f"Redis SADD失败: {str(e)}")


async def rpush_redis(key: str, value: str):
    """添加到Redis List"""
    try:
        redis = await get_redis_client()
        await redis.rpush(key, value)
    except Exception as e:
        logger.error(f"Redis RPUSH失败: {str(e)}")


async def lpush_redis(key: str, value: str):
    """从左侧添加到Redis List"""
    try:
        redis = await get_redis_client()
        await redis.lpush(key, value)
    except Exception as e:
        logger.error(f"Redis LPUSH失败: {str(e)}")


async def lrange_redis(key: str, start: int = 0, end: int = -1) -> List[str]:
    """获取Redis List范围数据"""
    try:
        redis = await get_redis_client()
        return await redis.lrange(key, start, end)
    except Exception as e:
        logger.error(f"Redis LRANGE失败: {str(e)}")
        return []


async def delete_redis_keys(pattern: str):
    """删除匹配的Redis Keys"""
    try:
        redis = await get_redis_client()
        keys = await redis.keys(pattern)
        if keys:
            await redis.delete(*keys)
    except Exception as e:
        logger.error(f"Redis DELETE失败: {str(e)}")
