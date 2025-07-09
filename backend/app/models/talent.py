from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Enum, Numeric
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
    OTHER = "其他"  # 其他证书

class CertificateSpecialty(enum.Enum):
    # 一级建造师专业（10个）
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
    # 注：二级建造师只有前6个专业

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
    certificate_info = Column(Text)  # 建造师证书信息
    certificate_expiry_date = Column(Date)  # 证书到期时间
    contract_price = Column(Numeric(10, 2))  # 签订合同价格
    intention_level = Column(Enum(IntentionLevel), default=IntentionLevel.C)  # 人才意向等级

    # 新增字段
    communication_content = Column(Text)  # 沟通内容
    certificate_level = Column(Enum(CertificateLevel))  # 证书等级
    certificate_specialty = Column(Enum(CertificateSpecialty))  # 证书专业
    social_security_status = Column(Enum(SocialSecurityStatus))  # 社保情况

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关联沟通记录
    communications = relationship("Communication", back_populates="talent")
