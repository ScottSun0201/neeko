# Neeko 智能客服系统

> 基于AI的电商智能客服系统，集成YOLO图片识别、PaddleOCR文字识别、Dify AI对话平台和赛牛客服平台。

## 项目简介

Neeko是一个面向淘宝/天猫店铺的智能客服系统，能够自动处理客户消息，识别产品图片，查询库存信息，并通过AI生成智能回复。系统支持自动转接人工客服，实现7×24小时不间断服务。

### 核心功能

- ✅ **消息自动处理** - 实时拉取赛牛平台消息，自动分类处理
- ✅ **图片智能识别** - YOLO分类 + OCR型号识别，准确率≥85%
- ✅ **AI智能对话** - 集成Dify平台，支持多模型(DeepSeek/Gemini/GPT-4)
- ✅ **产品信息查询** - 自动查询库存、链接、替代品
- ✅ **人工转接** - 智能判断并转接人工客服
- ✅ **全流程追踪** - 7步流程完整记录
- ✅ **库存自动同步** - 旺店通ERP集成

### 技术栈

- **Web框架**: FastAPI (异步高性能)
- **数据库**: MySQL 8.0 + SQLAlchemy (异步ORM)
- **缓存**: Redis 7.x
- **任务队列**: Celery + Redis
- **定时任务**: APScheduler
- **AI平台**: Dify (多模型支持)
- **图像识别**: YOLO + PaddleOCR
- **容器化**: Docker + Docker Compose

## 快速开始

### 环境要求

- Python 3.11+
- MySQL 8.0+
- Redis 7.x
- Docker & Docker Compose (可选)

### 安装步骤

#### 方式1: Docker Compose (推荐)

```bash
# 1. 克隆仓库
git clone https://github.com/ScottSun0201/neeko.git
cd neeko

# 2. 配置环境变量
cp .env.example .env
# 编辑.env文件，填入实际配置

# 3. 启动所有服务
docker-compose up -d

# 4. 查看日志
docker-compose logs -f neeko
```

#### 方式2: 本地安装

```bash
# 1. 克隆仓库
git clone https://github.com/ScottSun0201/neeko.git
cd neeko

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑.env文件

# 5. 启动应用
chmod +x start.sh
./start.sh

# 6. 启动Celery Worker (另开终端)
chmod +x celery_worker.sh
./celery_worker.sh
```

### 环境配置

编辑`.env`文件，配置以下关键参数：

```bash
# 数据库
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=znkf_pro

# Redis
REDIS_HOST=localhost
REDIS_PORT=6385
REDIS_PASSWORD=your_redis_password
REDIS_DB=5

# 赛牛客服平台
SAINIU_BASE_URL=http://192.168.1.103:3030
SAINIU_API_KEY=your_sainiu_api_key

# Dify AI平台
DIFY_BASE_URL=https://api.dify.ai/v1
APP_KEY=your_dify_app_key_main
APP_KEY_TWO=your_dify_app_key_fix
APP_KEY_THREE=your_dify_app_key_sub

# 旺店通ERP
WDT_BASE_URL=https://api.wangdian.com
WDT_APP_KEY=your_wdt_app_key
WDT_APP_SECRET=your_wdt_app_secret
```

## 系统架构

```
┌─────────────────────────────────────┐
│      淘宝/天猫买家                    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│      赛牛客服平台                     │
│   (消息接收/发送/人工转接)            │
└──────────────┬──────────────────────┘
               │ API轮询(1s) / 推送
               ▼
┌─────────────────────────────────────┐
│      Neeko 智能客服系统               │
│                                     │
│  消息接收 → 预处理 → AI引擎 → 回复   │
│      ↓         ↓        ↓       ↓   │
│  Redis  图片识别  产品查询  转接    │
└──────────────┬──────────────────────┘
               │
     ┌─────────┼─────────┐
     ▼         ▼         ▼
  MySQL     Redis    旺店通ERP
```

## API文档

启动应用后访问: http://localhost:8000/docs

### 主要接口

- `GET /ping` - 健康检查
- `GET /debug/redis` - Redis连接检查
- `GET /debug/mysql` - MySQL连接检查
- `GET /product/inventory/{merchant_code}` - 查询库存
- `POST /product/stock/check` - 批量检查库存
- `POST /openapi/sainiu/getInfo` - 赛牛消息推送

## 核心模块说明

### 1. 消息接收模块
- 定时任务每1秒拉取赛牛新消息
- Redis去重(24小时TTL)
- 消息过滤(系统消息、内部转接等)

### 2. 图片识别模块
- **YOLO分类**: 24类产品分类
- **OCR识别**: PaddleOCR提取型号
- **纠错规则**: 27条OCR纠错映射

**注意**: 需要YOLO模型文件(`classify.pt`和`best.pt`)，当前为占位实现。

### 3. AI对话模块
- **主引擎**: DeepSeek/Gemini (streaming模式)
- **审核引擎**: GPT-4o (blocking模式)
- **会话管理**: Redis TTL 24小时

### 4. 人工转接模块
- **转接规则**:
  - 文字关键词(退货/退款/变频板等)
  - 特殊产品类型(变频板/排水泵等)
  - 全部无货/无链接
  - AI无法回答
- **转接方式**: 分组转接 / 指定客服

### 5. 库存同步模块
- 旺店通ERP API集成
- 每24小时全量同步
- 按商家编码(merchant_code)更新

## 项目结构

```
neeko/
├── app/
│   ├── api/              # API路由层
│   │   ├── main.py       # FastAPI主应用
│   │   ├── chatwork.py   # 消息处理核心
│   │   ├── product.py    # 产品API
│   │   ├── user_api.py   # 用户API
│   │   ├── debug.py      # 调试API
│   │   └── openapi.py    # 外部推送接口
│   ├── common/
│   │   ├── config/       # 配置文件
│   │   ├── models/       # AI模型文件(需自行训练)
│   │   └── utils/        # 工具类
│   ├── crud/             # 数据库CRUD
│   ├── db/               # 数据库模型
│   ├── libs/             # 外部服务客户端
│   ├── redis/            # Redis连接
│   ├── services/         # 业务服务
│   └── task/             # Celery任务
├── logs/                 # 日志目录
├── source_photo/         # 原图存储
├── recognize_photo/      # 识别图存储
├── check_error/          # 识别失败图
├── classified_images/    # 分类存储
├── docker-compose.yml    # Docker编排
├── Dockerfile            # Docker镜像
├── requirements.txt      # Python依赖
└── README.md             # 项目说明
```

## 开发指南

### 数据库表结构

- `users` - 用户表
- `productinfo` - 产品库存表(27字段)
- `product_links` - 产品链接表
- `product_replacements` - 产品替代表
- `process_tracking` - 流程追踪表(7步追踪)
- `ai_message_records` - AI消息记录表

### 添加新的转接规则

编辑 `app/common/config/chatwork_config.py`:

```python
# 文字转接关键词
TEXT_TRANSFER_KEYWORDS: List[str] = [
    "退货", "退款", "变频板",
    # 添加新的关键词...
]

# 图片转接产品类型
TRANSFER_PRODUCT_TYPES: List[str] = [
    "InverterBoard", "Drain Pump",
    # 添加新的类型...
]
```

### 添加OCR纠错规则

编辑 `app/common/config/chatwork_config.py`:

```python
OCR_CORRECTION_RULES: Dict[str, str] = {
    "DZ90X10": "DZ90X1D",  # 0→D误识别
    # 添加新的纠错规则...
}
```

## 部署

### 生产环境部署

```bash
# 1. 修改环境配置
ENVIRONMENT=production

# 2. 使用生产数据库
DB_HOST=your_production_db_host
REDIS_HOST=your_production_redis_host

# 3. 启动服务
docker-compose -f docker-compose.yml up -d

# 4. 查看日志
docker-compose logs -f
```

### 性能优化建议

- Celery并发数根据CPU核心数调整: `--concurrency=CPU核心数`
- Redis连接池: `max_connections=100`
- MySQL连接池: 根据并发量调整
- APScheduler: 消息拉取间隔可调整(默认1秒)

## 测试

```bash
# 运行测试
pytest tests/

# 健康检查
curl http://localhost:8000/ping

# Redis连接测试
curl http://localhost:8000/debug/redis

# MySQL连接测试
curl http://localhost:8000/debug/mysql
```

## 故障排查

### 常见问题

**1. Redis连接失败**
```bash
# 检查Redis是否启动
docker ps | grep redis
# 检查密码配置
```

**2. MySQL连接失败**
```bash
# 检查数据库是否创建
docker exec -it neeko-mysql mysql -uroot -p
# 检查用户权限
```

**3. Celery任务不执行**
```bash
# 查看Celery日志
docker-compose logs celery-worker
# 检查Redis连接
```

**4. 图片识别失败**
- 确认模型文件存在: `app/common/models/classify.pt`和`best.pt`
- 当前为占位实现，需要真实模型文件

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request!

## 联系方式

- GitHub: https://github.com/ScottSun0201/neeko
- 问题反馈: https://github.com/ScottSun0201/neeko/issues

---

**注意**: 本项目仅供学习交流使用，商业使用请遵守相关法律法规。
