from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Communication(Base):
    __tablename__ = "communications"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)  # 沟通内容
    result = Column(Text)  # 沟通结果
    communication_time = Column(DateTime(timezone=True), server_default=func.now())
    communication_date = Column(Date)  # 沟通日期
    communication_type = Column(String(50))  # 沟通方式
    follow_up_required = Column(Boolean, default=False)  # 是否需要跟进
    follow_up_date = Column(Date)  # 跟进日期

    # 外键关联
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    talent_id = Column(Integer, ForeignKey("talents.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关联关系
    company = relationship("Company", back_populates="communications")
    talent = relationship("Talent", back_populates="communications")
