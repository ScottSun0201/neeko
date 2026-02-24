"""
外部推送接口
"""
from fastapi import APIRouter
from app.common.utils.logger import logger
from app.api.chatwork import process_message

router = APIRouter()


@router.post("/sainiu/getInfo")
async def sainiu_push(data: dict):
    """
    赛牛消息推送接口

    Args:
        data: 赛牛推送的消息数据
    """
    try:
        logger.info(f"收到赛牛推送消息: {data.get('messageId', 'unknown')}")
        await process_message(data)
        return {"status": "success"}
    except Exception as e:
        logger.error(f"处理推送消息失败: {str(e)}")
        return {"status": "error", "message": str(e)}
