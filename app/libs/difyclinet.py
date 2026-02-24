"""
Dify AI平台API客户端
"""
import json
import httpx
from typing import Dict, Any, Optional, List
from app.common.config.chatwork_config import settings
from app.common.utils.logger import logger


class DifyClient:
    """Dify API客户端"""

    def __init__(self, api_key: str):
        """
        初始化Dify客户端

        Args:
            api_key: Dify应用API Key
        """
        self.base_url = settings.DIFY_BASE_URL
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    async def send_chat_message_async(
        self,
        query: str,
        user: str,
        inputs: Optional[Dict[str, Any]] = None,
        conversation_id: str = "",
        files: Optional[List[Dict[str, str]]] = None,
        response_mode: str = "streaming"
    ) -> Dict[str, Any]:
        """
        发送聊天消息(异步)

        Args:
            query: 用户查询内容
            user: 用户标识
            inputs: 输入变量
            conversation_id: 会话ID(为空则创建新会话)
            files: 文件列表 [{"type": "image", "transfer_method": "remote_url", "url": "..."}]
            response_mode: 响应模式 streaming/blocking

        Returns:
            AI响应数据
        """
        try:
            url = f"{self.base_url}/chat-messages"

            payload = {
                "query": query or "这个",  # 空消息替换为"这个"
                "user": user,
                "inputs": inputs or {},
                "response_mode": response_mode,
            }

            if conversation_id:
                payload["conversation_id"] = conversation_id

            if files:
                payload["files"] = files

            async with httpx.AsyncClient(timeout=120.0) as client:
                if response_mode == "streaming":
                    # SSE流式响应
                    return await self._handle_streaming_response(client, url, payload)
                else:
                    # Blocking模式
                    response = await client.post(url, json=payload, headers=self.headers)
                    response.raise_for_status()
                    return response.json()

        except Exception as e:
            logger.error(f"Dify API调用失败: {str(e)}")
            return {}

    async def _handle_streaming_response(
        self,
        client: httpx.AsyncClient,
        url: str,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        处理SSE流式响应

        Args:
            client: HTTP客户端
            url: 请求URL
            payload: 请求数据

        Returns:
            完整的响应数据
        """
        try:
            answer = ""
            conversation_id = ""
            message_id = ""

            async with client.stream("POST", url, json=payload, headers=self.headers) as response:
                response.raise_for_status()

                async for line in response.aiter_lines():
                    if not line or not line.startswith("data: "):
                        continue

                    data_str = line[6:]  # 移除 "data: " 前缀
                    if data_str.strip() == "[DONE]":
                        break

                    try:
                        data = json.loads(data_str)
                        event = data.get("event", "")

                        if event == "agent_message":
                            answer += data.get("answer", "")

                        if "conversation_id" in data:
                            conversation_id = data["conversation_id"]

                        if "message_id" in data:
                            message_id = data["message_id"]

                    except json.JSONDecodeError:
                        continue

            return {
                "answer": answer,
                "conversation_id": conversation_id,
                "message_id": message_id,
            }

        except Exception as e:
            logger.error(f"处理SSE流失败: {str(e)}")
            return {}

    async def upload_file(
        self,
        file_path: str,
        user: str
    ) -> Optional[str]:
        """
        上传文件到Dify

        Args:
            file_path: 本地文件路径
            user: 用户标识

        Returns:
            文件ID(file_id)
        """
        try:
            url = f"{self.base_url}/files/upload"

            # 准备文件
            with open(file_path, 'rb') as f:
                files = {
                    'file': (file_path.split('/')[-1], f, 'image/jpeg')
                }
                data = {
                    'user': user
                }

                # 修改headers，移除Content-Type让httpx自动设置multipart
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                }

                async with httpx.AsyncClient(timeout=60.0) as client:
                    response = await client.post(url, files=files, data=data, headers=headers)
                    response.raise_for_status()

                    result = response.json()
                    file_id = result.get("id", "")
                    logger.info(f"文件上传成功: {file_id}")
                    return file_id

        except Exception as e:
            logger.error(f"文件上传失败 {file_path}: {str(e)}")
            return None
