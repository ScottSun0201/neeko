"""
赛牛客服平台API客户端
"""
import httpx
from typing import Dict, Any, Optional
from app.common.config.chatwork_config import settings
from app.common.utils.logger import logger


class SainiuClient:
    """赛牛API客户端"""

    def __init__(self):
        self.base_url = settings.SAINIU_BASE_URL
        self.api_key = settings.SAINIU_API_KEY

    async def async_httpcall(self, method: str, params: str = "{}") -> Dict[str, Any]:
        """
        异步HTTP调用赛牛API

        Args:
            method: API方法名(如 GetNewNews, SendMessages等)
            params: JSON参数字符串

        Returns:
            API响应数据
        """
        try:
            url = f"{self.base_url}/api/{method}"
            headers = {
                "Content-Type": "application/json",
            }

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    url,
                    content=params,
                    headers=headers
                )
                response.raise_for_status()

                # 解析响应
                result = response.json() if response.text else {}
                logger.debug(f"赛牛API调用成功: {method}")
                return result

        except Exception as e:
            logger.error(f"赛牛API调用失败 {method}: {str(e)}")
            return {}

    async def async_functioncall(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        异步函数调用(传入字典参数)

        Args:
            method: API方法名
            params: 参数字典

        Returns:
            API响应数据
        """
        import json
        params_str = json.dumps(params, ensure_ascii=False)
        return await self.async_httpcall(method, params_str)

    async def get_new_news(self) -> Dict[str, Any]:
        """获取新消息"""
        return await self.async_httpcall("GetNewNews", "{}")

    async def send_messages(
        self,
        user_nick: str,
        buyer_nick: str,
        text: str,
        siteid: str = "cntaobao",
        waiting_time: int = 3000
    ) -> Dict[str, Any]:
        """
        发送消息给买家

        Args:
            user_nick: 客服昵称
            buyer_nick: 买家昵称
            text: 消息内容
            siteid: 站点ID
            waiting_time: 等待时间(毫秒)

        Returns:
            发送结果
        """
        params = {
            "userNick": user_nick,
            "buyerNick": buyer_nick,
            "text": text,
            "siteid": siteid,
            "waitingTime": waiting_time,
        }
        return await self.async_functioncall("SendMessages", params)

    async def get_reception_group(self, user_nick: str) -> Dict[str, Any]:
        """获取接待分组"""
        params = {"userNick": user_nick}
        return await self.async_functioncall("GetReceptionGroup", params)

    async def transfer_buyer_to_groups(
        self,
        user_nick: str,
        buyer_nick: str,
        group_name: str
    ) -> Dict[str, Any]:
        """
        转接买家到分组

        Args:
            user_nick: 客服昵称
            buyer_nick: 买家昵称
            group_name: 分组名称

        Returns:
            转接结果
        """
        params = {
            "userNick": user_nick,
            "buyerNick": buyer_nick,
            "groupName": group_name,
        }
        return await self.async_functioncall("TransferBuyerToGroups", params)

    async def transfer_buyer_nick(
        self,
        user_nick: str,
        buyer_nick: str,
        target_nick: str
    ) -> Dict[str, Any]:
        """
        转接买家到指定客服

        Args:
            user_nick: 当前客服昵称
            buyer_nick: 买家昵称
            target_nick: 目标客服昵称

        Returns:
            转接结果
        """
        params = {
            "userNick": user_nick,
            "buyerNick": buyer_nick,
            "targetNick": target_nick,
        }
        return await self.async_functioncall("TransferBuyerNick", params)
