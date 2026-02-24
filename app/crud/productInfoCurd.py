"""
产品库存CRUD操作
"""
from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import ProductInfo
from app.common.utils.logger import logger


async def get_product_by_merchant_code(
    db: AsyncSession,
    merchant_code: str
) -> Optional[ProductInfo]:
    """
    根据商家编码查询产品

    Args:
        db: 数据库会话
        merchant_code: 商家编码

    Returns:
        产品信息或None
    """
    try:
        stmt = select(ProductInfo).where(
            and_(
                ProductInfo.merchant_code == merchant_code,
                ProductInfo.deleted_at.is_(None)
            )
        ).order_by(ProductInfo.sort_order, ProductInfo.updated_at.desc())

        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    except Exception as e:
        logger.error(f"查询产品失败 {merchant_code}: {str(e)}")
        return None


async def get_products_by_model(
    db: AsyncSession,
    model: str
) -> List[ProductInfo]:
    """
    根据型号查询产品列表

    Args:
        db: 数据库会话
        model: 产品型号

    Returns:
        产品列表
    """
    try:
        stmt = select(ProductInfo).where(
            and_(
                ProductInfo.model == model,
                ProductInfo.deleted_at.is_(None)
            )
        )

        result = await db.execute(stmt)
        return list(result.scalars().all())

    except Exception as e:
        logger.error(f"查询产品列表失败 {model}: {str(e)}")
        return []


async def update_product_quantity(
    db: AsyncSession,
    merchant_code: str,
    quantity: float
) -> bool:
    """
    更新产品库存数量

    Args:
        db: 数据库会话
        merchant_code: 商家编码
        quantity: 库存数量

    Returns:
        是否成功
    """
    try:
        product = await get_product_by_merchant_code(db, merchant_code)
        if not product:
            logger.warning(f"产品不存在，无法更新库存: {merchant_code}")
            return False

        product.quantity = int(quantity)
        await db.commit()

        logger.info(f"库存更新成功: {merchant_code} -> {quantity}")
        return True

    except Exception as e:
        logger.error(f"更新库存失败 {merchant_code}: {str(e)}")
        await db.rollback()
        return False
