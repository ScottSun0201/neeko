"""
规则引擎 - 5个规则类
"""
import re
from typing import List, Dict, Any, Optional
from app.common.config.chatwork_config import (
    TRANSFER_PRODUCT_TYPES,
    TEXT_TRANSFER_KEYWORDS,
    TEXT_TRANSFER_EXEMPT_KEYWORDS,
    ALIBABA_SECURITY_MESSAGES,
    OCR_CORRECTION_RULES,
)
from app.common.utils.logger import logger


class TextTransferRuleC:
    """文字转接规则"""

    @staticmethod
    def need_transfer(message: str) -> bool:
        """
        判断文本消息是否需要转人工

        Args:
            message: 消息内容

        Returns:
            True表示需要转接，False表示不转接
        """
        if not message:
            return False

        # 优先检查豁免词
        for exempt in TEXT_TRANSFER_EXEMPT_KEYWORDS:
            if exempt in message:
                return False

        # 检查转接关键词
        for keyword in TEXT_TRANSFER_KEYWORDS:
            if keyword in message:
                logger.info(f"文字转接触发: {keyword}")
                return True

        return False


class ImageTransferRule:
    """图片转接规则"""

    @staticmethod
    def should_transfer_to_manual(consult_list: List[Dict[str, Any]]) -> bool:
        """
        判断图片识别结果是否需要转人工

        Args:
            consult_list: 产品查询结果列表

        Returns:
            True表示需要转接，False表示不转接
        """
        if not consult_list:
            return False

        # 统计特殊情况
        no_stock_count = 0  # 无货数量
        no_link_count = 0  # 无链接数量
        all_nameplate = True  # 是否全部是冰箱铭牌
        total = len(consult_list)

        for item in consult_list:
            product_type = item.get("producttype", "")
            stock = item.get("stock", "")
            links = item.get("links", [])

            # 检查是否全部是冰箱铭牌
            if product_type != "Refrigerator Nameplate":
                all_nameplate = False

            # 检查是否需要转接的产品类型
            if product_type in TRANSFER_PRODUCT_TYPES:
                logger.info(f"图片转接触发: 产品类型={product_type}")
                return True

            # 统计无货
            if stock != "有货":
                no_stock_count += 1

            # 统计无链接
            if not links or all(link.get("url") == "无链接" for link in links):
                no_link_count += 1

        # 最高优先级：全部冰箱铭牌不转接
        if all_nameplate:
            return False

        # 全部无货
        if no_stock_count == total and total > 0:
            logger.info("图片转接触发: 全部无货")
            return True

        # 全部无链接
        if no_link_count == total and total > 0:
            logger.info("图片转接触发: 全部无链接")
            return True

        return False


class DiFyRuleC:
    """Dify回复处理规则"""

    @staticmethod
    def filter_data(message: str) -> Optional[str]:
        """
        过滤阿里安全提示等消息

        Args:
            message: 消息内容

        Returns:
            "continue"表示跳过，None表示继续处理
        """
        for filter_text in ALIBABA_SECURITY_MESSAGES:
            if message == filter_text:
                logger.info("阿里安全提示被过滤")
                return "continue"
        return None

    @staticmethod
    def deduplication(text: str) -> str:
        """
        去除重复句子

        Args:
            text: 原始文本

        Returns:
            去重后的文本
        """
        if not text:
            return text

        # 按句号分割
        sentences = text.split("。")
        seen = set()
        result = []

        for sentence in sentences:
            if sentence and sentence not in seen:
                seen.add(sentence)
                result.append(sentence)

        return "。".join(result) + ("。" if result and text.endswith("。") else "")

    @staticmethod
    def replace_t(text: str, replacements: Dict[str, str]) -> str:
        """
        字符串替换(主要用于URL编码)

        Args:
            text: 原始文本
            replacements: 替换映射 {old: new}

        Returns:
            替换后的文本
        """
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    @staticmethod
    def url_check(text: str) -> str:
        """
        检查并移除多余的URL(只保留第一个)

        Args:
            text: 原始文本

        Returns:
            处理后的文本
        """
        urls = re.findall(r'https?://[^\s]+', text)
        if len(urls) > 1:
            # 移除第二个及后续的URL
            for url in urls[1:]:
                text = text.replace(url, "")
            logger.info("多余的URL已移除")
        return text


class YoloRuleC:
    """YOLO OCR纠错规则"""

    @staticmethod
    def th_rule(data: str) -> str:
        """
        OCR型号纠错

        Args:
            data: OCR识别结果

        Returns:
            纠错后的型号
        """
        if data in OCR_CORRECTION_RULES:
            corrected = OCR_CORRECTION_RULES[data]
            logger.info(f"OCR纠错: {data} -> {corrected}")
            return corrected
        return data

    @staticmethod
    def data_cleaning(data: str) -> str:
        """
        数据清洗

        Args:
            data: 原始数据

        Returns:
            清洗后的数据
        """
        if not data:
            return ""

        # 去除空格
        data = data.strip().replace(" ", "")

        # 去除首尾非字母数字字符
        data = re.sub(r'^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$', '', data)

        return data


def emj_check(msg: str) -> Optional[str]:
    """
    表情检查

    Args:
        msg: 消息内容

    Returns:
        表情消息原样返回，否则返回None
    """
    if msg and msg.startswith('/:') and len(msg) < 6:
        return msg
    return None
