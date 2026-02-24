"""
数据信息处理工具类
"""
import re
import json
from typing import List, Dict, Any, Optional
from app.common.utils.logger import logger


class DataInfo:
    """数据信息处理类"""

    @staticmethod
    def product_check(
        product: str,
        producttype: str,
        user_nick: str,
        buyer_nick: str,
        message: str
    ) -> List[Dict[str, Any]]:
        """
        产品信息查询

        Args:
            product: 产品型号(多个用;分隔)
            producttype: 产品类型(多个用;分隔)
            user_nick: 客服昵称
            buyer_nick: 买家昵称
            message: 消息内容

        Returns:
            产品查询结果列表
        """
        try:
            # 分割产品型号和类型
            products = product.split(";") if product else []
            types = producttype.split(";") if producttype else []

            consult_list = []

            # 为每个产品查询信息
            for i, prod in enumerate(products):
                if not prod or prod in ["feature_error", "class_error"]:
                    continue

                ptype = types[i] if i < len(types) else ""

                # TODO: 实际查询数据库获取库存和链接
                # 占位实现
                item = {
                    "product": prod,
                    "producttype": ptype,
                    "stock": "有货",  # 占位
                    "links": [
                        {"status": "全新", "url": "http://example.com/product"},
                        {"status": "拆机", "url": "无链接"}
                    ]
                }
                consult_list.append(item)

            logger.debug(f"产品查询完成: {len(consult_list)}项")
            return consult_list

        except Exception as e:
            logger.error(f"产品查询失败: {str(e)}")
            return []

    @staticmethod
    def generate_combined_format(consult_list: List[Dict[str, Any]]) -> str:
        """
        生成结构化查询消息格式

        Args:
            consult_list: 产品查询结果列表

        Returns:
            格式化的查询消息
        """
        try:
            if not consult_list:
                return ""

            parts = []
            for i, item in enumerate(consult_list, 1):
                product = item.get("product", "")
                producttype = item.get("producttype", "")
                stock = item.get("stock", "")
                links = item.get("links", [])

                # 构建图片信息
                img_info = f"图片{i}[{producttype}:{product}]"

                # 构建查询结果
                link_str = "，".join([
                    f"（{link['status']}）链接为：{link['url']}"
                    for link in links if link.get("url") != "无链接"
                ])

                if link_str:
                    query_result = f"图片{i}[查询结果，({product})({stock}){link_str}]"
                else:
                    query_result = f"图片{i}[查询结果，({product})({stock})，无链接]"

                parts.append(f"{img_info}; {query_result}")

            return "咨询这个[" + "，".join(parts) + "]"

        except Exception as e:
            logger.error(f"生成查询消息失败: {str(e)}")
            return ""

    @staticmethod
    def extract_ids_general(text: str) -> Optional[str]:
        """
        从文本中提取淘宝商品ID

        Args:
            text: 包含链接的文本

        Returns:
            商品ID或None
        """
        try:
            # 排除包含skuId的链接
            if "skuId" in text:
                return None

            # 提取?id=后面的数字
            pattern = r'\?id=(\d+)'
            match = re.search(pattern, text)
            if match:
                return match.group(1)

            return None

        except Exception as e:
            logger.error(f"提取商品ID失败: {str(e)}")
            return None

    @staticmethod
    def build_product_query_message(
        item_id: str,
        url: str,
        product_links: List[Dict[str, Any]]
    ) -> str:
        """
        构建产品链接查询消息

        Args:
            item_id: 商品ID
            url: 商品URL
            product_links: 查询到的产品链接列表

        Returns:
            查询消息
        """
        try:
            if not product_links:
                return f"咨询这个 {item_id}\n[未查询到对应商品信息]"

            # 取前5个
            links_to_show = product_links[:5]
            models = [link.get("model", "") for link in links_to_show]

            result_str = f"咨询这个 {url}\n[查询结果，链接对应的商品有"
            result_str += "，".join(f"({model})" for model in models if model)

            if len(product_links) > 5:
                result_str += "等"

            result_str += "]"

            return result_str

        except Exception as e:
            logger.error(f"构建查询消息失败: {str(e)}")
            return ""
