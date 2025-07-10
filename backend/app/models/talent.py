from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base
import enum

class IntentionLevel(enum.Enum):
    A = "A"  # 高意向
    B = "B"  # 中等意向
    C = "C"  # 低意向

class CertificateLevel(enum.Enum):
    FIRST_CLASS = "一级"  # 一级建造师
    SECOND_CLASS = "二级"  # 二级建造师
    JUNIOR_ENGINEER = "初级工程师"  # 初级工程师
    MIDDLE_ENGINEER = "中级工程师"  # 中级工程师
    SENIOR_ENGINEER = "高级工程师"  # 高级工程师
    CLASS_A = "三类人员A类"  # 企业主要负责人
    CLASS_B = "三类人员B类"  # 项目负责人
    CLASS_C = "三类人员C类"  # 专职安全员
    OTHER = "其他"  # 其他证书

class CertificateSpecialty(enum.Enum):
    # 建造师专业（10个）
    ARCHITECTURE = "建筑工程"  # 房建
    MUNICIPAL = "市政公用工程"  # 市政
    MECHANICAL = "机电工程"  # 机电
    HIGHWAY = "公路工程"  # 公路
    WATER = "水利水电工程"  # 水利
    MINING = "矿业工程"  # 矿业
    RAILWAY = "铁路工程"  # 铁路
    AVIATION = "民航机场工程"  # 民航
    PORT = "港口与航道工程"  # 港口
    COMMUNICATION = "通信与广电工程"  # 通信

    # 工程师专业（10个）
    ARCHITECT_ENGINEER = "建筑工程师"
    STRUCTURAL_ENGINEER = "结构工程师"
    ELECTRICAL_ENGINEER = "电气工程师"
    PLUMBING_ENGINEER = "给排水工程师"
    HVAC_ENGINEER = "暖通工程师"
    DESIGN_ENGINEER = "建筑设计工程师"
    COST_ENGINEER = "工程造价工程师"
    SURVEYING_ENGINEER = "测绘工程师"
    GEOTECHNICAL_ENGINEER = "岩土工程师"
    MATERIAL_ENGINEER = "建筑材料工程师"

    # 三类人员（无具体专业分类）
    SAFETY_MANAGEMENT = "安全管理"

class SocialSecurityStatus(enum.Enum):
    UNIQUE = "唯一社保"  # 唯一社保
    NONE = "无社保"  # 无社保

class Talent(Base):
    __tablename__ = "talents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    gender = Column(String(10))
    age = Column(Integer)
    phone = Column(String(20))  # 电话号码
    wechat_note = Column(Text)  # 微信添加备注
    contract_price = Column(Numeric(10, 2))  # 签订合同价格
    intention_level = Column(Enum(IntentionLevel), default=IntentionLevel.C)  # 人才意向等级

    # 地区信息
    province = Column(String(50))  # 省份
    city = Column(String(50))  # 城市
    address = Column(Text)  # 详细地址

    # 新增字段
    communication_content = Column(Text)  # 沟通内容
    social_security_status = Column(String(20))  # 社保情况 - 改为字符串类型

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关联关系
    communications = relationship("Communication", back_populates="talent")
    certificates = relationship("Certificate", back_populates="talent")
