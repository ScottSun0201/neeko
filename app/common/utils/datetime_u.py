"""
日期时间工具类
"""
from datetime import datetime, timedelta
import pytz


def get_current_time() -> datetime:
    """获取当前时间(上海时区)"""
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.now(tz)


def get_current_timestamp() -> float:
    """获取当前时间戳"""
    return datetime.now().timestamp()


def get_current_date_str() -> str:
    """获取当前日期字符串 YYYY-MM-DD"""
    return get_current_time().strftime("%Y-%m-%d")


def get_current_datetime_str() -> str:
    """获取当前日期时间字符串 YYYY-MM-DD HH:MM:SS"""
    return get_current_time().strftime("%Y-%m-%d %H:%M:%S")


def timestamp_to_datetime(timestamp: float) -> datetime:
    """时间戳转datetime对象"""
    return datetime.fromtimestamp(timestamp)


def datetime_to_str(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """datetime对象转字符串"""
    return dt.strftime(fmt)


def str_to_datetime(date_str: str, fmt: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """字符串转datetime对象"""
    return datetime.strptime(date_str, fmt)
