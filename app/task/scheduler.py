"""
定时任务调度
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.common.utils.logger import logger


# 创建调度器
scheduler = AsyncIOScheduler()


async def check_new_info():
    """
    拉取赛牛新消息(每1秒执行一次)
    """
    try:
        from app.api.chatwork import check_new_info_data
        await check_new_info_data()
    except Exception as e:
        logger.error(f"拉取消息任务失败: {str(e)}")


async def sync_stock():
    """
    同步库存(每24小时执行一次)
    """
    try:
        logger.info("库存同步任务开始(占位)")
        # TODO: 实际库存同步实现
        logger.info("库存同步任务完成(占位)")
    except Exception as e:
        logger.error(f"库存同步任务失败: {str(e)}")


def start_scheduler():
    """启动定时任务调度器"""
    # 添加消息拉取任务(每1秒)
    scheduler.add_job(
        check_new_info,
        trigger=IntervalTrigger(seconds=1),
        id="check_new_info",
        name="拉取赛牛新消息",
        replace_existing=True,
    )

    # 添加库存同步任务(每24小时)
    scheduler.add_job(
        sync_stock,
        trigger=IntervalTrigger(hours=24),
        id="sync_stock",
        name="同步库存数据",
        replace_existing=True,
    )

    scheduler.start()
    logger.info("定时任务调度器已启动")


def stop_scheduler():
    """停止定时任务调度器"""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("定时任务调度器已停止")
