"""
AI消息记录CRUD操作
"""
from typing import Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import AIMessageRecord
from app.common.utils.logger import logger


async def create_ai_message_record(
    db: AsyncSession,
    dify_id: str,
    user_nickname: str,
    buyer_uid: str,
    message: str,
    forwarded_to_agent: bool = False,
    send_dify_data_info: str = "",
    data_type: str = "1"
) -> Optional[AIMessageRecord]:
    """
    创建AI消息记录

    Args:
        db: 数据库会话
        dify_id: Dify会话ID
        user_nickname: 客服昵称
        buyer_uid: 买家UID
        message: AI回复内容
        forwarded_to_agent: 是否转人工
        send_dify_data_info: 发送给Dify的数据
        data_type: 数据类型

    Returns:
        消息记录或None
    """
    try:
        record = AIMessageRecord(
            dify_id=dify_id,
            date=datetime.now(),
            user_nickname=user_nickname,
            buyer_uid=buyer_uid,
            message=message,
            forwarded_to_agent=forwarded_to_agent,
            send_dify_data_info=send_dify_data_info,
            data_type=data_type,
        )
        db.add(record)
        await db.commit()
        await db.refresh(record)

        logger.debug(f"AI消息记录已创建: {dify_id}")
        return record

    except Exception as e:
        logger.error(f"创建AI消息记录失败: {str(e)}")
        await db.rollback()
        return None
