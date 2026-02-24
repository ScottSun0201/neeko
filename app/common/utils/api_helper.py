"""
API辅助类
"""
import json
import httpx
from typing import Optional, Dict, Any
from app.redis.redis_client import get_redis_client
from app.common.utils.logger import logger


class ExpiringArray:
    """
    基于Redis的带过期时间的会话ID存储
    用于管理Dify会话ID
    """
    prefix = "expiring_array:"

    @classmethod
    async def add(cls, username: str, item: str, expire_time: int = 86400):
        """
        添加会话ID

        Args:
            username: 用户名(如: {buyerUid}_{nicker})
            item: conversation_id
            expire_time: 过期时间(秒)，默认24小时
        """
        try:
            redis = await get_redis_client()
            key = f"{cls.prefix}{username}"
            await redis.setex(key, expire_time, json.dumps(item))
            logger.debug(f"会话ID已存储: {username} -> {item}")
        except Exception as e:
            logger.error(f"存储会话ID失败: {str(e)}")

    @classmethod
    async def get_valid_items(cls, username: Optional[str] = None) -> Any:
        """
        获取有效的会话ID

        Args:
            username: 指定用户名，返回该用户的conversation_id；
                     不指定则返回所有有效会话 {username: conversation_id}

        Returns:
            conversation_id 或 {username: conversation_id} 字典
        """
        try:
            redis = await get_redis_client()

            if username:
                # 获取指定用户的会话ID
                key = f"{cls.prefix}{username}"
                value = await redis.get(key)
                if value:
                    return json.loads(value)
                return ""
            else:
                # 获取所有有效会话
                pattern = f"{cls.prefix}*"
                keys = await redis.keys(pattern)
                result = {}
                for key in keys:
                    value = await redis.get(key)
                    if value:
                        username = key.replace(cls.prefix, "")
                        result[username] = json.loads(value)
                return result

        except Exception as e:
            logger.error(f"获取会话ID失败: {str(e)}")
            return "" if username else {}


class APIHelper:
    """
    HTTP API调用辅助类
    """

    @staticmethod
    async def post_json(
        url: str,
        data: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
        timeout: float = 30.0
    ) -> Dict[str, Any]:
        """
        POST请求发送JSON数据

        Args:
            url: 请求URL
            data: JSON数据
            headers: 请求头
            timeout: 超时时间(秒)

        Returns:
            响应JSON数据
        """
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(url, json=data, headers=headers)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"POST请求失败 {url}: {str(e)}")
            raise

    @staticmethod
    async def get_json(
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: float = 30.0
    ) -> Dict[str, Any]:
        """
        GET请求获取JSON数据

        Args:
            url: 请求URL
            params: 查询参数
            headers: 请求头
            timeout: 超时时间(秒)

        Returns:
            响应JSON数据
        """
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(url, params=params, headers=headers)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"GET请求失败 {url}: {str(e)}")
            raise
