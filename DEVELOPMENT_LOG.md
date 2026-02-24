# Neeko 智能客服系统 - 开发日志

## 项目概述
基于AI的电商智能客服系统，集成YOLO图片识别、PaddleOCR、Dify AI对话平台和赛牛客服平台。

## 技术栈决策
- **Web框架**: FastAPI (异步高性能)
- **数据库**: MySQL + SQLAlchemy (异步ORM)
- **缓存**: Redis (消息去重、会话管理)
- **任务队列**: Celery + Redis
- **定时任务**: APScheduler
- **AI平台**: Dify (多模型支持)
- **图像识别**: YOLO + PaddleOCR
- **容器化**: Docker + Docker Compose

## 开发进度

### 阶段1: 项目基础搭建 ✅
- [x] 创建项目目录结构
- [x] requirements.txt - 90+ Python依赖
- [x] .env.example - 环境变量模板
- [x] chatwork_config.py - 全局配置、常量、映射表
- [x] models.py - 6个数据库表模型
- [x] database.py - 异步数据库连接

### 阶段2: 工具层实现 (进行中)
- [ ] logger.py - 日志系统
- [ ] redis_client.py - Redis连接
- [ ] redis_util.py - Redis工具函数
- [ ] datetime_u.py - 日期时间工具
- [ ] images.py - 图片下载工具
- [ ] parse.py - 数据解析工具

### 阶段3: 外部服务客户端
- [ ] sainiuclient.py - 赛牛API客户端
- [ ] difyclinet.py - Dify API客户端
- [ ] api_helper.py - API辅助类(ExpiringArray)
- [ ] qnapi_helper.py - 赛牛响应解析

### 阶段4: 图片识别模块
- [ ] ocr.py - YOLO图片分类
- [ ] images_recognition.py - YOLO+OCR特征提取
- [ ] 注意：需要模型文件 classify.pt 和 best.pt (占位)

### 阶段5: 规则引擎
- [ ] rule.py - 5个规则类
  - TextTransferRuleC - 文字转接规则
  - ImageTransferRule - 图片转接规则
  - DiFyRuleC - AI回复过滤规则
  - YoloRuleC - OCR纠错规则
  - EmjCheck - 表情检查

### 阶段6: 业务逻辑层
- [ ] productInfoCurd.py - 产品CRUD
- [ ] process_trackingCurd.py - 流程追踪CRUD
- [ ] ai_message_recordsCurd.py - AI消息记录CRUD
- [ ] data_info.py - 数据工具类
- [ ] productlinksServices.py - 产品链接服务
- [ ] stock_extractor.py - 库存同步服务

### 阶段7: 核心处理流程
- [ ] chatwork.py - 消息处理核心
  - check_new_info_data() - 消息拉取
  - preprocess_info() - 消息预处理
  - send_to_fluvio() - Fluvio推送
- [ ] model_excute_task.py - AI对话任务(Celery)
- [ ] data_info_cl.py - 转人工任务

### 阶段8: 定时任务
- [ ] scheduler.py - APScheduler配置
- [ ] celery_config.py - Celery配置
- [ ] celery_app.py - Celery应用实例

### 阶段9: API路由
- [ ] main.py - FastAPI主应用
- [ ] user_api.py - 用户API、流程追踪
- [ ] product.py - 产品API
- [ ] openapi.py - 外部推送接口
- [ ] debug.py - 调试接口

### 阶段10: 部署配置
- [ ] Dockerfile - 镜像构建
- [ ] docker-compose.yml - 容器编排
- [ ] start.sh - 应用启动脚本
- [ ] celery_worker.sh - Celery启动脚本
- [ ] .dockerignore - Docker忽略文件
- [ ] .gitignore - Git忽略文件

### 阶段11: 文档
- [ ] README.md - 项目说明
- [ ] DEPLOYMENT.md - 部署文档

### 阶段12: 提交代码
- [ ] Git初始化
- [ ] 提交到GitHub

## 实现策略

### 采用混合方案：
1. **完整框架** - 创建所有必需的文件和接口
2. **核心实现** - 优先实现P0/P1功能，确保系统可运行
3. **占位符** - 对于依赖外部资源的部分(如YOLO模型)，提供占位实现和说明

### 模块优先级：
- **P0 (阻塞)**: FastAPI主应用、数据库、Redis、日志、基础API
- **P1 (核心)**: 赛牛/Dify客户端、消息处理、规则引擎
- **P2 (重要)**: 图片识别、产品服务、Celery任务
- **P3 (增强)**: 库存同步、Fluvio、完整监控

### 关键决策点：

1. **数据库迁移**: 使用SQLAlchemy自动创建表，生产环境建议使用Alembic
2. **YOLO模型**: 提供占位实现，实际模型需要训练数据(用户自行训练)
3. **环境配置**: 所有敏感信息通过环境变量配置
4. **错误处理**: 所有外部调用都有try-except和降级方案
5. **日志追踪**: 使用TraceID跟踪整个消息链路

## 当前进展
正在实现阶段2：工具层
