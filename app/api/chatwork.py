"""
消息处理核心模块
"""
import uuid
from typing import Dict, Any, Optional
from app.libs.sainiuclient import SainiuClient
from app.common.utils.logger import logger
from app.common.utils.redis_util import handle_sainiu_message, check_inactive_users
from app.common.utils.qnapi_helper import parse_response
from app.common.config.chatwork_config import INFO_TYPE_DICT_CN


async def check_new_info_data():
    """
    拉取赛牛新消息并处理
    """
    try:
        # 优先检查非活跃用户
        inactive_data = await check_inactive_users()
        if inactive_data:
            logger.info("处理非活跃用户消息")
            await process_message(inactive_data)
            return

        # 拉取新消息
        client = SainiuClient()
        response = await client.get_new_news()

        # 解析响应
        data = parse_response(response)
        if not data:
            return

        # 消息去重
        if not await handle_sainiu_message(data):
            return

        # 处理消息
        await process_message(data)

    except Exception as e:
        logger.error(f"拉取消息失败: {str(e)}")


async def process_message(data: Dict[str, Any]):
    """
    处理单条消息

    Args:
        data: 消息数据
    """
    try:
        message_type = data.get("type", "")
        message_id = data.get("messageId", "")

        logger.info(f"处理消息: {message_id}, 类型: {message_type}")

        # 预处理
        processed_data = await preprocess_info(data)
        if not processed_data:
            logger.info(f"消息被过滤: {message_id}")
            return

        # 调用AI处理(简化版)
        logger.info(f"消息处理完成: {message_id}")

    except Exception as e:
        logger.error(f"处理消息失败: {str(e)}")


async def preprocess_info(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    消息预处理

    Args:
        data: 原始消息数据

    Returns:
        预处理后的数据或None(被过滤)
    """
    try:
        message_type = data.get("type", "")
        message = data.get("message", "")
        code_type = data.get("codeType", "")

        # 过滤非用户消息
        if code_type != "CHAT_RECEIVE_MSG":
            return None

        # 过滤系统消息
        if "将为您服务" in message:
            return None

        if "转交给" in message and "wsy" in message:
            return None

        # 生成TraceID
        trace_id = str(uuid.uuid4())
        data["trace_id"] = trace_id

        # 根据消息类型处理
        if message_type == "文本消息":
            return await preprocess_text(data)
        elif message_type == "图片消息":
            return await preprocess_image(data)
        elif message_type == "视频消息":
            data["message"] = "转接人工"
            return data
        else:
            return data

    except Exception as e:
        logger.error(f"消息预处理失败: {str(e)}")
        return None


async def preprocess_text(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    文本消息预处理

    Args:
        data: 消息数据

    Returns:
        处理后的数据
    """
    logger.debug(f"文本消息预处理: {data.get('messageId')}")
    # 文本消息直接返回
    return data


async def preprocess_image(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    图片消息预处理

    Args:
        data: 消息数据

    Returns:
        处理后的数据
    """
    try:
        image_url = data.get("message", "")
        logger.info(f"图片消息预处理: {image_url}")

        # TODO: 实际图片处理流程
        # 1. 下载图片
        # 2. 上传到Dify
        # 3. YOLO分类
        # 4. OCR识别
        # 5. 缓存结果到Redis

        # 占位实现
        data["product"] = "DZ120V1D"
        data["producttype"] = "Compressor"

        return data

    except Exception as e:
        logger.error(f"图片预处理失败: {str(e)}")
        return data
