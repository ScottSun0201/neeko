"""
流程追踪CRUD操作
"""
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import ProcessTracking
from app.common.utils.logger import logger


async def create_process_tracking(
    db: AsyncSession,
    sainiu_msg_id: str,
    message_type: str
) -> Optional[ProcessTracking]:
    """
    创建流程追踪记录

    Args:
        db: 数据库会话
        sainiu_msg_id: 赛牛消息ID
        message_type: 消息类型

    Returns:
        追踪记录或None
    """
    try:
        tracking = ProcessTracking(
            sainiu_msg_id=sainiu_msg_id,
            message_type=message_type,
            sainiu_fetch_info="1",  # 步骤1
            handler="AI",
            is_finished=0,
        )
        db.add(tracking)
        await db.commit()
        await db.refresh(tracking)

        logger.debug(f"流程追踪记录已创建: {sainiu_msg_id}")
        return tracking

    except Exception as e:
        logger.error(f"创建流程追踪失败: {str(e)}")
        await db.rollback()
        return None


async def update_process_step(
    db: AsyncSession,
    sainiu_msg_id: str,
    step_name: str,
    step_value: str
) -> bool:
    """
    更新流程步骤

    Args:
        db: 数据库会话
        sainiu_msg_id: 赛牛消息ID
        step_name: 步骤字段名
        step_value: 步骤值

    Returns:
        是否成功
    """
    try:
        stmt = select(ProcessTracking).where(
            ProcessTracking.sainiu_msg_id == sainiu_msg_id
        )
        result = await db.execute(stmt)
        tracking = result.scalar_one_or_none()

        if tracking:
            setattr(tracking, step_name, step_value)
            await db.commit()
            logger.debug(f"流程步骤已更新: {sainiu_msg_id} {step_name}={step_value}")
            return True
        else:
            logger.warning(f"流程追踪记录不存在: {sainiu_msg_id}")
            return False

    except Exception as e:
        logger.error(f"更新流程步骤失败: {str(e)}")
        await db.rollback()
        return False


async def mark_process_finished(
    db: AsyncSession,
    sainiu_msg_id: str
) -> bool:
    """
    标记流程完成

    Args:
        db: 数据库会话
        sainiu_msg_id: 赛牛消息ID

    Returns:
        是否成功
    """
    try:
        stmt = select(ProcessTracking).where(
            ProcessTracking.sainiu_msg_id == sainiu_msg_id
        )
        result = await db.execute(stmt)
        tracking = result.scalar_one_or_none()

        if tracking:
            tracking.sainiu_call_success = "6"  # 步骤6
            tracking.is_finished = 1
            await db.commit()
            logger.debug(f"流程已标记完成: {sainiu_msg_id}")
            return True
        else:
            return False

    except Exception as e:
        logger.error(f"标记流程完成失败: {str(e)}")
        await db.rollback()
        return False
