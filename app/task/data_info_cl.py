"""
转人工Celery任务
"""
from typing import Dict, Any
from app.common.config.celery_app import celery_app
from app.common.utils.logger import logger


@celery_app.task(name="transfer_to_manual_task")
def transfer_to_manual(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    转人工异步任务

    Args:
        data: 转接数据

    Returns:
        处理结果
    """
    try:
        logger.info(f"转人工任务开始: {data.get('buyerNick', 'unknown')}")

        # TODO: 实际转接实现
        # 1. 发送转接话术
        # 2. 调用赛牛转接API
        # 3. 设置转接标记
        # 4. 记录转接日志

        # 占位实现
        result = {
            "status": "success",
            "message": "转人工处理完成(占位)",
        }

        logger.info("转人工任务完成")
        return result

    except Exception as e:
        logger.error(f"转人工任务失败: {str(e)}")
        return {"status": "error", "message": str(e)}
