"""
产品相关API
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.crud.productInfoCurd import get_product_by_merchant_code
from app.common.utils.logger import logger

router = APIRouter()


@router.get("/inventory/{merchant_code}")
async def get_inventory(
    merchant_code: str,
    db: AsyncSession = Depends(get_db)
):
    """
    查询库存

    Args:
        merchant_code: 商家编码
    """
    product = await get_product_by_merchant_code(db, merchant_code)
    if product:
        return {
            "merchant_code": product.merchant_code,
            "model": product.model,
            "quantity": product.quantity,
            "brand": product.brand,
        }
    else:
        return {"message": "产品不存在"}


@router.post("/stock/check")
async def check_stock(data: dict, db: AsyncSession = Depends(get_db)):
    """
    批量检查库存

    Args:
        data: {"products": ["商家编码1", "商家编码2"]}
    """
    products = data.get("products", [])
    results = []

    for merchant_code in products:
        product = await get_product_by_merchant_code(db, merchant_code)
        if product:
            stock_status = "有货" if product.quantity and product.quantity > 0 else "无货"
            results.append({
                "merchant_code": merchant_code,
                "status": stock_status,
                "quantity": product.quantity,
            })
        else:
            results.append({
                "merchant_code": merchant_code,
                "status": "未找到",
                "quantity": 0,
            })

    return {"results": results}
