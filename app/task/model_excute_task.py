"""
AI对话Celery任务
"""
from typing import Dict, Any
from app.common.config.celery_app import celery_app
from app.common.utils.logger import logger


@celery_app.task(name="dify_api_task")
def dify_api(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    AI对话异步任务 (简化版本)

    Args:
        data: 消息数据

    Returns:
        处理结果
    """
    try:
        logger.info(f"AI对话任务开始: {data.get('buyerUid', 'unknown')}")

        # TODO: 实际AI对话实现
        # 1. 调用Dify API
        # 2. 审核回复
        # 3. 发送消息
        # 4. 转接判断

        # 占位实现
        result = {
            "status": "success",
            "message": "AI对话处理完成(占位)",
        }

        logger.info("AI对话任务完成")
        return result

    except Exception as e:
        logger.error(f"AI对话任务失败: {str(e)}")
        return {"status": "error", "message": str(e)}
