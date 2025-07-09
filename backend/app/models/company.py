from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base
import enum

class IntentionLevel(enum.Enum):
    A = "A"  # 高意向
    B = "B"  # 中等意向
    C = "C"  # 低意向

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    contact_info = Column(Text)  # 公司联系方式
    communication_notes = Column(Text)  # 沟通内容备注
    intention = Column(Text)  # 客户沟通意向
    intention_level = Column(Enum(IntentionLevel), default=IntentionLevel.C)  # 客户意向等级
    price = Column(String(100))  # 沟通价格
    certificate_requirements = Column(Text)  # 需求的建造师证书专业
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关联沟通记录
    communications = relationship("Communication", back_populates="company")
