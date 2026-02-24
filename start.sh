#!/bin/bash

# Neeko 智能客服系统 - 启动脚本

echo "==================================="
echo "Neeko 智能客服系统启动脚本"
echo "==================================="

# 检查.env文件
if [ ! -f .env ]; then
    echo "错误: .env文件不存在"
    echo "请从.env.example复制并配置环境变量"
    exit 1
fi

# 创建必要的目录
echo "创建目录..."
mkdir -p logs source_photo recognize_photo check_error classified_images/errors /tmp/images

# 启动应用
echo "启动FastAPI应用..."
uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload

echo "应用已启动在 http://0.0.0.0:8000"
