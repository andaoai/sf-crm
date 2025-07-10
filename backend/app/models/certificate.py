from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Enum, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base
import enum

class CertificateStatus(enum.Enum):
    VALID = "VALID"      # 有效
    EXPIRED = "EXPIRED"  # 过期
    REVOKED = "REVOKED"  # 注销

class Certificate(Base):
    """具体证书表 - 每个人才持有的具体证书实例"""
    __tablename__ = "certificates"

    certificate_id = Column(String(50), primary_key=True, index=True)  # 具体证书ID
    talent_id = Column(Integer, ForeignKey("talents.id", ondelete="CASCADE"), nullable=True, index=True)
    certificate_type = Column(String(100), nullable=False, index=True)  # 证书类型（用于搜索）
    certificate_name = Column(String(200))  # 证书全称
    certificate_number = Column(String(100))  # 证书编号
    issue_date = Column(Date)  # 颁发日期
    expiry_date = Column(Date)  # 到期日期
    issuing_authority = Column(String(100))  # 发证机构
    specialty = Column(String(100))  # 专业方向
    level = Column(String(50))  # 等级
    status = Column(Enum(CertificateStatus, name='certificatestatus'), default=CertificateStatus.VALID, index=True)  # 状态
    notes = Column(Text)  # 备注
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关联关系
    talent = relationship("Talent", back_populates="certificates")
    certificate_type_info = relationship("CertificateType", 
                                       foreign_keys=[certificate_type],
                                       primaryjoin="Certificate.certificate_type == CertificateType.type_name")

class CertificateType(Base):
    """证书类型字典表 - 用于标准化证书类型和搜索"""
    __tablename__ = "certificate_types"

    type_code = Column(String(50), primary_key=True, index=True)  # 类型代码
    type_name = Column(String(100), nullable=False, unique=True, index=True)  # 类型名称
    category = Column(String(50), index=True)  # 大类（建造师、工程师等）
    description = Column(Text)  # 描述
    is_active = Column(Boolean, default=True, index=True)  # 是否启用
    sort_order = Column(Integer, default=0)  # 排序
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<CertificateType(type_code='{self.type_code}', type_name='{self.type_name}')>"
