"""
赛牛API响应解析助手
"""
import json
from typing import Dict, Any, Optional
from app.common.utils.logger import logger


def parse_response(response: Any) -> Dict[str, Any]:
    """
    解析赛牛API响应

    Args:
        response: 赛牛API原始响应

    Returns:
        解析后的字典数据
    """
    try:
        if isinstance(response, dict):
            return response
        elif isinstance(response, str):
            return json.loads(response) if response else {}
        else:
            return {}
    except Exception as e:
        logger.warning(f"解析赛牛响应失败: {str(e)}")
        return {}
