"""
日志系统配置
"""
import sys
from loguru import logger
from app.common.config.chatwork_config import settings

# 移除默认处理器
logger.remove()

# 添加控制台输出
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>",
    level=settings.LOG_LEVEL,
    colorize=True,
)

# 添加文件输出
logger.add(
    "./logs/neeko_{time:YYYY-MM-DD}.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
    level=settings.LOG_LEVEL,
    rotation="00:00",  # 每天午夜轮换
    retention="30 days",  # 保留30天
    compression="zip",  # 压缩旧日志
    encoding="utf-8",
)

# 添加错误日志单独文件
logger.add(
    "./logs/error_{time:YYYY-MM-DD}.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
    level="ERROR",
    rotation="00:00",
    retention="90 days",
    compression="zip",
    encoding="utf-8",
)

__all__ = ["logger"]
