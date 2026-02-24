"""
智能客服系统 Neeko - 全局配置
"""
import os
from pathlib import Path
from typing import Dict, List
from pydantic_settings import BaseSettings

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Settings(BaseSettings):
    """系统配置"""

    # =============================================================================
    # 基础配置
    # =============================================================================
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_WORKERS: int = 4

    # =============================================================================
    # 数据库配置
    # =============================================================================
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "znkf_pro"
    DB_CHARSET: str = "utf8mb4"

    @property
    def DATABASE_URL(self) -> str:
        """数据库连接 URL"""
        return f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset={self.DB_CHARSET}"

    # =============================================================================
    # Redis 配置
    # =============================================================================
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6385
    REDIS_PASSWORD: str = ""
    REDIS_DB: int = 5

    # =============================================================================
    # 赛牛客服平台配置
    # =============================================================================
    SAINIU_BASE_URL: str = "http://192.168.1.103:3030"
    SAINIU_API_KEY: str = ""
    QN_TRANS_MODE: str = "Group"  # Group 或 Nick
    QN_TRANS_MESSAGE: str = "亲爱的，稍等给您转专席客服"

    # =============================================================================
    # Dify AI 平台配置
    # =============================================================================
    DIFY_BASE_URL: str = "https://api.dify.ai/v1"
    APP_KEY: str = ""  # 主对话引擎
    APP_KEY_TWO: str = ""  # 回复审核/优化
    APP_KEY_THREE: str = ""  # 备用对话引擎
    AUX_OFF_ON: bool = False  # 是否启用双模型模式

    # =============================================================================
    # 旺店通 ERP 配置
    # =============================================================================
    WDT_BASE_URL: str = "https://api.wangdian.com"
    WDT_APP_KEY: str = ""
    WDT_APP_SECRET: str = ""
    WDT_SID: str = ""

    # =============================================================================
    # Fluvio 消息流配置
    # =============================================================================
    FLUVIO_TOPIC: str = "chatwork-python"
    FLUVIO_BOOTSTRAP_SERVER: str = "localhost:9003"

    # =============================================================================
    # 图片存储路径
    # =============================================================================
    SOURCE_IMAGE_SAVE_PATH: str = "./source_photo/"
    RECOGNIZE_PHOTO: str = "./recognize_photo/"
    ERROR_IMAGE_SAVE_PATH: str = "./check_error/"

    # =============================================================================
    # 缓存配置
    # =============================================================================
    CACHE_DURATION: int = 20  # 秒

    # =============================================================================
    # Celery 配置
    # =============================================================================
    CELERY_BROKER_URL: str = "redis://localhost:6385/5"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6385/5"
    CELERY_TASK_SERIALIZER: str = "json"
    CELERY_RESULT_SERIALIZER: str = "json"
    CELERY_TIMEZONE: str = "Asia/Shanghai"
    CELERY_ENABLE_UTC: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


# 创建全局配置实例
settings = Settings()


# =============================================================================
# 消息类型映射
# =============================================================================
INFO_TYPE_DICT_CN: Dict[int, str] = {
    1: "文本消息",
    2: "图片消息",
    3: "视频消息",
    4: "语音消息",
    5: "文件消息",
    6: "链接消息",
    7: "其他消息",
}


# =============================================================================
# 产品类型映射（中文 -> 英文）
# =============================================================================
PRODUCT_TYPE_MAPPING: Dict[str, str] = {
    "压缩机": "Compressor",
    "主板": "Mainboard",
    "显示板": "Display Panel",
    "风机": "Fan",
    "冰箱": "Refrigerator",
    "洗衣机": "Washing Machine",
    "冰箱铭牌": "Refrigerator Nameplate",
    "洗衣机铭牌": "Washing Machine Nameplate",
    "玻璃": "Glass",
    "变频板": "InverterBoard",
    "排水泵": "Drain Pump",
    "风门": "Air Damper",
    "电热丝": "Heating wire",
    "加热管": "Defrost Heater",
    "传感器": "sensor",
    "LED灯条": "LED light strip",
    "冰箱门": "Refrigerator Door",
    "板子的背面": "the back of the board",
    "其他": "other",
    "快递单": "Express Bill",
    "订单": "Order",
    "洗衣机门锁": "washing machine door lock",
    "洗衣机电机": "washing machine motor",
    "保险管": "Insurance tube",
    "未知": "unknown",
}


# =============================================================================
# 需要转人工的产品分类
# =============================================================================
TRANSFER_PRODUCT_TYPES: List[str] = [
    "InverterBoard",  # 变频板
    "Drain Pump",  # 排水泵
    "Air Damper",  # 风门
    "Refrigerator Door",  # 冰箱门
    "Heating wire",  # 电热丝
    "sensor",  # 传感器
    "LED light strip",  # LED灯条
]


# =============================================================================
# 需要转人工的特殊分类
# =============================================================================
SPECIAL_TRANSFER_TYPES: List[str] = [
    "number",
    "Unlabeled",
    "AirDamper",
    "ExpressBill",
    "InverterBoard",
]


# =============================================================================
# 产品状态编码
# =============================================================================
PRODUCT_STATUS_MAPPING: Dict[str, str] = {
    "0": "原装",
    "1": "九成新",
    "2": "全新",
    "3": "原装九成新",
    "4": "拆机",
    "5": "无类型",
}


# =============================================================================
# 测试用户 ID（不触发转接和统计）
# =============================================================================
TEST_USER_IDS: List[str] = [
    "t_1514353800520_0314",
    "tb50918310",
]


# =============================================================================
# OCR 型号纠错映射表（27条规则）
# =============================================================================
OCR_CORRECTION_RULES: Dict[str, str] = {
    "DZ90X10": "DZ90X1D",
    "ASE520": "ASE52U",
    "B90M2SU1": "E90M2SU1",
    "MXA9C": "FMXA9C",
    "DZ90X18": "DZ90X1B",
    "EOOCY1": "L100CY1",
    "L1OOCY1": "L100CY1",
    "DZ1OOV1Z": "DZ100V1Z",
    "DZ120V10": "DZ120V1D",
    "A120CY": "A120CY1",
    "CHMO9OTV": "CHM090TV",
    "NTB1113Y": "VTB1113Y",
    "TIANyIN": "TIANYIN",
    "PA99HME": "PA99HMF",
    "Th1116Y": "TH1116Y",
    "SZ110H18": "SZ110H1H",
    "QD59L": "QD59U",
    "VFK79C": "VEK79C",
    "DZ120V18": "DZ120V1B",
    "QD75HHP": "QD75H",
    "VFA090CY!": "VFA090CY1",
    "ASK103053UFZ": "ASK103D53UFZ",
    "DLA5985X0EA": "DLA5985XOEA",
    "LU76gY": "LU76CY",
    "PZ130H1E": "PZ130H1Z",
    "DZ100V10": "DZ100V1C",
    "HVM90MS": "HVM90MS a",
    "VELO90CY7": "VELO90CY1",
    "HVD90MT": "HVD90MT a",
    "VETZ11OL": "VETZ110L",
}


# =============================================================================
# 阿里安全提示过滤内容
# =============================================================================
ALIBABA_SECURITY_MESSAGES: List[str] = [
    "您发送的消息中可能包含了存在交易风险的外部网站或移动互联网应用信息，请勿使用阿里旺旺、千牛以外的其它聊天工具，以确保买卖方沟通、交易安全",
]


# =============================================================================
# 文字转接关键词
# =============================================================================
TEXT_TRANSFER_KEYWORDS: List[str] = [
    "退货", "退款", "运费", "换货", "发票", "不要了",
    "转人工", "人工", "转接人工", "变频板", "万能板",
    "快递单", "吊杆", "加热丝",
]


# =============================================================================
# 文字转接豁免词（包含这些词不转接）
# =============================================================================
TEXT_TRANSFER_EXEMPT_KEYWORDS: List[str] = [
    "咨询人工客服",
]
