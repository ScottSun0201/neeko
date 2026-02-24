"""
Celery应用实例
"""
from celery import Celery
from app.common.config.chatwork_config import settings

# 创建Celery应用
celery_app = Celery(
    "neeko",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.task.model_excute_task",
        "app.task.data_info_cl",
    ]
)

# 配置Celery
celery_app.conf.update(
    task_serializer=settings.CELERY_TASK_SERIALIZER,
    result_serializer=settings.CELERY_RESULT_SERIALIZER,
    accept_content=[settings.CELERY_TASK_SERIALIZER],
    timezone=settings.CELERY_TIMEZONE,
    enable_utc=settings.CELERY_ENABLE_UTC,
    task_track_started=True,
    task_time_limit=600,  # 10分钟超时
    task_soft_time_limit=540,  # 9分钟软超时
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=100,
)

if __name__ == "__main__":
    celery_app.start()
