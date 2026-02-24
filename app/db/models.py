"""
智能客服系统 Neeko - 数据库模型
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import (
    BigInteger, Column, Integer, String, Text, DateTime,
    Boolean, DECIMAL, Index, func
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """用户表"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    name = Column(String(100), nullable=True, comment="用户名")
    email = Column(String(100), nullable=True, comment="邮箱")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")


class ProductInfo(Base):
    """产品库存表（27个字段）"""
    __tablename__ = "productinfo"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="自增ID")
    created_at = Column(DateTime(3), nullable=True, comment="创建时间")
    updated_at = Column(DateTime(3), nullable=True, comment="更新时间")
    deleted_at = Column(DateTime(3), nullable=True, comment="软删除时间")

    shelf_id = Column(BigInteger, nullable=True, comment="货架表的ID")
    db_name = Column(String(500), nullable=True, comment="库名")
    category = Column(String(500), nullable=True, comment="商品分类")
    model = Column(String(500), nullable=True, comment="型号")
    model_image = Column(String(500), nullable=True, comment="型号图片")
    brand = Column(String(500), nullable=True, comment="品牌")
    quantity = Column(BigInteger, nullable=True, comment="库存数量")
    description = Column(Text, nullable=True, comment="说明")

    batch_number = Column(String(500), nullable=True, comment="批次号")
    batch_quantity_range = Column(String(500), nullable=True, comment="批次数量区间")
    operator = Column(String(500), nullable=True, comment="操作人")
    merchant_code = Column(String(500), nullable=True, comment="商家编码")
    product_status = Column(String(500), nullable=True, comment="商品状态")
    relation = Column(String(500), nullable=True, comment="对应关系")
    replacement_model = Column(String(500), nullable=True, comment="型号替代")
    full_model_name = Column(String(500), nullable=True, comment="型号全称")

    source = Column(String(500), nullable=True, comment="来源")
    appliance_category = Column(String(500), nullable=True, comment="家电大类")
    identifier = Column(String(500), nullable=True, comment="标识")
    sort_order = Column(Integer, default=0, comment="排序字段")
    shelf_life = Column(String(500), nullable=True, comment="保质期(格式:YYYYMMDD)")
    weight = Column(DECIMAL(10, 2), nullable=True, comment="商品重量(kg)")
    cost_price = Column(DECIMAL(10, 2), nullable=True, comment="商品成本价(元)")

    # 索引
    __table_args__ = (
        Index('idx_ProductInfo_deleted_at', 'deleted_at'),
        Index('idx_merchant_code', 'merchant_code'),
        Index('idx_merchant_code_sort_updated', 'merchant_code', 'sort_order', 'updated_at'),
        Index('idx_merchant_code_deleted_sort', 'merchant_code', 'deleted_at', 'sort_order'),
        Index('idx_sort_order_updated_at', 'sort_order', 'updated_at'),
    )


class ProductLink(Base):
    """产品链接表"""
    __tablename__ = "product_links"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    shop_name = Column(String(255), nullable=True, comment="店铺名称")
    product_status = Column(String(50), nullable=True, comment="产品状态编码")
    model = Column(String(100), nullable=True, comment="产品型号")
    url = Column(String(255), nullable=True, comment="产品链接")
    item_id = Column(String(100), nullable=True, comment="商品大类ID")
    sku_id = Column(String(100), nullable=True, comment="SKU ID")
    product_type = Column(String(100), nullable=True, comment="产品类型")
    clean_after_models = Column(String(100), nullable=True, comment="清洗后的型号")
    shop_name_enmu = Column(String(100), nullable=True, comment="店铺名称枚举")
    standard_product_type = Column(String(100), nullable=True, comment="标准化产品类型")
    merchant_code = Column(String(100), nullable=True, comment="商家编码")
    handler = Column(String(100), nullable=True, comment="处理人")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")


class ProductReplacement(Base):
    """产品替代表"""
    __tablename__ = "product_replacements"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    type = Column(String(100), nullable=True, comment="产品类型")
    model = Column(String(100), nullable=True, comment="原产品型号")
    refrigerant = Column(String(50), nullable=True, comment="制冷剂")
    cooling_capacity = Column(String(50), nullable=True, comment="冷量")
    replacement_model = Column(String(100), nullable=True, comment="替代型号")
    replacement_brand = Column(String(100), nullable=True, comment="替代品牌")
    replacement_refrigerant = Column(String(50), nullable=True, comment="替代制冷剂")
    replacement_cooling_capacity = Column(String(50), nullable=True, comment="替代冷量")
    replacement_type = Column(String(100), nullable=True, comment="替代产品类型")
    handler = Column(String(50), nullable=True, comment="处理人")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")


class ProcessTracking(Base):
    """流程追踪表（7步追踪）"""
    __tablename__ = "process_tracking"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="主键ID")
    sainiu_msg_id = Column(String(100), nullable=True, comment="赛牛消息ID")
    message_type = Column(String(50), nullable=True, comment="消息类型编号(1-7)")

    # 7步流程追踪
    sainiu_fetch_info = Column(String(50), nullable=True, comment="步骤1: 赛牛获取信息")
    preprocess_info = Column(String(50), nullable=True, comment="步骤2/7: 预处理")
    dify_api_call = Column(String(50), nullable=True, comment="步骤3: Dify调用")
    dify_call_completed = Column(String(50), nullable=True, comment="步骤4: Dify调用完成")
    sainiu_api_call = Column(String(50), nullable=True, comment="步骤5: 赛牛API调用")
    sainiu_call_success = Column(String(50), nullable=True, comment="步骤6: 赛牛调用成功")

    handler = Column(String(100), nullable=True, default="AI", comment="处理人(固定AI)")
    is_finished = Column(Integer, default=0, comment="是否结束(0=进行中/1=完成)")

    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")


class AIMessageRecord(Base):
    """AI 消息记录表"""
    __tablename__ = "ai_message_records"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    date = Column(DateTime, nullable=True, comment="处理日期时间")
    need_backtest = Column(Boolean, default=False, comment="是否需要回测")
    resolved_at = Column(DateTime, nullable=True, comment="解决时间")
    human_analysis = Column(Text, nullable=True, comment="人工分析")

    user_nickname = Column(String(100), nullable=True, comment="客服昵称(店铺:客服)")
    buyer_uid = Column(String(100), nullable=True, comment="买家UID")
    message = Column(Text, nullable=True, comment="AI回复内容")
    forwarded_to_agent = Column(Boolean, default=False, comment="是否转人工")
    forward_reason = Column(Text, nullable=True, comment="转接原因")

    product_type = Column(String(100), nullable=True, comment="产品类型")
    model_response = Column(Text, nullable=True, comment="模型返回原始结果")
    source_image_path = Column(String(255), nullable=True, comment="原图路径")
    recognized_image_path = Column(String(255), nullable=True, comment="识别图路径")

    sainiu_id = Column(String(100), nullable=True, comment="赛牛消息ID")
    dify_id = Column(String(100), nullable=True, comment="Dify会话ID")
    send_dify_data_info = Column(Text, nullable=True, comment="发送给Dify的数据")
    data_type = Column(String(100), nullable=True, comment="数据类型编号(1-7)")

    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
