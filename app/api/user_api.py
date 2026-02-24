"""
用户相关API
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.common.utils.logger import logger

router = APIRouter()


@router.get("/")
async def get_users(db: AsyncSession = Depends(get_db)):
    """获取用户列表(占位)"""
    return {"users": []}


@router.post("/AICustomerServiceTesting")
async def ai_customer_service_testing(data: dict):
    """AI客服测试入口"""
    logger.info(f"AI客服测试: {data}")
    return {"status": "success", "message": "测试完成"}
