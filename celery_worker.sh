#!/bin/bash

# Neeko 智能客服系统 - Celery Worker启动脚本

echo "==================================="
echo "Neeko Celery Worker启动脚本"
echo "==================================="

# 检查.env文件
if [ ! -f .env ]; then
    echo "错误: .env文件不存在"
    echo "请从.env.example复制并配置环境变量"
    exit 1
fi

# 启动Celery Worker
echo "启动Celery Worker..."
celery -A app.common.config.celery_app worker \
    --loglevel=info \
    --concurrency=4 \
    --max-tasks-per-child=100

echo "Celery Worker已停止"
