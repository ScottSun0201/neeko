"""
数据解析工具
"""
import json
import re
from typing import Dict, Any, Optional
from app.common.utils.logger import logger


def safe_json_loads(data: str, default: Any = None) -> Any:
    """安全的JSON解析"""
    try:
        return json.loads(data)
    except Exception as e:
        logger.warning(f"JSON解析失败: {str(e)}")
        return default or {}


def extract_url(text: str) -> Optional[str]:
    """从文本中提取URL"""
    pattern = r'(https?://[^\s]+)'
    match = re.search(pattern, text)
    return match.group(1) if match else None


def is_url(text: str) -> bool:
    """判断文本是否包含URL"""
    pattern = r'https?://[^\s]+'
    return bool(re.search(pattern, text))


def clean_special_chars(text: str) -> str:
    """清理特殊字符"""
    if not text:
        return ""
    # 去除首尾非字母数字字符
    text = re.sub(r'^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$', '', text)
    return text.strip()
